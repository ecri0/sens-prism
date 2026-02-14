# API Reference

Base URL: `https://api.sens.ai/v1`

All requests require an `Authorization: Bearer` header with your API key (format: `sens_sk_...`).

Responses are JSON. Timestamps are ISO 8601 format.

---

## Authentication

```bash
curl -X GET https://api.sens.ai/v1/documents \
  -H "Authorization: Bearer sens_sk_your_key_here"
```

See [Authentication Guide](authentication.md) for key management and token refresh.

---

## Documents

### Upload Document

Upload a document to be processed and indexed.

**Endpoint**: `POST /v1/documents`

**Request**:
```bash
curl -X POST https://api.sens.ai/v1/documents \
  -H "Authorization: Bearer sens_sk_your_key_here" \
  -F "file=@example.pdf" \
  -F "title=My Document" \
  -F "tags=legal,contract"
```

**Parameters**:
- `file` (multipart, required) — Document file (PDF, DOCX, TXT, RTF)
- `title` (string, optional) — Human-readable document name
- `tags` (string, optional) — Comma-separated tags for organization

**Response** (202 Accepted):
```json
{
  "id": "doc_1a2b3c4d5e",
  "status": "processing",
  "title": "My Document",
  "size_bytes": 245680,
  "tags": ["legal", "contract"],
  "created_at": "2025-02-14T10:30:00Z",
  "estimated_ready_at": "2025-02-14T10:45:00Z"
}
```

**Status values**:
- `processing` — Being indexed and semantic layers extracted
- `ready` — Available for querying
- `failed` — Processing error (see error details)

---

### Get Document

Retrieve document metadata and status.

**Endpoint**: `GET /v1/documents/{id}`

**Request**:
```bash
curl -X GET https://api.sens.ai/v1/documents/doc_1a2b3c4d5e \
  -H "Authorization: Bearer sens_sk_your_key_here"
```

**Response** (200 OK):
```json
{
  "id": "doc_1a2b3c4d5e",
  "status": "ready",
  "title": "My Document",
  "size_bytes": 245680,
  "tags": ["legal", "contract"],
  "created_at": "2025-02-14T10:30:00Z",
  "ready_at": "2025-02-14T10:42:15Z",
  "page_count": 12,
  "chunk_count": 156,
  "concept_count": 342
}
```

---

### Delete Document

Remove a document from your account. This is permanent and cannot be undone.

**Endpoint**: `DELETE /v1/documents/{id}`

**Request**:
```bash
curl -X DELETE https://api.sens.ai/v1/documents/doc_1a2b3c4d5e \
  -H "Authorization: Bearer sens_sk_your_key_here"
```

**Response** (204 No Content):
```
(empty body)
```

After deletion:
- Document is immediately removed from all indexes
- Encrypted data is securely purged
- No recovery is possible

---

## Queries

### Query Knowledge

Submit a query to be answered using your document knowledge base.

**Endpoint**: `POST /v1/query`

**Request**:
```bash
curl -X POST https://api.sens.ai/v1/query \
  -H "Authorization: Bearer sens_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the payment terms?",
    "document_ids": ["doc_1a2b3c4d5e", "doc_2f3g4h5i6j"],
    "limit": 5,
    "confidence_threshold": 0.75
  }'
```

**Parameters**:
- `query` (string, required) — Your question or search query
- `document_ids` (array of strings, optional) — Specific documents to query. If omitted, searches all documents.
- `limit` (integer, optional, default: 3) — Maximum number of source chunks to include
- `confidence_threshold` (number, optional, default: 0.5) — Minimum confidence score (0.0–1.0) for results

**Response** (200 OK):
```json
{
  "query_id": "qry_xyz789",
  "query": "What are the payment terms?",
  "answer": "Payment shall be made within 30 days of invoice. Late payments incur 1.5% monthly interest.",
  "confidence_score": 0.94,
  "processing_time_ms": 245,
  "sources": [
    {
      "document_id": "doc_1a2b3c4d5e",
      "document_title": "My Document",
      "page": 3,
      "confidence_score": 0.98
    },
    {
      "document_id": "doc_1a2b3c4d5e",
      "document_title": "My Document",
      "page": 4,
      "confidence_score": 0.91
    }
  ]
}
```

---

### Get Context Rail

Retrieve detailed context information for a query, including excerpts and semantic layer details.

**Endpoint**: `GET /v1/context-rail/{query_id}`

**Request**:
```bash
curl -X GET https://api.sens.ai/v1/context-rail/qry_xyz789 \
  -H "Authorization: Bearer sens_sk_your_key_here"
```

**Response** (200 OK):
```json
{
  "query_id": "qry_xyz789",
  "query": "What are the payment terms?",
  "retrieved_at": "2025-02-14T10:35:00Z",
  "sources": [
    {
      "document_id": "doc_1a2b3c4d5e",
      "document_title": "My Document",
      "page": 3,
      "excerpt": "Payment shall be made within 30 days of invoice issuance.",
      "confidence_score": 0.98,
      "semantic_layer": "chunk",
      "matched_concepts": ["PAYMENT_TERM", "DURATION"]
    },
    {
      "document_id": "doc_1a2b3c4d5e",
      "document_title": "My Document",
      "page": 4,
      "excerpt": "Late payments incur a 1.5% monthly interest charge.",
      "confidence_score": 0.91,
      "semantic_layer": "pragmatic",
      "matched_concepts": ["PENALTY", "INTEREST_RATE"],
      "pragmatic_insights": [
        "18% annualized interest rate",
        "Recommend automated payment processing"
      ]
    }
  ],
  "summary": {
    "total_chunks_evaluated": 48,
    "chunks_returned": 2,
    "average_confidence": 0.945
  }
}
```

**Semantic layer values**:
- `chunk` — Raw text with linguistic features
- `concept` — Knowledge graph connections
- `context` — User-specific contextual meaning
- `pragmatic` — Actionable insights
- `universal` — Model-independent identifiers

---

## Rate Limits

Rate limits are enforced per API key. Limits depend on your plan:

| Plan | Requests/Min | Documents/Day | Storage |
|------|-------------|---------------|---------|
| Free | 10 | 5 | 1 GB |
| Pro (Prism) | 100 | 100 | 10 GB |
| Enterprise | Unlimited | Unlimited | Custom |

### Rate Limit Headers

Each response includes rate limit information:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 2025-02-14T10:35:00Z
```

When rate limited, the API returns `429 Too Many Requests`:

```json
{
  "error": "rate_limit_exceeded",
  "code": "SENS_008",
  "message": "Rate limit of 100 requests/minute exceeded",
  "retry_after_seconds": 30
}
```

---

## Error Handling

All errors follow a standard format:

```json
{
  "error": "error_type",
  "code": "SENS_###",
  "message": "Human-readable error message",
  "details": {
    "field": "additional context if applicable"
  }
}
```

See [Error Codes](errors.md) for complete reference.

---

## Example: Complete Workflow

```bash
# 1. Upload a document
DOC_RESPONSE=$(curl -s -X POST https://api.sens.ai/v1/documents \
  -H "Authorization: Bearer sens_sk_..." \
  -F "file=@contract.pdf" \
  -F "title=Service Agreement")

DOC_ID=$(echo $DOC_RESPONSE | jq -r '.id')
echo "Document uploading: $DOC_ID"

# 2. Wait for processing (optional—can query before done)
sleep 5

# 3. Query the document
QUERY_RESPONSE=$(curl -s -X POST https://api.sens.ai/v1/query \
  -H "Authorization: Bearer sens_sk_..." \
  -H "Content-Type: application/json" \
  -d "{
    \"query\": \"What is the termination clause?\",
    \"document_ids\": [\"$DOC_ID\"],
    \"limit\": 3
  }")

QUERY_ID=$(echo $QUERY_RESPONSE | jq -r '.query_id')
echo "Query result: $QUERY_ID"
echo $QUERY_RESPONSE | jq '.answer'

# 4. Get detailed context
curl -s -X GET https://api.sens.ai/v1/context-rail/$QUERY_ID \
  -H "Authorization: Bearer sens_sk_..." | jq '.sources'
```

---

## SDK Methods

The Python and TypeScript SDKs provide convenience wrappers:

**Python**:
```python
client = SensClient(api_key="sens_sk_...")
doc = client.upload_document("contract.pdf")
result = client.query("What is the termination clause?", document_ids=[doc.id])
context = client.get_context_rail(result.query_id)
```

**TypeScript**:
```typescript
const client = new SensClient({ apiKey: "sens_sk_..." });
const doc = await client.uploadDocument("contract.pdf");
const result = await client.query("What is the termination clause?", {
  documentIds: [doc.id]
});
const context = await client.getContextRail(result.queryId);
```

See [SDK documentation](../getting-started.md) for full examples.
