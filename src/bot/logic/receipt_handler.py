"""Receipt handling logic for the bot."""
import logging
import os
from pathlib import Path

from aiogram import F, Router, types
from aiogram.types import Message

from ...configuration import Configuration
from ..services.receipt_scanner import ReceiptScanner
from ..utils.telegram_wrapper import telegram_wrapper

logger = logging.getLogger(__name__)

receipt_router = Router(name="receipt")

# Temporary storage for downloaded images
TEMP_IMAGE_DIR = Path("./temp_images")
TEMP_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# Initialize receipt scanner once
_config = Configuration()
_receipt_scanner = ReceiptScanner(storage_path=_config.storage.receipts_path)


@receipt_router.message(F.photo)
async def handle_photo(message: Message):
    """Handle photo messages (receipts).

    Args:
        message: Telegram message with photo
        receipt_scanner: Receipt scanner service
    """
    try:
        # Send processing message
        await telegram_wrapper(
            message.answer,
            text="📸 Receipt received! Analyzing...",
        )

        # Get the largest photo (best quality)
        photo = message.photo[-1]

        # Download the photo
        file = await message.bot.get_file(photo.file_id)
        file_path = TEMP_IMAGE_DIR / f"{photo.file_id}.jpg"

        await message.bot.download_file(file.file_path, file_path)

        # Get user phone number (from Telegram) or use user ID
        user_phone = str(message.from_user.id)

        # Scan the receipt
        receipt_data = await _receipt_scanner.scan_receipt(
            str(file_path),
            user_phone,
        )

        # Format response
        response = _format_receipt_response(receipt_data)

        # Send result
        await telegram_wrapper(
            message.answer,
            text=response,
            parse_mode="HTML",
        )

        # Clean up temp file
        if file_path.exists():
            os.remove(file_path)

    except Exception as e:
        logger.error(f"Error processing receipt: {e}", exc_info=True)
        await telegram_wrapper(
            message.answer,
            text="❌ Sorry, I couldn't process this receipt. Please try again or send a clearer image.",
        )


def _format_receipt_response(receipt_data: dict) -> str:
    """Format receipt data for user display.

    Args:
        receipt_data: Extracted receipt information

    Returns:
        Formatted message text
    """
    location = receipt_data.get("location", "Unknown")
    date = receipt_data.get("date", "Unknown")
    category = receipt_data.get("category", "Unknown")
    amount = receipt_data.get("amount", 0)
    currency = receipt_data.get("currency", "USD")
    items = receipt_data.get("items", [])

    response = f"""✅ <b>Receipt Processed Successfully!</b>

📍 <b>Location:</b> {location}
📅 <b>Date:</b> {date}
🏷️ <b>Category:</b> {category}
💰 <b>Amount:</b> {amount} {currency}"""

    if items:
        items_text = "\n".join([f"  • {item}" for item in items])
        response += f"\n\n📦 <b>Items:</b>\n{items_text}"

    response += "\n\n✨ Your expense has been saved for tax tracking!"

    return response
