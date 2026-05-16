from qdrant_client import QdrantClient, AsyncQdrantClient


async def get_collection_data(
        async_client: AsyncQdrantClient,
        collection_name: str,
        batch_size: int = 500
):
    all_points = []
    offset = None

    while True:
        batch, next_offset = await async_client.scroll(
            collection_name=collection_name,
            limit=batch_size,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )

        all_points.extend([
            {
                "id": point.id,
                "payload": point.payload,
            }
            for point in batch
        ])

        if next_offset is None:
            break
        offset = next_offset

    return all_points
