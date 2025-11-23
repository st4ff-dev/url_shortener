from tortoise import fields
from tortoise.models import Model



class Url(Model):
    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    url = fields.CharField(1024, unique=True)
    short_url = fields.CharField(6, unique=True)

    class Meta:
        table = "urls"

