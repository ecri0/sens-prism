# Changelog

All notable changes to Sens Prism are documented in this file.

## [0.4.0] - 2025-02-14

### Released
- Initial public release of Sens Prism
- Python SDK with full API coverage
- TypeScript SDK with type safety
- Complete documentation and examples
- Support for all core features: Distill, Protect, Inject

### Features
- **Document Management**
  - Upload documents (PDF, DOCX, TXT, RTF)
  - Get document status and metadata
  - Delete documents with permanent removal
  - Support for tags and organization

- **Querying**
  - Query documents with natural language questions
  - Filter by document ID and tags
  - Configurable confidence thresholds
  - Detailed source attribution

- **Context Rail**
  - View source excerpts with page numbers
  - Semantic layer information (Chunk, Concept, Context, Pragmatic, Universal)
  - Confidence scores per source
  - Matched concepts and pragmatic insights

- **Data Sovereignty**
  - Smart Sanitizer for PII removal
  - Encrypted data enclave architecture
  - Zero-knowledge design principles
  - Full audit logging

- **Authentication**
  - API key-based authentication
  - Bearer token support
  - Key management via dashboard and API
  - Token expiration and rotation

- **Rate Limiting**
  - Plan-based rate limits (Free, Pro, Enterprise)
  - Rate limit headers in responses
  - Retry-After guidance for backoff

### SDKs
- **Python SDK** (0.4.0)
  - Sync and async support
  - Type hints and docstrings
  - Context manager support
  - Full error handling

- **TypeScript SDK** (0.4.0)
  - Full type safety
  - Node.js support
  - FormData for file uploads
  - Comprehensive error classes

### Documentation
- Getting Started guide (5-minute quickstart)
- API Reference with curl and SDK examples
- Authentication guide with best practices
- Error codes and troubleshooting
- Use case guides:
  - Legal research with confidential document handling
  - Academic literature review across 100+ papers
  - Financial analysis with proprietary metrics
- Concept documentation:
  - Sovereign AI Gateway principles
  - 5-Layer Semantic Model
  - Data Sovereignty architecture
- Examples:
  - Python quickstart
  - TypeScript quickstart

### Examples
- Python: Basic upload, query, and context rail usage
- TypeScript: Equivalent examples with async/await
- Both examples include error handling and cleanup

### License
- Business Source License 1.1
- Converts to Apache License 2.0 on February 14, 2029

### Known Limitations
- Processing time depends on document size (larger documents take longer)
- Storage limits vary by plan tier
- Enterprise features require separate contact

---

## Future Releases

### Planned for v0.5.0
- Streaming query results for large responses
- Batch document upload
- Advanced filtering (date ranges, content types)
- Custom semantic layer configuration
- Webhook support for document processing completion

### Planned for v1.0.0
- GraphQL API option
- Desktop application
- Advanced analytics dashboard
- Multi-team account support
- Custom fine-tuned models
- On-premise deployment

---

## Version History

### 0.4.0
Initial public release - See above

---

## Support

For questions about releases, features, or migrations, see [issues](https://github.com/ecri0/prism/issues) or email [support@sens.ai](mailto:support@sens.ai).
