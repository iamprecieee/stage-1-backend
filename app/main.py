from fastapi import FastAPI, Request
from .internal.exceptions import NumberException
from .internal.models import InvalidResponseModel
from fastapi.responses import JSONResponse
from .routers.data import router


app = FastAPI()


@app.exception_handler(NumberException)
async def number_type_exception_handler(request: Request, exc: NumberException):
    error_response = InvalidResponseModel(number=exc.detail, error=True)
    return JSONResponse(
        status_code=exc.status_code, content=error_response.model_dump()
    )


app.include_router(router, prefix="/api")
