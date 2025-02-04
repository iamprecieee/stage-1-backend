from pydantic import BaseModel


class NumbersAPIModel(BaseModel):
    """Defines structure for numbersapi JSON response."""

    text: str


class ResponseDataModel(BaseModel):
    """Defines structure for successful response for base api."""

    number: int
    is_prime: bool
    is_perfect: bool
    properties: list[str]
    digit_sum: int
    fun_fact: str


class InvalidResponseModel(BaseModel):
    """Defines structure for general api error response"""

    number: str
    error: bool
