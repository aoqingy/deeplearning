from django.db import models

# Create your models here.
class Axis(models.Model):
    aid = models.AutoField(primary_key=True)
    ax  = models.FloatField(null=False, verbose_name="X")
    ay  = models.FloatField(null=False, verbose_name="Y")
