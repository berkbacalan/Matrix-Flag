import { MatrixFlagClient } from '../client';
import { FeatureFlag, FeatureFlagCreate, FeatureFlagUpdate } from '../types';
import axios from 'axios';
import { NetworkError } from '../errors';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('MatrixFlagClient', () => {
    let client: MatrixFlagClient;
    const apiKey = 'test-api-key';
    const baseUrl = 'https://api.matrixflag.com';

    beforeEach(() => {
        client = new MatrixFlagClient(apiKey, baseUrl);
        jest.clearAllMocks();
    });

    describe('constructor', () => {
        it('should create client with default base URL', () => {
            const defaultClient = new MatrixFlagClient(apiKey);
            expect(defaultClient['baseUrl']).toBe('https://api.matrixflag.com');
        });

        it('should create client with custom base URL', () => {
            const customUrl = 'https://custom.matrixflag.com';
            const customClient = new MatrixFlagClient(apiKey, customUrl);
            expect(customClient['baseUrl']).toBe(customUrl);
        });
    });

    describe('listFeatureFlags', () => {
        it('should return list of feature flags', async () => {
            const mockFlags: FeatureFlag[] = [
                {
                    id: 1,
                    name: 'test-flag',
                    isActive: true,
                    environment: 'production',
                    createdAt: '2024-01-01T00:00:00Z',
                    updatedAt: '2024-01-01T00:00:00Z'
                }
            ];

            mockedAxios.request.mockResolvedValueOnce({ data: mockFlags });

            const result = await client.listFeatureFlags();
            expect(result).toEqual(mockFlags);
            expect(mockedAxios.request).toHaveBeenCalledWith({
                method: 'GET',
                url: '/api/v1/feature-flags/',
                params: undefined
            });
        });
    });

    describe('createFeatureFlag', () => {
        it('should create a new feature flag', async () => {
            const mockFlag: FeatureFlag = {
                id: 1,
                name: 'new-flag',
                isActive: true,
                environment: 'production',
                createdAt: '2024-01-01T00:00:00Z',
                updatedAt: '2024-01-01T00:00:00Z'
            };

            const createData: FeatureFlagCreate = {
                name: 'new-flag',
                isActive: true,
                environment: 'production'
            };

            mockedAxios.request.mockResolvedValueOnce({ data: mockFlag });

            const result = await client.createFeatureFlag(createData);
            expect(result).toEqual(mockFlag);
            expect(mockedAxios.request).toHaveBeenCalledWith({
                method: 'POST',
                url: '/api/v1/feature-flags/',
                data: createData
            });
        });
    });

    describe('getFeatureFlag', () => {
        it('should return feature flag when it exists', async () => {
            const mockResponse = {
                data: {
                    id: 'test-flag',
                    name: 'Test Flag',
                    description: 'Test Description',
                    enabled: true,
                    created_at: '2024-01-01T00:00:00Z',
                    updated_at: '2024-01-01T00:00:00Z'
                }
            };

            mockedAxios.request.mockResolvedValueOnce(mockResponse);

            const result = await client.getFeatureFlag('test-flag');

            expect(result).toEqual(mockResponse.data);
            expect(mockedAxios.request).toHaveBeenCalledWith({
                method: 'GET',
                url: `${baseUrl}/api/v1/flags/test-flag`,
                headers: {
                    'Authorization': `Bearer ${apiKey}`,
                    'Content-Type': 'application/json'
                }
            });
        });

        it('should throw NetworkError when request fails', async () => {
            const error = new Error('Network error');
            mockedAxios.request.mockRejectedValueOnce(error);

            await expect(client.getFeatureFlag('test-flag')).rejects.toThrow(NetworkError);
        });
    });

    describe('updateFeatureFlag', () => {
        it('should update a feature flag', async () => {
            const mockFlag: FeatureFlag = {
                id: 1,
                name: 'updated-flag',
                isActive: false,
                environment: 'production',
                createdAt: '2024-01-01T00:00:00Z',
                updatedAt: '2024-01-01T00:00:00Z'
            };

            const updateData: FeatureFlagUpdate = {
                name: 'updated-flag',
                isActive: false
            };

            mockedAxios.request.mockResolvedValueOnce({ data: mockFlag });

            const result = await client.updateFeatureFlag(1, updateData);
            expect(result).toEqual(mockFlag);
            expect(mockedAxios.request).toHaveBeenCalledWith({
                method: 'PUT',
                url: '/api/v1/feature-flags/1',
                data: updateData
            });
        });
    });

    describe('deleteFeatureFlag', () => {
        it('should delete a feature flag', async () => {
            const mockFlag: FeatureFlag = {
                id: 1,
                name: 'deleted-flag',
                isActive: true,
                environment: 'production',
                createdAt: '2024-01-01T00:00:00Z',
                updatedAt: '2024-01-01T00:00:00Z'
            };

            mockedAxios.request.mockResolvedValueOnce({ data: mockFlag });

            const result = await client.deleteFeatureFlag(1);
            expect(result).toEqual(mockFlag);
            expect(mockedAxios.request).toHaveBeenCalledWith({
                method: 'DELETE',
                url: '/api/v1/feature-flags/1'
            });
        });
    });

    describe('toggleFeatureFlag', () => {
        it('should toggle a feature flag', async () => {
            const mockFlag: FeatureFlag = {
                id: 1,
                name: 'test-flag',
                isActive: false,
                environment: 'production',
                createdAt: '2024-01-01T00:00:00Z',
                updatedAt: '2024-01-01T00:00:00Z'
            };

            mockedAxios.request.mockResolvedValueOnce({ data: mockFlag });

            const result = await client.toggleFeatureFlag(1);
            expect(result).toEqual(mockFlag);
            expect(mockedAxios.request).toHaveBeenCalledWith({
                method: 'POST',
                url: '/api/v1/feature-flags/1/toggle'
            });
        });
    });

    describe('webhook operations', () => {
        const webhookUrl = 'https://example.com/webhook';

        it('should add a webhook', async () => {
            mockedAxios.request.mockResolvedValueOnce({ data: undefined });

            await client.addWebhook(webhookUrl);
            expect(mockedAxios.request).toHaveBeenCalledWith({
                method: 'POST',
                url: `/api/v1/feature-flags/webhooks/${encodeURIComponent(webhookUrl)}`
            });
        });

        it('should remove a webhook', async () => {
            mockedAxios.request.mockResolvedValueOnce({ data: undefined });

            await client.removeWebhook(webhookUrl);
            expect(mockedAxios.request).toHaveBeenCalledWith({
                method: 'DELETE',
                url: `/api/v1/feature-flags/webhooks/${encodeURIComponent(webhookUrl)}`
            });
        });
    });
}); 