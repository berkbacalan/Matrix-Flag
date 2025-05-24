import { MatrixFlagClient } from '../client';
import { FeatureFlag, FeatureFlagCreate, FeatureFlagUpdate } from '../types';
import axios from 'axios';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('MatrixFlagClient', () => {
    let client: MatrixFlagClient;
    const mockConfig = {
        baseUrl: 'https://api.matrixflag.com',
        apiKey: 'test-api-key'
    };

    beforeEach(() => {
        client = new MatrixFlagClient(mockConfig);
        jest.clearAllMocks();
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
        it('should get a feature flag by id', async () => {
            const mockFlag: FeatureFlag = {
                id: 1,
                name: 'test-flag',
                isActive: true,
                environment: 'production',
                createdAt: '2024-01-01T00:00:00Z',
                updatedAt: '2024-01-01T00:00:00Z'
            };

            mockedAxios.request.mockResolvedValueOnce({ data: mockFlag });

            const result = await client.getFeatureFlag(1);
            expect(result).toEqual(mockFlag);
            expect(mockedAxios.request).toHaveBeenCalledWith({
                method: 'GET',
                url: '/api/v1/feature-flags/1'
            });
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