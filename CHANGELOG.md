# Changelog

All notable changes to the Expense Tracker Bot project.

## [1.0.0] - 2026-01-14

### Added
- 🤖 AI-powered receipt scanning using Strands Agents SDK
- 📸 Vision-enabled LLM integration (Claude 4 Sonnet via AWS Bedrock)
- 💾 File-based JSON storage for receipts
- 🏷️ Automatic expense categorization
- 📱 Telegram bot interface with photo message handling
- 🔧 Comprehensive configuration management
- 📚 Extensive documentation suite
- 🧪 Standalone testing script
- 🐳 Docker support with volume mounts
- 🛠️ Setup automation script

### Features
- Receipt data extraction: location, date, category, amount, currency, items
- Real-time processing with user feedback
- Clean architecture with dependency injection
- Async/await throughout
- Error handling and retry logic
- Configurable storage paths
- Support for multiple users

### Documentation
- `README.md` - Main project overview
- `README_EXPENSE_TRACKER.md` - Feature documentation
- `QUICKSTART.md` - 5-minute setup guide
- `AWS_BEDROCK_SETUP.md` - Detailed AWS setup instructions
- `ARCHITECTURE.md` - System design and architecture
- `IMPLEMENTATION_SUMMARY.md` - Implementation details
- `TROUBLESHOOTING.md` - Common issues and solutions
- `.env.example` - Comprehensive environment configuration example

### Technical Stack
- Python 3.13+
- Aiogram 3.x (Telegram bot framework)
- Strands Agents SDK (AI framework)
- AWS Bedrock (Claude 4 Sonnet)
- Dishka (Dependency injection)
- Poetry (Package management)
- Docker & Docker Compose

### Configuration
- **Simplified AWS Authentication**: Uses AWS Bedrock API keys instead of IAM credentials
  - `AWS_BEARER_TOKEN_BEDROCK` environment variable
  - Support for both long-term (30 days) and short-term (12 hours) keys
  - Easier setup for development and testing
  - More secure for production with short-term keys

### Security
- Environment-based configuration
- No hardcoded credentials
- Temporary file cleanup
- API keys not logged in CloudTrail
- Support for key rotation

### Testing
- Standalone test script (`test_receipt_scanner.py`)
- Manual testing without Telegram
- Diagnostic information collection

### Development Tools
- Makefile with common commands
- Setup automation script
- Linting and formatting tools
- Type checking with mypy
- Code quality with ruff

## Migration from IAM Credentials

If you were using IAM credentials before, migrate to API keys:

### Old Configuration (IAM):
```bash
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

### New Configuration (API Keys):
```bash
AWS_BEARER_TOKEN_BEDROCK=your_api_key_here
AWS_REGION=us-east-1
```

### Benefits of API Keys:
1. ✅ Simpler setup (no IAM user creation)
2. ✅ No complex permission policies
3. ✅ Quick start (5 minutes)
4. ✅ Automatic expiration (short-term keys)
5. ✅ Not logged in CloudTrail
6. ✅ Perfect for development and production

### How to Migrate:
1. Generate API key: AWS Console → Bedrock → API Keys
2. Update `.env` file with new variable
3. Remove old IAM credential variables
4. Test with `poetry run python test_receipt_scanner.py`

See [AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md) for detailed instructions.

## Future Roadmap

### Planned Features
- [ ] Database storage (PostgreSQL integration)
- [ ] Receipt history and search commands
- [ ] Export to CSV/Excel
- [ ] Monthly/yearly expense reports
- [ ] Multi-currency support with conversion
- [ ] Receipt image storage (S3 integration)
- [ ] User authentication and authorization
- [ ] Category customization per user
- [ ] Analytics dashboard
- [ ] Integration with accounting software
- [ ] Mobile app
- [ ] Team/organization support
- [ ] Tax report generation

### Technical Improvements
- [ ] Unit tests
- [ ] Integration tests
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Monitoring and alerting
- [ ] Performance optimization
- [ ] Caching layer (Redis)
- [ ] Message queue (Celery)
- [ ] Horizontal scaling support
- [ ] Webhook mode for bot
- [ ] Rate limiting
- [ ] API documentation

### Documentation
- [ ] API documentation
- [ ] Deployment guides (AWS, GCP, Azure)
- [ ] Video tutorials
- [ ] Contributing guidelines
- [ ] Code of conduct

## Known Issues

### Current Limitations
1. File-based storage (not suitable for high volume)
2. No user authentication beyond Telegram
3. Minimal data validation
4. Basic error handling
5. No rate limiting
6. Temporary images deleted after processing
7. English language only
8. Single bot instance only

### Workarounds
- For high volume: Migrate to PostgreSQL (database ready)
- For authentication: Add custom auth layer
- For validation: Extend receipt scanner service
- For rate limiting: Add middleware
- For images: Integrate S3 storage
- For multi-language: Add i18n support
- For scaling: Use webhook mode + load balancer

## Support

For issues, questions, or contributions:
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Review [AWS_BEDROCK_SETUP.md](AWS_BEDROCK_SETUP.md)
- Read the documentation
- Open an issue on GitHub

## License

MIT License - See [LICENSE](LICENSE) file for details

## Acknowledgments

- Built with [Strands Agents SDK](https://strandsagents.com/)
- Powered by [AWS Bedrock](https://aws.amazon.com/bedrock/)
- Uses [Anthropic Claude 4 Sonnet](https://www.anthropic.com/claude)
- Based on [Masson Aiogram Template](https://github.com/MassonNN/masson-aiogram-template)
- Telegram bot framework: [Aiogram](https://aiogram.dev/)

---

**Version**: 1.0.0  
**Release Date**: January 14, 2026  
**Status**: Production Ready ✅
