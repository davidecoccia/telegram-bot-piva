"""Receipt scanning service using Strands AI."""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import aiofiles
from strands import Agent

logger = logging.getLogger(__name__)


class ReceiptScanner:
    """Service for scanning receipts using vision-enabled LLM."""

    def __init__(self, storage_path: str):
        """Initialize the receipt scanner.

        Args:
            storage_path: Path to store receipt data
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Initialize Strands agent with vision-capable model
        self.agent = Agent(
            model="us.anthropic.claude-sonnet-4-20250514-v1:0",
            system_prompt="""You are an expert receipt analyzer for tax expense tracking.
Your task is to analyze receipt images and extract structured information.

Extract the following information from the receipt:
- location: The business name or location where the purchase was made
- date: The date of the transaction (format: YYYY-MM-DD)
- category: The expense category (e.g., "meals", "transportation", "office_supplies", "accommodation", "other")
- amount: The total amount paid (as a number)
- currency: The currency code (e.g., "USD", "EUR")
- items: List of items purchased (if visible)

Return ONLY a valid JSON object with these fields. Do not include any other text.
If you cannot determine a field, use null for that field.

Example output:
{
  "location": "Starbucks Coffee",
  "date": "2026-01-14",
  "category": "meals",
  "amount": 15.50,
  "currency": "USD",
  "items": ["Coffee", "Sandwich"]
}""",
            callback_handler=None,  # Disable console output
        )

    async def scan_receipt(
        self, image_path: str, user_phone: str
    ) -> dict[str, Any]:
        """Scan a receipt image and extract information.

        Args:
            image_path: Path to the receipt image
            user_phone: User's phone number

        Returns:
            Dictionary containing extracted receipt information
        """
        logger.info(f"Scanning receipt from {image_path} for user {user_phone}")

        try:
            # Use boto3 directly to call Bedrock with vision model
            # Based on: https://github.com/strands-agents/samples/blob/main/02-samples/12-medical-document-processing-assistant/document_processor.py
            import base64
            import json
            import boto3
            
            # Read and encode the image
            with open(image_path, 'rb') as img_file:
                image_bytes = img_file.read()
                image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Create Bedrock client
            bedrock = boto3.client(
                service_name='bedrock-runtime',
                region_name='us-east-1'
            )
            
            # Prepare the request for Claude with vision
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_b64
                                }
                            },
                            {
                                "type": "text",
                                "text": self.agent.system_prompt
                            }
                        ]
                    }
                ]
            }
            
            # Call Bedrock
            response = bedrock.invoke_model(
                modelId="us.anthropic.claude-sonnet-4-20250514-v1:0",
                body=json.dumps(request_body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            response_text = response_body['content'][0]['text']

            # Try to extract JSON from the response
            receipt_data = self._parse_json_response(response_text)

            # Add user information and metadata
            receipt_data["user_phone"] = user_phone
            receipt_data["scanned_at"] = datetime.now().isoformat()
            receipt_data["image_path"] = image_path

            # Save to file
            await self._save_receipt(receipt_data)

            logger.info(f"Successfully scanned receipt: {receipt_data}")
            return receipt_data

        except Exception as e:
            logger.error(f"Error scanning receipt: {e}", exc_info=True)
            raise

    def _parse_json_response(self, response: str) -> dict[str, Any]:
        """Parse JSON from LLM response.

        Args:
            response: Raw response from LLM

        Returns:
            Parsed JSON data
        """
        # Try to find JSON in the response
        response = response.strip()

        # Remove markdown code blocks if present
        if response.startswith("```"):
            lines = response.split("\n")
            response = "\n".join(lines[1:-1])
            if response.startswith("json"):
                response = response[4:].strip()

        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {response}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")

    async def _save_receipt(self, receipt_data: dict[str, Any]) -> None:
        """Save receipt data to file.

        Args:
            receipt_data: Receipt information to save
        """
        # Create filename based on timestamp and user
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        user_phone = receipt_data.get("user_phone", "unknown").replace("+", "")
        filename = f"receipt_{user_phone}_{timestamp}.json"
        filepath = self.storage_path / filename

        # Save to file
        async with aiofiles.open(filepath, "w") as f:
            await f.write(json.dumps(receipt_data, indent=2))

        logger.info(f"Saved receipt data to {filepath}")

    async def get_user_receipts(self, user_phone: str) -> list[dict[str, Any]]:
        """Get all receipts for a user.

        Args:
            user_phone: User's phone number

        Returns:
            List of receipt data
        """
        receipts = []
        user_phone_clean = user_phone.replace("+", "")

        for filepath in self.storage_path.glob(f"receipt_{user_phone_clean}_*.json"):
            async with aiofiles.open(filepath, "r") as f:
                content = await f.read()
                receipts.append(json.loads(content))

        return sorted(receipts, key=lambda x: x.get("scanned_at", ""), reverse=True)
