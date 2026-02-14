# Security Policy

Sens Prism takes security seriously. This document outlines our security practices and how to report vulnerabilities.

## Reporting Security Vulnerabilities

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, please report security issues by emailing [security@sens.ai](mailto:security@sens.ai) with:

1. **Description**: What is the vulnerability?
2. **Location**: Which component or file is affected?
3. **Reproduction**: Steps to reproduce the issue (if possible)
4. **Impact**: What could an attacker do with this vulnerability?
5. **Mitigation**: Have you tried any temporary fixes?

We will:
- Acknowledge receipt within 24 hours
- Provide a timeline for a fix
- Request confidentiality until the issue is resolved
- Credit you in the security advisory (if desired)

## Security Best Practices

### API Key Management

- **Never commit API keys** to version control
- **Rotate keys regularly** (every 90 days recommended)
- **Use environment variables** for sensitive credentials
- **Revoke immediately** if a key is exposed
- **Create separate keys** for dev/staging/production

```python
# ✓ Good: Use environment variables
import os
api_key = os.getenv("SENS_API_KEY")
client = SensClient(api_key=api_key)

# ✗ Bad: Hardcoded keys
client = SensClient(api_key="sens_sk_abc123")
```

### Data Protection

- **Enable TLS 1.3** for all connections
- **Verify certificate pinning** in production
- **Never log raw API keys** or request bodies
- **Encrypt sensitive data** at rest and in transit
- **Use HTTPS only** (never HTTP)

### Access Control

- **Use API key scopes** to limit permissions
- **Implement least privilege** access
- **Audit who accesses** which documents
- **Remove access immediately** when no longer needed

### Dependency Security

We keep dependencies up to date and monitor for vulnerabilities:

```bash
# Python SDK
pip install --upgrade sens-prism

# TypeScript SDK
npm update @sens/prism
```

Always keep the SDK updated for security patches.

## Platform Security

### Data Encryption

- **At Rest**: AES-256-GCM encryption
- **In Transit**: TLS 1.3 with certificate pinning
- **In Memory**: Sensitive data cleared after processing
- **Key Management**: Customer-owned encryption keys

### Zero-Knowledge Architecture

- Sens infrastructure cannot access your encrypted data
- Processing happens in your data plane
- Control plane handles routing, authentication, billing only
- No plaintext copies of documents stored by Sens

### Audit Logging

- All API calls are logged with timestamps
- User authentication is tracked
- Document access is audited
- Logs are encrypted and tamper-proof
- Deletion is logged (documents are unrecoverable)

### Compliance

Sens Prism meets standards for:
- **GDPR** (General Data Protection Regulation)
- **HIPAA** (Health Insurance Portability and Accountability Act)
- **SOC 2** Type II (System and Organization Controls)
- **CCPA** (California Consumer Privacy Act)
- **FedRAMP** (Federal Risk and Authorization Management Program)

## Vulnerability Management

### Severity Levels

- **Critical** (CVSS 9-10): Immediate patching required
- **High** (CVSS 7-8): Patch within 1 week
- **Medium** (CVSS 4-6): Patch within 2 weeks
- **Low** (CVSS 0-3): Patch within 1 month

### Patching

1. Security vulnerabilities are prioritized
2. Patches are tested thoroughly before release
3. Users are notified via email and GitHub security advisories
4. Critical patches are released as soon as possible

## Third-Party Security

### Dependencies

The Sens Prism SDK uses minimal dependencies:

**Python**:
- `httpx` — HTTP client library
- `pydantic` — Data validation

**TypeScript**:
- `form-data` — File upload support

All dependencies are:
- Actively maintained
- Regularly scanned for vulnerabilities
- Updated as security patches are released
- Chosen for minimal dependency footprint

### External Services

Sens Prism integrates with:
- OpenAI, Anthropic, or local LLMs (for query processing)
- AWS/GCP/Azure (for infrastructure)
- None of these services receive your unencrypted data

## User Responsibilities

While Sens Prism provides security, users must also:

- **Protect API keys** — Don't share or commit them
- **Use strong authentication** — Enable 2FA if available
- **Monitor usage** — Check account activity regularly
- **Review access logs** — Audit who's accessing documents
- **Keep SDKs updated** — Use latest versions with patches

## Security Advisories

We publish security advisories for all vulnerabilities:

- GitHub Security Advisories: https://github.com/ecri0/prism/security/advisories
- Email notifications: Subscribe at [sens.ai/security](https://sens.ai/security)

## Responsible Disclosure

If you find a vulnerability, please follow responsible disclosure:

1. **Report privately** to [security@sens.ai](mailto:security@sens.ai)
2. **Do not exploit** the vulnerability
3. **Do not disclose publicly** until we've patched
4. **Give us time** to develop and test a fix
5. **Coordinate timing** for public disclosure

We believe responsible disclosure protects all users.

## Security Contacts

- **Security Issues**: [security@sens.ai](mailto:security@sens.ai)
- **General Support**: [support@sens.ai](mailto:support@sens.ai)
- **Enterprise Security**: [enterprise@sens.ai](mailto:enterprise@sens.ai)

## Changelog

We maintain a [CHANGELOG.md](CHANGELOG.md) documenting all releases and security updates.

## Questions?

If you have security questions or concerns, please contact us at [security@sens.ai](mailto:security@sens.ai).

Thank you for helping keep Sens Prism secure!
