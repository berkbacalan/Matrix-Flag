package com.matrixflag.sdk;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.ObjectMapper;
import okhttp3.*;
import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class MatrixFlagClient {
    private final String baseUrl;
    private final String apiKey;
    private final OkHttpClient httpClient;
    private final ObjectMapper objectMapper;

    private MatrixFlagClient(Builder builder) {
        this.baseUrl = builder.baseUrl;
        this.apiKey = builder.apiKey;
        this.objectMapper = new ObjectMapper();

        this.httpClient = new OkHttpClient.Builder()
            .connectTimeout(builder.timeout, TimeUnit.MILLISECONDS)
            .readTimeout(builder.timeout, TimeUnit.MILLISECONDS)
            .writeTimeout(builder.timeout, TimeUnit.MILLISECONDS)
            .retryOnConnectionFailure(true)
            .build();
    }

    public static class Builder {
        private String baseUrl;
        private String apiKey;
        private long timeout = 30000; // 30 seconds

        public Builder baseUrl(String baseUrl) {
            this.baseUrl = baseUrl;
            return this;
        }

        public Builder apiKey(String apiKey) {
            this.apiKey = apiKey;
            return this;
        }

        public Builder timeout(long timeout) {
            this.timeout = timeout;
            return this;
        }

        public MatrixFlagClient build() {
            if (baseUrl == null || apiKey == null) {
                throw new IllegalStateException("baseUrl and apiKey must be set");
            }
            return new MatrixFlagClient(this);
        }
    }

    // Models

    public static class FeatureFlag {
        private int id;
        private String name;
        private String description;
        @JsonProperty("is_active")
        private boolean isActive;
        private String environment;
        @JsonProperty("project_id")
        private Integer projectId;
        @JsonProperty("created_at")
        private Instant createdAt;
        @JsonProperty("updated_at")
        private Instant updatedAt;

        // Getters and setters
        public int getId() { return id; }
        public void setId(int id) { this.id = id; }
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }
        public boolean isActive() { return isActive; }
        public void setActive(boolean active) { isActive = active; }
        public String getEnvironment() { return environment; }
        public void setEnvironment(String environment) { this.environment = environment; }
        public Integer getProjectId() { return projectId; }
        public void setProjectId(Integer projectId) { this.projectId = projectId; }
        public Instant getCreatedAt() { return createdAt; }
        public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
        public Instant getUpdatedAt() { return updatedAt; }
        public void setUpdatedAt(Instant updatedAt) { this.updatedAt = updatedAt; }
    }

    public static class FeatureFlagCreate {
        private String name;
        private String description;
        @JsonProperty("is_active")
        private boolean isActive = true;
        private String environment;
        @JsonProperty("project_id")
        private Integer projectId;

        // Getters and setters
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }
        public boolean isActive() { return isActive; }
        public void setActive(boolean active) { isActive = active; }
        public String getEnvironment() { return environment; }
        public void setEnvironment(String environment) { this.environment = environment; }
        public Integer getProjectId() { return projectId; }
        public void setProjectId(Integer projectId) { this.projectId = projectId; }
    }

    public static class FeatureFlagUpdate {
        private String name;
        private String description;
        @JsonProperty("is_active")
        private Boolean isActive;
        private String environment;
        @JsonProperty("project_id")
        private Integer projectId;

        // Getters and setters
        public String getName() { return name; }
        public void setName(String name) { this.name = name; }
        public String getDescription() { return description; }
        public void setDescription(String description) { this.description = description; }
        public Boolean isActive() { return isActive; }
        public void setActive(Boolean active) { isActive = active; }
        public String getEnvironment() { return environment; }
        public void setEnvironment(String environment) { this.environment = environment; }
        public Integer getProjectId() { return projectId; }
        public void setProjectId(Integer projectId) { this.projectId = projectId; }
    }

    // API Methods

    public FeatureFlag[] listFeatureFlags(Map<String, String> params) throws IOException {
        HttpUrl.Builder urlBuilder = HttpUrl.parse(baseUrl + "/api/v1/feature-flags/").newBuilder();
        if (params != null) {
            for (Map.Entry<String, String> entry : params.entrySet()) {
                urlBuilder.addQueryParameter(entry.getKey(), entry.getValue());
            }
        }

        Request request = new Request.Builder()
            .url(urlBuilder.build())
            .header("Authorization", "Bearer " + apiKey)
            .get()
            .build();

        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected response code: " + response);
            }
            return objectMapper.readValue(response.body().string(), FeatureFlag[].class);
        }
    }

    public FeatureFlag createFeatureFlag(FeatureFlagCreate flag) throws IOException {
        RequestBody body = RequestBody.create(
            MediaType.parse("application/json"),
            objectMapper.writeValueAsString(flag)
        );

        Request request = new Request.Builder()
            .url(baseUrl + "/api/v1/feature-flags/")
            .header("Authorization", "Bearer " + apiKey)
            .post(body)
            .build();

        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected response code: " + response);
            }
            return objectMapper.readValue(response.body().string(), FeatureFlag.class);
        }
    }

    public FeatureFlag getFeatureFlag(int id) throws IOException {
        Request request = new Request.Builder()
            .url(baseUrl + "/api/v1/feature-flags/" + id)
            .header("Authorization", "Bearer " + apiKey)
            .get()
            .build();

        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected response code: " + response);
            }
            return objectMapper.readValue(response.body().string(), FeatureFlag.class);
        }
    }

    public FeatureFlag updateFeatureFlag(int id, FeatureFlagUpdate flag) throws IOException {
        RequestBody body = RequestBody.create(
            MediaType.parse("application/json"),
            objectMapper.writeValueAsString(flag)
        );

        Request request = new Request.Builder()
            .url(baseUrl + "/api/v1/feature-flags/" + id)
            .header("Authorization", "Bearer " + apiKey)
            .put(body)
            .build();

        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected response code: " + response);
            }
            return objectMapper.readValue(response.body().string(), FeatureFlag.class);
        }
    }

    public FeatureFlag deleteFeatureFlag(int id) throws IOException {
        Request request = new Request.Builder()
            .url(baseUrl + "/api/v1/feature-flags/" + id)
            .header("Authorization", "Bearer " + apiKey)
            .delete()
            .build();

        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected response code: " + response);
            }
            return objectMapper.readValue(response.body().string(), FeatureFlag.class);
        }
    }

    public FeatureFlag toggleFeatureFlag(int id) throws IOException {
        Request request = new Request.Builder()
            .url(baseUrl + "/api/v1/feature-flags/" + id + "/toggle")
            .header("Authorization", "Bearer " + apiKey)
            .post(RequestBody.create(null, new byte[0]))
            .build();

        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected response code: " + response);
            }
            return objectMapper.readValue(response.body().string(), FeatureFlag.class);
        }
    }

    public void addWebhook(String url) throws IOException {
        Request request = new Request.Builder()
            .url(baseUrl + "/api/v1/feature-flags/webhooks/" + url)
            .header("Authorization", "Bearer " + apiKey)
            .post(RequestBody.create(null, new byte[0]))
            .build();

        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected response code: " + response);
            }
        }
    }

    public void removeWebhook(String url) throws IOException {
        Request request = new Request.Builder()
            .url(baseUrl + "/api/v1/feature-flags/webhooks/" + url)
            .header("Authorization", "Bearer " + apiKey)
            .delete()
            .build();

        try (Response response = httpClient.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Unexpected response code: " + response);
            }
        }
    }
} 