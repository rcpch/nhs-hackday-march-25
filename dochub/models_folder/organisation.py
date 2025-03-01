# django
from django.contrib.gis.db import models
from django.contrib.gis.db.models import (
    PointField,
    CharField,
    FloatField,
    BooleanField,
)
from django.contrib.gis.geos import Point
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Organisation(models.Model):
    """
    This class details information about organisations.
    It represents a list of organisations that can be looked up
    """

    ods_code = CharField(
        max_length=100, null=True, blank=True, default=None, unique=True
    )
    name = CharField(max_length=100, null=True, blank=True, default=None)
    website = CharField(max_length=100, null=True, blank=True, default=None)
    address1 = CharField(max_length=100, null=True, blank=True, default=None)
    address2 = CharField(max_length=100, null=True, blank=True, default=None)
    address3 = CharField(max_length=100, null=True, blank=True, default=None)
    telephone = CharField(max_length=100, null=True, blank=True, default=None)
    email = CharField(max_length=200, null=True, blank=True, default=None)
    city = CharField(max_length=100, null=True, blank=True, default=None)
    county = CharField(max_length=100, null=True, blank=True, default=None)
    latitude = FloatField(max_length=100, null=True, blank=True, default=None)
    longitude = FloatField(null=True, blank=True, default=None)
    postcode = CharField(max_length=10, null=True, blank=True, default=None)
    geocode_coordinates = PointField(null=True, blank=True, default=None, srid=27700)
    active = BooleanField(
        default=True
    )  # a boolean representing if this Organisation is still operational
    published_at = models.DateField(
        null=True, blank=True, default=None
    )  # date this Organisation was last amended according to the ORD

    trust = models.ForeignKey(
        to="dochub.Trust",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    local_health_board = models.ForeignKey(
        to="dochub.LocalHealthBoard",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    integrated_care_board = models.ForeignKey(
        to="dochub.IntegratedCareBoard",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    nhs_england_region = models.ForeignKey(
        to="dochub.NHSEnglandRegion",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )
    # administrative regions
    london_borough = models.ForeignKey(
        to="dochub.LondonBorough",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
    )

    country = models.ForeignKey(
        to="dochub.Country", on_delete=models.PROTECT, null=True, blank=True
    )

    class Meta:
        indexes = [models.Index(fields=["name"])]
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.latitude and self.longitude and not self.geocode_coordinates:
            self.geocode_coordinates = Point(
                x=self.longitude, y=self.latitude, srid=4326
            )
        super(Organisation, self).save(*args, **kwargs)


# This ensures that the geocode coordinates are set before saving, even if update is called
@receiver(pre_save, sender=Organisation)
def set_geocode_coordinates(sender, instance, **kwargs):
    from django.contrib.gis.geos import Point

    if instance.latitude and instance.longitude and not instance.geocode_coordinates:
        instance.geocode_coordinates = Point(
            x=instance.longitude, y=instance.latitude, srid=4326
        )


# Ensure the signal is connected
pre_save.connect(set_geocode_coordinates, sender=Organisation)
