from rest_framework import serializers
from gestiondpi.models import BilanBiologique, ParametreBioMesure, Laborantin,DPI, Consultation,DPI,Patient
from authentification.models import User

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class PatientSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer()

    class Meta:
        model = Patient
        fields = ['id_patient', 'utilisateur']


class DPISerializer(serializers.ModelSerializer):
    utilisateur = serializers.SerializerMethodField()

    class Meta:
        model = DPI
        fields = ['id_dpi', 'utilisateur']

    def get_utilisateur(self, obj):
        # Safely handle cases where patient or utilisateur is None
        if obj.patient and obj.patient.utilisateur:
            return UserSerializer(obj.patient.utilisateur).data

        return None

