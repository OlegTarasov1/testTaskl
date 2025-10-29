from settings.database_settings import async_session
from sqlalchemy.orm import (
    joinedload,
    selectinload
)
from models.models import (
    BuildingBase,
    OrganizationBase
)
from sqlalchemy import (
    select,
    func,
    or_
)


class AsyncRequests:
    @staticmethod
    async def get_organizations_by_building_id(
        building_id: int
    ) -> BuildingBase | None:
        async with async_session() as session:
            stmt = (
                select(
                    BuildingBase
                )
                .where(
                    BuildingBase.id == building_id
                )
                .options(
                    joinedload(
                        BuildingBase.orgs
                    )
                        .joinedload(
                            OrganizationBase.phone_numbers
                        )
                )
            )
            building_with_orgs = await session.execute(stmt)
            building_with_orgs = building_with_orgs.unique().scalar_one_or_none()

            await session.commit()

            return building_with_orgs
        

    @staticmethod
    async def get_orgs_by_activity(
        search_data: list
    ) -> list[OrganizationBase]:
        async with async_session() as session:
            data = [OrganizationBase.activity.contains([i]) for i in search_data]
            stmt = (
                select(
                    OrganizationBase
                )
                .options(
                    joinedload(
                        OrganizationBase.phone_numbers
                    )
                )
                .where(
                    or_(
                        *data
                    )
                )
            )

            orgs = await session.execute(stmt)
            orgs = orgs.scalars().unique().all()

            return orgs
        

    @staticmethod
    async def get_org_by_name(
        org_name: str
    ) -> OrganizationBase | None:
        async with async_session() as session:
            stmt = (
                select(
                    OrganizationBase
                )
                .options(
                    joinedload(
                        OrganizationBase.building
                    ),
                    joinedload(
                        OrganizationBase.phone_numbers
                    )
                )
                .where(
                    OrganizationBase.name.ilike(org_name)
                )
            )

            org = await session.execute(stmt)
            org = org.unique().scalar_one_or_none()

            return org
        

    @staticmethod
    async def get_building_data(
        id: int
    ) -> BuildingBase | None:
        async with async_session() as session:
            stmt = (
                select(
                    BuildingBase
                )
                .where(
                    BuildingBase.id == id
                )
            )

            building = await session.execute(stmt)
            building = building.scalar_one_or_none()

            return building
        
    
    @staticmethod
    async def get_places_in_radius(
        coords: tuple[float, float],
        radius: float
    ) -> list[OrganizationBase]:
        async with async_session() as session:
            stmt = (
                select(
                    BuildingBase
                )
                .where(
                    func.circle(
                        func.point(*coords),
                        radius
                    )
                    .op("@>")
                    (
                        BuildingBase.place_on_the_map
                    )
                )
                .options(
                    selectinload(
                        BuildingBase.orgs
                    )
                        .selectinload(OrganizationBase.phone_numbers)
                )
            )

            places = await session.execute(stmt)
            places = places.unique().scalars().all()

            return places


    @staticmethod
    async def get_places_in_box(
        left_btm_corner: tuple[float, float],
        right_top_corner: tuple[float, float]
    ) -> list[BuildingBase]:
        async with async_session() as session:
            stmt = (
                select(
                    BuildingBase
                )
                .where(
                    func.box(
                        func.point(*left_btm_corner),
                        func.point(*right_top_corner)
                    )
                    .op("@>")
                    (
                        BuildingBase.place_on_the_map
                    )
                )
                .options(
                    selectinload(
                        BuildingBase.orgs
                    )
                        .selectinload(OrganizationBase.phone_numbers)
                )
            )

            buildings_with_places = await session.execute(stmt)
            buildings_with_places = buildings_with_places.unique().scalars().all()

            return buildings_with_places


    @staticmethod
    async def get_org_by_id(
        org_id: int
    ) -> OrganizationBase | None:
        async with async_session() as session:
            stmt = (
                select(
                    OrganizationBase
                )
                .options(
                    joinedload(
                        OrganizationBase.building
                    ),
                    joinedload(
                        OrganizationBase.phone_numbers
                    )
                )
                .where(
                    OrganizationBase.id == org_id
                )
            )

            org = await session.execute(stmt)
            org = org.unique().scalar_one_or_none()

            return org