import httpx
from .models import NumbersAPIModel
from .exceptions import NumberException
from fastapi import status


class NumberUtils:
    def __init__(self, number: int):
        self.number: int = int(number)
        self.properties_list: list[str | None] = []

    async def get_fun_fact(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=f"http://numbersapi.com/{self.number}/math?json",
                    timeout=10,
                )
                response.raise_for_status()
                return NumbersAPIModel(**response.json()).model_dump()["text"]
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

    async def check_prime(self):
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

    async def check_perfect(self):
        if self.number > 0:
            divisor_sum = 0
            for i in range(1, self.number):
                if self.number % i == 0:
                    divisor_sum += i
            if divisor_sum == self.number:
                return True
        return False

    async def check_armstrong(self):
        if self.number >= 0:
            if sum(int(digit) ** len(str(self.number)) for digit in str(self.number)):
                self.properties_list.append("armstrong")

    async def check_parity(self):
        (
            self.properties_list.append("even")
            if self.number % 2 == 0
            else self.properties_list.append("odd")
        )

    async def get_digit_sum(self):
        number_str = str(self.number)
        if number_str.startswith("-"):
            return -int(number_str[1]) + (sum(int(digit) for digit in number_str[2:]))
        return sum((int(digit) for digit in number_str))

    async def check_all(self):
        fun_fact = await self.get_fun_fact()
        is_prime = await self.check_prime()
        is_perfect = await self.check_perfect()
        await self.check_parity()
        await self.check_armstrong()
        digit_sum = await self.get_digit_sum()
        response_dict = {
            "number": self.number,
            "fun_fact": fun_fact,
            "is_prime": is_prime,
            "is_perfect": is_perfect,
            "properties": self.properties_list,
            "digit_sum": digit_sum,
        }
        return response_dict
