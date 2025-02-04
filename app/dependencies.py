from typing import Any
from .internal.exceptions import NumberException
from fastapi import status


class NumberValidator:
    def __call__(self, number: Any = None) -> int:
        try:
            int(number)
            return number
        except:
            raise NumberException(
                detail=number, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
            )


number_validator = NumberValidator()
