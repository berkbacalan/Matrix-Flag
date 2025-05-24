export interface RetryConfig {
    maxRetries: number;
    retryDelay: number;
    maxRetryDelay: number;
}

export const defaultRetryConfig: RetryConfig = {
    maxRetries: 3,
    retryDelay: 1000,
    maxRetryDelay: 10000
};

export interface CacheConfig {
    enabled: boolean;
    ttl: number;
    maxSize: number;
}

export const defaultCacheConfig: CacheConfig = {
    enabled: true,
    ttl: 60000, // 1 minute
    maxSize: 1000
};

export interface LoggingConfig {
    enabled: boolean;
    level: 'debug' | 'info' | 'warn' | 'error';
    format: 'json' | 'text';
}

export const defaultLoggingConfig: LoggingConfig = {
    enabled: true,
    level: 'info',
    format: 'text'
};

export interface MetricsConfig {
    enabled: boolean;
    prefix: string;
}

export const defaultMetricsConfig: MetricsConfig = {
    enabled: true,
    prefix: 'matrix_flag_'
}; 