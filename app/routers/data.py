from fastapi import APIRouter, Depends
from typing import Annotated
from ..dependencies import number_validator
from ..internal.numbers import NumberUtils
from ..internal.models import ResponseDataModel


router = APIRouter()


@router.get("/classify-number", status_code=200, response_model=ResponseDataModel)
async def number_data(number: Annotated[int, Depends(number_validator)]):
    data = await NumberUtils(number=number).check_all()
    return data
