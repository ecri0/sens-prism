/**
 * Exception classes for Sens Prism SDK
 */

export interface ErrorDetails {
  [key: string]: any;
}

export class SensError extends Error {
  public code?: string;
  public details: ErrorDetails;

  constructor(message: string, code?: string, details?: ErrorDetails) {
    super(message);
    this.name = "SensError";
    this.code = code;
    this.details = details || {};
  }

  toString(): string {
    if (this.code) {
      return `[${this.code}] ${this.message}`;
    }
    return this.message;
  }
}

export class SensAuthError extends SensError {
  constructor(message: string, code?: string, details?: ErrorDetails) {
    super(message, code, details);
    this.name = "SensAuthError";
  }
}

export class SensRateLimitError extends SensError {
  public retryAfter?: number;

  constructor(
    message: string,
    code?: string,
    details?: ErrorDetails,
    retryAfter?: number
  ) {
    super(message, code, details);
    this.name = "SensRateLimitError";
    this.retryAfter = retryAfter;
  }
}

export class SensNotFoundError extends SensError {
  constructor(message: string, code?: string, details?: ErrorDetails) {
    super(message, code, details);
    this.name = "SensNotFoundError";
  }
}

export class SensValidationError extends SensError {
  constructor(message: string, code?: string, details?: ErrorDetails) {
    super(message, code, details);
    this.name = "SensValidationError";
  }
}

export class SensConflictError extends SensError {
  constructor(message: string, code?: string, details?: ErrorDetails) {
    super(message, code, details);
    this.name = "SensConflictError";
  }
}

export class SensPayloadTooLargeError extends SensError {
  constructor(message: string, code?: string, details?: ErrorDetails) {
    super(message, code, details);
    this.name = "SensPayloadTooLargeError";
  }
}

export class SensServiceUnavailableError extends SensError {
  public retryAfter?: number;

  constructor(
    message: string,
    code?: string,
    details?: ErrorDetails,
    retryAfter?: number
  ) {
    super(message, code, details);
    this.name = "SensServiceUnavailableError";
    this.retryAfter = retryAfter;
  }
}
