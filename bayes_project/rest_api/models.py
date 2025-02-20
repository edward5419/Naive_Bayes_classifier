from django.db import models


#defines MySQL tables
class DataProb(models.Model):
    Id = models.AutoField(primary_key=True)
    char = models.CharField(max_length=100, unique=True) #unique True : does not allow same Hanzi in same table
    positive_prob = models.FloatField(default=0.0) #float column 
    negative_prob = models.FloatField(default=0.0)
    natural_prob = models.FloatField(default=0.0)

class MetaData(models.Model): #data for total values. 
    total_positive_freq = models.IntegerField(default=0) # int column
    total_negative_freq = models.IntegerField(default=0)
    total_natural_freq = models.IntegerField(default=0)
    total_freq = models.IntegerField(default=0)
    total_positive_prob = models.FloatField(default=0.0) # float column
    total_negative_prob = models.FloatField(default=0.0)
    total_natural_prob = models.FloatField(default=0.0)