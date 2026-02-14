# Authentication

Sens Prism uses API key-based authentication with Bearer tokens. All requests to the API must include a valid authentication header.

## Getting Your API Key

### From Dashboard

1. Sign up at [sens.ai](https://sens.ai)
2. Navigate to [dashboard.sens.ai](https://dashboard.sens.ai)
3. Go to **Settings** → **API Keys**
4. Click **Create New Key**
5. Choose a name (e.g., "Production", "Development")
6. Click **Generate**
7. **Copy and save your key immediately**—you won't be able to see it again

### Via API (Programmatic)

If you have an existing session, you can create a key programmatically:

```bash
curl -X POST https://api.sens.ai/v1/auth/keys \
  -H "Authorization: Bearer sens_session_existing_key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production",
    "expires_in_days": 90
  }'
```

Response:
```json
{
  "id": "key_abc123def456",
  "key": "sens_sk_abc123def456789...",
  "name": "Production",
  "created_at": "2025-02-14T10:30:00Z",
  "expires_at": "2025-05-15T10:30:00Z"
}
```

## Using API Keys

### Bearer Token Format

Include the API key in the `Authorization` header:

```bash
curl -X GET https://api.sens.ai/v1/documents \
  -H "Authorization: Bearer sens_sk_your_key_here"
```

### In SDK Code

**Python**:
```python
from sens import SensClient

client = SensClient(api_key="sens_sk_your_key_here")
```

**TypeScript**:
```typescript
import { SensClient } from "@sens/prism";

const client = new SensClient({
  apiKey: "sens_sk_your_key_here"
});
```

### Environment Variables

Recommended: store your API key in an environment variable:

```bash
export SENS_API_KEY="sens_sk_your_key_here"
```

Then reference it in code:

**Python**:
```python
import os
from sens import SensClient

api_key = os.getenv("SENS_API_KEY")
client = SensClient(api_key=api_key)
```

**TypeScript**:
```typescript
const apiKey = process.env.SENS_API_KEY;
const client = new SensClient({ apiKey });
```

**Never commit API keys to version control.** Use environment variables or secret management systems.

## Token Management

### Viewing Active Keys

List all API keys for your account:

```bash
curl -X GET https://api.sens.ai/v1/auth/keys \
  -H "Authorization: Bearer sens_sk_your_key_here"
```

Response:
```json
{
  "keys": [
    {
      "id": "key_abc123",
      "name": "Production",
      "created_at": "2025-02-14T10:30:00Z",
      "expires_at": "2025-05-15T10:30:00Z",
      "last_used_at": "2025-02-14T11:00:00Z"
    },
    {
      "id": "key_def456",
      "name": "Development",
      "created_at": "2025-02-10T14:22:00Z",
      "expires_at": "2025-05-11T14:22:00Z",
      "last_used_at": null
    }
  ]
}
```

### Revoking Keys

Immediately revoke (deactivate) an API key:

```bash
curl -X DELETE https://api.sens.ai/v1/auth/keys/key_abc123 \
  -H "Authorization: Bearer sens_sk_your_key_here"
```

Response (204 No Content):
```
(empty)
```

Revoked keys stop working immediately. This is useful if a key is compromised.

### Setting Expiration

When creating a key, specify how long it should remain valid:

```bash
curl -X POST https://api.sens.ai/v1/auth/keys \
  -H "Authorization: Bearer sens_sk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Temporary",
    "expires_in_days": 7
  }'
```

Keys with expiration dates must be refreshed before they expire. We recommend setting 90-day expirations for production keys.

## API Key Scopes

All Sens Prism API keys have full access to:
- Document upload and deletion
- Query execution
- Context Rail retrieval
- Usage reporting

For fine-grained access control (e.g., read-only keys), contact [enterprise@sens.ai](mailto:enterprise@sens.ai).

## Security Best Practices

### DO

✅ **Store keys in environment variables** — Never hardcode them
✅ **Use separate keys for dev/staging/production** — Limits blast radius if compromised
✅ **Rotate keys regularly** — Set 90-day expiration and refresh
✅ **Revoke immediately if exposed** — Don't wait for expiration
✅ **Use short-lived keys for CI/CD** — Set 7-30 day expiration for automated processes
✅ **Monitor key usage** — Check `last_used_at` in the keys list
✅ **Use strong naming** — "Production" vs "prod_main_2025_feb" helps you remember what's what

### DON'T

❌ **Commit keys to repositories** — Use `.gitignore` and environment variables
❌ **Share keys via email or chat** — Use secure key sharing or dashboard delegation
❌ **Log raw API keys** — If logs contain a key, rotate it immediately
❌ **Use the same key for multiple systems** — Limits your ability to isolate compromises
❌ **Create keys without expiration** — Set a reminder to rotate them
❌ **Use browser/client-side keys** — API keys should only be used server-to-server

## Error Handling

### Invalid Key

```bash
curl -X GET https://api.sens.ai/v1/documents \
  -H "Authorization: Bearer sens_sk_invalid"
```

Response (401 Unauthorized):
```json
{
  "error": "invalid_authentication",
  "code": "SENS_001",
  "message": "Invalid or expired API key"
}
```

### Expired Key

```json
{
  "error": "authentication_expired",
  "code": "SENS_002",
  "message": "API key has expired. Please generate a new key.",
  "expires_at": "2025-02-14T10:30:00Z"
}
```

Refresh your key:
1. Go to dashboard
2. Delete the expired key
3. Create a new key
4. Update your application configuration

### Missing Header

```bash
curl -X GET https://api.sens.ai/v1/documents
# (no Authorization header)
```

Response (401 Unauthorized):
```json
{
  "error": "missing_authentication",
  "code": "SENS_001",
  "message": "Authorization header is required"
}
```

## Third-Party Integrations

### Zapier / Make Integration

If using Sens Prism through a third-party integration platform:

1. Generate a dedicated API key in the dashboard
2. Provide only the key (not your account email/password)
3. Use the integration's built-in secret storage
4. Test the connection before going live
5. Revoke the key if you disconnect the integration

### Custom Scripts

For scripts that authenticate as a user:

```bash
# Use application/x-www-form-urlencoded for form-based auth
# (contact support for user authentication flow details)
```

## Session Tokens vs. API Keys

**API Keys** (`sens_sk_...`):
- Long-lived (90 days typical)
- For server-to-server authentication
- High privilege level

**Session Tokens** (used internally):
- Short-lived (1 hour typical)
- For browser-based access
- Generated via OAuth or email/password login

Use **API keys** for SDKs and integrations. Session tokens are handled internally by the dashboard.

## Next Steps

- [API Reference](reference.md) — See all available endpoints
- [Getting Started](../getting-started.md) — Make your first API call
- [Error Codes](errors.md) — Handle authentication errors gracefully
