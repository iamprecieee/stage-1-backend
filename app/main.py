from .internal.exceptions import NumberException
from .internal.models import InvalidResponseModel
from .routers.data import router
from .internal.middleware import middleware

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


app = FastAPI(docs_url="/", middleware=middleware)

@app.exception_handler(NumberException)
async def number_type_exception_handler(request: Request, exc: NumberException) -> JSONResponse:
    error_response = InvalidResponseModel(number=exc.detail, error=True)
    return JSONResponse(
        status_code=exc.status_code, content=error_response.model_dump()
    )

app.include_router(router, prefix="/api")