from schemas.pydantic_schemas.orgs_schemas import (
    OrganizationsTemplate,
    BuildingTemplate,
    OrganizationTemplateExtended,
    BuildingTemplateExtended
)
from utils.async_requests.async_requests import AsyncRequests
from fastapi import (
    APIRouter,
    Path,
    Query,
    HTTPException
)


org_router = APIRouter(prefix = "/api/v1") 


# organizations in building
@org_router.get("/orgs/building/{building_id}", response_model = list[OrganizationsTemplate]) 
async def get_orgs_in_building(
    building_id: int = Path(ge=1)
):
    building_with_orgs = await AsyncRequests.get_organizations_by_building_id(building_id)

    if building_with_orgs:
        return building_with_orgs.orgs
    else:
        raise HTTPException(
            status_code = 404,
            detail = "No building was found for this id."
        )
    

# organization by id
@org_router.get("/orgs/{organization_id}", response_model = OrganizationTemplateExtended)
async def oganization_by_id(
    organization_id: int
):
    organization = await AsyncRequests.get_org_by_id(organization_id)
    if organization:
        return organization
    else:
        raise HTTPException(
            status_code=404,
            detail = "No organization was found by this id."
        )


# organizations by name
@org_router.get("/orgs/name/{org_name}", response_model = OrganizationTemplateExtended)
async def get_org_by_name(
    org_name: str
):
    org = await AsyncRequests.get_org_by_name(org_name)
    if org:
        return org
    else:
        raise HTTPException(
            status_code = 404,
            detail = "No organization with this name was found."
        )



# organizations by activity
@org_router.get("/orgs/specified", response_model = list[OrganizationsTemplate])
async def list_orgs_with_specific_activity(
    request_data: list[str] = Query()
):
    orgs_list = await AsyncRequests.get_orgs_by_activity(request_data)

    if orgs_list:
        return orgs_list
    else:
        raise HTTPException(status_code = 404, detail = "Nothing was found for your request")
    
    
# get buildings in cicle area
@org_router.get("/orgs/in_area/circle", response_model = list[BuildingTemplateExtended])
async def get_org_in_radius(
    center_coords: tuple[float, float] = Query(),
    radius: float = Query()
):
    places = await AsyncRequests.get_places_in_radius(
        coords = center_coords,
        radius = radius    
    )
    if places:
        return places
    else:
        raise HTTPException(
            status_code=404,
            detail = "No organization was found in the area."
        )


# get buildings in box area
@org_router.get("/orgs/in_area/box", response_model = list[BuildingTemplateExtended])
async def get_org_in_box(
    left_btm_corner: tuple[float, float] = Query(),
    right_top_corner: tuple[float, float] = Query()
):
    places = await AsyncRequests.get_places_in_box(
        left_btm_corner = left_btm_corner,
        right_top_corner = right_top_corner    
    )
    if places:
        return places
    else:
        raise HTTPException(
            status_code=404,
            detail = "No organization was found in the area."
        )










































































# @org_router.get("orgs/{org_name}", response_model = ...)
# async def get_org_by_name(
#     org_name: str
# ):
#     org = await AsyncRequests.get_org_by_name(org_name)
    
#     return org