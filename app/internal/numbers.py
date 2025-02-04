from .models import NumbersAPIModel
from .exceptions import NumberException
from .config import settings

import httpx
from fastapi import status


class NumberUtils:
    def __init__(self, number: int) -> None:
        self.number= int(number)
        self.properties_list: list[str | None] = []

    def check_prime(self) -> bool:
        if self.number > 1:
            if self.number == 2:
                return True
            if self.number % 2 == 0:
                return False
            for i in range(3, int(self.number**0.5) + 1, 2):
                if self.number % i == 0:
                    return False
            return True
        return False
    
    def check_perfect(self) -> bool:
        if self.number > 0:
            divisor_sum = 0
            for i in range(1, self.number):
                if self.number % i == 0:
                    divisor_sum += i
            if divisor_sum == self.number:
                return True
        return False

    def check_armstrong(self) -> None:
        if self.number >= 0:
            digit_sum = sum(int(digit) ** len(str(self.number)) for digit in str(self.number))
            if digit_sum == self.number:
                self.properties_list.append("armstrong")

    def check_parity(self) -> None:
        (
            self.properties_list.append("even")
            if self.number % 2 == 0
            else self.properties_list.append("odd")
        )
        
    def get_digit_sum(self) -> int:
        number_str = str(self.number)
        if number_str.startswith("-"):
            return -int(number_str[1]) + (sum(int(digit) for digit in number_str[2:]))
        return sum((int(digit) for digit in number_str))
    
    async def get_fun_fact(self) -> NumbersAPIModel:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=f"{settings.numbers_api_base_url}/{self.number}/math?json",
                    timeout=settings.numbers_api_timeout,
                )
                response.raise_for_status()
                return NumbersAPIModel(**response.json())
        except (httpx.ReadTimeout, httpx.PoolTimeout, httpx.ConnectTimeout) as e:
            raise NumberException(
                detail="Numbers API timed out",
                status_code=status.HTTP_408_REQUEST_TIMEOUT,
            )
        except httpx.HTTPStatusError as e:
            raise NumberException(
                detail=f"Numbers API error: {e.response.text}",
                status_code=e.response.status_code,
            )

    async def check_all(self) -> dict:
        fun_fact = await self.get_fun_fact()
        is_prime = self.check_prime()
        is_perfect = self.check_perfect()
        self.check_armstrong()
        self.check_parity()
        digit_sum = self.get_digit_sum()
        response_dict = {
            "number": self.number,
            "is_prime": is_prime,
            "is_perfect": is_perfect,
            "properties": self.properties_list,
            "digit_sum": digit_sum,
            "fun_fact": fun_fact.text,
        }
        return response_dict
