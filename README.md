# Matrix Flag - Feature Flag & Remote Config Service

A self-hosted, production-ready feature flag and remote configuration service built with FastAPI and Redis. Matrix Flag enables teams to manage feature releases, conduct A/B testing, and control application behavior in real-time without deploying new code.

## 🎯 Business Value

### Why Matrix Flag?

1. **Cost-Effective Solution**
   - No recurring SaaS subscription fees
   - Self-hosted, giving you complete control over your data
   - Minimal infrastructure requirements

2. **Risk Mitigation**
   - Gradual feature rollouts
   - Instant feature toggling in case of issues
   - Controlled A/B testing capabilities

3. **Development Efficiency**
   - Faster development cycles
   - Reduced deployment risks
   - Simplified feature management
   - Real-time configuration changes

4. **Business Agility**
   - Quick response to market changes
   - Targeted feature releases
   - Data-driven decision making
   - Flexible user segmentation

### Use Cases

1. **Feature Management**
   - Gradual feature rollouts
   - Feature toggling for maintenance
   - Emergency feature disabling
   - Feature experimentation

2. **A/B Testing**
   - User experience testing
   - Pricing strategy testing
   - Content optimization
   - Performance testing

3. **Configuration Management**
   - Dynamic application settings
   - Environment-specific configurations
   - User-specific settings
   - Service configuration

4. **Release Management**
   - Canary releases
   - Blue-green deployments
   - Dark launches
   - Feature flags for CI/CD

## 🚀 Technical Features

- **High Performance**
  - FastAPI for high-speed API responses
  - Redis for sub-millisecond data access
  - Async/await for optimal resource utilization
  - Connection pooling for efficient database access

- **Scalability**
  - Horizontal scaling support
  - Redis clustering ready
  - Stateless architecture
  - Load balancing friendly

- **Reliability**
  - Real-time updates
  - Webhook notifications
  - Audit logging
  - Error handling and recovery

- **Security**
  - Type-safe with Pydantic
  - Input validation
  - CORS configuration
  - Environment variable management

## 🛠️ Technical Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: Redis 7+
- **Container**: Docker & Docker Compose
- **API Documentation**: OpenAPI (Swagger/ReDoc)
- **Testing**: Pytest
- **Monitoring**: Built-in health checks

## 📦 Installation

### Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/yourusername/matrix-flag.git
cd matrix-flag
```

2. Start the service:
```bash
docker-compose up -d
```

The service will be available at `http://localhost:8000`

### Manual Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn app.main:app --reload
```

## 📚 API Documentation

Access the interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Core Endpoints

#### Feature Flags
- `POST /api/v1/flags/` - Create a new feature flag
- `GET /api/v1/flags/{key}` - Get a specific feature flag
- `PUT /api/v1/flags/{key}` - Update a feature flag
- `DELETE /api/v1/flags/{key}` - Delete a feature flag
- `GET /api/v1/flags/` - List all feature flags

#### Webhooks
- `POST /api/v1/flags/webhooks/{url}` - Add a webhook URL
- `DELETE /api/v1/flags/webhooks/{url}` - Remove a webhook URL

## 💡 Usage Examples

### Python Client Example

```python
import requests

# Create a feature flag
response = requests.post(
    "http://localhost:8000/api/v1/flags/",
    json={
        "key": "new-feature",
        "name": "New Feature",
        "description": "Enable the new feature",
        "type": "boolean",
        "value": True,
        "enabled": True
    }
)

# Check feature flag status
response = requests.get("http://localhost:8000/api/v1/flags/new-feature")
flag = response.json()
if flag["enabled"] and flag["value"]:
    # Feature is enabled
    pass
```

### JavaScript Client Example

```javascript
// Create a feature flag
await fetch('http://localhost:8000/api/v1/flags/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        key: 'new-feature',
        name: 'New Feature',
        description: 'Enable the new feature',
        type: 'boolean',
        value: true,
        enabled: true
    })
});

// Check feature flag status
const response = await fetch('http://localhost:8000/api/v1/flags/new-feature');
const flag = await response.json();
if (flag.enabled && flag.value) {
    // Feature is enabled
}
```

## 🔧 Configuration

### Environment Variables

- `REDIS_URL`: Redis connection URL (default: redis://localhost:6379)
- `SECRET_KEY`: Application secret key
- `WEBHOOK_TIMEOUT`: Webhook request timeout in seconds (default: 5)

### Redis Configuration

The service uses Redis for:
- Feature flag storage
- Webhook URL management
- Real-time updates
- Caching

## 📈 Performance Considerations

- **Caching**: Redis provides sub-millisecond response times
- **Connection Pooling**: Efficient database connection management
- **Async Operations**: Non-blocking I/O operations
- **Horizontal Scaling**: Support for multiple instances

## 🔍 Monitoring

- Health check endpoint: `GET /health`
- Webhook delivery status logging
- Redis connection status monitoring
- API response time tracking

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 📞 Support

For support, please:
1. Check the documentation
2. Open an issue on GitHub
3. Contact the maintainers

## 🗺️ Roadmap

### ✅ Completed Features
- [x] User Authentication and Authorization
  - JWT-based authentication
  - Role-based access control (Admin, Manager, Viewer)
  - Secure password hashing
  - User management API
  - Session management
- [x] Advanced Targeting Rules
  - User segmentation
  - Percentage-based rollout
  - Time-based rules
  - Custom attribute support
  - A/B testing capabilities
- [x] Analytics Dashboard
  - Metric management and monitoring
  - Customizable dashboards
  - Reporting and analysis
  - Real-time data visualization
  - Performance metrics
- [x] Monitoring & Observability
  - Prometheus integration
  - Grafana dashboards
  - HTTP request metrics
  - User operation metrics
  - Redis operation metrics
  - System metrics (CPU, Memory)
  - Real-time monitoring
  - Custom dashboards

### 🚧 In Progress
- [ ] Enhanced Security
  - Two-factor authentication
  - API key management
  - IP-based access control
  - Security audit logs

### 📅 Upcoming Features
- [ ] SDK Development
  - Python SDK
  - JavaScript SDK
  - Java SDK
  - Go SDK
- [ ] CI/CD Integration
  - GitHub Actions integration
  - GitLab CI integration
  - Jenkins integration
- [ ] Advanced Management Features
  - Bulk operations
  - Import/export
  - Backup and restore
- [ ] Monitoring & Observability
  - Prometheus integration
  - Grafana dashboards
  - Alert system
- [ ] Developer Experience
  - API documentation
  - Sample applications
  - Testing tools
- [ ] Enterprise Features
  - SSO integration
  - LDAP/Active Directory support
  - Audit logging
- [ ] Multi-region Support
  - Geographic replication
  - Local data storage
  - Low latency

### 🔮 Future Considerations
- [ ] Machine Learning Integration
  - Automatic feature optimization
  - User behavior analysis
  - Anomaly detection
- [ ] Advanced Testing Features
  - Canary deployments
  - Blue/Green deployments
  - Chaos testing
- [ ] Community Features
  - Feature templates
  - Shared dashboards
  - User feedback

## 🎨 Modern and User-Friendly Interface

Matrix Flag offers a modern and user-friendly interface for managing feature flags and remote configurations.

## 📊 Prometheus and Grafana Monitoring

The service integrates with Prometheus and Grafana for monitoring and metrics collection.

### Monitoring Metrics

The service collects and tracks the following metrics:

#### HTTP Metrics
- `http_requests_total`: Total HTTP request count
- `http_request_duration_seconds`: HTTP request duration

#### User Metrics
- `user_operations_total`: User operation count (create, update, delete)
- `user_login_attempts_total`: Login attempt count
- `active_users_total`: Active user count

#### Redis Metrics
- `redis_operations_total`: Redis operation count
- `redis_operation_duration_seconds`: Redis operation duration

#### System Metrics
- `system_memory_usage_bytes`: Memory usage
- `system_cpu_usage_percent`: CPU usage

### Monitoring Tools

1. Prometheus:
   - Access Prometheus metrics by navigating to `http://localhost:9090`
   - Use the "Graph" tab to query metrics
   - Enter metric name (e.g., `user_operations_total`)
   - Click "Execute"

2. Grafana:
   - Access Grafana by navigating to `http://localhost:3000`
   - Login with username: admin, password: admin
   - Add Prometheus as a data source (URL: http://prometheus:9090)
   - Create new dashboards

### Monitoring Features

- Health check endpoint: `GET /health`
- Webhook delivery status logging
- Redis connection status monitoring
- API response time tracking

## 🔄 Webhook Integration

Matrix Flag supports webhook notifications for real-time updates and integrations.

### Webhook Usage

1. **Creating a Webhook**:
   - Use the `POST /api/v1/flags/webhooks/{url}` endpoint to add a new webhook URL.
   - The webhook URL should be a valid HTTP or HTTPS endpoint.

2. **Removing a Webhook**:
   - Use the `DELETE /api/v1/flags/webhooks/{url}` endpoint to remove an existing webhook URL.

## 🎨 Modern and User-Friendly Interface

Matrix Flag offers a modern and user-friendly interface for managing feature flags and remote configurations.

## 📊 Prometheus and Grafana Monitoring

The service integrates with Prometheus and Grafana for monitoring and metrics collection.

### Monitoring Metrics

The service collects and tracks the following metrics:

#### HTTP Metrics
- `http_requests_total`: Total HTTP request count
- `http_request_duration_seconds`: HTTP request duration

#### User Metrics
- `user_operations_total`: User operation count (create, update, delete)
- `user_login_attempts_total`: Login attempt count
- `active_users_total`: Active user count

#### Redis Metrics
- `redis_operations_total`: Redis operation count
- `redis_operation_duration_seconds`: Redis operation duration

#### Sistem Metrikleri
- `system_memory_usage_bytes`: Bellek kullanımı
- `system_cpu_usage_percent`: CPU kullanımı

### Monitoring Tools

1. Prometheus:
   - Access Prometheus metrics by navigating to `http://localhost:9090`
   - Use the "Graph" tab to query metrics
   - Enter metric name (örn: `user_operations_total`)
   - Click "Execute"

2. Grafana:
   - Access Grafana by navigating to `http://localhost:3000`
   - Login with username: admin, Şifre: admin
   - Prometheus veri kaynağını ekleyin (URL: http://prometheus:9090)
   - Yeni dashboard'lar oluşturun

### Monitoring Features

- Health check endpoint: `GET /health`
- Webhook delivery status logging
- Redis connection status monitoring
- API response time tracking

## 🔄 Webhook Integration

Matrix Flag supports webhook notifications for real-time updates and integrations.

### Webhook Usage

1. **Creating a Webhook**:
   - Use the `POST /api/v1/flags/webhooks/{url}` endpoint to add a new webhook URL.
   - The webhook URL should be a valid HTTP or HTTPS endpoint.

2. **Removing a Webhook**:
   - Use the `DELETE /api/v1/flags/webhooks/{url}` endpoint to remove an existing webhook URL.

## 🎨 Modern and User-Friendly Interface

Matrix Flag offers a modern and user-friendly interface for managing feature flags and remote configurations.

## 📊 Prometheus and Grafana Monitoring

The service integrates with Prometheus and Grafana for monitoring and metrics collection.

### Monitoring Metrics

The service collects and tracks the following metrics:

#### HTTP Metrics
- `http_requests_total`: Total HTTP request count
- `http_request_duration_seconds`: HTTP request duration

#### User Metrics
- `user_operations_total`: User operation count (create, update, delete)
- `user_login_attempts_total`: Login attempt count
- `active_users_total`: Active user count

#### Redis Metrics
- `redis_operations_total`: Redis operation count
- `redis_operation_duration_seconds`: Redis operation duration

#### Sistem Metrikleri
- `system_memory_usage_bytes`: Bellek kullanımı
- `system_cpu_usage_percent`: CPU kullanımı

### Monitoring Tools

1. Prometheus:
   - Access Prometheus metrics by navigating to `http://localhost:9090`
   - Use the "Graph" tab to query metrics
   - Enter metric name (örn: `user_operations_total`)
   - Click "Execute"

2. Grafana:
   - Access Grafana by navigating to `http://localhost:3000`
   - Login with username: admin, Şifre: admin
   - Prometheus veri kaynağını ekleyin (URL: http://prometheus:9090)
   - Yeni dashboard'lar oluşturun

### Monitoring Features

- Health check endpoint: `GET /health`
- Webhook delivery status logging
- Redis connection status monitoring
- API response time tracking

## 🔄 Webhook Integration

Matrix Flag supports webhook notifications for real-time updates and integrations.

### Webhook Usage

1. **Creating a Webhook**:
   - Use the `POST /api/v1/flags/webhooks/{url}` endpoint to add a new webhook URL.
   - The webhook URL should be a valid HTTP or HTTPS endpoint.

2. **Removing a Webhook**:
   - Use the `DELETE /api/v1/flags/webhooks/{url}` endpoint to remove an existing webhook URL. 