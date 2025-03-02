from django.contrib.gis.db import models

from ..constants import INDICATOR_CHOICES, POST_SPECIALITY_CHOICES, BENCHMARK_CHOICES

class GMC(models.Model):
    deanery_code = models.CharField(max_length=3)
    deanery_name = models.CharField(max_length=100)
    post_specialty = models.IntegerField(choices=POST_SPECIALITY_CHOICES, blank=True)
    indicator = models.IntegerField(choices=INDICATOR_CHOICES, blank=True)
    year = models.IntegerField()
    outcome = models.CharField(max_length=100)
    response_rate = models.FloatField()
    mean = models.FloatField()
    ci_lower = models.FloatField()
    ci_upper = models.FloatField()
    n = models.IntegerField()
    benchmark_name = models.IntegerField(choices=BENCHMARK_CHOICES, blank= True)
    national_mean = models.FloatField()
    national_min = models.FloatField()
    national_Q1 = models.FloatField()
    national_median = models.FloatField()
    national_Q3 = models.FloatField()
    national_max = models.FloatField()
    national_ci_lower = models.FloatField()
    national_ci_upper = models.FloatField()
    national_n = models.IntegerField()

    organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE) # This is a foreign key to the Organisation model (unique ID is the ods_code)

    def __str__(self):
        return f"{self.deanery_name} - {self.post_specialty} - {self.indicator} - {self.year}"
    
    class Meta:
        verbose_name = "GMC"
        verbose_name_plural = "GMC"


    
