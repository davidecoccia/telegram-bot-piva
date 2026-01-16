"""This file represents a start logic."""


from aiogram import Router, types
from aiogram.filters import CommandStart

from ..utils.telegram_wrapper import telegram_wrapper

start_router = Router(name="start")


@start_router.message(CommandStart())
async def start_handler(message: types.Message):
    """Start command handler."""
    welcome_text = """👋 Welcome to <b>Expense Tracker Bot</b>!

I help professionals track expenses for tax purposes using AI-powered receipt scanning.

📸 <b>How to use:</b>
Simply send me a photo of your receipt, and I'll automatically extract:
• Location/Business name
• Date of purchase
• Expense category
• Amount and currency
• Items purchased

All your expenses are saved securely for easy tax reporting!

Try it now - just send me a receipt photo! 📄"""

    return await telegram_wrapper(
        message.answer,
        text=welcome_text,
        parse_mode="HTML",
    )
