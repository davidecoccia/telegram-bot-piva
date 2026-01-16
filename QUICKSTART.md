# Quick Start Guide

Get your Expense Tracker Bot running in 5 minutes!

## Prerequisites

- Python 3.13+
- Poetry (Python package manager)
- AWS Account with Bedrock access
- Telegram Bot Token

## Step 1: Install Poetry (if needed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Step 2: Clone and Setup

```bash
# Run the setup script
./setup.sh
```

Or manually:

```bash
# Install dependencies
poetry install

# Copy environment template
cp .env.dist .env

# Create storage directories
mkdir -p receipts_data temp_images
```

## Step 3: Configure Environment

Edit `.env` file:

```bash
# Copy the minimal template (recommended for getting started)
cp .env.minimal .env

# Or copy the full template
# cp .env.dist .env

# Edit with your values
nano .env
```

**Minimal configuration (all you need):**
```bash
# Telegram Bot Token (get from @BotFather)
BOT_TOKEN=your_telegram_bot_token_here

# AWS Bedrock API Key
AWS_BEARER_TOKEN_BEDROCK=your_bedrock_api_key_here
AWS_REGION=us-east-1

# Storage path (optional, defaults to ./receipts_data)
RECEIPTS_STORAGE_PATH=./receipts_data

# Logging (optional)
LOGGING_LEVEL=20
```

**Note**: PostgreSQL and Redis are **optional** and not needed for expense tracking. See [OPTIONAL_SERVICES.md](OPTIONAL_SERVICES.md) for details.

### Getting a Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the token provided

### AWS Bedrock Setup

**Quick Start (30-day API key):**

1. Log into [AWS Console](https://console.aws.amazon.com/bedrock/)
2. Navigate to Amazon Bedrock
3. Click "API Keys" in the left sidebar
4. Click "Generate API key"
5. Select "Long-term" (30 days for testing)
6. Copy the API key
7. Go to "Model access" and request access to "Claude 4 Sonnet"
8. Add the API key to `.env` as `AWS_BEARER_TOKEN_BEDROCK`

**For Production (12-hour keys):**
- Use "Short-term" API keys that expire after 12 hours
- More secure for production environments
- See [AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md) for detailed instructions

## Step 4: Run the Bot

```bash
poetry run python -m src.bot
```

You should see:
```
INFO:aiogram:Bot started
```

## Step 5: Test It!

1. Open Telegram
2. Search for your bot by username
3. Send `/start` to begin
4. Send a photo of any receipt
5. Watch the magic happen! ✨

## Testing Without Telegram

Test the receipt scanner directly:

```bash
poetry run python test_receipt_scanner.py
```

Then provide a path to a receipt image when prompted.

## Example Receipt

The bot will extract information like:

```json
{
  "location": "Starbucks Coffee",
  "date": "2026-01-14",
  "category": "meals",
  "amount": 15.50,
  "currency": "USD",
  "items": ["Latte", "Croissant"],
  "user_phone": "1234567890",
  "scanned_at": "2026-01-14T10:30:00"
}
```

## Troubleshooting

### Bot doesn't respond
- Check BOT_TOKEN is correct
- Ensure bot is running (check terminal)
- Verify bot is not blocked
- Check logs for errors

### Database/Redis connection errors
- **These are optional!** See [OPTIONAL_SERVICES.md](OPTIONAL_SERVICES.md)
- The bot will show warnings but receipt scanning will work fine
- You can safely ignore PostgreSQL/Redis connection errors
- Only needed if you want to use database storage instead of files

### Receipt scanning fails
- Verify AWS credentials are correct
- Check Bedrock model access is enabled
- Ensure image is clear and readable
- Check AWS region is correct

### Import errors
- Run `poetry install` again
- Check Python version (3.13+ required)

### AWS Bedrock errors
- Verify model access is enabled in Bedrock console
- Check IAM permissions include `bedrock:InvokeModel`
- Ensure correct region is set

## Next Steps

- Check `README_EXPENSE_TRACKER.md` for full documentation
- Explore the code in `src/bot/`
- Customize expense categories
- Add database storage
- Build export features

## Support

For issues or questions:
- Check the logs in terminal
- Review AWS CloudWatch logs
- Verify all environment variables are set
- Test with the standalone test script first

Happy expense tracking! 💰
