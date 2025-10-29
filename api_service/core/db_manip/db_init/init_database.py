from settings.database_settings import async_session
from db_manip.raw_data.insert_data import (
    phone_numbers,
    buildings,
    organizations
)
from sqlalchemy.dialects.postgresql import insert
# from sqlalchemy import insert
from models.models import (
    PhoneNumberBase,
    BuildingBase,
    OrganizationBase
)
import asyncio


async def database_init():
    async with async_session() as session:
        stmt = (
            insert(
                PhoneNumberBase
            )
            .values(
                phone_numbers
            )
        ).on_conflict_do_nothing(index_elements=['id'])
        stmt1 = (
            insert(
                BuildingBase
            )
            .values(
                buildings
            )
        ).on_conflict_do_nothing(index_elements=['id'])
        stmt2 = (
            insert(
                OrganizationBase
            )
            .values(
                organizations
            )
        ).on_conflict_do_nothing(index_elements=['id'])

        await session.execute(stmt1)
        await session.commit()

        await session.execute(stmt2)
        await session.commit()

        await session.execute(stmt)
        await session.commit()




if __name__ == "__main__":
    asyncio.run(
        database_init()
    )