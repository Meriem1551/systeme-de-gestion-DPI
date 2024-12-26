from rest_framework import serializers
from gestiondpi.models import BilanBiologique, ParametreBioMesure, Laborantin,DPI, Consultation

class ParametreBioMesureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametreBioMesure
        fields = '__all__'

class BilanBiologiqueSerializer(serializers.ModelSerializer):
    parametre_bio_mesures = ParametreBioMesureSerializer(many=True, read_only=True)
    
    class Meta:
        model = BilanBiologique
        fields = '__all__'

class LaborantinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laborantin
        fields = '__all__'


class ConsultationSerializer(serializers.ModelSerializer):
    bilan_biologique = BilanBiologiqueSerializer()

    class Meta:
        model = Consultation
        fields = ['id_consultation', 'bilan_biologique']

class DPISerializer(serializers.ModelSerializer):
    consultations = ConsultationSerializer(many=True)

    class Meta:
        model = DPI
        fields = ['id_dpi']
