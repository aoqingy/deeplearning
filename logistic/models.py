from django.db import models

# Create your models here.
class Data(models.Model):
    did = models.AutoField(primary_key=True)
    dx1 = models.FloatField(null=False, verbose_name="X1")
    dx2 = models.FloatField(null=False, verbose_name="X2")
    dy  = models.IntegerField(null=False, verbose_name="Y")
