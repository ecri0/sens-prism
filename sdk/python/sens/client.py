"""Sens Prism Python SDK client."""

import asyncio
import os
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

import httpx

from sens.exceptions import (
    SensError,
    SensAuthError,
    SensRateLimitError,
    SensNotFoundError,
    SensValidationError,
    SensConflictError,
    SensPayloadTooLargeError,
    SensServiceUnavailableError,
)


@dataclass
class Document:
    """Represents a document in Sens Prism."""

    id: str
    status: str
    title: Optional[str] = None
    size_bytes: Optional[int] = None
    tags: Optional[List[str]] = None
    created_at: Optional[str] = None
    estimated_ready_at: Optional[str] = None
    ready_at: Optional[str] = None
    page_count: Optional[int] = None
    chunk_count: Optional[int] = None
    concept_count: Optional[int] = None


@dataclass
class Source:
    """Represents a source reference in query results."""

    document_id: str
    document_title: Optional[str] = None
    page: Optional[int] = None
    excerpt: Optional[str] = None
    confidence_score: Optional[float] = None
    semantic_layer: Optional[str] = None
    matched_concepts: Optional[List[str]] = None
    pragmatic_insights: Optional[List[str]] = None


@dataclass
class QueryResult:
    """Represents the result of a query."""

    query_id: str
    query: str
    answer: str
    confidence_score: float
    processing_time_ms: int
    sources: List[Source]


@dataclass
class ContextRail:
    """Represents detailed context information for a query."""

    query_id: str
    query: str
    retrieved_at: str
    sources: List[Source]
    summary: Dict[str, Any]


class SensClient:
    """Client for interacting with Sens Prism API.

    Attributes:
        api_key: Your Sens Prism API key (format: sens_sk_...)
        base_url: Base URL for the API (default: https://api.sens.ai/v1)
        timeout: Request timeout in seconds (default: 30)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.sens.ai/v1",
        timeout: int = 30,
    ):
        """Initialize the Sens Prism client.

        Args:
            api_key: Your API key. If not provided, reads from SENS_API_KEY env var.
            base_url: Base URL for the API.
            timeout: Request timeout in seconds.

        Raises:
            SensValidationError: If no API key is provided or found.
        """
        self.api_key = api_key or os.getenv("SENS_API_KEY")
        if not self.api_key:
            raise SensValidationError(
                "API key required. Provide 'api_key' parameter or set SENS_API_KEY environment variable.",
                code="SENS_003",
            )

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.Client(
            headers=self._get_headers(),
            timeout=timeout,
        )

    def _get_headers(self) -> Dict[str, str]:
        """Get default headers for requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "sens-prism-sdk/0.4.0",
        }

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and raise exceptions for errors.

        Args:
            response: The HTTP response object.

        Returns:
            Parsed JSON response.

        Raises:
            SensError: For various API error conditions.
        """
        try:
            data = response.json()
        except Exception:
            data = {}

        # Success responses
        if response.status_code in (200, 201, 202, 204):
            return data

        # Error responses
        error_message = data.get("message", f"HTTP {response.status_code}")
        error_code = data.get("code")
        error_details = data.get("details", {})

        if response.status_code == 400:
            raise SensValidationError(
                error_message, code=error_code, details=error_details
            )
        elif response.status_code == 401:
            raise SensAuthError(
                error_message, code=error_code, details=error_details
            )
        elif response.status_code == 403:
            raise SensAuthError(
                error_message, code=error_code, details=error_details
            )
        elif response.status_code == 404:
            raise SensNotFoundError(
                error_message, code=error_code, details=error_details
            )
        elif response.status_code == 409:
            raise SensConflictError(
                error_message, code=error_code, details=error_details
            )
        elif response.status_code == 413:
            raise SensPayloadTooLargeError(
                error_message, code=error_code, details=error_details
            )
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise SensRateLimitError(
                error_message,
                code=error_code,
                retry_after=int(retry_after) if retry_after else None,
                details=error_details,
            )
        elif response.status_code == 503:
            retry_after = response.headers.get("Retry-After")
            raise SensServiceUnavailableError(
                error_message,
                retry_after=int(retry_after) if retry_after else None,
                code=error_code,
                details=error_details,
            )
        else:
            raise SensError(error_message, code=error_code, details=error_details)

    def upload_document(
        self,
        file_path: str,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Document:
        """Upload a document to be processed and indexed.

        Args:
            file_path: Path to the document file (PDF, DOCX, TXT, RTF)
            title: Human-readable document name
            tags: List of tags for organization (e.g., ["legal", "contract"])

        Returns:
            Document object with ID and status.

        Raises:
            SensValidationError: If file doesn't exist or format invalid.
            SensPayloadTooLargeError: If file exceeds size limits.
        """
        if not os.path.exists(file_path):
            raise SensValidationError(f"File not found: {file_path}", code="SENS_003")

        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {}
            if title:
                data["title"] = title
            if tags:
                data["tags"] = ",".join(tags)

            response = self._client.post(
                f"{self.base_url}/documents",
                files=files,
                data=data if data else None,
            )

        result = self._handle_response(response)
        return Document(
            id=result["id"],
            status=result["status"],
            title=result.get("title"),
            size_bytes=result.get("size_bytes"),
            tags=result.get("tags"),
            created_at=result.get("created_at"),
            estimated_ready_at=result.get("estimated_ready_at"),
        )

    def get_document(self, document_id: str) -> Document:
        """Get document metadata and status.

        Args:
            document_id: The document ID (from upload_document response)

        Returns:
            Document object with current status.

        Raises:
            SensNotFoundError: If document doesn't exist.
        """
        response = self._client.get(f"{self.base_url}/documents/{document_id}")
        result = self._handle_response(response)

        return Document(
            id=result["id"],
            status=result["status"],
            title=result.get("title"),
            size_bytes=result.get("size_bytes"),
            tags=result.get("tags"),
            created_at=result.get("created_at"),
            ready_at=result.get("ready_at"),
            page_count=result.get("page_count"),
            chunk_count=result.get("chunk_count"),
            concept_count=result.get("concept_count"),
        )

    def delete_document(self, document_id: str) -> None:
        """Delete a document. This action is permanent.

        Args:
            document_id: The document ID to delete.

        Raises:
            SensNotFoundError: If document doesn't exist.
        """
        response = self._client.delete(f"{self.base_url}/documents/{document_id}")
        self._handle_response(response)

    def query(
        self,
        query: str,
        document_ids: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        limit: int = 3,
        confidence_threshold: float = 0.5,
    ) -> QueryResult:
        """Query your knowledge base.

        Args:
            query: Your question or search query.
            document_ids: Specific documents to query. If omitted, searches all.
            tags: Filter documents by tags.
            limit: Maximum number of source chunks to include.
            confidence_threshold: Minimum confidence score (0.0-1.0).

        Returns:
            QueryResult with answer and sources.

        Raises:
            SensValidationError: If query parameters are invalid.
            SensConflictError: If a document is still processing.
        """
        payload = {
            "query": query,
            "limit": limit,
            "confidence_threshold": confidence_threshold,
        }

        if document_ids:
            payload["document_ids"] = document_ids
        if tags:
            payload["tags"] = tags

        response = self._client.post(
            f"{self.base_url}/query",
            json=payload,
        )

        result = self._handle_response(response)

        sources = [
            Source(
                document_id=s["document_id"],
                document_title=s.get("document_title"),
                page=s.get("page"),
                confidence_score=s.get("confidence_score"),
            )
            for s in result.get("sources", [])
        ]

        return QueryResult(
            query_id=result["query_id"],
            query=result["query"],
            answer=result["answer"],
            confidence_score=result["confidence_score"],
            processing_time_ms=result["processing_time_ms"],
            sources=sources,
        )

    def get_context_rail(self, query_id: str) -> ContextRail:
        """Get detailed context information for a query.

        Includes excerpts, page numbers, semantic layers, and confidence scores.

        Args:
            query_id: The query ID (from query response).

        Returns:
            ContextRail object with detailed source information.

        Raises:
            SensNotFoundError: If query doesn't exist or has expired.
        """
        response = self._client.get(f"{self.base_url}/context-rail/{query_id}")
        result = self._handle_response(response)

        sources = [
            Source(
                document_id=s["document_id"],
                document_title=s.get("document_title"),
                page=s.get("page"),
                excerpt=s.get("excerpt"),
                confidence_score=s.get("confidence_score"),
                semantic_layer=s.get("semantic_layer"),
                matched_concepts=s.get("matched_concepts"),
                pragmatic_insights=s.get("pragmatic_insights"),
            )
            for s in result.get("sources", [])
        ]

        return ContextRail(
            query_id=result["query_id"],
            query=result["query"],
            retrieved_at=result["retrieved_at"],
            sources=sources,
            summary=result.get("summary", {}),
        )

    async def upload_document_async(
        self,
        file_path: str,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> Document:
        """Async version of upload_document."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self.upload_document, file_path, title, tags
        )

    async def query_async(
        self,
        query: str,
        document_ids: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        limit: int = 3,
        confidence_threshold: float = 0.5,
    ) -> QueryResult:
        """Async version of query."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.query,
            query,
            document_ids,
            tags,
            limit,
            confidence_threshold,
        )

    def close(self) -> None:
        """Close the HTTP client connection."""
        self._client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
