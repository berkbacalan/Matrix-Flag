from typing import List, Optional, Dict, Any
import httpx
from pydantic import BaseModel

class FeatureFlag(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    environment: str
    project_id: Optional[int] = None
    created_at: str
    updated_at: str

class FeatureFlagCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    environment: str
    project_id: Optional[int] = None

class FeatureFlagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    environment: Optional[str] = None
    project_id: Optional[int] = None

class MatrixFlagClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30
    ):
        """
        Initialize the Matrix Flag client.
        
        Args:
            base_url: Base URL of the Matrix Flag API
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=timeout
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def list_feature_flags(
        self,
        skip: int = 0,
        limit: int = 100,
        project_id: Optional[int] = None,
        environment: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[FeatureFlag]:
        """
        List feature flags with optional filtering.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            project_id: Filter by project ID
            environment: Filter by environment
            is_active: Filter by active status
            
        Returns:
            List of feature flags
        """
        params = {
            "skip": skip,
            "limit": limit
        }
        if project_id is not None:
            params["project_id"] = project_id
        if environment is not None:
            params["environment"] = environment
        if is_active is not None:
            params["is_active"] = is_active

        response = await self.client.get("/api/v1/feature-flags/", params=params)
        response.raise_for_status()
        return [FeatureFlag(**item) for item in response.json()]

    async def create_feature_flag(self, flag: FeatureFlagCreate) -> FeatureFlag:
        """
        Create a new feature flag.
        
        Args:
            flag: Feature flag data
            
        Returns:
            Created feature flag
        """
        response = await self.client.post(
            "/api/v1/feature-flags/",
            json=flag.dict(exclude_none=True)
        )
        response.raise_for_status()
        return FeatureFlag(**response.json())

    async def get_feature_flag(self, feature_flag_id: int) -> FeatureFlag:
        """
        Get a feature flag by ID.
        
        Args:
            feature_flag_id: ID of the feature flag
            
        Returns:
            Feature flag details
        """
        response = await self.client.get(f"/api/v1/feature-flags/{feature_flag_id}")
        response.raise_for_status()
        return FeatureFlag(**response.json())

    async def update_feature_flag(
        self,
        feature_flag_id: int,
        flag: FeatureFlagUpdate
    ) -> FeatureFlag:
        """
        Update a feature flag.
        
        Args:
            feature_flag_id: ID of the feature flag to update
            flag: Updated feature flag data
            
        Returns:
            Updated feature flag
        """
        response = await self.client.put(
            f"/api/v1/feature-flags/{feature_flag_id}",
            json=flag.dict(exclude_none=True)
        )
        response.raise_for_status()
        return FeatureFlag(**response.json())

    async def delete_feature_flag(self, feature_flag_id: int) -> FeatureFlag:
        """
        Delete a feature flag.
        
        Args:
            feature_flag_id: ID of the feature flag to delete
            
        Returns:
            Deleted feature flag
        """
        response = await self.client.delete(f"/api/v1/feature-flags/{feature_flag_id}")
        response.raise_for_status()
        return FeatureFlag(**response.json())

    async def toggle_feature_flag(self, feature_flag_id: int) -> FeatureFlag:
        """
        Toggle a feature flag's active status.
        
        Args:
            feature_flag_id: ID of the feature flag to toggle
            
        Returns:
            Updated feature flag
        """
        response = await self.client.post(f"/api/v1/feature-flags/{feature_flag_id}/toggle")
        response.raise_for_status()
        return FeatureFlag(**response.json()) 