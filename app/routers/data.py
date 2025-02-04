from ..internal.models import ResponseDataModel
from ..internal.dependencies import number_validator
from ..internal.numbers import NumberUtils
from ..internal.cache import CustomCache
from ..internal.config import settings

from fastapi import APIRouter, status, Depends
from typing import Annotated


router = APIRouter()

number_cache = CustomCache(expiry_seconds=settings.cache_expiry, max_size=settings.cache_max_size)

@router.get("/classify-number", status_code=status.HTTP_200_OK, response_model=ResponseDataModel, name="data")
@number_cache
async def number_data(number: Annotated[int, Depends(number_validator)]):
    response_data = await NumberUtils(number=number).check_all()
    return response_data
