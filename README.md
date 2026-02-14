# Sens Prism

[![License: BSL 1.1](https://img.shields.io/badge/License-BSL%201.1-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.0-brightgreen.svg)](https://github.com/ecri0/sens-prism/releases/tag/v0.4.0)
[![Python SDK](https://img.shields.io/badge/python-3.9%2B-blue.svg)](sdk/python)
[![TypeScript SDK](https://img.shields.io/badge/typescript-5.0%2B-blue.svg)](sdk/typescript)

**Make Sens of your AI.**

Sens Prism is a Sovereign AI Gateway that sits between you and large language models, providing unprecedented transparency, control, and data ownership. Query your documents with confidence, knowing exactly why the AI says what it says—without surrendering your data to third parties.

🌐 **Website**: [sens-thread.io](https://sens-thread.io)

## Why Sens Prism?

- **Distill**: Extract meaning from your documents using mechanistic interpretability. Understand concepts, connections, and context at multiple semantic layers.
- **Protect**: Sensitive data never reaches the LLM. Our Smart Sanitizer removes PII, financial figures, and confidential information before processing.
- **Inject**: Relevant context is automatically added to your prompts, improving accuracy while the Confidence Meter explains AI reasoning in real time.

## Features

### Distill
Extract actionable meaning from any document through a 5-layer semantic model—from raw chunks to universal, model-independent representations.

### Protect
Your data stays your data. Encrypted enclave architecture, zero-knowledge design, and Smart Sanitizer technology ensure sensitive information never leaves your control.

### Inject
Automatically enhance prompts with relevant context from your knowledge base. View source citations, confidence scores, and reasoning traces via the Context Rail.

## Quick Start

### Installation

```bash
pip install sens-prism
```

### Usage

```python
from sens import SensClient

client = SensClient(api_key="sens_sk_your_key_here")
doc = client.upload_document("path/to/document.pdf")
results = client.query("What are the key findings?", doc_id=doc.id)
print(results.answer)
print(results.context_rail.sources)  # View where the AI found this
```

## Documentation

- **[Getting Started](docs/getting-started.md)** — 5-minute quickstart
- **[Concepts](docs/concepts/overview.md)** — Understand Sovereign AI Gateways
- **[Semantic Layers](docs/concepts/semantic-layers.md)** — Our 5-layer model explained
- **[Data Sovereignty](docs/concepts/data-sovereignty.md)** — Why your data stays yours
- **[API Reference](docs/api/reference.md)** — Complete endpoint documentation
- **[Authentication](docs/api/authentication.md)** — API key management
- **[Use Cases](docs/guides/)** — Legal research, academic reviews, financial analysis

## Examples

Python quickstart:
```bash
cd examples/python
python quickstart.py
```

TypeScript quickstart:
```bash
cd examples/typescript
npm install && npx ts-node quickstart.ts
```

## Pricing

**Sens Prism** starts at **$29/month** for professional use. Includes 100 requests/minute, 100 documents/day, and 10GB storage.

Compare plans at [sens-thread.io](https://sens-thread.io).

## SDK Support

- **[Python SDK](sdk/python)** — Production-ready with async support
- **[TypeScript SDK](sdk/typescript)** — Full type safety

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Licensed under the Business Source License 1.1. See [LICENSE](LICENSE) for details.
Converts to Apache License 2.0 on February 14, 2029.

## Support

- Website: [sens-thread.io](https://sens-thread.io)
- Issues: [GitHub Issues](https://github.com/ecri0/sens-prism/issues)
- Email: support@sens-thread.io

---

Built with ❤️ by the Sens team. Making AI transparent, safe, and yours.
