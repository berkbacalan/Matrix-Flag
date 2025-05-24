export interface FeatureFlag {
    id: number;
    name: string;
    description?: string;
    isActive: boolean;
    environment: string;
    projectId?: number;
    createdAt: string;
    updatedAt: string;
}

export interface FeatureFlagCreate {
    name: string;
    description?: string;
    isActive?: boolean;
    environment: string;
    projectId?: number;
}

export interface FeatureFlagUpdate {
    name?: string;
    description?: string;
    isActive?: boolean;
    environment?: string;
    projectId?: number;
}

export interface ClientConfig {
    baseUrl: string;
    apiKey: string;
    timeout?: number;
    retryConfig?: RetryConfig;
    cacheConfig?: CacheConfig;
    loggingConfig?: LoggingConfig;
    metricsConfig?: MetricsConfig;
}

export interface RetryConfig {
    maxRetries: number;
    retryDelay: number;
    maxRetryDelay: number;
}

export interface CacheConfig {
    enabled: boolean;
    ttl: number;
    maxSize: number;
}

export interface LoggingConfig {
    enabled: boolean;
    level: 'debug' | 'info' | 'warn' | 'error';
    format: 'json' | 'text';
}

export interface MetricsConfig {
    enabled: boolean;
    prefix: string;
} 