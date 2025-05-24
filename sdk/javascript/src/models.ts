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

export interface WebhookEvent {
    type: 'feature_flag.created' | 'feature_flag.updated' | 'feature_flag.deleted' | 'feature_flag.toggled';
    data: FeatureFlag;
    timestamp: string;
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    size: number;
    hasMore: boolean;
}

export interface ErrorResponse {
    message: string;
    code: string;
    details?: any;
} 