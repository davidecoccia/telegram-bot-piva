"""Test script for receipt scanner (without Telegram)."""
import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.bot.services.receipt_scanner import ReceiptScanner


async def test_scanner():
    """Test the receipt scanner with a sample image."""
    print("🧪 Testing Receipt Scanner...")

    # Check for AWS Bedrock API key
    if not os.getenv("AWS_BEARER_TOKEN_BEDROCK"):
        print("❌ AWS_BEARER_TOKEN_BEDROCK not set in environment")
        print("Please set AWS Bedrock API key:")
        print("  export AWS_BEARER_TOKEN_BEDROCK=your_api_key")
        print("  export AWS_REGION=us-east-1")
        print("")
        print("Get your API key from:")
        print("  AWS Console → Bedrock → API Keys → Generate API key")
        print("  https://docs.aws.amazon.com/bedrock/latest/userguide/api-keys.html")
        return

    # Initialize scanner
    scanner = ReceiptScanner(storage_path="./receipts_data")

    # Check if test image exists
    test_image = input("Enter path to a receipt image (or press Enter to skip): ").strip()

    if not test_image or not Path(test_image).exists():
        print("⚠️  No valid image provided. Skipping test.")
        print("To test, run: python test_receipt_scanner.py")
        print("Then provide a path to a receipt image.")
        return

    try:
        print(f"📸 Scanning receipt: {test_image}")
        result = await scanner.scan_receipt(
            image_path=test_image,
            user_phone="test_user_123",
        )

        print("\n✅ Receipt scanned successfully!")
        print("\n📊 Extracted Data:")
        print(f"  Location: {result.get('location')}")
        print(f"  Date: {result.get('date')}")
        print(f"  Category: {result.get('category')}")
        print(f"  Amount: {result.get('amount')} {result.get('currency')}")
        print(f"  Items: {result.get('items')}")
        print(f"\n💾 Saved to: receipts_data/")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_scanner())
