# Expense Tracker Bot

AI-powered Telegram bot for tracking professional expenses for tax purposes.

## Features

- 📸 **Receipt Scanning**: Send a photo of any receipt
- 🤖 **AI-Powered**: Uses Strands AI with Claude 4 Sonnet vision model
- 💾 **Automatic Storage**: Saves all receipt data as JSON files
- 🏷️ **Smart Categorization**: Automatically categorizes expenses
- 📊 **Tax Ready**: Structured data perfect for tax reporting

## Setup

### 1. Install Dependencies

```bash
poetry install
```

### 2. Configure Environment

Copy `.env.dist` to `.env` and fill in the required values:

```bash
cp .env.dist .env
```

Required environment variables:
- `BOT_TOKEN`: Your Telegram bot token from [@BotFather](https://t.me/botfather)
- `AWS_BEARER_TOKEN_BEDROCK`: AWS Bedrock API key
- `AWS_REGION`: AWS region (default: us-east-1)
- `RECEIPTS_STORAGE_PATH`: Path to store receipt data (default: ./receipts_data)

### 3. AWS Bedrock Setup

The bot uses Amazon Bedrock with Claude 4 Sonnet for vision capabilities.

**Quick Setup:**
1. Go to [AWS Console → Bedrock → API Keys](https://console.aws.amazon.com/bedrock/)
2. Click "Generate API key"
3. Choose "Long-term" (30 days) for testing or "Short-term" (12 hours) for production
4. Enable Claude 4 Sonnet model access in Model access section
5. Copy the API key and add it to your `.env` file as `AWS_BEARER_TOKEN_BEDROCK`

**Detailed Instructions**: See [AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md) for step-by-step guide with screenshots and troubleshooting.

**Documentation**: [AWS Bedrock API Keys](https://docs.aws.amazon.com/bedrock/latest/userguide/api-keys.html)

### 4. Run the Bot

```bash
poetry run python -m src.bot
```

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to see the welcome message
3. Send a photo of any receipt
4. The bot will analyze it and extract:
   - Business location
   - Date of purchase
   - Expense category
   - Amount and currency
   - Items purchased

## Receipt Data Storage

All receipts are stored as JSON files in the `receipts_data` directory (configurable).

Example receipt file structure:
```json
{
  "location": "Starbucks Coffee",
  "date": "2026-01-14",
  "category": "meals",
  "amount": 15.50,
  "currency": "USD",
  "items": ["Coffee", "Sandwich"],
  "user_phone": "1234567890",
  "scanned_at": "2026-01-14T10:30:00",
  "image_path": "./temp_images/xyz.jpg"
}
```

## Architecture

- **Telegram Bot**: Built with aiogram 3.x
- **AI Framework**: Strands Agents SDK
- **Vision Model**: Claude 4 Sonnet (via AWS Bedrock)
- **Storage**: File-based JSON storage (easily upgradable to database)
- **DI Container**: Dishka for dependency injection

## Future Enhancements

- Database storage for receipts
- Export to CSV/Excel for tax filing
- Monthly/yearly expense reports
- Multi-currency support with conversion
- Receipt image storage
- User authentication and multi-user support
- Expense categories customization
- Integration with accounting software

## Development

The bot follows a clean architecture pattern:

- `src/bot/logic/`: Message handlers
- `src/bot/services/`: Business logic (receipt scanning)
- `src/bot/di_services.py`: Service dependency injection
- `src/configuration.py`: Configuration management

## License

MIT License
