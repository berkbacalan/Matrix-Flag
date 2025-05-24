# Matrix Flag Java SDK

This is the official Java SDK for the Matrix Flag API. It provides a simple and intuitive interface for managing feature flags in your applications.

## Installation

Add the following dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.matrixflag</groupId>
    <artifactId>matrix-flag-sdk</artifactId>
    <version>1.0.0</version>
</dependency>
```

## Usage

```java
import com.matrixflag.sdk.MatrixFlagClient;
import com.matrixflag.sdk.MatrixFlagClient.FeatureFlag;
import com.matrixflag.sdk.MatrixFlagClient.FeatureFlagCreate;
import com.matrixflag.sdk.MatrixFlagClient.FeatureFlagUpdate;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class Example {
    public static void main(String[] args) {
        // Initialize the client
        MatrixFlagClient client = new MatrixFlagClient.Builder()
            .baseUrl("https://api.matrixflag.com")
            .apiKey("your-api-key")
            .timeout(30000) // 30 seconds
            .build();

        try {
            // List feature flags
            Map<String, String> params = new HashMap<>();
            params.put("environment", "production");
            FeatureFlag[] flags = client.listFeatureFlags(params);

            // Create a new feature flag
            FeatureFlagCreate newFlag = new FeatureFlagCreate();
            newFlag.setName("new-feature");
            newFlag.setDescription("Enable new feature");
            newFlag.setActive(true);
            newFlag.setEnvironment("production");
            FeatureFlag createdFlag = client.createFeatureFlag(newFlag);

            // Get a feature flag
            FeatureFlag flag = client.getFeatureFlag(1);

            // Update a feature flag
            FeatureFlagUpdate update = new FeatureFlagUpdate();
            update.setActive(false);
            FeatureFlag updatedFlag = client.updateFeatureFlag(1, update);

            // Delete a feature flag
            FeatureFlag deletedFlag = client.deleteFeatureFlag(1);

            // Toggle a feature flag
            FeatureFlag toggledFlag = client.toggleFeatureFlag(1);

            // Add a webhook
            client.addWebhook("https://your-webhook-url.com");

            // Remove a webhook
            client.removeWebhook("https://your-webhook-url.com");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

## Configuration

The client can be configured with the following options:

```java
MatrixFlagClient client = new MatrixFlagClient.Builder()
    .baseUrl("https://api.matrixflag.com")
    .apiKey("your-api-key")
    .timeout(30000) // 30 seconds
    .build();
```

## Error Handling

The SDK throws `IOException` for all API errors. You can handle them like this:

```java
try {
    FeatureFlag flag = client.getFeatureFlag(1);
} catch (IOException e) {
    // Handle the error
    e.printStackTrace();
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