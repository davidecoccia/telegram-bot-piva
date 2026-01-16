# Troubleshooting Guide

Common issues and solutions for the Expense Tracker Bot.

## Installation Issues

### Poetry Not Found

**Problem**: `zsh: command not found: poetry`

**Solution**:
```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add to PATH (add to ~/.zshrc or ~/.bashrc)
export PATH="$HOME/.local/bin:$PATH"

# Reload shell
source ~/.zshrc
```

### Python Version Error

**Problem**: `Python 3.13+ required`

**Solution**:
```bash
# Check Python version
python --version

# Install Python 3.13+ using pyenv or your system package manager
# macOS with Homebrew:
brew install python@3.13

# Or use pyenv:
pyenv install 3.13.0
pyenv local 3.13.0
```

### Dependency Installation Fails

**Problem**: `poetry install` fails

**Solution**:
```bash
# Clear poetry cache
poetry cache clear pypi --all

# Update poetry
poetry self update

# Try again
poetry install
```

## Configuration Issues

### Missing .env File

**Problem**: Bot crashes with "BOT_TOKEN not found"

**Solution**:
```bash
# Copy template
cp .env.dist .env

# Or use the example
cp .env.example .env

# Edit with your values
nano .env
```

### Invalid Bot Token

**Problem**: `TokenValidationError: Token is invalid! It must be 'str' type instead of <class 'NoneType'> type.`

**Solution**:
This means the BOT_TOKEN is not being read from your `.env` file.

1. Check `.env` file exists:
   ```bash
   ls -la .env
   ```

2. Check BOT_TOKEN is set in `.env`:
   ```bash
   grep BOT_TOKEN .env
   ```

3. Make sure there are no spaces around the `=`:
   ```bash
   # ✅ Correct
   BOT_TOKEN=1234567890:ABC...
   
   # ❌ Wrong
   BOT_TOKEN = 1234567890:ABC...
   ```

4. Verify the fix is applied:
   ```bash
   grep "load_dotenv" src/configuration.py
   ```
   Should show: `from dotenv import load_dotenv` and `load_dotenv()`

5. Test configuration:
   ```bash
   python -c "from src.configuration import Configuration; print('Token:', 'Set' if Configuration().bot.token else 'Missing')"
   ```

### Invalid Bot Token

**Problem**: `Unauthorized: bot token is invalid`

**Solution**:
1. Go to [@BotFather](https://t.me/botfather) on Telegram
2. Send `/mybots`
3. Select your bot
4. Click "API Token"
5. Copy the token
6. Update `BOT_TOKEN` in `.env`

### AWS Bedrock API Key Not Working

**Problem**: `Unable to locate credentials` or `Invalid bearer token`

**Solution**:
```bash
# Check if API key is set
echo $AWS_BEARER_TOKEN_BEDROCK

# If empty, set it in .env
# Or export it:
export AWS_BEARER_TOKEN_BEDROCK=your_api_key
export AWS_REGION=us-east-1

# Generate a new API key if needed:
# AWS Console → Bedrock → API Keys → Generate API key
```

## AWS Bedrock Issues

### Model Access Denied

**Problem**: `AccessDeniedException: You don't have access to the model`

**Solution**:
1. Go to AWS Console → Amazon Bedrock
2. Click "Model access" in left sidebar
3. Click "Manage model access"
4. Find "Claude 4 Sonnet" (us.anthropic.claude-sonnet-4-20250514-v1:0)
5. Check the box and click "Request model access"
6. Wait for approval (usually instant)

### Wrong Region

**Problem**: `Model not found in region`

**Solution**:
```bash
# Claude 4 Sonnet is available in specific regions
# Update .env with a supported region:
AWS_REGION=us-east-1  # or us-west-2
```

Supported regions for Claude 4 Sonnet:
- us-east-1 (N. Virginia)
- us-west-2 (Oregon)
- eu-west-1 (Ireland)
- ap-southeast-1 (Singapore)

### API Key Permission Issues

**Problem**: `AccessDeniedException: User is not authorized`

**Solution**:

1. **For Long-term API keys**: The key automatically has basic Bedrock permissions
2. **For Short-term API keys**: Ensure your IAM principal has these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*::foundation-model/anthropic.claude-*"
    }
  ]
}
```

3. **Regenerate the API key** if it's expired or compromised

## Runtime Issues

### Bot Doesn't Respond

**Problem**: Bot is running but doesn't respond to messages

**Checklist**:
1. Check bot is running: `ps aux | grep python`
2. Check logs for errors
3. Verify bot token is correct
4. Test with `/start` command
5. Check if bot is blocked by user
6. Verify internet connection

### Receipt Scanning Fails

**Problem**: Bot receives photo but fails to process

**Debug Steps**:
```bash
# 1. Test scanner directly
poetry run python test_receipt_scanner.py

# 2. Check logs for specific error
# Look for:
# - AWS credential errors
# - Model access errors
# - JSON parsing errors
# - File permission errors

# 3. Verify image is valid
file path/to/image.jpg
# Should show: JPEG image data

# 4. Check storage directory exists and is writable
ls -la receipts_data/
```

### JSON Parsing Error

**Problem**: `Invalid JSON response from LLM`

**Causes**:
- LLM returned text instead of JSON
- Image quality too poor
- Receipt text not readable

**Solutions**:
1. Try with a clearer image
2. Ensure receipt is well-lit
3. Check if text is readable
4. Try a different receipt

### File Permission Error

**Problem**: `Permission denied` when saving receipt

**Solution**:
```bash
# Check directory permissions
ls -la receipts_data/

# Fix permissions
chmod 755 receipts_data/

# Or recreate directory
rm -rf receipts_data/
mkdir -p receipts_data/
```

## Performance Issues

### Slow Response Time

**Problem**: Bot takes too long to respond

**Normal**: 2-5 seconds per receipt (LLM processing)

**If slower**:
1. Check AWS region latency
2. Verify internet speed
3. Check image size (large images take longer)
4. Monitor AWS Bedrock throttling

**Optimize**:
```python
# Compress images before sending (future enhancement)
# Use smaller image resolution
# Batch process multiple receipts
```

### High AWS Costs

**Problem**: Unexpected AWS bills

**Monitor**:
```bash
# Check AWS Cost Explorer
# Set up billing alerts in AWS Console

# Estimate costs:
# ~$0.006 per receipt
# 1000 receipts = ~$6/month
```

**Reduce Costs**:
1. Optimize prompt length
2. Use smaller images
3. Cache common responses
4. Consider cheaper models for simple receipts

## Docker Issues

### Docker Compose Fails

**Problem**: `docker-compose up` fails

**Solution**:
```bash
# Check Docker is running
docker ps

# Check docker-compose version
docker-compose --version

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check logs
docker-compose logs -f bot
```

### Volume Mount Issues

**Problem**: Data not persisting

**Solution**:
```bash
# Check volume mounts in docker-compose.yml
# Should have:
volumes:
  - ./receipts_data:/app/receipts_data
  - ./temp_images:/app/temp_images

# Create directories
mkdir -p receipts_data temp_images

# Check permissions
chmod 755 receipts_data temp_images
```

## Testing Issues

### Test Script Fails

**Problem**: `test_receipt_scanner.py` crashes

**Debug**:
```bash
# Run with verbose output
python -u test_receipt_scanner.py

# Check Python path
python -c "import sys; print(sys.path)"

# Verify imports
python -c "from src.bot.services.receipt_scanner import ReceiptScanner"

# Check AWS credentials
python -c "import os; print(os.getenv('AWS_ACCESS_KEY_ID'))"
```

## Database Issues (Future)

### Migration Fails

**Problem**: `alembic upgrade head` fails

**Solution**:
```bash
# Check database connection
psql -h localhost -U postgres -d expense_tracker

# Reset migrations (careful!)
alembic downgrade base
alembic upgrade head

# Or regenerate
make generate NAME=init
make migrate
```

## Common Error Messages

### `ModuleNotFoundError: No module named 'strands'`

**Solution**:
```bash
poetry install
# Or
pip install strands-agents
```

### `FileNotFoundError: [Errno 2] No such file or directory: './receipts_data'`

**Solution**:
```bash
mkdir -p receipts_data temp_images
```

### `RetryAfter: Flood control exceeded`

**Solution**:
- Telegram rate limiting
- Wait before sending more messages
- Implement rate limiting in bot

### `ConnectionError: Failed to connect to Bedrock`

**Solution**:
1. Check internet connection
2. Verify AWS region
3. Check AWS service status
4. Verify credentials

## Getting Help

### Enable Debug Logging

```python
# In src/configuration.py or .env
LOGGING_LEVEL=10  # DEBUG level

# Or in code:
import logging
logging.getLogger("strands").setLevel(logging.DEBUG)
logging.getLogger("aiogram").setLevel(logging.DEBUG)
```

### Collect Diagnostic Info

```bash
# System info
python --version
poetry --version
docker --version

# Check environment (without exposing secrets)
env | grep -E '(BOT_TOKEN|AWS_BEARER|AWS_REGION|RECEIPTS)' | sed 's/=.*/=***/'

# Check files
ls -la receipts_data/
ls -la temp_images/

# Check processes
ps aux | grep python

# Check network
ping bedrock-runtime.us-east-1.amazonaws.com
```

### Report Issues

When reporting issues, include:
1. Error message (full traceback)
2. Python version
3. Operating system
4. Steps to reproduce
5. Relevant logs
6. Configuration (without secrets!)

## Prevention Tips

### Best Practices

1. **Always use .env file** - Don't hardcode credentials
2. **Test with test script first** - Before using Telegram
3. **Monitor AWS costs** - Set up billing alerts
4. **Keep dependencies updated** - `poetry update`
5. **Backup receipt data** - Regular backups of receipts_data/
6. **Use version control** - Git for code changes
7. **Read logs** - Check logs regularly for issues

### Health Checks

```bash
# Daily checks
make test-scanner  # Test scanner works
docker-compose ps  # Check containers running
du -sh receipts_data/  # Check storage usage

# Weekly checks
poetry update  # Update dependencies
docker-compose pull  # Update images
aws bedrock list-foundation-models  # Check model access
```

## Still Having Issues?

1. Check all documentation files
2. Review code comments
3. Search error messages online
4. Check AWS Bedrock documentation
5. Check Strands documentation
6. Check Aiogram documentation

## Quick Fixes Checklist

- [ ] .env file exists and has all values
- [ ] BOT_TOKEN is valid
- [ ] AWS_BEARER_TOKEN_BEDROCK is set and valid
- [ ] AWS region is supported (us-east-1, us-west-2, etc.)
- [ ] Claude 4 Sonnet access is enabled in Bedrock console
- [ ] API key is not expired (check expiration date)
- [ ] Python 3.13+ is installed
- [ ] Poetry dependencies are installed
- [ ] receipts_data/ directory exists
- [ ] temp_images/ directory exists
- [ ] Internet connection is working
- [ ] Bot is running (check terminal)
- [ ] No firewall blocking AWS
- [ ] Sufficient disk space

If all checked and still not working, enable debug logging and check the specific error message above.
