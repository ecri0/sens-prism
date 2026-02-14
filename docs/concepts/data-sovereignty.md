# Data Sovereignty

Data sovereignty isn't just a buzzword—it's a technical commitment. Sens Prism ensures your data stays yours through architecture, encryption, and design principles that make it impossible for us to access or expose your information.

## Why Data Sovereignty Matters

### Compliance

Regulations like GDPR, HIPAA, and SOC 2 require data minimization—sharing information with third parties only when necessary. Traditional LLM-based workflows force you to upload documents to vendors' infrastructure, creating compliance risk.

Sens Prism lets you:
- Keep documents in your infrastructure
- Process queries without transmitting raw data
- Maintain audit trails for regulatory reviews
- Delete documents immediately with no residual access

### Intellectual Property Protection

Your documents contain:
- Trade secrets and proprietary methods
- Customer information and business relationships
- Strategic plans and competitive advantages
- Sensitive negotiations and contracts

Uploading these to external LLM providers creates IP risk. Sens Prism extracts meaning locally and sanitizes before any external processing.

### Vendor Independence

Once your data is processed by a vendor's proprietary system, you're locked in:
- Switching LLM providers requires re-uploading and re-processing
- Your documents are stored in their format and infrastructure
- Pricing changes and policy shifts affect your access

Sens Prism's USID system (see [Semantic Layers](semantic-layers.md)) makes knowledge portable across any LLM.

---

## Enclave Architecture

Sens Prism uses an enclave model where your data is isolated and protected:

```
┌──────────────────────────────────────┐
│         Your Infrastructure          │
├──────────────────────────────────────┤
│  Data Enclave (Encrypted)            │
│  ├─ Documents (at rest)              │
│  ├─ Processing context (in transit)  │
│  └─ Audit logs                       │
└──────────────────────────────────────┘
         │
         │ (Encrypted tunnel, anonymized)
         ↓
┌──────────────────────────────────────┐
│      Sens Control Plane               │
│  (no access to raw data)              │
└──────────────────────────────────────┘
```

### Control Plane vs. Data Plane

**Data Plane** (your infrastructure):
- Raw documents
- Processed semantic layers
- User context and preferences
- Query logs
- Encryption keys

**Control Plane** (Sens managed):
- API routing and rate limiting
- User authentication
- Billing and usage tracking
- Model availability information
- Anonymized performance metrics

The Control Plane never sees your data. It only sees:
- Document IDs (hashed)
- Query IDs (hashed)
- Aggregated usage statistics
- No content, no PII, no context

---

## Smart Sanitizer

Before a sanitized version of your data reaches an LLM, the Smart Sanitizer removes sensitive information:

### What Gets Removed

- **PII**: Names, email addresses, phone numbers, social security numbers, passport numbers
- **Financial Data**: Bank account numbers, credit card numbers, salary information, account balances
- **Medical**: Patient IDs, diagnoses, medication names, test results
- **Legal**: Client names, case numbers, settlement amounts
- **Trade Secrets**: Proprietary formulas, source code, algorithms, supplier names

### How It Works

1. **Detection**: NLP-based recognition of sensitive patterns
2. **Classification**: Categorize the sensitivity level (public, internal, confidential, restricted)
3. **Redaction**: Replace with synthetic tokens (`[PII_NAME_0]`, `[AMOUNT_DOLLARS_15000]`)
4. **Retention**: Keep a mapping table encrypted in your data plane
5. **Reconstruction**: Original values restored only in your infrastructure

### Example

**Original document excerpt**:
```
Invoice from Acme Corp (vendor ID: 12345) to Johnson & Associates
Amount: $150,000
Finance contact: sarah.johnson@acme.com, +1-555-0123
Payment to account: 4532 1234 5678 9012
```

**After Smart Sanitizer**:
```
Invoice from [ORGANIZATION_NAME_0] (vendor ID: [VENDOR_ID_1]) to [ORGANIZATION_NAME_1]
Amount: [AMOUNT_DOLLARS_150000]
Finance contact: [PII_EMAIL_0], [PII_PHONE_0]
Payment to account: [FINANCIAL_ACCOUNT_0]
```

**Mapping table** (encrypted, stays in your enclave):
```
[ORGANIZATION_NAME_0] → Acme Corp
[VENDOR_ID_1] → 12345
[ORGANIZATION_NAME_1] → Johnson & Associates
[AMOUNT_DOLLARS_150000] → $150,000
[PII_EMAIL_0] → sarah.johnson@acme.com
[PII_PHONE_0] → +1-555-0123
[FINANCIAL_ACCOUNT_0] → 4532 1234 5678 9012
```

The sanitized version goes to the LLM. The mapping stays in your infrastructure, encrypted.

---

## Zero-Knowledge Design

Sens Prism is built on zero-knowledge principles:

### What Sens Cannot Do

- **Access your raw documents**: Even during processing, your documents are encrypted
- **See your queries**: Query content is hashed and encrypted
- **Access encryption keys**: You hold encryption keys; Sens cannot decrypt your data
- **Build ML models on your data**: No model training on customer documents
- **Share your data with third parties**: We have no copy of your data to share

### What Sens Can Do

- Route your requests to the right infrastructure
- Ensure documents are available when you query
- Track usage for billing
- Monitor system health (without accessing content)
- Apply patches and security updates

### Verification

In enterprise deployments, customers can:
- Run Sens on their own infrastructure
- Audit our code and architecture
- Verify no data leaves their control
- Maintain full chain of custody

---

## Encryption at Every Stage

### At Rest

Documents are encrypted with AES-256-GCM:
- Encryption key is customer-owned
- Key is never transmitted to Sens infrastructure
- Encrypted data is stored in your enclave

### In Transit

All data transmission uses TLS 1.3:
- End-to-end encryption
- Certificates pinned for additional security
- No plaintext logging

### In Processing

When documents are processed to extract semantic layers:
- Processing happens in your data plane
- Sensitive data is removed before any external call
- Results are encrypted before transmission

---

## Compliance & Audit

### Audit Logging

Every operation is logged:
- Who accessed what document
- When queries were made
- What results were returned
- When data was deleted

Logs are encrypted and tamper-proof.

### Deletion Guarantees

When you delete a document:
- It's immediately removed from your data plane
- All encrypted copies are deleted
- Processing artifacts are purged
- Logs are anonymized (document ID replaced with hash)

We cannot recover deleted data—it's gone.

### Regulatory Alignment

Sens Prism supports:
- **GDPR**: Data minimization, right to deletion, audit trails
- **HIPAA**: Encryption, access controls, audit logging
- **SOC 2**: Security, availability, integrity, confidentiality
- **FedRAMP**: For US government deployments (enterprise)

---

## Common Questions

**Can Sens employees access my data?**

No. Even Sens employees cannot access your encrypted data. We have no decryption keys.

**What if there's a security breach?**

Encrypted data is useless without keys. We maintain key separation so even a complete server breach cannot expose plaintext documents.

**Can you comply with law enforcement requests?**

We comply with legal requests, but we cannot produce data we don't have. We can only provide:
- Encrypted blobs (useless without your keys)
- Audit logs (showing access patterns, not content)
- Metadata (document counts, query timestamps)

**How does this compare to on-premise deployment?**

Running Sens on your infrastructure (enterprise option) gives you complete control:
- No data ever leaves your network
- You maintain all encryption keys
- You control all access and audit logs
- Full air-gapped operation is possible

---

## Next Steps

- [Semantic Layers](semantic-layers.md) — How we extract meaning safely
- [Getting Started](../getting-started.md) — Try sovereign processing yourself
- [API Reference](../api/reference.md) — See privacy features in action
- Contact [enterprise@sens.ai](mailto:enterprise@sens.ai) for on-premise options

Your data is your responsibility. We're just here to help you use it safely.
