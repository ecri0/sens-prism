---
name: Bug Report
about: Report a bug in Sens Prism
title: "[BUG] "
labels: bug
assignees: ''

---

## Description

Please describe the bug clearly and concisely.

## Steps to Reproduce

1. ...
2. ...
3. ...

## Expected Behavior

What did you expect to happen?

## Actual Behavior

What actually happened?

## Environment

- **SDK Version**: (e.g., 0.4.0)
- **Language**: (Python / TypeScript)
- **Python Version**: (if applicable, e.g., 3.9, 3.10, 3.11)
- **Node Version**: (if applicable, e.g., 16, 18, 20)
- **Operating System**: (e.g., Windows, macOS, Linux)

## Error Messages

Please include any error messages or stack traces:

```
[Paste error output here]
```

## Minimal Reproducible Example

Please provide a minimal code example that reproduces the issue:

```python
# Python example
from sens import SensClient

client = SensClient(api_key="sens_sk_...")
# ... minimal reproduction code ...
```

Or:

```typescript
// TypeScript example
import { SensClient } from "@sens/prism";

const client = new SensClient({ apiKey: "sens_sk_..." });
// ... minimal reproduction code ...
```

## Additional Context

Any other context or information that might help debug this issue?

## Workarounds

Have you found any workarounds? Please describe them here.

---

**Note**: Please don't include any API keys, credentials, or sensitive information in this report.
