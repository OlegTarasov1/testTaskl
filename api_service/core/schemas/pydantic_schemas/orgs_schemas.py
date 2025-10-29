from schemas.annotations.activity import activity_annotation
from pydantic import BaseModel


class PhoneNumberTemplate(BaseModel):
    id: int
    phone_number: str | None
    org_id: int

class OrganizationsTemplate(BaseModel):
    
    id: int
    name: str
    building_id: int | None
    activity: activity_annotation | None
    description: str | None
    phone_numbers: list[PhoneNumberTemplate] | None


class BuildingTemplate(BaseModel):
    id: int
    address: str
    place_on_the_map: tuple[float, float]


class BuildingTemplateExtended(
    BuildingTemplate,
    BaseModel
):
    orgs: list[OrganizationsTemplate] | None



class OrganizationTemplateExtended(
    OrganizationsTemplate,
    BaseModel
):
    building: BuildingTemplate



