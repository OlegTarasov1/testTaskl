from fastapi import APIRouter


health_check_router = APIRouter(prefix = "/api/v1") 

@health_check_router.get("/health")
async def health_check():
    return "Healthy"