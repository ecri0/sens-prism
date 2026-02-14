/**
 * Sens Prism TypeScript SDK Client
 */

import * as fs from "fs";
import * as path from "path";
import FormData from "form-data";

import {
  Document,
  QueryResult,
  ContextRail,
  ClientOptions,
  UploadOptions,
  QueryOptions,
} from "./types";

import {
  SensError,
  SensAuthError,
  SensRateLimitError,
  SensNotFoundError,
  SensValidationError,
  SensConflictError,
  SensPayloadTooLargeError,
  SensServiceUnavailableError,
} from "./exceptions";

interface FetchOptions extends RequestInit {
  body?: BodyInit | object;
}

interface ApiErrorResponse {
  error: string;
  code?: string;
  message: string;
  details?: { [key: string]: any };
}

/**
 * Sens Prism Client for TypeScript/Node.js
 *
 * @example
 * ```typescript
 * const client = new SensClient({ apiKey: "sens_sk_..." });
 * const doc = await client.uploadDocument("contract.pdf");
 * const result = await client.query("What are the terms?", {
 *   documentIds: [doc.id]
 * });
 * console.log(result.answer);
 * ```
 */
export class SensClient {
  private apiKey: string;
  private baseUrl: string;
  private timeout: number;

  constructor(options: ClientOptions = {}) {
    this.apiKey = options.apiKey || process.env.SENS_API_KEY || "";
    if (!this.apiKey) {
      throw new SensValidationError(
        "API key required. Provide 'apiKey' option or set SENS_API_KEY environment variable.",
        "SENS_003"
      );
    }

    this.baseUrl = (options.baseUrl || "https://api.sens.ai/v1").replace(
      /\/+$/,
      ""
    );
    this.timeout = options.timeout || 30000;
  }

  private getHeaders(contentType?: string): HeadersInit {
    const headers: HeadersInit = {
      Authorization: `Bearer ${this.apiKey}`,
      "User-Agent": "@sens/prism/0.4.0",
    };

    if (contentType) {
      headers["Content-Type"] = contentType;
    }

    return headers;
  }

  private async handleResponse<T>(
    response: Response,
    contentType?: string
  ): Promise<T> {
    let data: any;

    try {
      if (contentType === "application/octet-stream") {
        data = {};
      } else {
        data = await response.json();
      }
    } catch {
      data = {};
    }

    // Success responses
    if (response.ok) {
      return data as T;
    }

    // Error responses
    const errorMessage =
      data.message || `HTTP ${response.status}: ${response.statusText}`;
    const errorCode = data.code;
    const errorDetails = data.details || {};

    switch (response.status) {
      case 400:
        throw new SensValidationError(errorMessage, errorCode, errorDetails);
      case 401:
      case 403:
        throw new SensAuthError(errorMessage, errorCode, errorDetails);
      case 404:
        throw new SensNotFoundError(errorMessage, errorCode, errorDetails);
      case 409:
        throw new SensConflictError(errorMessage, errorCode, errorDetails);
      case 413:
        throw new SensPayloadTooLargeError(
          errorMessage,
          errorCode,
          errorDetails
        );
      case 429:
        const retryAfter = response.headers.get("Retry-After");
        throw new SensRateLimitError(
          errorMessage,
          errorCode,
          errorDetails,
          retryAfter ? parseInt(retryAfter) : undefined
        );
      case 503:
        const retryAfter503 = response.headers.get("Retry-After");
        throw new SensServiceUnavailableError(
          errorMessage,
          errorCode,
          errorDetails,
          retryAfter503 ? parseInt(retryAfter503) : undefined
        );
      default:
        throw new SensError(errorMessage, errorCode, errorDetails);
    }
  }

  /**
   * Upload a document for processing and indexing.
   *
   * @param filePath - Path to the document file (PDF, DOCX, TXT, RTF)
   * @param options - Upload options (title, tags)
   * @returns Uploaded document with ID and status
   */
  async uploadDocument(
    filePath: string,
    options?: UploadOptions
  ): Promise<Document> {
    if (!fs.existsSync(filePath)) {
      throw new SensValidationError(
        `File not found: ${filePath}`,
        "SENS_003"
      );
    }

    const form = new FormData();
    form.append("file", fs.createReadStream(filePath));

    if (options?.title) {
      form.append("title", options.title);
    }
    if (options?.tags) {
      form.append("tags", options.tags.join(","));
    }

    const response = await fetch(`${this.baseUrl}/documents`, {
      method: "POST",
      headers: this.getHeaders(),
      body: form,
    });

    const data = await this.handleResponse<any>(response);
    return this.parseDocument(data);
  }

  /**
   * Get document metadata and status.
   *
   * @param documentId - The document ID
   * @returns Document with current status
   */
  async getDocument(documentId: string): Promise<Document> {
    const response = await fetch(`${this.baseUrl}/documents/${documentId}`, {
      method: "GET",
      headers: this.getHeaders(),
    });

    const data = await this.handleResponse<any>(response);
    return this.parseDocument(data);
  }

  /**
   * Delete a document. This action is permanent.
   *
   * @param documentId - The document ID to delete
   */
  async deleteDocument(documentId: string): Promise<void> {
    const response = await fetch(`${this.baseUrl}/documents/${documentId}`, {
      method: "DELETE",
      headers: this.getHeaders(),
    });

    await this.handleResponse<void>(response);
  }

  /**
   * Query your knowledge base.
   *
   * @param query - Your question or search query
   * @param options - Query options (documentIds, tags, limit, confidenceThreshold)
   * @returns Query result with answer and sources
   */
  async query(
    query: string,
    options?: QueryOptions
  ): Promise<QueryResult> {
    const payload: any = {
      query,
      limit: options?.limit || 3,
      confidence_threshold: options?.confidenceThreshold || 0.5,
    };

    if (options?.documentIds) {
      payload.document_ids = options.documentIds;
    }
    if (options?.tags) {
      payload.tags = options.tags;
    }

    const response = await fetch(`${this.baseUrl}/query`, {
      method: "POST",
      headers: { ...this.getHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await this.handleResponse<any>(response);
    return this.parseQueryResult(data);
  }

  /**
   * Get detailed context information for a query.
   *
   * @param queryId - The query ID from a query response
   * @returns Context rail with detailed source information
   */
  async getContextRail(queryId: string): Promise<ContextRail> {
    const response = await fetch(`${this.baseUrl}/context-rail/${queryId}`, {
      method: "GET",
      headers: this.getHeaders(),
    });

    const data = await this.handleResponse<any>(response);
    return this.parseContextRail(data);
  }

  // Helper methods for parsing responses

  private parseDocument(data: any): Document {
    return {
      id: data.id,
      status: data.status,
      title: data.title,
      sizeBytes: data.size_bytes,
      tags: data.tags,
      createdAt: data.created_at,
      estimatedReadyAt: data.estimated_ready_at,
      readyAt: data.ready_at,
      pageCount: data.page_count,
      chunkCount: data.chunk_count,
      conceptCount: data.concept_count,
    };
  }

  private parseQueryResult(data: any): QueryResult {
    return {
      queryId: data.query_id,
      query: data.query,
      answer: data.answer,
      confidenceScore: data.confidence_score,
      processingTimeMs: data.processing_time_ms,
      sources: (data.sources || []).map((s: any) => ({
        documentId: s.document_id,
        documentTitle: s.document_title,
        page: s.page,
        confidenceScore: s.confidence_score,
      })),
    };
  }

  private parseContextRail(data: any): ContextRail {
    return {
      queryId: data.query_id,
      query: data.query,
      retrievedAt: data.retrieved_at,
      sources: (data.sources || []).map((s: any) => ({
        documentId: s.document_id,
        documentTitle: s.document_title,
        page: s.page,
        excerpt: s.excerpt,
        confidenceScore: s.confidence_score,
        semanticLayer: s.semantic_layer,
        matchedConcepts: s.matched_concepts,
        pragmaticInsights: s.pragmatic_insights,
      })),
      summary: {
        totalChunksEvaluated: data.summary?.total_chunks_evaluated || 0,
        chunksReturned: data.summary?.chunks_returned || 0,
        averageConfidence: data.summary?.average_confidence || 0,
      },
    };
  }
}
