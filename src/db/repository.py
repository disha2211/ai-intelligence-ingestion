from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Entity


class EntityRepository:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def get_by_url(
        self,
        entity_type: str,
        url: str,
    ) -> Entity | None:

        result = await self.session.execute(
            select(Entity).where(
                Entity.entity_type == entity_type,
                Entity.url == url,
            )
        )

        return result.scalar_one_or_none()

    async def upsert(
        self,
        *,
        entity_type: str,
        name: str,
        description: str | None,
        url: str,
        source: str,
        metadata: dict,
    ) -> Entity:

        existing = await self.get_by_url(
            entity_type,
            url,
        )

        if existing:

            existing.name = name
            existing.description = description
            existing.source = source
            existing.extra_metadata = metadata
            existing.updated_at = (
                datetime.now(timezone.utc)
            )

            await self.session.flush()

            return existing

        entity = Entity(
    entity_type=entity_type,
    name=name,
    description=description,
    url=url,
    source=source,
    extra_metadata=metadata,
)

        self.session.add(entity)

        await self.session.flush()

        return entity