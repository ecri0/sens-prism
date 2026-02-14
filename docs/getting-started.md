# Getting Started with Sens Prism

Get up and running with Sens Prism in 5 minutes. This guide walks you through authentication, uploading your first document, and querying it.

## Prerequisites

- Python 3.9+ or Node.js 16+
- An API key (get one at [dashboard.sens.ai](https://dashboard.sens.ai))
- A document to upload (PDF, DOCX, or TXT)

## Step 1: Get Your API Key

1. Sign up at [sens.ai](https://sens.ai)
2. Navigate to **Settings → API Keys**
3. Click **Create Key** and copy your `sens_sk_...` token
4. Keep this secret—treat it like a password

## Step 2: Install the SDK

### Python

```bash
pip install sens-prism
```

### TypeScript/JavaScript

```bash
npm install @sens/prism
```

## Step 3: Upload Your First Document

### Python

```python
from sens import SensClient

client = SensClient(api_key="sens_sk_your_key_here")

# Upload a document
doc = client.upload_document(
    file_path="example.pdf",
    title="My Document"
)

print(f"Document uploaded: {doc.id}")
```

### cURL

```bash
curl -X POST https://api.sens.ai/v1/documents \
  -H "Authorization: Bearer sens_sk_your_key_here" \
  -F "file=@example.pdf"
```

Response:
```json
{
  "id": "doc_1a2b3c4d5e",
  "status": "processing",
  "title": "My Document",
  "created_at": "2025-02-14T10:30:00Z"
}
```

## Step 4: Query Your Knowledge

Once the document is processed (status: `ready`), query it:

### Python

```python
# Query the document
result = client.query(
    query="What are the main topics covered?",
    document_ids=["doc_1a2b3c4d5e"]
)

print(result.answer)
```

### cURL

```bash
curl -X POST https://api.sens.ai/v1/query \
  -H "Authorization: Bearer sens_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main topics covered?",
    "document_ids": ["doc_1a2b3c4d5e"]
  }'
```

Response:
```json
{
  "query_id": "qry_xyz789",
  "answer": "The document covers three main topics: foundational concepts, implementation strategies, and case studies.",
  "confidence_score": 0.94,
  "processing_time_ms": 245
}
```

## Step 5: View Context Rail Details

The Context Rail shows exactly where the AI found information:

### Python

```python
# Get detailed context information
context = client.get_context_rail(query_id="qry_xyz789")

for source in context.sources:
    print(f"Page {source.page}: {source.excerpt}")
    print(f"Confidence: {source.confidence_score}")
    print()
```

### cURL

```bash
curl -X GET https://api.sens.ai/v1/context-rail/qry_xyz789 \
  -H "Authorization: Bearer sens_sk_your_key_here"
```

Response:
```json
{
  "query_id": "qry_xyz789",
  "sources": [
    {
      "document_id": "doc_1a2b3c4d5e",
      "page": 3,
      "excerpt": "The three foundational concepts are transparency, control, and ownership.",
      "confidence_score": 0.98,
      "semantic_layer": "concept"
    },
    {
      "document_id": "doc_1a2b3c4d5e",
      "page": 7,
      "excerpt": "Implementation requires careful planning of context injection.",
      "confidence_score": 0.91,
      "semantic_layer": "pragmatic"
    }
  ]
}
```

## Next Steps

- **[Explore Concepts](concepts/overview.md)** — Understand Sovereign AI Gateways
- **[Review Semantic Layers](concepts/semantic-layers.md)** — How we extract meaning
- **[Read API Reference](api/reference.md)** — All available endpoints
- **[Check Use Cases](guides/)** — See Sens Prism in action
- **[View Examples](../examples/)** — Working code samples

## Troubleshooting

**API returns 401 Unauthorized**
- Verify your API key is correct
- Check that it starts with `sens_sk_`
- Ensure you're using the right environment (dev vs. production)

**Document shows status: processing for too long**
- Processing times vary by document size
- Large documents (100+ MB) may take several minutes
- Check your usage limits at dashboard.sens.ai

**Query returns low confidence scores**
- Try refining your query to be more specific
- Ensure the document contains relevant information
- Check the Context Rail sources to see what was found

## Rate Limits

| Plan | Requests/Min | Documents/Day | Storage |
|------|-------------|---------------|---------|
| Free | 10 | 5 | 1 GB |
| Pro (Prism) | 100 | 100 | 10 GB |
| Enterprise | Unlimited | Unlimited | Custom |

You're now ready to use Sens Prism! For detailed API documentation, see the [API Reference](api/reference.md).
