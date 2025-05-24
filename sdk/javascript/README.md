# Matrix Flag JavaScript SDK

This is the official JavaScript SDK for the Matrix Flag API. It provides a simple and intuitive interface for managing feature flags in your applications.

## Installation

```bash
npm install @matrixflag/sdk
```

## Usage

```typescript
import { MatrixFlagClient } from '@matrixflag/sdk';

// Initialize the client
const client = new MatrixFlagClient({
  baseUrl: 'https://api.matrixflag.com',
  apiKey: 'your-api-key'
});

// List feature flags
const flags = await client.listFeatureFlags();

// Create a new feature flag
const newFlag = await client.createFeatureFlag({
  name: 'new-feature',
  description: 'Enable new feature',
  isActive: true,
  environment: 'production'
});

// Get a feature flag
const flag = await client.getFeatureFlag(1);

// Update a feature flag
const updatedFlag = await client.updateFeatureFlag(1, {
  isActive: false
});

// Delete a feature flag
const deletedFlag = await client.deleteFeatureFlag(1);

// Toggle a feature flag
const toggledFlag = await client.toggleFeatureFlag(1);

// Add a webhook
await client.addWebhook('https://your-webhook-url.com');

// Remove a webhook
await client.removeWebhook('https://your-webhook-url.com');
```

## Configuration

The client can be configured with the following options:

```typescript
interface ClientConfig {
  baseUrl: string;
  apiKey: string;
  timeout?: number;
  retryConfig?: {
    maxRetries: number;
    retryDelay: number;
    maxRetryDelay: number;
  };
  cacheConfig?: {
    enabled: boolean;
    ttl: number;
    maxSize: number;
  };
  loggingConfig?: {
    enabled: boolean;
    level: 'debug' | 'info' | 'warn' | 'error';
    format: 'json' | 'text';
  };
  metricsConfig?: {
    enabled: boolean;
    prefix: string;
  };
}
```

## Error Handling

The SDK uses custom error classes for different types of errors:

```typescript
try {
  await client.getFeatureFlag(1);
} catch (error) {
  if (error instanceof AuthenticationError) {
    // Handle authentication error
  } else if (error instanceof AuthorizationError) {
    // Handle authorization error
  } else if (error instanceof NotFoundError) {
    // Handle not found error
  } else if (error instanceof ValidationError) {
    // Handle validation error
  } else if (error instanceof RateLimitError) {
    // Handle rate limit error
  } else if (error instanceof ServerError) {
    // Handle server error
  } else if (error instanceof NetworkError) {
    // Handle network error
  }
}
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 