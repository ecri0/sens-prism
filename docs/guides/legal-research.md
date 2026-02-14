# Legal Research with Sens Prism

Lawyers and legal professionals manage thousands of pages of contracts, case law, and regulatory documents. Sens Prism makes it faster to find key clauses while keeping sensitive client information protected.

## The Challenge

A mid-size law firm handles 50+ active cases with:
- Hundreds of client contracts across different jurisdictions
- Regulatory documents and precedent cases
- Confidential client communications
- Payment and settlement details

Traditional approaches:
- Manual document review (hours per document)
- Keyword search misses semantic variations
- Risk of exposing confidential information if documents go to cloud
- No transparency into why a clause is "relevant"

## Solution: Sens Prism Workflow

### Step 1: Upload Case Documents

Upload all relevant documents securely:

```bash
# Upload client contracts
curl -X POST https://api.sens.ai/v1/documents \
  -H "Authorization: Bearer sens_sk_..." \
  -F "file=@smith_v_acme_contract.pdf" \
  -F "title=Smith v. Acme - Service Agreement" \
  -F "tags=contract,smith_v_acme,service"

# Upload regulatory documents
curl -X POST https://api.sens.ai/v1/documents \
  -H "Authorization: Bearer sens_sk_..." \
  -F "file=@state_labor_code_2025.pdf" \
  -F "title=State Labor Code - Section 2025" \
  -F "tags=regulatory,labor_law"
```

**Smart Sanitizer** automatically:
- Identifies client names and marks them for protection
- Flags confidential settlement amounts
- Detects personal identifiers (email, phone)
- Removes but tracks all PII for your records

Sensitive data never reaches the LLM.

### Step 2: Query Specific Legal Concepts

Find relevant clauses across your case file:

```bash
curl -X POST https://api.sens.ai/v1/query \
  -H "Authorization: Bearer sens_sk_..." \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the termination rights if either party breaches?",
    "document_ids": ["smith_v_acme_contract.pdf"],
    "limit": 5,
    "confidence_threshold": 0.85
  }'
```

Response:
```json
{
  "query_id": "qry_legal_001",
  "answer": "Either party may terminate immediately upon material breach if the breaching party fails to cure within 30 days of written notice. The non-breaching party is entitled to pursue remedies including injunctive relief.",
  "confidence_score": 0.96,
  "sources": [
    {
      "document_id": "smith_v_acme_contract.pdf",
      "page": 7,
      "confidence_score": 0.98
    },
    {
      "document_id": "smith_v_acme_contract.pdf",
      "page": 8,
      "confidence_score": 0.94
    }
  ]
}
```

### Step 3: View Context Rail for Provenance

Get the exact excerpts and understand the reasoning:

```bash
curl -X GET https://api.sens.ai/v1/context-rail/qry_legal_001 \
  -H "Authorization: Bearer sens_sk_..."
```

Response:
```json
{
  "sources": [
    {
      "document_id": "smith_v_acme_contract.pdf",
      "page": 7,
      "excerpt": "Either party may terminate this Agreement immediately upon written notice if the other party commits a material breach and fails to cure such breach within thirty (30) days of receiving written notice of the breach.",
      "confidence_score": 0.98,
      "semantic_layer": "chunk",
      "matched_concepts": ["TERMINATION_RIGHT", "BREACH", "CURE_PERIOD"]
    },
    {
      "document_id": "smith_v_acme_contract.pdf",
      "page": 8,
      "excerpt": "The non-breaching party shall be entitled to all available remedies at law or in equity, including injunctive relief and specific performance.",
      "confidence_score": 0.94,
      "semantic_layer": "pragmatic",
      "matched_concepts": ["REMEDY", "INJUNCTIVE_RELIEF"],
      "pragmatic_insights": [
        "Provides both equitable and legal remedies",
        "Enables emergency injunction if breach is imminent"
      ]
    }
  ]
}
```

You now have:
- **Exact page citations** for your legal brief
- **Full excerpts** to include in filings
- **Confidence scores** showing relevance strength
- **Semantic layer** indicating clause type (substantive vs. procedural)
- **Pragmatic insights** for case strategy

### Step 4: Cross-Reference Across Multiple Cases

Query all relevant documents in your case database:

```bash
curl -X POST https://api.sens.ai/v1/query \
  -H "Authorization: Bearer sens_sk_..." \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Are there any 30-day cure periods in service agreements?",
    "tags": ["contract", "service"],
    "limit": 10
  }'
```

Sens Prism searches semantically across all matching documents and shows:
- Which contracts have this clause
- Variations in the language
- Cross-client patterns (e.g., "Are 30-day cure periods standard for this vendor type?")

---

## Use Case Examples

### Example 1: Finding Similar Clauses

**Scenario**: You're drafting a new employment contract and want to check what termination clauses your firm has used before.

```python
from sens import SensClient

client = SensClient(api_key="sens_sk_...")

# Search all employment contracts
result = client.query(
    query="What are the grounds for termination for cause?",
    tags=["contract", "employment"]
)

print(f"Found {len(result.sources)} relevant clauses")
for source in result.sources:
    context = client.get_context_rail(result.query_id)
    for src in context.sources:
        if src.document_id == source.document_id:
            print(f"\n{src.document_title}:")
            print(f"  Page {src.page}: {src.excerpt[:100]}...")
            print(f"  Confidence: {src.confidence_score:.0%}")
```

### Example 2: Compliance Checking

**Scenario**: Verify that all client contracts comply with recent regulatory changes.

```python
# Query: Do our contracts comply with the new CCPA data deletion requirement?
result = client.query(
    query="Does this contract include a data deletion obligation within 45 days?",
    tags=["contract"],
    confidence_threshold=0.80  # Only high-confidence matches
)

# Check each contract
for source in result.sources:
    doc = client.get_document(source.document_id)
    if result.confidence_score > 0.85:
        print(f"✓ {doc.title} - CCPA compliant")
    else:
        print(f"? {doc.title} - REVIEW NEEDED (confidence: {result.confidence_score:.0%})")
```

### Example 3: Due Diligence on Acquisition

**Scenario**: Reviewing a target company's contracts for risk during M&A due diligence.

```python
# Upload all target company contracts
doc_ids = []
for contract in target_contracts:
    doc = client.upload_document(contract)
    doc_ids.append(doc.id)

# Key risk questions
risk_queries = [
    "Are there any change-of-control provisions that terminate the contract?",
    "What are the financial penalties if this contract is breached?",
    "Are there exclusive dealing or non-compete clauses?",
    "What termination rights does the other party have?"
]

for query in risk_queries:
    result = client.query(query, document_ids=doc_ids)
    print(f"\n{query}")
    print(f"Answer: {result.answer}")
    print(f"Confidence: {result.confidence_score:.0%}")
```

---

## Privacy & Compliance

### Data Protection

- **Client names** are automatically redacted before LLM processing
- **Settlement amounts** are flagged and protected
- **Personal details** (SSN, DOB, email) are removed
- **You maintain control** of encryption keys

Your firm's confidential client information never leaves your control.

### Audit Trail

Every query is logged with:
- Who made the query
- When it was made
- What was queried
- Which documents were searched
- What results were returned

This audit trail helps you demonstrate compliance with client confidentiality obligations.

### Regulatory Alignment

Sens Prism helps with:
- **GDPR**: Data minimization—sensitive data is removed before processing
- **CCPA**: Right to deletion—documents deleted immediately, no residual copies
- **Attorney-Client Privilege**: Queries remain confidential; no data shared with vendors
- **Work Product Doctrine**: All results stay within your firm's infrastructure

---

## Best Practices

### 1. Use Consistent Tagging

Tag documents for easier filtering:
```python
# Upload with meaningful tags
client.upload_document(
    file="settlement_agreement.pdf",
    tags=["contract", "settlement", "smith_v_acme", "2025"]
)
```

Then query by tag:
```python
result = client.query(
    "What is the payment schedule?",
    tags=["settlement"]  # Only searches settlement docs
)
```

### 2. Be Specific in Queries

✓ Good: "Does this contract require 30-day termination notice?"
✗ Vague: "Tell me about termination"

Specific queries yield more accurate results.

### 3. Review Context Rail Always

Never rely only on the answer. Always check the Context Rail to:
- Verify the source is relevant
- See the exact wording
- Understand the confidence score
- Include proper citations

### 4. Use Confidence Thresholds

For critical work, set high confidence:
```python
result = client.query(
    "What indemnification is required?",
    confidence_threshold=0.90  # Only very confident matches
)
```

### 5. Cross-Reference with Manual Review

Sens Prism augments but doesn't replace legal review:
- Use it to quickly narrow down relevant documents
- Always manually review the source excerpts
- Verify legal implications with senior attorneys
- Document your use of AI in legal work product

---

## Integration with Your Workflow

### Microsoft Word / Google Docs

Copy results directly from Context Rail into your briefs:
- Page citations are included
- Confidence scores add credibility
- Excerpts can be pasted directly

### Legal Research Databases

Use Sens Prism alongside traditional legal research:
- Find key clauses in your own documents first
- Cross-reference with precedent and statutes
- Build a more complete legal argument

### Case Management Systems

Some law firm case management platforms (LexisNexis, Westlaw, etc.) support API integrations. Contact [integrations@sens.ai](mailto:integrations@sens.ai) to discuss embedding Sens Prism into your existing workflow.

---

## Getting Started

1. **Sign up** at [sens.ai](https://sens.ai)
2. **Get your API key** from dashboard
3. **Upload a test contract** using the [Getting Started guide](../getting-started.md)
4. **Run some queries** to familiarize yourself with the Context Rail
5. **Integrate into your workflow** (manual queries first, then automation)

For questions specific to legal use cases, email [legal@sens.ai](mailto:legal@sens.ai).
