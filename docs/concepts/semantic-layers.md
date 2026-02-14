# The 5-Layer Semantic Model

Sens Prism doesn't just index documents—it extracts meaning at multiple levels. Understanding these layers helps you appreciate why Sens Prism provides superior context and reasoning traces.

## Overview

```
Universal (L5)
    ↑
    ↓
Pragmatic (L4)
    ↑
    ↓
Context (L3)
    ↑
    ↓
Concept (L2)
    ↑
    ↓
Chunk (L1)

Your Document
```

Each layer builds on the previous, extracting increasingly sophisticated meaning.

## Layer 1: Chunk

**What it is**: Raw text segments with linguistic and structural features extracted.

**Example**: A paragraph from a contract about payment terms.

```
"Payment shall be made within 30 days of invoice issuance.
Late payments incur a 1.5% monthly interest charge."
```

**Features extracted**:
- Linguistic: sentence boundaries, part-of-speech tags, entities (numbers, dates)
- Structural: paragraph metadata, section hierarchy, formatting
- Statistical: word frequency, semantic density, key term presence

**Purpose**: Preserves the original text and its surface-level properties for accurate retrieval.

---

## Layer 2: Concept

**What it is**: Knowledge graph connections between chunks. Concepts are abstract ideas and relationships.

**Example**: From the chunk above, we extract concepts:
- **PAYMENT_TERM** (relation to chunk): 30 days
- **PENALTY** (relation to chunk): 1.5% monthly interest
- **OBLIGATION** (type): Payment must occur

These concepts connect to other chunks discussing:
- Payment methods (Layer 1 chunks elsewhere)
- Interest rate definitions (other contracts)
- Late payment handling (policy documents)

**Features**:
- Knowledge graph edges (is-a, has-a, causes)
- Entity types (AMOUNT, DURATION, PENALTY)
- Relationship confidence scores

**Purpose**: Enables semantic search beyond keyword matching. A query about "interest charges" now connects to all payment-related chunks, even if they use different terminology.

---

## Layer 3: Context

**What it is**: User-specific contextual meaning. The same concept means different things depending on context.

**Example**: The "30 days" payment term means something different depending on context:
- In a vendor agreement → standard net-30 terms
- In a high-risk customer agreement → potentially unusual (might indicate cash flow concerns)
- In a law firm service agreement → typical professional services term

Context factors:
- Document type and domain
- Organizational role of the user
- Historical patterns in your documents
- Regulatory environment

**Features**:
- Context vector: captures semantic relevance to your specific situation
- Contextual relationships: links between concepts that matter to you
- User signals: your past queries, frequent terms, relevant domains

**Purpose**: Personalize results without sharing your documents with the LLM. Context is computed locally and used to rank what's most relevant to you.

---

## Layer 4: Pragmatic

**What it is**: Actionable insights. What should you do with this information?

**Example**: The "30 days + 1.5% interest" concept transforms into:
- **Action**: "Review late-paying customers for cash flow risk"
- **Risk**: "Interest penalties add up (1.5% × 12 = 18% annually)"
- **Opportunity**: "We could tighten payment terms with strong customers"
- **Compliance**: "Interest rate must comply with usury laws in relevant jurisdictions"

**Features**:
- Action items
- Risk assessments
- Decision recommendations
- Compliance flags

**Purpose**: The AI doesn't just answer "what is this?" but "what does this mean for me?" Pragmatic layers enable proactive insights and decision support.

---

## Layer 5: Universal

**What it is**: Model-independent semantic identifiers (USID). Universal representations that remain constant regardless of which LLM interprets them.

**Format**: `sens://v1/universal/f{id}`

Example: `sens://v1/universal/f7d4a9b2c1e8f5`

**How it works**:
- Each concept, stripped of model-specific embeddings, gets a stable universal ID
- The same concept maintains the same ID whether you query with GPT-4, Claude, or a local model
- Allows you to switch LLMs without re-indexing or re-processing documents

**Features**:
- Deterministic: same input → same USID always
- Model-agnostic: works with any LLM
- Version-stable: survives updates to embedding models
- Traceable: enables auditing and citing across systems

**Purpose**: True vendor independence. Your knowledge base remains portable and future-proof.

---

## How Layers Work Together

When you query "What are the payment terms?":

1. **Chunk** matches relevant text segments
2. **Concept** connects related payment definitions and rules
3. **Context** ranks them by relevance to your organization and situation
4. **Pragmatic** highlights actionable implications
5. **Universal** ensures the same meaning regardless of which LLM interprets it

The **Context Rail** shows you this entire chain:

```
Query: "What are the payment terms?"

Answer: "30 days net with 1.5% monthly interest on late payments."

Context Rail:
├─ Chunk (L1): [Page 3] "Payment shall be made within 30 days..."
├─ Concept (L2): PAYMENT_TERM, PENALTY connected in knowledge graph
├─ Context (L3): Marked as "typical for vendor agreements" based on your docs
├─ Pragmatic (L4): Risk flagged: "18% annualized interest rate"
└─ Universal (L5): USID=sens://v1/universal/f7d4a9b2c1e8f5
```

---

## Technical Benefits

- **Better Search**: Semantic layer matching beats keyword search
- **Confidence Scores**: Each layer contributes a confidence assessment
- **Compliance Ready**: Audit trail shows how the answer was derived
- **Privacy Preserved**: Context and pragmatic layers computed locally, data never exposed to LLM
- **Model Agnostic**: Universal layer makes you independent of vendor embeddings

---

## Next Steps

- [Data Sovereignty](data-sovereignty.md) — How layers enable secure processing
- [API Reference](../api/reference.md) — Query parameters for layer-specific results
- [Getting Started](../getting-started.md) — Try it yourself

