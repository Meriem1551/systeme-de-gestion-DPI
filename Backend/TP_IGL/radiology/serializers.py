from rest_framework import serializers
from gestiondpi.models import BilanRadiologique, RadiologyImage,Consultation,DPI,Patient
from authentification.models import User


class RadiologyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiologyImage
        fields = '__all__'

class BilanRadiologiqueSerializer(serializers.ModelSerializer):
    images = RadiologyImageSerializer(many=True, read_only=True)

    class Meta:
        model = BilanRadiologique
        fields = '__all__'

class ConsultationSerializer(serializers.ModelSerializer):
    bilan_radiologique = BilanRadiologiqueSerializer(read_only=True)
    

    class Meta:
        model = Consultation
        fields = '__all__'





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
