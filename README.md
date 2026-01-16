![template](https://user-images.githubusercontent.com/35528949/212500045-feb51ec0-e26a-45a6-bc8c-75d01379faf9.png)
![](https://img.shields.io/badge/version-0.2.0%20-brightgreen)
![](https://img.shields.io/github/license/MassonNN/masson-aiogram-template)
![](https://img.shields.io/github/forks/MassonNn/masson-aiogram-template)
![](https://img.shields.io/github/stars/MassonNn/masson-aiogram-template?style=flat-square)
[![telegram](https://img.shields.io/badge/Telegram-Join-blue)](https://t.me/massonnn_yt)

# 🤖 AI-Powered Expense Tracker Bot

A professional Telegram bot for tracking business expenses using AI-powered receipt scanning. Built with **Strands AI**, **AWS Bedrock**, and **Claude 4 Sonnet** vision model.

## ✨ Features

- 📸 **Smart Receipt Scanning** - Just send a photo, AI does the rest
- 🧠 **Vision AI** - Powered by Claude 4 Sonnet via AWS Bedrock
- 💾 **Automatic Storage** - Structured JSON data for tax reporting
- 🏷️ **Smart Categorization** - Automatic expense categorization
- 📊 **Tax Ready** - Export-ready data format
- ⚡ **Real-time Processing** - Get results in seconds

## 🚀 Quick Start

See **[QUICKSTART.md](QUICKSTART.md)** for detailed setup instructions.

```bash
# 1. Setup
./setup.sh

# 2. Configure .env with your credentials
cp .env.dist .env
# Edit .env with BOT_TOKEN and AWS credentials

# 3. Run
poetry run python -m src.bot
```

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md)** - Detailed AWS Bedrock API key setup
- **[README_EXPENSE_TRACKER.md](README_EXPENSE_TRACKER.md)** - Full feature documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design and architecture
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Implementation details
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

## 🎯 Use Case

Perfect for:
- Freelancers tracking business expenses
- Small business owners
- Professionals managing tax deductions
- Anyone who needs to track receipts for reimbursement

## 🛠️ Tech Stack

- **Bot Framework**: Aiogram 3.x
- **AI Framework**: Strands Agents SDK
- **LLM**: Claude 4 Sonnet (AWS Bedrock)
- **Storage**: File-based JSON (PostgreSQL ready)
- **DI**: Dishka
- **Language**: Python 3.13+

## 📋 Requirements

- Python 3.13+
- Telegram Bot Token
- AWS Bedrock API Key

**Optional** (not needed for basic expense tracking):
- PostgreSQL (for database storage instead of files)
- Redis (for caching)
- Docker (for containerized deployment)

**Note**: Uses AWS Bedrock API keys (simpler than IAM credentials). Get yours from AWS Console → Bedrock → API Keys.

See [OPTIONAL_SERVICES.md](OPTIONAL_SERVICES.md) for details on what's required vs optional.

---

## Setup bot

1. Clone this repository

2. Change the name of `.env.dist` to `.env` and set all environment variables as you need

3. Change password for redis in build/redis.conf (`requirepass` and `masterauth`). Set same password in `.env` 
   (`REDIS_PASSWORD`).

4. Change project name and other information in `pyproject.toml`

5. `make project-start` to start project with docker-compose or `make help` if you want to know more about make commands

---
## Development

If you want to lint your code: \
```make lint``` \
This will start isort, blue and ruff to src and tests folders

You can manually run any instrument by: \
`make ruff`, `make blue` or `make isort`

### Testing

Test the receipt scanner without Telegram:
```bash
make test-scanner
```

### Migrations
`make generate NAME=<name>` \
Generate alembic revision for migration with given name

`make migrate` \
Apply migrations to the target database

---
## Roadmap

- [x] AI-powered receipt scanning
- [x] Vision LLM integration (Claude 4 Sonnet)
- [x] File-based storage
- [ ] Database storage (PostgreSQL)
- [ ] Receipt history and search
- [ ] Export to CSV/Excel
- [ ] Monthly expense reports
- [ ] Multi-currency support
- [ ] Category customization
- [ ] Github Actions CI/CD
- [ ] Light (simplified) version without docker and CI/CD
- [ ] Highload version with NATS and Docker Swarm
- [ ] More tests kit and update factory

## 📄 License

MIT License

