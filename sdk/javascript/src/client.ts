import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import {
    ClientConfig,
    FeatureFlag,
    FeatureFlagCreate,
    FeatureFlagUpdate,
} from './types';
import {
    AuthenticationError,
    AuthorizationError,
    MatrixFlagError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
} from './errors';
import { defaultRetryConfig, defaultCacheConfig, defaultLoggingConfig, defaultMetricsConfig } from './config';

export class MatrixFlagClient {
    private readonly axiosInstance: AxiosInstance;
    private readonly config: Required<ClientConfig>;

    constructor(config: ClientConfig) {
        this.config = {
            ...config,
            timeout: config.timeout || 30000,
            retryConfig: config.retryConfig || defaultRetryConfig,
            cacheConfig: config.cacheConfig || defaultCacheConfig,
            loggingConfig: config.loggingConfig || defaultLoggingConfig,
            metricsConfig: config.metricsConfig || defaultMetricsConfig,
        };

        this.axiosInstance = axios.create({
            baseURL: this.config.baseUrl,
            timeout: this.config.timeout,
            headers: {
                'Authorization': `Bearer ${this.config.apiKey}`,
                'Content-Type': 'application/json',
            },
        });

        this.setupInterceptors();
    }

    private setupInterceptors(): void {
        this.axiosInstance.interceptors.response.use(
            (response) => response,
            (error) => {
                if (error.response) {
                    const { status, data } = error.response;
                    switch (status) {
                        case 401:
                            throw new AuthenticationError(data.message, data.details);
                        case 403:
                            throw new AuthorizationError(data.message, data.details);
                        case 404:
                            throw new NotFoundError(data.message, data.details);
                        case 400:
                            throw new ValidationError(data.message, data.details);
                        case 429:
                            throw new RateLimitError(data.message, data.details);
                        case 500:
                            throw new ServerError(data.message, data.details);
                        default:
                            throw new MatrixFlagError(data.message, status, data.details);
                    }
                } else if (error.request) {
                    throw new NetworkError(error.message);
                } else {
                    throw error;
                }
            }
        );
    }

    private async request<T>(config: AxiosRequestConfig): Promise<T> {
        try {
            const response = await this.axiosInstance.request<T>(config);
            return response.data;
        } catch (error) {
            if (error instanceof MatrixFlagError) {
                throw error;
            }
            throw new NetworkError(error.message);
        }
    }

    async listFeatureFlags(params?: Record<string, string>): Promise<FeatureFlag[]> {
        return this.request<FeatureFlag[]>({
            method: 'GET',
            url: '/api/v1/feature-flags/',
            params,
        });
    }

    async createFeatureFlag(flag: FeatureFlagCreate): Promise<FeatureFlag> {
        return this.request<FeatureFlag>({
            method: 'POST',
            url: '/api/v1/feature-flags/',
            data: flag,
        });
    }

    async getFeatureFlag(id: number): Promise<FeatureFlag> {
        return this.request<FeatureFlag>({
            method: 'GET',
            url: `/api/v1/feature-flags/${id}`,
        });
    }

    async updateFeatureFlag(id: number, flag: FeatureFlagUpdate): Promise<FeatureFlag> {
        return this.request<FeatureFlag>({
            method: 'PUT',
            url: `/api/v1/feature-flags/${id}`,
            data: flag,
        });
    }

    async deleteFeatureFlag(id: number): Promise<FeatureFlag> {
        return this.request<FeatureFlag>({
            method: 'DELETE',
            url: `/api/v1/feature-flags/${id}`,
        });
    }

    async toggleFeatureFlag(id: number): Promise<FeatureFlag> {
        return this.request<FeatureFlag>({
            method: 'POST',
            url: `/api/v1/feature-flags/${id}/toggle`,
        });
    }

    async addWebhook(url: string): Promise<void> {
        await this.request<void>({
            method: 'POST',
            url: `/api/v1/feature-flags/webhooks/${encodeURIComponent(url)}`,
        });
    }

    async removeWebhook(url: string): Promise<void> {
        await this.request<void>({
            method: 'DELETE',
            url: `/api/v1/feature-flags/webhooks/${encodeURIComponent(url)}`,
        });
    }
} 