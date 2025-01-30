from django.db import models
from authentification.models import User
import qrcode
import uuid
from io import BytesIO
from django.core.files.base import ContentFile

# Represents a patient with personal and medical details, linked to a User account
class Patient(models.Model):
    id_patient = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one link with User
    NSS = models.CharField(max_length=20, unique=True)  # Unique Social Security Number
    date_de_naissance = models.DateField()  # Date of birth
    adresse = models.TextField()  # Address
    telephone = models.CharField(max_length=15)  # Phone number
    mutuelle = models.CharField(max_length=100)  # Insurance provider
    personne_a_contacter = models.CharField(max_length=100)  # Emergency contact

# Represents a doctor with a specialty, linked to a User account
class Medecin(models.Model):
    id_medecin = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one link with User
    specialite = models.CharField(max_length=100)  # Medical specialty

# Represents a nurse, linked to a User account
class Infirmier(models.Model):
    id_infirmier = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one link with User

# Represents a lab technician, linked to a User account
class Laborantin(models.Model):
    id_laborantin = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one link with User

# Represents a radiologist, linked to a User account
class Radiologue(models.Model):
    id_radiologue = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one link with User

# Represents an administrator, linked to a User account
class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one link with User


# Represents a Digital Patient Record, linked to a patient and a doctor, with a QR code
class DPI(models.Model):
    id_dpi = models.AutoField(primary_key=True)
    patient = models.OneToOneField('Patient', on_delete=models.CASCADE, default=1)  # Each patient has one DPI
    medecin = models.ForeignKey('Medecin', related_name="medcin", on_delete=models.CASCADE, default=1)  # Linked to a doctor
    qr_code = models.ImageField(upload_to='qrcodes/', unique=True)  # QR code for identification

    def save(self, *args, **kwargs):
        """Generates a QR code before saving the DPI."""
        if not self.qr_code:  # Check if a QR code doesn't already exist
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def generate_qr_code(self):
        """Generates and assigns a unique QR code based on the patient's NSS."""
        if not self.patient or not self.patient.NSS:
            raise ValueError("Le NSS du patient est requis pour générer un QR code.")

        # Generate QR code data and image
        nom_patient = self.patient.utilisateur.last_name
        prenom_patient = self.patient.utilisateur.first_name
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.patient.NSS)  # NSS as QR code data
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")

        # Create a unique filename for the QR code
        unique_filename = f"qrcodes/{nom_patient}_{prenom_patient}_{self.patient.NSS}_qrcode_{uuid.uuid4().hex}.png"
        self.qr_code.save(unique_filename, ContentFile(buffer.getvalue()), save=False)

# Represents a summary of medical information
class Resume(models.Model):
    diagnostic = models.TextField(blank=True, null=True)  # Diagnostic details
    symptomes = models.TextField(blank=True, null=True)  # Symptoms
    antecedents = models.TextField(blank=True, null=True)  # Medical history
    autres_informations = models.TextField(blank=True, null=True)  # Other information

    def __str__(self):
        return "Résumé"

# Represents a prescription document
class Ordonnance(models.Model):
    id_ordonnance = models.AutoField(primary_key=True)
    date_prescription = models.DateField()  # Date of prescription
    etat_ordonnance = models.BooleanField(default=False)  # Validation status

# Represents a medical consultation
class Consultation(models.Model):
    id_consultation = models.AutoField(primary_key=True)
    dpi = models.ForeignKey(DPI, related_name="consultations", on_delete=models.CASCADE)  # Linked to DPI
    date_consult = models.DateField()  # Date of consultation
    resume = models.OneToOneField(Resume, related_name="consultation", on_delete=models.CASCADE)  # Linked to Resume
    ordonnance = models.OneToOneField(Ordonnance, related_name="consultation", on_delete=models.CASCADE, null=True)  # Linked to Ordonnance
    bilan_radiologue = models.ForeignKey('BilanRadiologique', related_name="consultations", on_delete=models.SET_NULL, null=True, blank=True)  # Radiological report
    bilan_biologique = models.ForeignKey('BilanBiologique', related_name="consultations", on_delete=models.SET_NULL, null=True, blank=True)  # Biological report

    def __str__(self):
        return f"Consultation {self.id_consultation} pour DPI {self.dpi.id_dpi}"

# Represents a prescription within an ordonnance
class Prescription(models.Model):
    id_prescription = models.AutoField(primary_key=True)
    ordonnance = models.ForeignKey(Ordonnance, related_name="prescriptions", on_delete=models.CASCADE)  # Linked to Ordonnance
    dose = models.CharField(max_length=50)  # Medication dose
    duree = models.CharField(max_length=50)  # Duration of treatment
    medicament = models.CharField(max_length=100, default='Default Value')  # Medication name

# Represents a biological analysis
class BilanBiologique(models.Model):
    id_bilanbiologique = models.AutoField(primary_key=True)
    description = models.TextField(default="")  # Description of the analysis
    parametres_bio_mesures = models.ManyToManyField('ParametreBioMesure', related_name="bilans_biologiques")  # Biological parameters
    laborantin = models.ForeignKey('Laborantin', related_name="bilanbiologiques", on_delete=models.CASCADE, null=True)  # Linked to Laborantin

# Represents a measured biological parameter
class ParametreBioMesure(models.Model):
    id_parametrebiomesure = models.AutoField(primary_key=True)
    bilan_biologique = models.ForeignKey('BilanBiologique', on_delete=models.CASCADE, related_name="parametre_bio_mesures")  # Linked to BilanBiologique
    nom = models.CharField(max_length=100)  # Parameter name
    unite_mesure = models.CharField(max_length=20)  # Unit of measurement
    valeur_normale = models.CharField(max_length=100)  # Normal value range
    valeur_mesuree = models.CharField(max_length=100)  # Measured value
    date_mesure = models.DateField()  # Date of measurement

# Represents a radiological analysis
class BilanRadiologique(models.Model):
    id_bilanradiologique = models.AutoField(primary_key=True)
    description = models.TextField(default="")  # Description of the analysis
    type = models.TextField(default="")  # Type of radiological analysis
    compte_rendu = models.TextField()  # Report details
    radiologue = models.ForeignKey('Radiologue', related_name="bilanradiologiques", on_delete=models.CASCADE, null=True)  # Linked to Radiologue

# Represents images in a radiological analysis
class RadiologyImage(models.Model):
    id_image = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="radiologies/")  # Radiology image
    bilan_radiologique = models.ForeignKey(BilanRadiologique, related_name="images", on_delete=models.CASCADE)  # Linked to BilanRadiologique

# Represents a nursing care record
class Soin(models.Model):
    id_soin = models.AutoField(primary_key=True)
    dpi = models.ForeignKey(DPI, related_name="soins", on_delete=models.CASCADE)  # Linked to DPI
    infirmier = models.ForeignKey(Infirmier, related_name="soins", on_delete=models.CASCADE)  # Linked to Infirmier
    description = models.CharField(max_length=255)  # Care description
    date_soin = models.DateField()  # Date of care
    observation = models.TextField()  # Observations
