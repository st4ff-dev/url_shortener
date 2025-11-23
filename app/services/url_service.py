from tortoise.exceptions import IntegrityError

from app.utils.funcs import generate_short_url

from app.models.url import Url
from app.utils.types import ServiceResponse



class UrlService:

    @staticmethod
    async def get_by_slug(slug: str) -> ServiceResponse:
        url_obj = await Url.filter(short_url=slug).first()

        if not url_obj:
            return ServiceResponse(
                data={
                    "message": "URL not found"
                },
                status=404
            )

        return ServiceResponse(
            data={
                "long_url": url_obj.url
            },
            status=302
        )


    @staticmethod
    async def create_or_get(long_url: str) -> ServiceResponse:
        short_url = generate_short_url()
        
        try:
            url_obj = await Url.create(
                url=long_url,
                short_url=short_url
            )
            
        except IntegrityError:
            url_obj = await Url.filter(url=long_url).first()

        if not url_obj:
            return ServiceResponse(
                data={
                    "message": "URL is not created, please try again"
                },
                status=500
            )

        return ServiceResponse(
            data={
                "short_url": url_obj.short_url
            },
            status=200
        )
    

url_service = UrlService()