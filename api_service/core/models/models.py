from schemas.annotations.activity import activity_annotation
from sqlalchemy.dialects.postgresql import (
    JSONB,
)
from models.base import Base
from sqlalchemy import (
    String,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from schemas.sqlalchemy_templates.point_template import PointType


class OrganizationBase(Base):
    __tablename__ = "organization"

    name: Mapped[str] = mapped_column(String(255))
    building_id: Mapped[int | None] = mapped_column(ForeignKey("building.id"), nullable = True)
    activity: Mapped[activity_annotation] = mapped_column(JSONB, nullable = True)
    description: Mapped[str | None] = mapped_column(String(1000), nullable = True)

    phone_numbers: Mapped[list["PhoneNumberBase"]] = relationship(back_populates = "org", cascade="all, delete-orphan")
    building: Mapped["BuildingBase"] = relationship(back_populates = "orgs")


class PhoneNumberBase(Base):
    __tablename__ = "phone_number"

    phone_number: Mapped[str] = mapped_column(String(20))
    org_id: Mapped[int | None] = mapped_column(ForeignKey("organization.id", ondelete="CASCADE"), nullable = True)

    org: Mapped["OrganizationBase"] = relationship(back_populates = "phone_numbers")
     

class BuildingBase(Base):
    __tablename__ = "building"

    address: Mapped[str] = mapped_column()
    place_on_the_map: Mapped[tuple[float, float]] = mapped_column(PointType, nullable = False)

    orgs: Mapped[list["OrganizationBase"]] = relationship(back_populates = "building")
