from django.db import models


class Timestampable:
    created_at = models.DateTimeField(models.DateTimeField(auto_now_add=True))
    updated_at = models.DateTimeField(models.DateTimeField(auto_now=True))
