# Optional Services Guide

## PostgreSQL and Redis - Do You Need Them?

**Short answer: NO** - For the expense tracking feature, you don't need PostgreSQL or Redis.

## What's Currently Used

### ✅ Required Services
1. **Telegram Bot API** - For receiving messages
2. **AWS Bedrock** - For AI receipt scanning
3. **File System** - For storing receipt JSON files

### ⚠️ Optional Services (Not Used for Receipts)
1. **PostgreSQL** - Database (template includes it, but receipts use files)
2. **Redis** - Cache/session storage (template includes it, but not used for receipts)

## Why Are They in the Template?

This project is based on the [Masson Aiogram Template](https://github.com/MassonNN/masson-aiogram-template), which is designed for scalable bots that might need:
- User management (database)
- Session state (Redis)
- Complex workflows (database)
- High-volume operations (Redis cache)

For our **expense tracking use case**, we simplified it to use file-based storage.

## Running Without Database/Redis

### Option 1: Use Minimal Configuration (Recommended)

Copy the minimal template:
```bash
cp .env.minimal .env
```

Then edit `.env` and add only:
- `BOT_TOKEN`
- `AWS_BEARER_TOKEN_BEDROCK`

### Option 2: Comment Out Database/Redis

If you copied `.env.dist`, just leave the database/redis fields empty or commented:
```bash
# These can be empty or commented out
#POSTGRES_DATABASE=
#POSTGRES_USER=
#REDIS_HOST=
```

The bot will still try to initialize these providers, but they won't be used for receipt scanning.

## When Would You Need Them?

### PostgreSQL Database
You'd want PostgreSQL if you plan to:
- Store receipts in a database instead of files
- Add user authentication/profiles
- Build receipt search and filtering
- Generate reports from stored data
- Scale to thousands of receipts

**Migration path**: The code is already structured to easily switch from file storage to database storage.

### Redis Cache
You'd want Redis if you plan to:
- Cache frequent queries
- Store user session state
- Implement rate limiting
- Handle high-volume traffic
- Add real-time features

## Current Architecture

```
User → Telegram → Bot → Receipt Scanner → File Storage
                                ↓
                         AWS Bedrock (Claude)
```

**Not used for receipts:**
- PostgreSQL ❌
- Redis ❌

## Future Migration (Optional)

If you later want to use a database:

### 1. Set up PostgreSQL
```bash
# Using Docker
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=yourpassword \
  -e POSTGRES_DB=expense_tracker \
  -p 5432:5432 \
  postgres:15-alpine
```

### 2. Update .env
```bash
POSTGRES_DATABASE=expense_tracker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_PORT=5432
POSTGRES_HOST=localhost
```

### 3. Run migrations
```bash
alembic upgrade head
```

### 4. Update receipt scanner
Modify `src/bot/services/receipt_scanner.py` to save to database instead of files.

## Docker Compose Setup

If you want to use the full Docker setup (with PostgreSQL and Redis):

```bash
# Start all services
docker-compose up -d

# This will start:
# - PostgreSQL
# - Redis
# - Bot (in container)
```

But for local development with just the expense tracker, you don't need Docker at all!

## Recommended Setup for Beginners

**Simplest setup (no database, no Redis, no Docker):**

1. Create `.env` from `.env.minimal`:
   ```bash
   cp .env.minimal .env
   ```

2. Add your tokens:
   ```bash
   BOT_TOKEN=your_telegram_token
   AWS_BEARER_TOKEN_BEDROCK=your_aws_key
   ```

3. Run the bot:
   ```bash
   source .venv/bin/activate
   python -m src.bot
   ```

That's it! No database, no Redis, no Docker needed.

## Summary

| Service | Required? | Used For | Can Skip? |
|---------|-----------|----------|-----------|
| Telegram Bot API | ✅ Yes | Receiving messages | ❌ No |
| AWS Bedrock | ✅ Yes | AI receipt scanning | ❌ No |
| File System | ✅ Yes | Storing receipts | ❌ No |
| PostgreSQL | ❌ No | Database storage | ✅ Yes |
| Redis | ❌ No | Caching/sessions | ✅ Yes |

## Questions?

**Q: Will the bot crash without PostgreSQL/Redis?**  
A: The current template tries to initialize them, but they're not used for receipt scanning. You might see connection warnings in logs, but the receipt feature will work fine.

**Q: Should I set them up anyway?**  
A: Only if you plan to extend the bot with features that need them (user management, search, reports, etc.)

**Q: How do I completely remove them?**  
A: You can remove the `DatabaseProvider()` and modify the FSM storage to use memory instead of Redis. But it's easier to just leave them as-is since they don't interfere with receipt scanning.

**Q: What's the best setup for production?**  
A: For production with many users, you'd want PostgreSQL for receipts and Redis for caching. But start simple with files and migrate later if needed.

## Next Steps

1. ✅ Use `.env.minimal` for simplest setup
2. ✅ Focus on getting Telegram and AWS Bedrock working
3. ✅ Test receipt scanning with file storage
4. ⏭️ Later: Consider database if you need advanced features

---

**TL;DR**: You only need Telegram Bot Token and AWS Bedrock API Key. PostgreSQL and Redis are optional and not used for the expense tracking feature.
