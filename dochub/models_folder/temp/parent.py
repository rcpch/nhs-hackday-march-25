from django.contrib.gis.db import models

class Parent(models.Model):
    ods_code = models.CharField()

    name = models.TextField()

    welsh_name = models.TextField(
        null=True,
        blank=True
    )

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

    class Meta:
        indexes = [models.Index(fields=["ods_code"])]
        verbose_name = "Parent"
        verbose_name_plural = "Parents"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} [{self.ods_code}]"