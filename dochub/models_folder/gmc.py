from django.contrib.gis.db import models

from ..constants import INDICATOR_CHOICES, POST_SPECIALITY_CHOICES, BENCHMARK_CHOICES

class GMC(models.Model):
    deanery_name = models.CharField(max_length=100, null=True, blank=True)
    post_specialty = models.IntegerField(choices=POST_SPECIALITY_CHOICES, blank=True, null=True)
    indicator = models.IntegerField(choices=INDICATOR_CHOICES, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    outcome = models.CharField(max_length=100, null=True, blank=True)
    response_rate = models.FloatField(null=True, blank=True)
    mean = models.FloatField(null=True, blank=True)
    ci_lower = models.FloatField(null=True, blank=True)
    ci_upper = models.FloatField(null=True, blank=True)
    n_range = models.CharField(max_length=100, null=True, blank=True)
    benchmark_name = models.IntegerField(choices=BENCHMARK_CHOICES, blank= True, null=True)
    national_mean = models.FloatField(null=True, blank=True)
    national_min = models.FloatField(null=True, blank=True)
    national_Q1 = models.FloatField(null=True, blank=True)
    national_median = models.FloatField(null=True, blank=True)
    national_Q3 = models.FloatField(null=True, blank=True)
    national_max = models.FloatField(null=True, blank=True)
    national_ci_lower = models.FloatField(null=True, blank=True)
    national_ci_upper = models.FloatField(null=True, blank=True)
    national_n = models.IntegerField(null=True, blank=True)

    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE) # This is a foreign key to the Organisation model (unique ID is the ods_code)

    def __str__(self):
        return f"{self.deanery_name} - {self.post_specialty} - {self.indicator} - {self.year}"
    
    class Meta:
        verbose_name = "GMC"
        verbose_name_plural = "GMC"


    
