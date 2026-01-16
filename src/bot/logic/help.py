"""This file represents a start logic."""


from aiogram import Router, types
from aiogram.filters import Command

help_router = Router(name="help")


@help_router.message(Command(commands="help"))
async def help_handler(message: types.Message):
    """Help command handler."""
    help_text = """🤖 <b>Expense Tracker Bot - Help</b>

<b>Available Commands:</b>
/start - Welcome message and introduction
/help - Show this help message

<b>How to Track Expenses:</b>
1️⃣ Take a photo of your receipt
2️⃣ Send the photo to this bot
3️⃣ I'll automatically extract and save:
   • Business location
   • Purchase date
   • Expense category
   • Amount and currency
   • Items purchased

<b>Supported Receipt Types:</b>
✅ Restaurant receipts
✅ Transportation (taxi, uber, parking)
✅ Office supplies
✅ Accommodation (hotels)
✅ Any business expense

<b>Data Storage:</b>
All receipts are saved as structured JSON files, perfect for tax reporting and accounting software integration.

<b>Tips for Best Results:</b>
📸 Take clear, well-lit photos
📄 Ensure text is readable
🔍 Include the entire receipt in frame

Need help? Contact support or check the documentation."""

    return await message.answer(help_text, parse_mode="HTML")
