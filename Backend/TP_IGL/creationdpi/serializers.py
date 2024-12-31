from rest_framework import serializers
from gestiondpi.models import Patient, DPI, Medecin
from authentification.models import User
from authentification.views import AddUserView
from authentification.serializers import UserRegisterSerializer
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile


from io import BytesIO
from django.core.files.base import ContentFile
import qrcode
import uuid  # To ensure a unique filename
from django.db import IntegrityError
from django.urls import reverse


########################################Creation d DPI###########################################################
class DPICreationSerializer(serializers.Serializer):
    nom_patient = serializers.CharField(max_length=100)
    prenom_patient = serializers.CharField(max_length=100)
    nss = serializers.CharField(max_length=20)
    date_de_naissance = serializers.DateField()
    adresse = serializers.CharField()
    telephone = serializers.CharField(max_length=15)
    mutuelle = serializers.CharField(max_length=100)
    personne_a_contacter = serializers.CharField(max_length=100)
    nom_complet_medecin = serializers.CharField(
        max_length=200
    )  # Nom complet du médecin (prénom + nom ou nom + prénom)

    def validate(self, data):
        nom_complet = data["nom_complet_medecin"].strip()

        # Essayer d'extraire le prénom et le nom, en testant les deux possibilités
        try:
            parts = nom_complet.split()
            if len(parts) < 2:
                raise ValueError("Le nom doit contenir au moins deux parties")
            prenom_medecin, nom_medecin = parts[0], parts[1]
        except ValueError:
            raise serializers.ValidationError(
                {
                    "medecin": "Le nom du médecin doit être composé d'au moins un prénom et un nom."
                }
            )

        # Chercher le médecin en vérifiant les deux permutations
        utilisateur_medecin = None
        try:
            utilisateur_medecin = User.objects.get(
                first_name=prenom_medecin, last_name=nom_medecin, role=User.MEDECIN
            )
        except User.DoesNotExist:
            try:
                utilisateur_medecin = User.objects.get(
                    first_name=nom_medecin, last_name=prenom_medecin, role=User.MEDECIN
                )
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {"medecin": "Médecin introuvable avec ce nom complet."}
                )

        # Ajouter le médecin validé au contexte
        data["utilisateur_medecin"] = utilisateur_medecin
        return data

    def create(self, validated_data):
        # Création de l'email patient
        email = f"{validated_data['prenom_patient'].lower()}{validated_data['nom_patient'].lower()}{validated_data['nss']}@gmail.com"
        password = validated_data["nss"]

        # Créer l'utilisateur patient avec UserRegisterSerializer
        user_data = {
            "email": email,
            "first_name": validated_data["prenom_patient"],
            "last_name": validated_data["nom_patient"],
            "role": User.PATIENT,
            "password": password,
            "password2": password,
        }

        user_serializer = UserRegisterSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        utilisateur_patient = user_serializer.save()

        # Création du dossier patient
        patient = Patient.objects.create(
            utilisateur=utilisateur_patient,
            NSS=validated_data["nss"],
            date_de_naissance=validated_data["date_de_naissance"],
            adresse=validated_data["adresse"],
            telephone=validated_data["telephone"],
            mutuelle=validated_data["mutuelle"],
            personne_a_contacter=validated_data["personne_a_contacter"],
        )

        # Récupérer ou créer le médecin
        medecin, created = Medecin.objects.get_or_create(
            utilisateur=validated_data["utilisateur_medecin"]
        )

        # Création du DPI
        dpi = DPI.objects.create(
            patient=patient,
            medecin=medecin,
        )

        # Génération automatique du QR code
        dpi.save()

        return dpi


class QRCodeSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = DPI
        fields = ["id_dpi", "qr_code_url"]

    def get_qr_code_url(self, obj):
        if obj.qr_code:
            return obj.qr_code.url
        return None


###################################Affichage############################################################
class DPIListSerializer(serializers.ModelSerializer):
    nss = serializers.CharField(source="patient.NSS")
    nom_patient = serializers.CharField(source="patient.utilisateur.last_name")
    prenom_patient = serializers.CharField(source="patient.utilisateur.first_name")
    dpi_url = serializers.SerializerMethodField()
    id = serializers.CharField(source="patient.id_patient")

    class Meta:
        model = DPI
        fields = ["nss", "nom_patient", "prenom_patient", "dpi_url", "id"]

    def get_dpi_url(self, obj):
        # Génère l'URL vers les détails du DPI
        return reverse("dpi-detail", kwargs={"pk": obj.id_dpi})


class DPIDetailSerializer(serializers.ModelSerializer):
    nom_patient = serializers.CharField(source="patient.utilisateur.last_name")
    prenom_patient = serializers.CharField(source="patient.utilisateur.first_name")
    nss = serializers.CharField(source="patient.NSS")
    date_de_naissance = serializers.DateField(source="patient.date_de_naissance")
    adresse = serializers.CharField(source="patient.adresse")
    telephone = serializers.CharField(source="patient.telephone")
    mutuelle = serializers.CharField(source="patient.mutuelle")
    personne_a_contacter = serializers.CharField(source="patient.personne_a_contacter")
    nom_complet_medecin = serializers.SerializerMethodField()

    class Meta:
        model = DPI
        fields = [
            "nss",
            "nom_patient",
            "prenom_patient",
            "date_de_naissance",
            "adresse",
            "telephone",
            "mutuelle",
            "personne_a_contacter",
            "nom_complet_medecin",
        ]

    def get_nom_complet_medecin(self, obj):
        """Retourne le nom complet du médecin (prénom + nom)."""
        utilisateur = obj.medecin.utilisateur
        return f"{utilisateur.first_name} {utilisateur.last_name}"
