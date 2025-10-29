from views.extra_handlers.health_api import health_check_router
from views.organizaions_handler.org_api import org_router
from fastapi import FastAPI
import uvicorn

app = FastAPI()


app.include_router(health_check_router)
app.include_router(org_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host = "0.0.0.0")