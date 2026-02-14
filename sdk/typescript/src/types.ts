/**
 * Type definitions for Sens Prism SDK
 */

export type DocumentStatus = "processing" | "ready" | "failed";

export interface Document {
  id: string;
  status: DocumentStatus;
  title?: string;
  sizeBytes?: number;
  tags?: string[];
  createdAt?: string;
  estimatedReadyAt?: string;
  readyAt?: string;
  pageCount?: number;
  chunkCount?: number;
  conceptCount?: number;
}

export interface Source {
  documentId: string;
  documentTitle?: string;
  page?: number;
  excerpt?: string;
  confidenceScore?: number;
  semanticLayer?: "chunk" | "concept" | "context" | "pragmatic" | "universal";
  matchedConcepts?: string[];
  pragmaticInsights?: string[];
}

export interface QueryResult {
  queryId: string;
  query: string;
  answer: string;
  confidenceScore: number;
  processingTimeMs: number;
  sources: Source[];
}

export interface ContextRailSummary {
  totalChunksEvaluated: number;
  chunksReturned: number;
  averageConfidence: number;
}

export interface ContextRail {
  queryId: string;
  query: string;
  retrievedAt: string;
  sources: Source[];
  summary: ContextRailSummary;
}

export interface ClientOptions {
  apiKey?: string;
  baseUrl?: string;
  timeout?: number;
}

export interface UploadOptions {
  title?: string;
  tags?: string[];
}

export interface QueryOptions {
  documentIds?: string[];
  tags?: string[];
  limit?: number;
  confidenceThreshold?: number;
}
