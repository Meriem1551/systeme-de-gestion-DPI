from rest_framework import serializers
from gestiondpi.models import Patient, DPI, Medecin
from authentification.models import User


import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


from io import BytesIO
from django.core.files.base import ContentFile
import qrcode
import uuid  # To ensure a unique filename
from django.db import IntegrityError

class DPICreationSerializer(serializers.Serializer):
    nom_patient = serializers.CharField(max_length=100)
    prenom_patient = serializers.CharField(max_length=100)
    nss = serializers.CharField(max_length=20)
    date_de_naissance = serializers.DateField()
    adresse = serializers.CharField()
    telephone = serializers.CharField(max_length=15)
    mutuelle = serializers.CharField(max_length=100)
    personne_a_contacter = serializers.CharField(max_length=100)
    nom_medecin = serializers.CharField(max_length=100)
    antecedents = serializers.CharField(allow_blank=True, default="")

    def validate(self, data):
        # Recherche du patient
        try:
            utilisateur_patient = User.objects.get(
                first_name=data['nom_patient'],
                last_name=data['prenom_patient'],
                role=User.PATIENT
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({"patient": "Patient introuvable avec ce nom et prénom."})

        # Recherche du médecin
        try:
            utilisateur_medecin = User.objects.get(
                first_name=data['nom_medecin'],
                role=User.MEDECIN
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({"medecin": "Médecin introuvable avec ce nom."})

        # Ajout des utilisateurs validés au contexte
        data['utilisateur_patient'] = utilisateur_patient
        data['utilisateur_medecin'] = utilisateur_medecin
        return data

    def create(self, validated_data):
        # Create the patient record
        patient = Patient.objects.create(
            utilisateur=validated_data['utilisateur_patient'],
            NSS=validated_data['nss'],
            date_de_naissance=validated_data['date_de_naissance'],
            adresse=validated_data['adresse'],
            telephone=validated_data['telephone'],
            mutuelle=validated_data['mutuelle'],
            personne_a_contacter=validated_data['personne_a_contacter']
        )

        # Retrieve or create the doctor record
        medecin, created = Medecin.objects.get_or_create(
            utilisateur=validated_data['utilisateur_medecin']
        )

        # Create the DPI object
        dpi = DPI.objects.create(
            patient=patient,
            medecin=medecin,
            antecedents=validated_data.get("antecedents", "")
        )

        # QR code is generated automatically when the DPI is saved
        dpi.save()  # Save will trigger QR code generation

        return dpi


class PatientSerializer(serializers.ModelSerializer):
    nom_patient = serializers.CharField(source='utilisateur.first_name')
    prenom_patient = serializers.CharField(source='utilisateur.last_name')

    class Meta:
        model = Patient
        fields = ['nom_patient', 'prenom_patient', 'NSS', 'date_de_naissance', 'adresse', 'telephone', 'mutuelle',
                  'personne_a_contacter']


class QRCodeSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = DPI
        fields = ['id_dpi', 'qr_code_url']

    def get_qr_code_url(self, obj):
        if obj.qr_code:
            return obj.qr_code.url
        return None


class SearchDPIByNSSSerializer(serializers.Serializer):
    nss = serializers.CharField(max_length=20)

    def validate_nss(self, value):
        # Ensure that the NSS exists in the Patient's record
        try:
            patient = Patient.objects.get(NSS=value)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient with this NSS does not exist.")
        return value

class QRSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DPI
        fields = ['id_dpi', 'patient', 'medecin', 'antecedents', 'qr_code']