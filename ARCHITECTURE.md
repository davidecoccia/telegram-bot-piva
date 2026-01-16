# Architecture Overview

## System Design

The Expense Tracker Bot follows a clean architecture pattern with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                      Telegram User                          │
└────────────────────┬────────────────────────────────────────┘
                     │ Sends receipt photo
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Telegram Bot API                          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Aiogram Framework                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Receipt Handler (receipt_handler.py)               │  │
│  │  - Receives photo messages                          │  │
│  │  - Downloads images                                 │  │
│  │  - Coordinates scanning                             │  │
│  └──────────────────┬───────────────────────────────────┘  │
└─────────────────────┼───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Receipt Scanner Service                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  receipt_scanner.py                                  │  │
│  │  - Manages Strands Agent                            │  │
│  │  - Processes images with vision LLM                 │  │
│  │  - Extracts structured data                         │  │
│  │  - Saves to file storage                            │  │
│  └──────────────────┬───────────────────────────────────┘  │
└─────────────────────┼───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Strands AI Agent                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  - Vision-enabled Claude 4 Sonnet                   │  │
│  │  - Analyzes receipt images                          │  │
│  │  - Extracts: location, date, amount, category       │  │
│  │  - Returns structured JSON                          │  │
│  └──────────────────┬───────────────────────────────────┘  │
└─────────────────────┼───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  AWS Bedrock API                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Claude 4 Sonnet Model                              │  │
│  │  - Multimodal (text + vision)                       │  │
│  │  - High accuracy OCR                                │  │
│  │  - Contextual understanding                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  File Storage                               │
│  receipts_data/                                             │
│  └── receipt_<phone>_<timestamp>.json                       │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Telegram Bot Layer (`src/bot/`)

**Purpose**: Handle Telegram interactions and message routing

**Key Files**:
- `__main__.py` - Bot initialization and startup
- `dispatcher.py` - Router setup
- `di.py` - Infrastructure dependency injection
- `di_services.py` - Service dependency injection

**Responsibilities**:
- Receive messages from Telegram
- Route to appropriate handlers
- Manage bot lifecycle
- Handle errors and retries

### 2. Logic Layer (`src/bot/logic/`)

**Purpose**: Business logic for different bot commands

**Key Files**:
- `start.py` - Welcome message handler
- `help.py` - Help command handler
- `receipt_handler.py` - Receipt photo processing

**Responsibilities**:
- Handle specific message types
- Coordinate with services
- Format responses for users
- Manage temporary files

### 3. Service Layer (`src/bot/services/`)

**Purpose**: Core business logic and external integrations

**Key Files**:
- `receipt_scanner.py` - Receipt scanning service

**Responsibilities**:
- Initialize and manage Strands Agent
- Process images with vision LLM
- Parse and validate responses
- Save data to storage
- Provide data retrieval methods

### 4. Configuration (`src/configuration.py`)

**Purpose**: Centralized configuration management

**Components**:
- `BotConfig` - Telegram bot settings
- `AWSConfig` - AWS Bedrock API key configuration
- `StorageConfig` - File storage paths
- `DatabaseConfig` - Database connection (future use)
- `RedisConfig` - Redis cache (future use)

### 5. Dependency Injection

**Framework**: Dishka

**Providers**:
- `ConfigurationProvider` - Configuration instances
- `InfrastructureProvider` - Bot and storage
- `FSMStorageProvider` - State management
- `DatabaseProvider` - Database connections
- `ServicesProvider` - Business services

**Benefits**:
- Loose coupling
- Easy testing
- Clear dependencies
- Lifecycle management

## Data Flow

### Receipt Processing Flow

1. **User sends photo** → Telegram API
2. **Bot receives message** → `receipt_handler.py`
3. **Download image** → Save to `temp_images/`
4. **Call scanner service** → `receipt_scanner.py`
5. **Initialize Strands Agent** → With vision model
6. **Send to LLM** → AWS Bedrock (Claude 4 Sonnet)
7. **Parse response** → Extract JSON data
8. **Validate data** → Ensure required fields
9. **Save to file** → `receipts_data/receipt_*.json`
10. **Format response** → User-friendly message
11. **Send to user** → Telegram API
12. **Cleanup** → Remove temp image

### Data Structure

**Receipt JSON Schema**:
```json
{
  "location": "string",        // Business name
  "date": "YYYY-MM-DD",        // Purchase date
  "category": "string",        // Expense category
  "amount": number,            // Total amount
  "currency": "string",        // Currency code
  "items": ["string"],         // List of items
  "user_phone": "string",      // User identifier
  "scanned_at": "ISO8601",     // Processing timestamp
  "image_path": "string"       // Original image path
}
```

## Technology Stack

### Core Framework
- **Python 3.13** - Programming language
- **Aiogram 3.x** - Telegram Bot framework
- **Dishka** - Dependency injection

### AI/ML
- **Strands Agents SDK** - AI agent framework
- **AWS Bedrock** - Model hosting
- **Claude 4 Sonnet** - Vision-enabled LLM

### Storage
- **File System** - JSON file storage (current)
- **PostgreSQL** - Database (available, not used yet)
- **Redis** - Caching (available, not used yet)

### Development
- **Poetry** - Dependency management
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Scalability Considerations

### Current Implementation
- File-based storage (simple, works for single instance)
- Synchronous file I/O with aiofiles
- No caching layer
- Single bot instance

### Future Enhancements

**Database Migration**:
```python
# Replace file storage with PostgreSQL
class ReceiptRepository:
    async def save_receipt(self, receipt: Receipt) -> int:
        # Save to database with proper indexing
        pass
    
    async def get_user_receipts(self, user_id: int) -> List[Receipt]:
        # Query with pagination
        pass
```

**Caching Layer**:
```python
# Add Redis caching for frequent queries
@cached(ttl=3600)
async def get_user_receipts(user_id: int):
    # Cache user receipts
    pass
```

**Horizontal Scaling**:
- Use webhook mode instead of polling
- Deploy multiple bot instances
- Load balancer for webhooks
- Shared database and Redis

**Message Queue**:
- Add Celery for async processing
- Queue receipt scanning tasks
- Handle high volume gracefully

## Security Considerations

### Current Implementation
- AWS credentials via environment variables
- No user authentication (Telegram handles it)
- File system permissions for storage
- Temporary files cleaned up after processing

### Recommendations
- Encrypt stored receipt data
- Add user authentication/authorization
- Implement rate limiting
- Audit logging for compliance
- Secure file upload validation
- PII data handling compliance

## Testing Strategy

### Unit Tests
- Service layer logic
- Data parsing and validation
- Configuration management

### Integration Tests
- Strands Agent integration
- File storage operations
- End-to-end receipt processing

### Manual Testing
- Use `test_receipt_scanner.py`
- Test with various receipt types
- Verify data accuracy

## Deployment

### Local Development
```bash
poetry run python -m src.bot
```

### Docker
```bash
docker-compose up -d
```

### Production Considerations
- Use environment-specific configs
- Enable monitoring and logging
- Set up health checks
- Configure auto-restart
- Use secrets management
- Enable CloudWatch logging

## Monitoring & Observability

### Current Logging
- Python logging module
- Console output
- Configurable log levels

### Future Enhancements
- Structured logging (JSON)
- Centralized log aggregation
- Metrics collection (Prometheus)
- Distributed tracing
- Error tracking (Sentry)
- Performance monitoring

## Cost Optimization

### AWS Bedrock Costs
- Pay per token (input + output)
- Vision models cost more than text-only
- Optimize prompt length
- Cache common responses
- Batch processing when possible

### Monitoring Costs
- Track token usage per request
- Set up billing alerts
- Optimize image resolution
- Consider model alternatives for simple receipts
