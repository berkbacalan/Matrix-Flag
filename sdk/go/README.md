# Matrix Flag Go SDK

This is the official Go SDK for the Matrix Flag API. It provides a simple and intuitive interface for managing feature flags in your applications.

## Installation

```bash
go get github.com/matrixflag/sdk
```

## Usage

```go
package main

import (
    "context"
    "fmt"
    "log"
    "time"

    "github.com/matrixflag/sdk"
)

func main() {
    // Initialize the client
    client := matrixflag.NewClient(
        "https://api.matrixflag.com",
        "your-api-key",
        &matrixflag.Config{
            Timeout: 30 * time.Second,
            MaxRetries: 3,
            RetryDelay: time.Second,
            MaxRetryDelay: 10 * time.Second,
        },
    )

    ctx := context.Background()

    // List feature flags
    flags, err := client.ListFeatureFlags(ctx, map[string]string{
        "environment": "production",
    })
    if err != nil {
        log.Fatal(err)
    }

    // Create a new feature flag
    newFlag, err := client.CreateFeatureFlag(ctx, matrixflag.FeatureFlagCreate{
        Name:        "new-feature",
        Description: "Enable new feature",
        IsActive:    true,
        Environment: "production",
    })
    if err != nil {
        log.Fatal(err)
    }

    // Get a feature flag
    flag, err := client.GetFeatureFlag(ctx, 1)
    if err != nil {
        log.Fatal(err)
    }

    // Update a feature flag
    updatedFlag, err := client.UpdateFeatureFlag(ctx, 1, matrixflag.FeatureFlagUpdate{
        IsActive: false,
    })
    if err != nil {
        log.Fatal(err)
    }

    // Delete a feature flag
    deletedFlag, err := client.DeleteFeatureFlag(ctx, 1)
    if err != nil {
        log.Fatal(err)
    }

    // Toggle a feature flag
    toggledFlag, err := client.ToggleFeatureFlag(ctx, 1)
    if err != nil {
        log.Fatal(err)
    }

    // Add a webhook
    err = client.AddWebhook(ctx, "https://your-webhook-url.com")
    if err != nil {
        log.Fatal(err)
    }

    // Remove a webhook
    err = client.RemoveWebhook(ctx, "https://your-webhook-url.com")
    if err != nil {
        log.Fatal(err)
    }
}
```

## Configuration

The client can be configured with the following options:

```go
type Config struct {
    Timeout        time.Duration
    MaxRetries     int
    RetryDelay     time.Duration
    MaxRetryDelay  time.Duration
}
```

## Error Handling

The SDK uses custom error types for different types of errors:

```go
flag, err := client.GetFeatureFlag(ctx, 1)
if err != nil {
    switch {
    case errors.Is(err, matrixflag.ErrAuthentication):
        // Handle authentication error
    case errors.Is(err, matrixflag.ErrAuthorization):
        // Handle authorization error
    case errors.Is(err, matrixflag.ErrNotFound):
        // Handle not found error
    case errors.Is(err, matrixflag.ErrValidation):
        // Handle validation error
    case errors.Is(err, matrixflag.ErrRateLimit):
        // Handle rate limit error
    case errors.Is(err, matrixflag.ErrServer):
        // Handle server error
    case errors.Is(err, matrixflag.ErrNetwork):
        // Handle network error
    default:
        // Handle other errors
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