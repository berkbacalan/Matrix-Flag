package matrixflag

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// Client represents a Matrix Flag API client
type Client struct {
	baseURL    string
	apiKey     string
	httpClient *http.Client
	config     *Config
}

// Config represents the client configuration
type Config struct {
	Timeout     time.Duration
	MaxRetries  int
	RetryDelay  time.Duration
	MaxRetryDelay time.Duration
}

// DefaultConfig returns the default client configuration
func DefaultConfig() *Config {
	return &Config{
		Timeout:     30 * time.Second,
		MaxRetries:  3,
		RetryDelay:  time.Second,
		MaxRetryDelay: 10 * time.Second,
	}
}

// NewClient creates a new Matrix Flag client
func NewClient(baseURL, apiKey string, config *Config) *Client {
	if config == nil {
		config = DefaultConfig()
	}

	return &Client{
		baseURL: baseURL,
		apiKey:  apiKey,
		httpClient: &http.Client{
			Timeout: config.Timeout,
		},
		config: config,
	}
}

// request represents an API request
type request struct {
	method  string
	path    string
	body    interface{}
	query   map[string]string
	headers map[string]string
}

// doRequest performs an HTTP request with retries
func (c *Client) doRequest(ctx context.Context, req request) ([]byte, error) {
	var body io.Reader
	if req.body != nil {
		jsonBody, err := json.Marshal(req.body)
		if err != nil {
			return nil, fmt.Errorf("failed to marshal request body: %w", err)
		}
		body = bytes.NewReader(jsonBody)
	}

	httpReq, err := http.NewRequestWithContext(ctx, req.method, c.baseURL+req.path, body)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	// Add headers
	httpReq.Header.Set("Authorization", "Bearer "+c.apiKey)
	httpReq.Header.Set("Content-Type", "application/json")
	for k, v := range req.headers {
		httpReq.Header.Set(k, v)
	}

	// Add query parameters
	q := httpReq.URL.Query()
	for k, v := range req.query {
		q.Set(k, v)
	}
	httpReq.URL.RawQuery = q.Encode()

	// Perform request with retries
	var resp *http.Response
	var lastErr error
	for i := 0; i <= c.config.MaxRetries; i++ {
		resp, err = c.httpClient.Do(httpReq)
		if err == nil {
			break
		}
		lastErr = err
		if i < c.config.MaxRetries {
			delay := c.config.RetryDelay * time.Duration(1<<uint(i))
			if delay > c.config.MaxRetryDelay {
				delay = c.config.MaxRetryDelay
			}
			time.Sleep(delay)
		}
	}
	if lastErr != nil {
		return nil, fmt.Errorf("failed to perform request after %d retries: %w", c.config.MaxRetries, lastErr)
	}
	defer resp.Body.Close()

	// Read response body
	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read response body: %w", err)
	}

	// Check for errors
	if resp.StatusCode >= 400 {
		var apiErr APIError
		if err := json.Unmarshal(respBody, &apiErr); err != nil {
			return nil, fmt.Errorf("API error (status %d): %s", resp.StatusCode, string(respBody))
		}
		return nil, apiErr
	}

	return respBody, nil
}

// FeatureFlag represents a feature flag
type FeatureFlag struct {
	ID          int       `json:"id"`
	Name        string    `json:"name"`
	Description string    `json:"description,omitempty"`
	IsActive    bool      `json:"is_active"`
	Environment string    `json:"environment"`
	ProjectID   int       `json:"project_id,omitempty"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

// FeatureFlagCreate represents the data needed to create a feature flag
type FeatureFlagCreate struct {
	Name        string `json:"name"`
	Description string `json:"description,omitempty"`
	IsActive    bool   `json:"is_active"`
	Environment string `json:"environment"`
	ProjectID   int    `json:"project_id,omitempty"`
}

// FeatureFlagUpdate represents the data needed to update a feature flag
type FeatureFlagUpdate struct {
	Name        string `json:"name,omitempty"`
	Description string `json:"description,omitempty"`
	IsActive    bool   `json:"is_active,omitempty"`
	Environment string `json:"environment,omitempty"`
	ProjectID   int    `json:"project_id,omitempty"`
}

// APIError represents an API error response
type APIError struct {
	Message string `json:"message"`
	Code    string `json:"code"`
	Details any    `json:"details,omitempty"`
}

func (e APIError) Error() string {
	return fmt.Sprintf("API error: %s (code: %s)", e.Message, e.Code)
}

// ListFeatureFlags retrieves a list of feature flags
func (c *Client) ListFeatureFlags(ctx context.Context, params map[string]string) ([]FeatureFlag, error) {
	respBody, err := c.doRequest(ctx, request{
		method: "GET",
		path:   "/api/v1/feature-flags/",
		query:  params,
	})
	if err != nil {
		return nil, err
	}

	var flags []FeatureFlag
	if err := json.Unmarshal(respBody, &flags); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %w", err)
	}
	return flags, nil
}

// CreateFeatureFlag creates a new feature flag
func (c *Client) CreateFeatureFlag(ctx context.Context, flag FeatureFlagCreate) (*FeatureFlag, error) {
	respBody, err := c.doRequest(ctx, request{
		method: "POST",
		path:   "/api/v1/feature-flags/",
		body:   flag,
	})
	if err != nil {
		return nil, err
	}

	var createdFlag FeatureFlag
	if err := json.Unmarshal(respBody, &createdFlag); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %w", err)
	}
	return &createdFlag, nil
}

// GetFeatureFlag retrieves a feature flag by ID
func (c *Client) GetFeatureFlag(ctx context.Context, id int) (*FeatureFlag, error) {
	respBody, err := c.doRequest(ctx, request{
		method: "GET",
		path:   fmt.Sprintf("/api/v1/feature-flags/%d", id),
	})
	if err != nil {
		return nil, err
	}

	var flag FeatureFlag
	if err := json.Unmarshal(respBody, &flag); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %w", err)
	}
	return &flag, nil
}

// UpdateFeatureFlag updates a feature flag
func (c *Client) UpdateFeatureFlag(ctx context.Context, id int, flag FeatureFlagUpdate) (*FeatureFlag, error) {
	respBody, err := c.doRequest(ctx, request{
		method: "PUT",
		path:   fmt.Sprintf("/api/v1/feature-flags/%d", id),
		body:   flag,
	})
	if err != nil {
		return nil, err
	}

	var updatedFlag FeatureFlag
	if err := json.Unmarshal(respBody, &updatedFlag); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %w", err)
	}
	return &updatedFlag, nil
}

// DeleteFeatureFlag deletes a feature flag
func (c *Client) DeleteFeatureFlag(ctx context.Context, id int) (*FeatureFlag, error) {
	respBody, err := c.doRequest(ctx, request{
		method: "DELETE",
		path:   fmt.Sprintf("/api/v1/feature-flags/%d", id),
	})
	if err != nil {
		return nil, err
	}

	var deletedFlag FeatureFlag
	if err := json.Unmarshal(respBody, &deletedFlag); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %w", err)
	}
	return &deletedFlag, nil
}

// ToggleFeatureFlag toggles a feature flag's active status
func (c *Client) ToggleFeatureFlag(ctx context.Context, id int) (*FeatureFlag, error) {
	respBody, err := c.doRequest(ctx, request{
		method: "POST",
		path:   fmt.Sprintf("/api/v1/feature-flags/%d/toggle", id),
	})
	if err != nil {
		return nil, err
	}

	var toggledFlag FeatureFlag
	if err := json.Unmarshal(respBody, &toggledFlag); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %w", err)
	}
	return &toggledFlag, nil
}

// AddWebhook adds a webhook URL
func (c *Client) AddWebhook(ctx context.Context, url string) error {
	_, err := c.doRequest(ctx, request{
		method: "POST",
		path:   fmt.Sprintf("/api/v1/feature-flags/webhooks/%s", url),
	})
	return err
}

// RemoveWebhook removes a webhook URL
func (c *Client) RemoveWebhook(ctx context.Context, url string) error {
	_, err := c.doRequest(ctx, request{
		method: "DELETE",
		path:   fmt.Sprintf("/api/v1/feature-flags/webhooks/%s", url),
	})
	return err
} 