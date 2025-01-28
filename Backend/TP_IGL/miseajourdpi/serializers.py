from rest_framework import serializers
from gestiondpi.models import (
    Consultation, DPI, Resume, Ordonnance, Prescription, Soin, Patient, Infirmier,
    BilanRadiologique, BilanBiologique
)
from datetime import date


# -------------------------------------------------------------------------------------------
# Serializer for the Resume model
class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['diagnostic', 'symptomes', 'antecedents', 'autres_informations']


# -------------------------------------------------------------------------------------------
# Serializer for the Prescription model
class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['dose', 'duree', 'medicament']
        extra_kwargs = {
            'dose': {'allow_blank': True},
            'duree': {'allow_blank': True},
            'medicament': {'allow_blank': True},
        }

    def create(self, validated_data):
        # Create and return a Prescription instance
        prescription = Prescription.objects.create(**validated_data)
        return prescription


# -------------------------------------------------------------------------------------------
# Serializer for the Ordonnance model
class OrdonnanceSerializer(serializers.ModelSerializer):
    prescription = PrescriptionSerializer(many=True, required=False)  # Nested prescriptions

    class Meta:
        model = Ordonnance
        fields = ['prescription']

    def create(self, validated_data):
        prescription_data = validated_data.pop('prescription', [])

        # Set default values for Ordonnance
        validated_data['date_prescription'] = date.today()
        validated_data['etat_ordonnance'] = False

        # Create the Ordonnance instance
        ordonnance = Ordonnance.objects.create(**validated_data)

        # Create associated prescriptions
        for prescription in prescription_data:
            prescription_serializer = PrescriptionSerializer(data=prescription)
            if prescription_serializer.is_valid(raise_exception=True):
                prescription_serializer.save(ordonnance=ordonnance)

        return ordonnance


# -------------------------------------------------------------------------------------------
# Serializer for the BilanRadiologique model
class BilanRadiologiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BilanRadiologique
        fields = ['description', 'type']
        extra_kwargs = {
            'description': {'allow_blank': True},
            'type': {'allow_blank': True},
        }


# -------------------------------------------------------------------------------------------
# Serializer for the BilanBiologique model
class BilanBiologiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BilanBiologique
        fields = ['description']
        extra_kwargs = {
            'description': {'allow_blank': True},
        }


# -------------------------------------------------------------------------------------------
# Serializer for the Consultation model
class ConsultationSerializer(serializers.ModelSerializer):
    dpi = serializers.PrimaryKeyRelatedField(queryset=DPI.objects.all())
    resume = ResumeSerializer(required=True)
    ordonnance = OrdonnanceSerializer(required=False)
    bilan_biologique = BilanBiologiqueSerializer(required=False)
    bilan_radiologue = BilanRadiologiqueSerializer(required=False)

    class Meta:
        model = Consultation
        fields = ['dpi', 'resume', 'ordonnance', 'bilan_biologique', 'bilan_radiologue']

    def create(self, validated_data):
        dpi = validated_data.pop('dpi')
        resume_data = validated_data.pop('resume')
        ordonnance_data = validated_data.pop('ordonnance', None)
        bilan_biologique_data = validated_data.pop('bilan_biologique', None)
        bilan_radiologue_data = validated_data.pop('bilan_radiologue', None)

        # Create Resume instance
        resume = Resume.objects.create(**resume_data)

        # Create Ordonnance if data is valid
        ordonnance = None
        if ordonnance_data and ordonnance_data.get('prescription'):
            valid_prescriptions = [
                pres for pres in ordonnance_data['prescription']
                if all(pres.get(field) for field in ['dose', 'duree', 'medicament'])
            ]

            if valid_prescriptions:
                ordonnance_serializer = OrdonnanceSerializer(data={'prescription': valid_prescriptions})
                if ordonnance_serializer.is_valid(raise_exception=True):
                    ordonnance = ordonnance_serializer.save()

        # Create BilanBiologique if data is valid
        bilan_biologique = None
        if bilan_biologique_data:
            valid_bilan_biologique = {
                field: bilan_biologique_data.get(field)
                for field in ['description'] if bilan_biologique_data.get(field)
            }
            if valid_bilan_biologique:
                bilan_biologique_serializer = BilanBiologiqueSerializer(data=valid_bilan_biologique)
                if bilan_biologique_serializer.is_valid(raise_exception=True):
                    bilan_biologique = bilan_biologique_serializer.save()

        # Create BilanRadiologique if data is valid
        bilan_radiologue = None
        if bilan_radiologue_data:
            valid_bilan_radiologue = {
                field: bilan_radiologue_data.get(field)
                for field in ['description', 'type'] if bilan_radiologue_data.get(field)
            }
            if valid_bilan_radiologue:
                bilan_radiologue_serializer = BilanRadiologiqueSerializer(data=valid_bilan_radiologue)
                if bilan_radiologue_serializer.is_valid(raise_exception=True):
                    bilan_radiologue = bilan_radiologue_serializer.save()

        # Create Consultation instance
        consultation = Consultation.objects.create(
            dpi=dpi,
            resume=resume,
            ordonnance=ordonnance,
            date_consult=date.today(),
            bilan_biologique=bilan_biologique,
            bilan_radiologue=bilan_radiologue
        )

        return consultation


# -------------------------------------------------------------------------------------------
# Serializer for the Soin model
class SoinSerializer(serializers.ModelSerializer):
    dpi = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)  # Reference Patient by ID
    infirmier = serializers.PrimaryKeyRelatedField(queryset=Infirmier.objects.all())

    class Meta:
        model = Soin
        fields = ['dpi', 'infirmier', 'description', 'date_soin', 'observation']

    def create(self, validated_data):
        patient_id = validated_data.pop('dpi')

        # Retrieve the corresponding DPI
        try:
            dpi = DPI.objects.get(patient=patient_id)
        except DPI.DoesNotExist:
            raise serializers.ValidationError("DPI for the given patient does not exist.")

        # Create and return Soin instance
        soin = Soin.objects.create(dpi=dpi, **validated_data)
        return soin


# -------------------------------------------------------------------------------------------
# Serializer for the Patient model
class PatientSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='utilisateur.first_name')
    last_name = serializers.CharField(source='utilisateur.last_name')

    class Meta:
        model = Patient
        fields = ['id_patient', 'first_name', 'last_name']


# -------------------------------------------------------------------------------------------
# Serializer for the DPI model
class DPISerializer(serializers.ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = DPI
        fields = ['patient']

