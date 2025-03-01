from django.contrib import admin

from .models import Parent, Organisation


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    pass


@admin.register(Organisation)
class OrganistionAdmin(admin.ModelAdmin):
    pass