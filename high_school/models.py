from django.db import models


class HighSchool(models.Model):
    dbn = models.CharField(max_length=10, blank=False, null=False, primary_key=True)
    school_name = models.CharField(max_length=200, blank=False, null=False)
    boro = models.CharField(max_length=1, blank=False, null=False)
    overview_paragraph = models.CharField(max_length=1000)
    neighborhood = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    school_email = models.EmailField(blank=False, null=False)
    website = models.CharField(max_length=70)
    total_students = models.IntegerField()
    start_time = models.CharField(max_length=6)
    end_time = models.CharField(max_length=6)
    graduation_rate = models.CharField(max_length=5)

    class Meta:
        ordering = ['school_name']

    def __str__(self):
        return self.school_name


# TODO: add Requirements
class Program(models.Model):
    high_school = models.ForeignKey(HighSchool, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(unique=True, max_length=20, blank=False, null=False)
    description = models.CharField(max_length=2000, blank=True, null=True)
    number_of_seats = models.IntegerField(blank=True, null=True)
    # Percent of fall 2017 offers that went to students in program's first priority
    # group for school's program
    offer_rate = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
