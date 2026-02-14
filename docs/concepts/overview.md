# Sovereign AI Gateways

## The Problem

Modern AI systems force you into a dilemma:

1. **The Black Box Trap**: You send your documents to an LLM and get an answer, but you don't know why or where it came from.
2. **Vendor Lock-in**: Your data is processed by proprietary systems you can't control or inspect.
3. **Data Leakage**: Sensitive information—trade secrets, personal data, financial details—is transmitted to third parties and potentially used for model training.

These issues have real consequences: regulatory risk, IP exposure, and loss of control over your knowledge.

## The Solution: Sovereign AI Gateway

Sens Prism is a gateway that sits between you and LLMs. It transforms how you interact with AI:

```
Your Documents
      ↓
   DISTILL (Extract meaning via semantic layers)
      ↓
   PROTECT (Remove sensitive data, keep it encrypted)
      ↓
   INJECT (Add relevant context to prompts)
      ↓
   LLM (Only processes clean, contextualized queries)
      ↓
   Results (With confidence scores and source citations)
```

### Distill

Sens Prism doesn't just store documents—it extracts meaning through a 5-layer semantic model:

- **Chunks**: Raw text segments with linguistic features
- **Concepts**: Knowledge graph connections between ideas
- **Context**: User-specific meaning and relationships
- **Pragmatic**: Actionable insights and decision-relevant information
- **Universal**: Model-independent semantic identifiers (USID) that remain consistent across LLMs

### Protect

Sensitive data is removed before your query ever reaches an LLM:

- **Smart Sanitizer** identifies and redacts PII, financial figures, confidential identifiers
- **Encrypted Enclave Architecture** ensures your data is encrypted at rest and in transit
- **Zero-Knowledge Design** means Sens processes your data without ever accessing its content
- Your data never leaves your control or your infrastructure (in Enterprise deployments)

### Inject

Prompts are automatically enhanced with relevant context:

- **Context Rail** shows exactly which document sections informed the answer
- **Confidence Meter** displays why the AI chose that response
- **Citation Tracking** provides page numbers, excerpts, and confidence scores
- **Semantic Awareness** ensures injected context is semantically relevant, not just keyword-matched

## How It Differs from Traditional RAG

Traditional Retrieval-Augmented Generation (RAG):
- Chunks documents naively (keyword splits, page breaks)
- Injects raw text into prompts (poor semantic understanding)
- No protection of sensitive data
- Limited interpretability of why results were selected

Sens Prism:
- Extracts meaning through 5 semantic layers
- Automatically sanitizes sensitive data
- Injects contextually relevant information with confidence scores
- Provides full transparency via Context Rail and reasoning traces

## Model Independence

One key feature: **USID** (Universal Semantic Identifier).

Instead of embedding documents into vectors tied to a specific LLM's embedding model, Sens Prism uses model-independent semantic identifiers. This means:

- Switch LLMs without re-processing your documents
- Use the same knowledge base with GPT-4, Claude, or open-source models
- No vendor lock-in or reindexing costs

## Core Principles

1. **Transparency**: You see exactly where AI gets its answers
2. **Control**: You decide what's sensitive and what can be processed
3. **Sovereignty**: Your data stays yours—encrypted, encapsulated, and under your control
4. **Portability**: Use any LLM without re-uploading or re-indexing
5. **Auditability**: Full logs and traces for compliance and security

## Common Use Cases

- **Legal**: Query contracts without exposing confidential clauses to LLMs
- **Finance**: Analyze earnings reports while protecting proprietary metrics
- **Healthcare**: Process medical documents with HIPAA-compliant data protection
- **Research**: Cross-reference academic papers with traceable citations
- **Enterprise**: Maintain IP security while leveraging AI analysis

Ready to get started? See [Getting Started](../getting-started.md) for a 5-minute quickstart.
