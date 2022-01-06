from django.db import models
import datetime


# Create your models here.
class Jobs(models.Model):
    id = models.CharField(max_length=130, primary_key=True)
    name = models.CharField(max_length=128)
    company = models.CharField(max_length=200)
    salary = models.CharField(max_length=64)
    requires = models.TextField()
    # issue = models.DateTimeField(null=True, default=datetime.date)
    education = models.CharField(max_length=64, null=True)
    position = models.CharField(max_length=128, null=True)
    platform = models.CharField(max_length=20)

    # get_data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Label(models.Model):
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='label_set')
    value = models.CharField(max_length=64)

    def __str__(self):
        return self.value


