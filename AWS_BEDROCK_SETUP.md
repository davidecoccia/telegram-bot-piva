# AWS Bedrock API Key Setup Guide

This guide walks you through setting up AWS Bedrock API keys for the Expense Tracker Bot.

## Why API Keys?

AWS Bedrock API keys are simpler than traditional IAM credentials:
- ✅ No IAM user creation needed
- ✅ No complex permission policies
- ✅ Quick setup (5 minutes)
- ✅ Perfect for development and testing
- ✅ Can be used for production with short-term keys

## Step-by-Step Setup

### 1. Create AWS Account

If you don't have an AWS account:
1. Go to [aws.amazon.com](https://aws.amazon.com)
2. Click "Create an AWS Account"
3. Follow the registration process
4. Add payment method (required, but we'll stay in free tier)

### 2. Access Bedrock Console

1. Log into [AWS Console](https://console.aws.amazon.com)
2. In the search bar, type "Bedrock"
3. Click on "Amazon Bedrock"
4. Make sure you're in a supported region (top-right corner):
   - **us-east-1** (N. Virginia) - Recommended
   - us-west-2 (Oregon)
   - eu-west-1 (Ireland)
   - ap-southeast-1 (Singapore)

### 3. Enable Model Access

Before generating an API key, you need to enable Claude 4 Sonnet:

1. In the Bedrock console, click **"Model access"** in the left sidebar
2. Click **"Manage model access"** button (top-right)
3. Find **"Claude 4 Sonnet"** in the list
   - Look for: `us.anthropic.claude-sonnet-4-20250514-v1:0`
4. Check the box next to it
5. Click **"Request model access"** at the bottom
6. Wait for approval (usually instant, sometimes takes a few minutes)
7. Refresh the page - status should show "Access granted" ✅

### 4. Generate API Key

Now you can generate your API key:

#### For Testing/Development (30-day key):

1. Click **"API Keys"** in the left sidebar
2. Click **"Generate API key"** button
3. Select **"Long-term"**
4. Set expiration: **30 days** (or your preference)
5. Add a description: "Expense Tracker Bot - Development"
6. Click **"Generate"**
7. **IMPORTANT**: Copy the API key immediately!
   - You won't be able to see it again
   - Store it securely
8. Click **"Done"**

#### For Production (12-hour key):

1. Click **"API Keys"** in the left sidebar
2. Click **"Generate API key"** button
3. Select **"Short-term"**
4. The key will inherit permissions from your IAM principal
5. Key expires after 12 hours or when your session ends
6. Click **"Generate"**
7. Copy the API key
8. Click **"Done"**

**Note**: Short-term keys require you to have an IAM principal (user or role) with Bedrock permissions.

### 5. Add to Environment

Add the API key to your `.env` file:

```bash
# Copy .env.dist to .env if you haven't already
cp .env.dist .env

# Edit .env and add your API key
nano .env
```

Add these lines:
```bash
AWS_BEARER_TOKEN_BEDROCK=your_api_key_here
AWS_REGION=us-east-1
```

### 6. Test the Setup

Test that everything works:

```bash
# Test the receipt scanner
poetry run python test_receipt_scanner.py

# Or run the bot
poetry run python -m src.bot
```

## API Key Types Comparison

| Feature | Long-term (30 days) | Short-term (12 hours) |
|---------|---------------------|----------------------|
| **Setup** | Very easy | Requires IAM setup |
| **Duration** | Up to 30 days | Max 12 hours |
| **Use Case** | Development, testing | Production |
| **Permissions** | Basic Bedrock access | Inherits from IAM |
| **Security** | Good | Better |
| **Rotation** | Manual | Automatic |

## Security Best Practices

### For Development
1. ✅ Use long-term keys (30 days)
2. ✅ Store in `.env` file (never commit to git)
3. ✅ Rotate every 30 days
4. ✅ Delete unused keys
5. ✅ Use separate keys for different projects

### For Production
1. ✅ Use short-term keys (12 hours)
2. ✅ Automate key generation/rotation
3. ✅ Use AWS Secrets Manager for storage
4. ✅ Monitor usage with CloudWatch
5. ✅ Set up billing alerts
6. ✅ Use least-privilege permissions

## Troubleshooting

### "Model access denied"

**Problem**: API key works but model access is denied

**Solution**:
1. Go to Bedrock console → Model access
2. Check if Claude 4 Sonnet shows "Access granted"
3. If not, request access again
4. Wait a few minutes and try again

### "Invalid bearer token"

**Problem**: API key is not recognized

**Solutions**:
1. Check if key is copied correctly (no extra spaces)
2. Verify key hasn't expired
3. Ensure you're using the right region
4. Regenerate the key if needed

### "Region not supported"

**Problem**: Model not available in your region

**Solution**:
Change to a supported region:
```bash
AWS_REGION=us-east-1  # Try this first
# or
AWS_REGION=us-west-2
```

### Key Expired

**Problem**: Long-term key expired after 30 days

**Solution**:
1. Go to Bedrock console → API Keys
2. Delete the old key
3. Generate a new key
4. Update `.env` file

## Cost Information

### Pricing (as of 2026)

**Claude 4 Sonnet via Bedrock**:
- Input: ~$3 per 1M tokens
- Output: ~$15 per 1M tokens
- Images: Additional cost per image

**Estimated Costs**:
- Per receipt: ~$0.006
- 100 receipts: ~$0.60
- 1,000 receipts: ~$6.00
- 10,000 receipts: ~$60.00

### Free Tier

AWS Bedrock offers a free tier for the first 2 months:
- Check current free tier limits at [aws.amazon.com/bedrock/pricing](https://aws.amazon.com/bedrock/pricing/)

### Cost Monitoring

Set up billing alerts:
1. Go to AWS Console → Billing
2. Click "Budgets"
3. Create a budget (e.g., $10/month)
4. Set up email alerts

## Managing API Keys

### View All Keys

1. Bedrock console → API Keys
2. See all active keys with:
   - Creation date
   - Expiration date
   - Last used date
   - Description

### Delete a Key

1. Bedrock console → API Keys
2. Select the key
3. Click "Delete"
4. Confirm deletion

**Note**: Deleting a key immediately revokes access. Update your `.env` file!

### Rotate Keys

For security, rotate keys regularly:

**Long-term keys**:
1. Generate new key
2. Update `.env` with new key
3. Test that bot works
4. Delete old key

**Short-term keys**:
- Automatically expire after 12 hours
- Regenerate as needed

## Advanced: Programmatic Key Generation

For production, automate key generation:

```python
import boto3

# Create Bedrock client
client = boto3.client('bedrock', region_name='us-east-1')

# Generate short-term key
response = client.create_api_key(
    keyType='SHORT_TERM',
    description='Auto-generated for production'
)

api_key = response['apiKey']
# Store securely (e.g., AWS Secrets Manager)
```

## Support Resources

- [AWS Bedrock API Keys Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/api-keys.html)
- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [AWS Support](https://console.aws.amazon.com/support/)
- [AWS Bedrock Forum](https://repost.aws/tags/TA4ckYBCSTQWKWNy-0Zt8e-g/amazon-bedrock)

## Quick Reference

```bash
# Environment variables needed
AWS_BEARER_TOKEN_BEDROCK=your_api_key_here
AWS_REGION=us-east-1

# Test command
poetry run python test_receipt_scanner.py

# Run bot
poetry run python -m src.bot

# Check if key is set
echo $AWS_BEARER_TOKEN_BEDROCK

# Set key temporarily (for testing)
export AWS_BEARER_TOKEN_BEDROCK=your_key
export AWS_REGION=us-east-1
```

## Next Steps

After setting up your API key:
1. ✅ Test with `test_receipt_scanner.py`
2. ✅ Run the bot with `poetry run python -m src.bot`
3. ✅ Send a test receipt to your Telegram bot
4. ✅ Check `receipts_data/` for saved JSON
5. ✅ Set up billing alerts
6. ✅ Plan for key rotation

Happy expense tracking! 🚀
