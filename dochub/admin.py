from django.contrib import admin

from .models import Trust, Organisation, NHSEnglandRegion, LondonBorough, LocalHealthBoard, IntegratedCareBoard, Country, GMC


@admin.register(Trust)
class TrustAdmin(admin.ModelAdmin):
    pass

@admin.register(Organisation)
class OrganistionAdmin(admin.ModelAdmin):
    pass

@admin.register(NHSEnglandRegion)
class NHSEnglandRegionAdmin(admin.ModelAdmin):
    pass

@admin.register(LondonBorough)
class LondonBoroughAdmin(admin.ModelAdmin):
    pass

@admin.register(LocalHealthBoard)
class LocalHealthBoardAdmin(admin.ModelAdmin):
    pass

@admin.register(IntegratedCareBoard)
class IntegratedCareBoardAdmin(admin.ModelAdmin):
    pass

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass

@admin.register(GMC)
class GMCAdmin(admin.ModelAdmin):
    pass