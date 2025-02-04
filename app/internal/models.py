from pydantic import BaseModel


class NumbersAPIModel(BaseModel):
    text: str
    
    
class ResponseDataModel(BaseModel):
    number: int
    is_prime: bool
    is_perfect: bool
    properties: list[str]
    digit_sum: int
    fun_fact: str
    
    
class InvalidResponseModel(BaseModel):
    number: str
    error: bool