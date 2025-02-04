from .exceptions import NumberException

from typing import Any
from fastapi import status


class NumberValidator:
    """Ensures only valid integers(+ve or -ve) are accepted. Returns a HTTPException if invalid."""
    
    def __call__(self, number: Any = None) -> int:
        try:
            int(number)
            return number
        except:
            raise NumberException(
                detail=number, status_code=status.HTTP_400_BAD_REQUEST
            )


number_validator = NumberValidator()
