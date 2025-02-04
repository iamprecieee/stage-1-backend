from .exceptions import NumberException

from typing import Any
from fastapi import status


class NumberValidator:
    async def __call__(self, number: Any = None) -> int:
        try:
            int(number)
            return number
        except:
            raise NumberException(
                detail=number, status_code=status.HTTP_400_BAD_REQUEST
            )


number_validator = NumberValidator()
