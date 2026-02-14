# Sens Prism Python SDK

The official Python SDK for Sens Prism, the Sovereign AI Gateway. Query your documents with confidence, knowing exactly why the AI says what it says.

## Installation

```bash
pip install sens-prism
```

## Quick Start

```python
from sens import SensClient

# Initialize the client
client = SensClient(api_key="sens_sk_your_key_here")

# Upload a document
doc = client.upload_document(
    file_path="contract.pdf",
    title="Service Agreement"
)
print(f"Document uploaded: {doc.id}")

# Query your knowledge
result = client.query(
    query="What are the payment terms?",
    document_ids=[doc.id]
)

print(f"Answer: {result.answer}")
print(f"Confidence: {result.confidence_score:.0%}")

# Get detailed context (sources, page numbers, confidence per source)
context = client.get_context_rail(result.query_id)
for source in context.sources:
    print(f"\nPage {source.page}: {source.excerpt}")
    print(f"Confidence: {source.confidence_score:.0%}")
```

## Authentication

Get your API key at [dashboard.sens.ai](https://dashboard.sens.ai):

```python
# Provide API key directly
client = SensClient(api_key="sens_sk_...")

# Or use environment variable
import os
os.environ["SENS_API_KEY"] = "sens_sk_..."
client = SensClient()  # Reads from SENS_API_KEY
```

## Documentation

- **[Getting Started](../../docs/getting-started.md)** — 5-minute quickstart
- **[API Reference](../../docs/api/reference.md)** — All endpoints
- **[Concepts](../../docs/concepts/overview.md)** — Understanding Sens Prism
- **[Examples](../../examples/python/)** — Complete working examples

## Core Methods

### `upload_document(file_path, title=None, tags=None) -> Document`

Upload a document for processing and indexing.

```python
doc = client.upload_document(
    file_path="earnings_report.pdf",
    title="Q1 2024 Earnings",
    tags=["financial", "q1", "2024"]
)

# Check status
doc_status = client.get_document(doc.id)
print(f"Status: {doc_status.status}")  # processing, ready, or failed
```

**Supported formats**: PDF, DOCX, TXT, RTF

### `get_document(document_id) -> Document`

Get document metadata and current status.

```python
doc = client.get_document("doc_abc123")
print(f"Pages: {doc.page_count}")
print(f"Status: {doc.status}")
```

### `delete_document(document_id) -> None`

Permanently delete a document (cannot be undone).

```python
client.delete_document("doc_abc123")
```

### `query(query, document_ids=None, tags=None, limit=3, confidence_threshold=0.5) -> QueryResult`

Query your documents.

```python
# Query all documents
result = client.query("What are the key risks?")

# Query specific documents
result = client.query(
    query="What is the termination clause?",
    document_ids=["doc_1", "doc_2"],
    limit=5,
    confidence_threshold=0.80
)

print(f"Answer: {result.answer}")
print(f"Query ID: {result.query_id}")
print(f"Confidence: {result.confidence_score:.0%}")
print(f"Sources: {len(result.sources)}")
```

**Parameters**:
- `query` (str, required) — Your question
- `document_ids` (list, optional) — Specific documents to search
- `tags` (list, optional) — Filter by tags (e.g., `["legal", "2024"]`)
- `limit` (int, default: 3) — Max sources to return
- `confidence_threshold` (float, default: 0.5) — Min confidence (0-1)

### `get_context_rail(query_id) -> ContextRail`

Get detailed context information for a query, including source excerpts and confidence per source.

```python
context = client.get_context_rail(result.query_id)

for source in context.sources:
    print(f"Document: {source.document_title}")
    print(f"Page: {source.page}")
    print(f"Excerpt: {source.excerpt}")
    print(f"Confidence: {source.confidence_score:.0%}")
    print(f"Semantic Layer: {source.semantic_layer}")
    print(f"Concepts: {source.matched_concepts}")
    print()
```

## Async Support

All methods have async variants:

```python
import asyncio
from sens import SensClient

async def main():
    client = SensClient(api_key="sens_sk_...")

    # Upload async
    doc = await client.upload_document_async("document.pdf")

    # Query async
    result = await client.query_async(
        "What is the answer?",
        document_ids=[doc.id]
    )

    print(result.answer)

asyncio.run(main())
```

## Error Handling

```python
from sens.exceptions import (
    SensAuthError,
    SensNotFoundError,
    SensRateLimitError,
    SensValidationError,
)

try:
    result = client.query("What is this?")
except SensAuthError as e:
    print(f"Authentication failed: {e.message}")
except SensNotFoundError as e:
    print(f"Document not found: {e.details}")
except SensRateLimitError as e:
    print(f"Rate limited. Retry in {e.retry_after} seconds")
except SensValidationError as e:
    print(f"Invalid request: {e.message}")
```

## Context Manager

Use the client as a context manager for automatic cleanup:

```python
with SensClient(api_key="sens_sk_...") as client:
    doc = client.upload_document("file.pdf")
    result = client.query("What is this?", document_ids=[doc.id])
    print(result.answer)
# Client connection is automatically closed
```

## Batch Operations

Process multiple documents efficiently:

```python
import glob

documents = []

# Upload multiple documents
for pdf_path in glob.glob("documents/*.pdf"):
    doc = client.upload_document(
        file_path=pdf_path,
        tags=["batch_upload", "2024"]
    )
    documents.append(doc)

print(f"Uploaded {len(documents)} documents")

# Query all of them
result = client.query(
    "What are the key takeaways?",
    document_ids=[d.id for d in documents],
    limit=10
)

print(f"Found in {len(result.sources)} locations")
```

## Polling for Document Status

Wait for documents to finish processing:

```python
import time

doc = client.upload_document("large_file.pdf")

# Poll until ready
while True:
    status = client.get_document(doc.id)
    if status.status == "ready":
        print("Document ready to query!")
        break
    elif status.status == "failed":
        print(f"Processing failed: {status}")
        break
    else:
        print(f"Still processing... (estimated {status.estimated_ready_at})")
        time.sleep(5)
```

## Rate Limits

The SDK automatically includes rate limit headers in responses:

```python
result = client.query("What is this?")
# Check your rate limits in the response metadata
```

Rate limits by plan:
- **Free**: 10 req/min, 5 docs/day, 1 GB storage
- **Pro**: 100 req/min, 100 docs/day, 10 GB storage
- **Enterprise**: Unlimited

For production use, implement exponential backoff:

```python
import time
import random

def query_with_backoff(client, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.query(query)
        except SensRateLimitError as e:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f"Rate limited. Waiting {wait_time:.1f}s...")
            time.sleep(wait_time)
    raise SensRateLimitError("Max retries exceeded")
```

## Pricing

Sens Prism starts at **$29/month**. See [sens.ai/pricing](https://sens.ai/pricing) for details.

## Support

- Documentation: [sens.ai/docs](https://sens.ai/docs)
- Issues: [GitHub Issues](https://github.com/ecri0/prism/issues)
- Email: [support@sens.ai](mailto:support@sens.ai)

## License

Licensed under Business Source License 1.1. See [LICENSE](../../LICENSE) for details.
