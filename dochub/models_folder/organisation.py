from django.contrib.gis.db import models

class Organisation(models.Model):
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
        indexes = [models.Index(fields=["ods_code"])]
        verbose_name = "Organisation"
        verbose_name_plural = "Organisations"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} [{self.ods_code}]"