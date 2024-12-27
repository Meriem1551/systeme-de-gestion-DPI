from rest_framework import serializers
from gestiondpi.models import BilanRadiologique, RadiologyImage


class RadiologyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiologyImage
        fields = ['id_image', 'image']

class BilanRadiologiqueSerializer(serializers.ModelSerializer):
    images = RadiologyImageSerializer(many=True, read_only=True)

    class Meta:
        model = BilanRadiologique
        fields = ['id_bilanradiologique', 'description', 'type', 'compte_rendu', 'radiologue', 'images']
