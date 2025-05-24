export class MatrixFlagError extends Error {
    public status: number;
    public details?: any;

    constructor(message: string, status: number, details?: any) {
        super(message);
        this.name = 'MatrixFlagError';
        this.status = status;
        this.details = details;
    }
}

export class AuthenticationError extends MatrixFlagError {
    constructor(message: string = 'Authentication failed', details?: any) {
        super(message, 401, details);
        this.name = 'AuthenticationError';
    }
}

export class AuthorizationError extends MatrixFlagError {
    constructor(message: string = 'Not authorized', details?: any) {
        super(message, 403, details);
        this.name = 'AuthorizationError';
    }
}

export class NotFoundError extends MatrixFlagError {
    constructor(message: string = 'Resource not found', details?: any) {
        super(message, 404, details);
        this.name = 'NotFoundError';
    }
}

export class ValidationError extends MatrixFlagError {
    constructor(message: string = 'Validation failed', details?: any) {
        super(message, 400, details);
        this.name = 'ValidationError';
    }
}

export class RateLimitError extends MatrixFlagError {
    constructor(message: string = 'Rate limit exceeded', details?: any) {
        super(message, 429, details);
        this.name = 'RateLimitError';
    }
}

export class ServerError extends MatrixFlagError {
    constructor(message: string = 'Internal server error', details?: any) {
        super(message, 500, details);
        this.name = 'ServerError';
    }
}

export class NetworkError extends MatrixFlagError {
    constructor(message: string = 'Network error', details?: any) {
        super(message, 0, details);
        this.name = 'NetworkError';
    }
} 