# Error Codes & Troubleshooting

Sens Prism returns structured error responses. Every error includes a human-readable message and a machine-readable code for programmatic handling.

## Error Response Format

All errors follow this structure:

```json
{
  "error": "error_type",
  "code": "SENS_###",
  "message": "Human-readable description",
  "details": {
    "field": "additional context"
  },
  "request_id": "req_abc123"
}
```

Use the `request_id` when contacting support for debugging.

---

## HTTP Status Codes

### 400 Bad Request

The request was malformed or invalid.

**Common causes**:
- Missing required parameters
- Invalid JSON syntax
- File upload format not supported
- Query parameter out of valid range

**Example**:
```json
{
  "error": "invalid_request",
  "code": "SENS_003",
  "message": "Missing required parameter: query",
  "details": {}
}
```

**Fix**: Review the [API Reference](reference.md) for required parameters.

---

### 401 Unauthorized

Authentication failed. Your API key is missing, invalid, or expired.

**Common causes**:
- API key not provided
- Malformed Authorization header
- API key expired or revoked

**Example**:
```json
{
  "error": "invalid_authentication",
  "code": "SENS_001",
  "message": "Invalid or expired API key"
}
```

**Fix**: See [Authentication Guide](authentication.md) to get or refresh your API key.

---

### 403 Forbidden

The API key lacks permission for this operation.

**Common causes**:
- Accessing another user's documents
- Insufficient plan tier for the operation
- API key scopes too restrictive

**Example**:
```json
{
  "error": "insufficient_permissions",
  "code": "SENS_004",
  "message": "Your API key does not have permission to delete documents"
}
```

**Fix**: Contact [support@sens.ai](mailto:support@sens.ai) to adjust permissions or upgrade your plan.

---

### 404 Not Found

The requested resource doesn't exist.

**Common causes**:
- Document ID not found
- Query ID expired or invalid
- Typo in endpoint URL

**Example**:
```json
{
  "error": "not_found",
  "code": "SENS_005",
  "message": "Document 'doc_invalid123' not found",
  "details": {
    "resource": "document",
    "id": "doc_invalid123"
  }
}
```

**Fix**: Double-check the resource ID. Use the correct document ID from upload response.

---

### 409 Conflict

The request conflicts with the current state of the resource.

**Common causes**:
- Attempting to query a document still processing
- Document already exists with same name

**Example**:
```json
{
  "error": "resource_conflict",
  "code": "SENS_006",
  "message": "Document is still processing. Try again in 30 seconds.",
  "details": {
    "document_id": "doc_abc123",
    "status": "processing",
    "estimated_ready_at": "2025-02-14T10:45:00Z"
  }
}
```

**Fix**: Wait for the document to finish processing before querying.

---

### 413 Payload Too Large

The uploaded file exceeds size limits.

**Limits by plan**:
- Free: 50 MB per file, 1 GB total storage
- Pro: 500 MB per file, 10 GB total storage
- Enterprise: Custom limits

**Example**:
```json
{
  "error": "payload_too_large",
  "code": "SENS_007",
  "message": "File size exceeds 500 MB limit",
  "details": {
    "file_size_mb": 750,
    "limit_mb": 500,
    "plan": "pro"
  }
}
```

**Fix**: Split large documents or upgrade your plan.

---

### 429 Too Many Requests

You've exceeded rate limits.

**Rate limits by plan**:
- Free: 10 requests/min, 5 documents/day
- Pro: 100 requests/min, 100 documents/day
- Enterprise: Unlimited

**Example**:
```json
{
  "error": "rate_limit_exceeded",
  "code": "SENS_008",
  "message": "Rate limit of 100 requests/minute exceeded",
  "details": {
    "limit": 100,
    "window_seconds": 60,
    "retry_after_seconds": 30
  }
}
```

**Response headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 2025-02-14T10:35:00Z
Retry-After: 30
```

**Fix**: Wait before retrying. Use `Retry-After` header for backoff timing.

---

### 500 Internal Server Error

An unexpected error occurred on our side.

**Example**:
```json
{
  "error": "internal_error",
  "code": "SENS_010",
  "message": "Internal server error. Our team has been notified.",
  "request_id": "req_xyz789"
}
```

**Fix**: Wait a moment and retry. If the error persists, contact [support@sens.ai](mailto:support@sens.ai) with the `request_id`.

---

### 503 Service Unavailable

The Sens API is temporarily unavailable.

**Common causes**:
- Scheduled maintenance
- Infrastructure issues
- High server load

**Example**:
```json
{
  "error": "service_unavailable",
  "code": "SENS_009",
  "message": "Service temporarily unavailable. Expected to recover in 5 minutes.",
  "details": {
    "retry_after_seconds": 300
  }
}
```

**Fix**: Check [status.sens.ai](https://status.sens.ai) for maintenance updates. Retry after the suggested delay.

---

## Sens-Specific Error Codes

| Code | HTTP | Error | Cause | Fix |
|------|------|-------|-------|-----|
| SENS_001 | 401 | Invalid authentication | API key missing, invalid, or expired | Refresh your API key |
| SENS_002 | 401 | Authentication expired | API key has expired | Generate a new API key |
| SENS_003 | 400 | Invalid request | Missing or malformed parameters | Check [API Reference](reference.md) |
| SENS_004 | 403 | Insufficient permissions | API key lacks required scopes | Contact support |
| SENS_005 | 404 | Not found | Resource doesn't exist | Verify resource ID |
| SENS_006 | 409 | Resource conflict | State prevents operation | Wait or retry later |
| SENS_007 | 413 | Payload too large | File exceeds size limit | Upgrade plan or split file |
| SENS_008 | 429 | Rate limit exceeded | Too many requests | Wait and retry |
| SENS_009 | 503 | Service unavailable | Temporary infrastructure issue | Retry later |
| SENS_010 | 500 | Internal error | Unexpected server error | Retry and contact support |

---

## Common Troubleshooting

### "Document is still processing"

**Error**: SENS_006

**What happened**: You tried to query a document that's still being indexed.

**Solution**:
- Wait 30-60 seconds for processing to complete
- Check status with `GET /v1/documents/{id}`
- Retry when status is `ready`

```python
import time
doc = client.upload_document("large_file.pdf")
while True:
    status = client.get_document(doc.id)
    if status.status == "ready":
        break
    print(f"Processing... ({status.status})")
    time.sleep(5)
```

---

### "Rate limit exceeded"

**Error**: SENS_008

**What happened**: You've made too many requests too quickly.

**Solution**:
- Implement exponential backoff
- Space out requests over time
- Upgrade to a higher plan tier

```python
import time
import random

for attempt in range(5):
    try:
        result = client.query("my query")
        break
    except SensRateLimitError as e:
        wait_time = (2 ** attempt) + random.uniform(0, 1)
        print(f"Rate limited. Waiting {wait_time:.1f}s...")
        time.sleep(wait_time)
```

---

### "File size exceeds limit"

**Error**: SENS_007

**What happened**: Your file is larger than your plan allows.

**Solution**:
- Split the PDF into multiple smaller files
- Upgrade to a higher plan tier
- Request custom limits for enterprise

```python
# Split a large document (example using PyPDF2)
from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("large_file.pdf")
chunk_size = 50  # pages per chunk

for i in range(0, len(reader.pages), chunk_size):
    writer = PdfWriter()
    for page_num in range(i, min(i + chunk_size, len(reader.pages))):
        writer.add_page(reader.pages[page_num])

    with open(f"chunk_{i}.pdf", "wb") as output:
        writer.write(output)

    doc = client.upload_document(f"chunk_{i}.pdf")
    print(f"Uploaded: {doc.id}")
```

---

### "Invalid API key"

**Error**: SENS_001

**What happened**: Your API key is missing, invalid, or typo'd.

**Solution**:
1. Check the Authorization header format: `Authorization: Bearer sens_sk_...`
2. Verify the key starts with `sens_sk_`
3. Generate a new key in the dashboard
4. Check for leading/trailing whitespace
5. Use environment variables to avoid typos

```python
import os

# Good: use environment variable
api_key = os.getenv("SENS_API_KEY")
if not api_key:
    raise ValueError("SENS_API_KEY environment variable not set")

client = SensClient(api_key=api_key)
```

---

### "Document not found"

**Error**: SENS_005

**What happened**: The document ID doesn't exist or has been deleted.

**Solution**:
- Verify the document ID from the upload response
- Check if the document was deleted
- Confirm you're querying the correct account

```python
# Save document IDs after upload
doc = client.upload_document("my_file.pdf")
print(f"Saved ID for later: {doc.id}")

# Later: verify the document still exists
try:
    doc_status = client.get_document(doc.id)
    print(f"Document status: {doc_status.status}")
except SensNotFoundError:
    print("Document was deleted. Upload again.")
```

---

### "Missing required parameter"

**Error**: SENS_003

**What happened**: You're missing a required field in your request.

**Solution**:
- Check the [API Reference](reference.md) for required fields
- Review the error `details` for which field is missing
- All endpoints require the Authorization header

```python
# Missing 'query' parameter
# result = client.query()  # ERROR!

# Correct:
result = client.query("What is this about?")
```

---

## Getting Help

If you can't resolve an error:

1. **Check [status.sens.ai](https://status.sens.ai)** — Is there a known incident?
2. **Review this guide** — Is your error listed above?
3. **Check the [API Reference](reference.md)** — Are you using the endpoint correctly?
4. **Contact support** — Email [support@sens.ai](mailto:support@sens.ai) with:
   - The `request_id` from the error response
   - Your API key (first 10 chars only)
   - Steps to reproduce
   - Expected vs. actual behavior

We typically respond to support emails within 2 hours during business hours.
