# Matrix Flag Python SDK

This SDK provides a Python client for interacting with the Matrix Flag API.

## Installation

```bash
pip install matrix-flag
```

## Quick Start

```python
import asyncio
from matrix_flag.client import MatrixFlagClient, FeatureFlagCreate

async def main():
    async with MatrixFlagClient(
        base_url="http://localhost:8000",
        api_key="your-api-key"
    ) as client:
        new_flag = await client.create_feature_flag(
            FeatureFlagCreate(
                name="new-feature",
                description="Enable new feature",
                is_active=True,
                environment="production"
            )
        )
        print(f"Created feature flag: {new_flag}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Features

- Full API coverage
- Type hints and validation
- Async/await support
- Context manager support
- Error handling
- Pagination support

## API Reference

### MatrixFlagClient

The main client class for interacting with the Matrix Flag API.

```python
client = MatrixFlagClient(
    base_url="http://localhost:8000",
    api_key="your-api-key",
    timeout=30  # optional, defaults to 30 seconds
)
```

### Methods

#### list_feature_flags

List feature flags with optional filtering.

```python
flags = await client.list_feature_flags(
    skip=0,
    limit=100,
    project_id=None,
    environment=None,
    is_active=None
)
```

#### create_feature_flag

Create a new feature flag.

```python
new_flag = await client.create_feature_flag(
    FeatureFlagCreate(
        name="new-feature",
        description="Enable new feature",
        is_active=True,
        environment="production"
    )
)
```

#### get_feature_flag

Get a feature flag by ID.

```python
flag = await client.get_feature_flag(feature_flag_id=1)
```

#### update_feature_flag

Update a feature flag.

```python
updated_flag = await client.update_feature_flag(
    feature_flag_id=1,
    flag=FeatureFlagUpdate(
        description="Updated description",
        is_active=False
    )
)
```

#### delete_feature_flag

Delete a feature flag.

```python
deleted_flag = await client.delete_feature_flag(feature_flag_id=1)
```

#### toggle_feature_flag

Toggle a feature flag's active status.

```python
toggled_flag = await client.toggle_feature_flag(feature_flag_id=1)
```

## Models

### FeatureFlag

```python
class FeatureFlag(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    environment: str
    project_id: Optional[int] = None
    created_at: str
    updated_at: str
```

### FeatureFlagCreate

```python
class FeatureFlagCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    environment: str
    project_id: Optional[int] = None
```

### FeatureFlagUpdate

```python
class FeatureFlagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    environment: Optional[str] = None
    project_id: Optional[int] = None
```

## Error Handling

The SDK raises exceptions for HTTP errors:

```python
try:
    flag = await client.get_feature_flag(feature_flag_id=999)
except httpx.HTTPStatusError as e:
    if e.response.status_code == 404:
        print("Feature flag not found")
    else:
        print(f"HTTP error: {e}")
```

## Best Practices

1. Always use the context manager to ensure proper cleanup:
   ```python
   async with MatrixFlagClient(...) as client:
       # use client
   ```

2. Handle errors appropriately:
   ```python
   try:
       flag = await client.get_feature_flag(feature_flag_id=1)
   except httpx.HTTPStatusError as e:
       # handle error
   ```

3. Use type hints for better IDE support:
   ```python
   from typing import List
   from matrix_flag.client import FeatureFlag

   async def get_active_flags() -> List[FeatureFlag]:
       return await client.list_feature_flags(is_active=True)
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 