---
name: log-analysis-patterns
description: Identifies log analysis best practices including log structure, log levels, structured logging, log aggregation, and log analysis techniques. Use when analyzing logs for debugging, reviewing logging practices, planning logging strategy, checking log quality, and ensuring observability. Provides log analysis patterns, structured logging templates, log parsing techniques, and logging checklists. Loaded by debugger agent during DEBUG workflow or when log analysis needed. Complements systematic-debugging with specific log-focused guidance. Critical for debugging, monitoring, and troubleshooting.
license: MIT
---

# Log Analysis Patterns

## Progressive Loading Stages

### Stage 1: Metadata
- **Skill**: Log Analysis Patterns
- **Purpose**: Analyze logs effectively to debug issues
- **When**: Debugging, log analysis, troubleshooting
- **Core Rule**: Good logs make debugging 10x faster
- **Sections Available**: Log Levels, Structured Logging, Log Parsing, Quick Checks

---

### Stage 2: Quick Reference

#### Log Analysis Checklist

```
Log Quality:
- [ ] Log levels used correctly
- [ ] Structured logging implemented
- [ ] Timestamps in ISO 8601 format
- [ ] Request IDs for tracing
- [ ] Error stack traces included
- [ ] Context information present
- [ ] Sensitive data redacted
- [ ] Log aggregation configured
- [ ] Log retention policy defined
- [ ] Alerts configured
```

#### Critical Log Patterns

**Log Levels**:
```
ERROR:   System errors, exceptions, failures
WARN:    Warnings, deprecated usage, potential issues
INFO:    Important events, state changes, milestones
DEBUG:   Detailed information for debugging
TRACE:   Very detailed information, function calls

‚ùBAD LOGGING
console.log('User login');
console.log('Error: ' + error);
console.log('Processing...');

‚úGOOD LOGGING
logger.info('User login', { userId: 123, timestamp: new Date() });
logger.error('Login failed', { userId: 123, error: error.message, stack: error.stack });
logger.debug('Processing user data', { userId: 123, data: userData });
```

**Structured Logging**:
```typescript
// ‚ùUNSTRUCTURED
console.log('User 123 logged in at 2024-01-15 10:30:00');

// ‚úSTRUCTURED
logger.info('user_login', {
  userId: 123,
  email: 'user@example.com',
  timestamp: '2024-01-15T10:30:00Z',
  ipAddress: '192.168.1.1',
  userAgent: 'Mozilla/5.0...',
  duration: 245 // ms
});
```

**Request Tracing**:
```typescript
// ‚úREQUEST ID TRACING
const requestId = generateUUID();
logger.info('request_start', {
  requestId,
  method: 'POST',
  path: '/api/users',
  timestamp: new Date().toISOString()
});

// All logs in this request include requestId
logger.info('database_query', {
  requestId,
  query: 'SELECT * FROM users',
  duration: 45
});

logger.info('request_end', {
  requestId,
  status: 200,
  duration: 245
});
```

**Error Logging**:
```typescript
// ‚ùINCOMPLETE
logger.error('Error occurred');

// ‚úCOMPLETE
logger.error('Payment processing failed', {
  requestId: 'req-123',
  userId: 456,
  amount: 99.99,
  error: error.message,
  stack: error.stack,
  context: {
    paymentMethod: 'credit_card',
    retryCount: 2,
    timestamp: new Date().toISOString()
  }
});
```

#### Red Flags üö©
```bash
# Find console.log (should use logger)
grep -r "console\." src/ --include="*.ts"

# Find unstructured logging
grep -r "logger\.log\|logger\.info.*\+" src/

# Find missing error context
grep -r "catch.*{" src/ -A 2 | grep -v "logger\|throw"

# Find missing request IDs
grep -r "logger\." src/ | grep -v "requestId\|traceId"
```

---

### Stage 3: Detailed Guide

## Structured Logging Implementation

### Winston Logger Setup

```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'api-service' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}
```

### Pino Logger Setup

```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',
    options: {
      colorize: true,
      translateTime: 'SYS:standard',
      ignore: 'pid,hostname'
    }
  }
});

// Usage:
logger.info({ userId: 123 }, 'User logged in');
logger.error({ error: err }, 'Payment failed');
```

## Log Analysis Techniques

### Grep Patterns

```bash
# Find all errors
grep "ERROR" combined.log

# Find errors for specific user
grep "userId.*123" combined.log | grep "ERROR"

# Find slow requests (> 1000ms)
grep "duration.*[0-9]\{4,\}" combined.log

# Find failed payments
grep "payment_failed" combined.log

# Find requests from specific IP
grep "ipAddress.*192.168" combined.log

# Find requests in time range
grep "2024-01-15T10:" combined.log
```

### Log Aggregation with ELK Stack

```
Elasticsearch: Store and index logs
Logstash: Parse and transform logs
Kibana: Visualize and analyze logs

Pipeline:
Application ‚ÜLogstash ‚ÜElasticsearch ‚ÜKibana
```

### Log Parsing

```typescript
// Parse log line
const logLine = '2024-01-15T10:30:00Z ERROR user_login userId=123 error="Invalid password"';

const pattern = /(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)\s+(\w+)\s+(\w+)\s+(.*)/;
const match = logLine.match(pattern);

const [, timestamp, level, event, data] = match;
// timestamp: 2024-01-15T10:30:00Z
// level: ERROR
// event: user_login
// data: userId=123 error="Invalid password"
```

## Debugging with Logs

### Finding Root Cause

```
1. Find the error log
   grep "ERROR" combined.log | grep "payment_failed"

2. Get the request ID
   2024-01-15T10:30:00Z ERROR payment_failed requestId=req-123

3. Find all logs for that request
   grep "req-123" combined.log

4. Trace the flow
   10:30:00 request_start
   10:30:01 database_query
   10:30:02 payment_api_call
   10:30:03 payment_failed
   10:30:04 request_end

5. Identify the issue
   payment_api_call returned 500 error
```

### Common Log Patterns

```
Database Connection Error:
  "error": "ECONNREFUSED",
  "code": "ECONNREFUSED",
  "address": "localhost",
  "port": 5432

Timeout Error:
  "error": "ETIMEDOUT",
  "code": "ETIMEDOUT",
  "timeout": 5000

Memory Leak:
  "heapUsed": 1024000000,  // 1GB
  "heapTotal": 2048000000, // 2GB
  "external": 512000000    // 512MB

Rate Limit:
  "status": 429,
  "error": "Too Many Requests",
  "retryAfter": 60
```

## Logging Best Practices

### What to Log

```
‚úDO LOG:
- Application startup/shutdown
- User actions (login, logout, purchase)
- API requests and responses
- Database queries (in debug mode)
- Errors and exceptions
- Performance metrics
- Security events
- State changes

‚ùDON'T LOG:
- Passwords or API keys
- Credit card numbers
- Personal identification numbers
- Session tokens
- Sensitive user data
- Verbose debug info in production
```

### Log Retention

```
ERROR logs:   Keep for 90 days
WARN logs:    Keep for 30 days
INFO logs:    Keep for 7 days
DEBUG logs:   Keep for 1 day (production)
TRACE logs:   Keep for 1 hour (development only)
```

## Logging Checklist

### Implementation
- [ ] Logger configured
- [ ] Log levels used correctly
- [ ] Structured logging implemented
- [ ] Request IDs included
- [ ] Timestamps in ISO 8601
- [ ] Error stack traces included
- [ ] Sensitive data redacted
- [ ] Performance metrics logged

### Monitoring
- [ ] Log aggregation configured
- [ ] Alerts set up for errors
- [ ] Dashboards created
- [ ] Log retention policy defined
- [ ] Log rotation configured
- [ ] Disk space monitored

### Analysis
- [ ] Logs searchable
- [ ] Logs indexed
- [ ] Queries optimized
- [ ] Trends identified
- [ ] Anomalies detected
- [ ] Root causes found

---

**Remember**: Good logs are your best debugging tool. Invest in logging!
