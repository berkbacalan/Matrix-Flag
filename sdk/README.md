# Matrix Flag SDKs

This repository contains official SDKs for the Matrix Flag API in multiple programming languages.

## Available SDKs

- [Python SDK](./python/README.md)
- [JavaScript/TypeScript SDK](./javascript/README.md)
- [Go SDK](./go/README.md)
- [Java SDK](./java/README.md)

## Common Features

All SDKs provide the following features:

- Full API coverage
- Type safety
- Error handling
- Authentication
- Rate limiting
- Retry mechanism
- Pagination
- Webhook support
- Event handling
- Caching
- Logging
- Metrics

## Installation

### Python
```bash
pip install matrix-flag
```

### JavaScript/TypeScript
```bash
npm install @matrix-flag/sdk
# or
yarn add @matrix-flag/sdk
```

### Go
```bash
go get github.com/matrix-flag/sdk-go
```

### Java
```xml
<dependency>
    <groupId>com.matrix-flag</groupId>
    <artifactId>sdk</artifactId>
    <version>1.0.0</version>
</dependency>
```

## Quick Start

### Python
```python
from matrix_flag import MatrixFlagClient

client = MatrixFlagClient(
    base_url="http://localhost:8000",
    api_key="your-api-key"
)

# Create a feature flag
flag = client.create_feature_flag(
    name="new-feature",
    description="Enable new feature",
    is_active=True,
    environment="production"
)
```

### JavaScript/TypeScript
```typescript
import { MatrixFlagClient } from '@matrix-flag/sdk';

const client = new MatrixFlagClient({
    baseUrl: 'http://localhost:8000',
    apiKey: 'your-api-key'
});

// Create a feature flag
const flag = await client.createFeatureFlag({
    name: 'new-feature',
    description: 'Enable new feature',
    isActive: true,
    environment: 'production'
});
```

### Go
```go
import "github.com/matrix-flag/sdk-go"

client := matrixflag.NewClient(
    "http://localhost:8000",
    "your-api-key",
)

// Create a feature flag
flag, err := client.CreateFeatureFlag(context.Background(), matrixflag.FeatureFlagCreate{
    Name:        "new-feature",
    Description: "Enable new feature",
    IsActive:    true,
    Environment: "production",
})
```

### Java
```java
import com.matrixflag.sdk.MatrixFlagClient;

MatrixFlagClient client = new MatrixFlagClient.Builder()
    .baseUrl("http://localhost:8000")
    .apiKey("your-api-key")
    .build();

// Create a feature flag
FeatureFlag flag = client.createFeatureFlag(FeatureFlagCreate.builder()
    .name("new-feature")
    .description("Enable new feature")
    .isActive(true)
    .environment("production")
    .build());
```

## Contributing

We welcome contributions to our SDKs! Please see our [Contributing Guide](./CONTRIBUTING.md) for more information.

## License

All SDKs are licensed under the MIT License - see the [LICENSE](./LICENSE) file for details. 