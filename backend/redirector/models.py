from django.db import models

from .behaviors import Timestampable


class DomainPool(Timestampable, models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    @property
    def size(self) -> int:
        return self.domains.count()


class Domain(Timestampable, models.Model):
    name = models.URLField(unique=True)
    weight = models.SmallIntegerField()
    domain_pool = models.ForeignKey(DomainPool, related_name="domains", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def redirects_count(self) -> int:
        return self.redirects.count()


class DomainRedirect(Timestampable, models.Model):
    domain = models.ForeignKey(Domain, related_name="redirects", on_delete=models.CASCADE)
    user_agent = models.TextField(null=True, blank=True)
    referer = models.TextField(null=True, blank=True)
    ip = models.TextField(null=True, blank=True)
    redirect_date = models.DateTimeField()
