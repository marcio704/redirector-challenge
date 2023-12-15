from django.contrib import admin

from .models import Domain, DomainPool, DomainRedirect


# Register your models here.
admin.site.register(Domain)
admin.site.register(DomainPool)
admin.site.register(DomainRedirect)
