from rest_framework import serializers

class PredictionInputSerializer(serializers.Serializer):
    commune = serializers.CharField(max_length=100)
    annee = serializers.IntegerField(min_value=2024, max_value=2100)