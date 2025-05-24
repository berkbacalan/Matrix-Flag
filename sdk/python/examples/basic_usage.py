import asyncio
from matrix_flag.client import MatrixFlagClient, FeatureFlagCreate, FeatureFlagUpdate

async def main():
    # Initialize the client
    async with MatrixFlagClient(
        base_url="http://localhost:8000",
        api_key="your-api-key"
    ) as client:
        # Create a new feature flag
        new_flag = await client.create_feature_flag(
            FeatureFlagCreate(
                name="new-feature",
                description="Enable new feature",
                is_active=True,
                environment="production"
            )
        )
        print(f"Created feature flag: {new_flag}")

        # List all feature flags
        flags = await client.list_feature_flags(
            environment="production",
            is_active=True
        )
        print(f"Found {len(flags)} active feature flags in production")

        # Get a specific feature flag
        flag = await client.get_feature_flag(new_flag.id)
        print(f"Retrieved feature flag: {flag}")

        # Update a feature flag
        updated_flag = await client.update_feature_flag(
            new_flag.id,
            FeatureFlagUpdate(
                description="Updated description",
                is_active=False
            )
        )
        print(f"Updated feature flag: {updated_flag}")

        # Toggle a feature flag
        toggled_flag = await client.toggle_feature_flag(new_flag.id)
        print(f"Toggled feature flag: {toggled_flag}")

        # Delete a feature flag
        deleted_flag = await client.delete_feature_flag(new_flag.id)
        print(f"Deleted feature flag: {deleted_flag}")

if __name__ == "__main__":
    asyncio.run(main()) 