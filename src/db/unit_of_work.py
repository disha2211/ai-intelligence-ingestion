from src.db.database import (
    AsyncSessionLocal,
)


class DatabaseSession:

    async def __aenter__(self):

        self.session = (
            AsyncSessionLocal()
        )

        return self.session

    async def __aexit__(
        self,
        exc_type,
        exc,
        traceback,
    ):

        if exc_type:

            await self.session.rollback()

        else:

            await self.session.commit()

        await self.session.close()

