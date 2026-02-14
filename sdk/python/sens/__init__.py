"""Sens Prism Python SDK.

The Sens Prism SDK provides a Python interface to the Sovereign AI Gateway API.
Authenticate with your API key and query your documents with transparency and control.

Example:
    from sens import SensClient

    client = SensClient(api_key="sens_sk_...")
    doc = client.upload_document("path/to/document.pdf")
    result = client.query("What are the key findings?", document_ids=[doc.id])
    print(result.answer)
    print(result.context_rail.sources)
"""

from sens.client import SensClient
from sens.exceptions import (
    SensError,
    SensAuthError,
    SensRateLimitError,
    SensNotFoundError,
    SensValidationError,
)

__version__ = "0.4.0"
__author__ = "Sens Team"
__license__ = "BSL 1.1"

__all__ = [
    "SensClient",
    "SensError",
    "SensAuthError",
    "SensRateLimitError",
    "SensNotFoundError",
    "SensValidationError",
]
