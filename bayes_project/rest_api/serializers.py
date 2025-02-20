from rest_framework import serializers
from rest_api.models import *

class DataProbSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataProb
        fields=('Id','char','positive_prob','negative_prob','natural_prob')

class MetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaData
        fields=('total_positive_freq','total_negative_freq','total_natural_freq','total_freq','total_positive_prob','total_negative_prob','total_natural_prob')