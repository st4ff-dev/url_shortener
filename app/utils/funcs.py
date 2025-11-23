from random import choice
from string import ascii_letters, digits



def generate_short_url(length: int = 6) -> str:
    short_url = "".join(choice(ascii_letters + digits) for _ in range(length))

    return short_url