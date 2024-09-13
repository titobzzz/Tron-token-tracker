from django.db import models

# Create your models here.
       
class Token(models.Model):
    identifier = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=50)
    decimals = models.IntegerField()
    total_supply = models.BigIntegerField()
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    img_url = models.URLField(blank=True, null=True)