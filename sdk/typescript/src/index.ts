/**
 * Sens Prism TypeScript SDK
 * The official TypeScript client for Sens Prism - Sovereign AI Gateway
 */

export { SensClient } from "./client";
export {
  SensError,
  SensAuthError,
  SensRateLimitError,
  SensNotFoundError,
  SensValidationError,
  SensConflictError,
  SensPayloadTooLargeError,
  SensServiceUnavailableError,
} from "./exceptions";

export type {
  Document,
  DocumentStatus,
  Source,
  QueryResult,
  ContextRail,
  ContextRailSummary,
  ClientOptions,
} from "./types";

export const version = "0.4.0";
