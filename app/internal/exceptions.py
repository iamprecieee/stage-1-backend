from fastapi import HTTPException


class NumberException(HTTPException):
    def __init__(self, status_code, detail=None, headers=None) -> None:
        super().__init__(status_code, detail, headers)
