# Getting Started - Simplest Path

The absolute simplest way to get your expense tracker bot running.

## What You Actually Need

### ✅ Required (3 things)
1. **Telegram Bot Token** - Free, takes 2 minutes
2. **AWS Bedrock API Key** - Free tier available
3. **Python 3.13+** - Already installed ✅

### ❌ NOT Required
- ❌ PostgreSQL database
- ❌ Redis cache
- ❌ Docker
- ❌ Poetry (we're using pip)
- ❌ Complex setup

## 5-Minute Setup

### 1. Get Telegram Bot Token (2 minutes)

1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow instructions
5. Copy the token (looks like: `1234567890:ABCdefGHI...`)

### 2. Get AWS Bedrock API Key (3 minutes)

1. Go to [AWS Console](https://console.aws.amazon.com/bedrock/)
2. Click "API Keys" in sidebar
3. Click "Generate API key"
4. Select "Long-term" (30 days)
5. Click "Generate"
6. Copy the key
7. Go to "Model access" → Enable "Claude 4 Sonnet"

Detailed guide: [AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md)

### 3. Configure (30 seconds)

```bash
# Copy minimal template
cp .env.minimal .env

# Edit and add your tokens
nano .env
```

Add these two lines:
```bash
BOT_TOKEN=your_telegram_token_here
AWS_BEARER_TOKEN_BEDROCK=your_aws_key_here
```

### 4. Run (10 seconds)

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the bot
python -m src.bot
```

You should see:
```
INFO:aiogram.dispatcher:Start polling
```

### 5. Test (1 minute)

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Take a photo of any receipt
5. Send it to the bot
6. Wait 2-5 seconds
7. Get structured expense data! 🎉

## That's It!

You now have a working AI-powered expense tracker.

## Common Questions

### Do I need PostgreSQL?
**No.** Receipts are saved as JSON files in `receipts_data/` folder.

### Do I need Redis?
**No.** Not used for expense tracking.

### Do I need Docker?
**No.** Run directly with Python.

### Do I need Poetry?
**No.** We installed with pip (see `requirements.txt`).

### What about the database errors in logs?
**Ignore them.** The template includes database support, but it's not used for receipts. See [OPTIONAL_SERVICES.md](OPTIONAL_SERVICES.md).

### Can I use this in production?
**Yes!** File-based storage works fine for personal use or small teams. For high volume, migrate to PostgreSQL later.

### How much does it cost?
- **Telegram**: Free
- **AWS Bedrock**: ~$0.006 per receipt (~$6 for 1000 receipts)
- **Storage**: Negligible (JSON files are tiny)

### Where are receipts stored?
In `receipts_data/` folder as JSON files:
```
receipts_data/
├── receipt_1234567890_20260115_120000.json
├── receipt_1234567890_20260115_130000.json
└── ...
```

### Can I see the receipt data?
Yes! Just open any JSON file:
```bash
cat receipts_data/receipt_*.json
```

### How do I stop the bot?
Press `Ctrl+C` in the terminal.

### How do I run it again?
```bash
source .venv/bin/activate
python -m src.bot
```

## Troubleshooting

### "BOT_TOKEN not found"
- Make sure you created `.env` file
- Check the token is on the line `BOT_TOKEN=...`
- No spaces around the `=`

### "AWS credentials not found"
- Make sure `AWS_BEARER_TOKEN_BEDROCK` is in `.env`
- Check you copied the full API key
- Verify the key hasn't expired (30 days for long-term keys)

### "Model access denied"
- Go to AWS Console → Bedrock → Model access
- Enable "Claude 4 Sonnet"
- Wait a few minutes for approval

### Bot doesn't respond to photos
- Check bot is running (terminal shows "Start polling")
- Verify you sent a photo (not a file)
- Check AWS API key is valid
- Look at terminal for error messages

### More help
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Detailed troubleshooting
- [QUICKSTART.md](QUICKSTART.md) - Full setup guide
- [AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md) - AWS setup details

## Next Steps

Once it's working:

1. **Test with real receipts** - Try different types
2. **Check the data** - Look at JSON files in `receipts_data/`
3. **Customize categories** - Edit the prompt in `receipt_scanner.py`
4. **Add features** - Export to CSV, monthly reports, etc.
5. **Scale up** - Migrate to PostgreSQL if needed

## File Structure (What You Need to Know)

```
telegram-bot-piva/
├── .env                    # ← Your config (create this!)
├── .env.minimal            # ← Template (copy this)
├── receipts_data/          # ← Receipts saved here
├── temp_images/            # ← Temp storage (auto-cleaned)
├── .venv/                  # ← Python environment
└── src/bot/
    ├── logic/
    │   └── receipt_handler.py   # Handles photos
    └── services/
        └── receipt_scanner.py   # AI scanning
```

## Quick Commands

```bash
# Activate environment
source .venv/bin/activate

# Run bot
python -m src.bot

# Test scanner (without Telegram)
python test_receipt_scanner.py

# View receipts
ls -la receipts_data/
cat receipts_data/receipt_*.json

# Check logs
# (shown in terminal while bot runs)

# Stop bot
# Press Ctrl+C
```

## Success Checklist

- [ ] Python 3.13+ installed
- [ ] Virtual environment activated
- [ ] `.env` file created with tokens
- [ ] Bot running (shows "Start polling")
- [ ] Sent `/start` to bot
- [ ] Sent receipt photo
- [ ] Received structured data
- [ ] JSON file created in `receipts_data/`

If all checked, you're done! 🎉

---

**Need more details?** See [QUICKSTART.md](QUICKSTART.md)  
**Having issues?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)  
**Want to understand the code?** See [ARCHITECTURE.md](ARCHITECTURE.md)
