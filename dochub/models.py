from django.contrib.gis.db import models

class Parent(models.Model):
    ods_code = models.CharField()

    name = models.TextField()

    welsh_name = models.TextField()

    location_wgs = models.PointField(
        srid=27700,
        null=True,
        blank=True,
    )

    location_bng = models.PointField(
        srid=27700,
        null=True,
        blank=True,
    )

    location_wgs84 = models.PointField(
        srid=4326,
        null=True,
        blank=True,
    )

    organisations = models.ForeignKey(
        to="Organisation",
        on_delete=models.CASCADE,
        related_name="organisations",
    )


class Organisation(models.Model):
    ods_code = models.CharField()

    name = models.TextField()

    welsh_name = models.TextField()

    location_wgs = models.PointField(
        srid=27700,
        null=True,
        blank=True,
    )

    location_bng = models.PointField(
        srid=27700,
        null=True,
        blank=True,
    )

    location_wgs84 = models.PointField(
        srid=4326,
        null=True,
        blank=True,
    )
