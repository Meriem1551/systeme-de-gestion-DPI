from django.db import models
from authentification.models import User
import qrcode
import uuid
from io import BytesIO
from django.core.files.base import ContentFile

class Patient(models.Model):
    id_patient = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    NSS = models.CharField(max_length=20, unique=True)
    date_de_naissance = models.DateField()
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    mutuelle = models.CharField(max_length=100)
    personne_a_contacter = models.CharField(max_length=100)


class Medecin(models.Model):
    id_medecin = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=100)

class Infirmier(models.Model):
        id_infirmier = models.AutoField(primary_key=True)
        utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)

class Laborantin(models.Model):
    id_laborantin= models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)

class Radiologue(models.Model):
    id_radiologue = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)

class Admin(models.Model):
    id_admin = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)

class PharmacienHospitalier(models.Model):
    id_pharmacienHospitalier = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)

    def valider_ordonnance(self, ordonnance):
        ordonnance.etat_ordonnance = True
        ordonnance.save()
        
class DPI(models.Model):
id_dpi = models.AutoField(primary_key=True)
    patient = models.OneToOneField('Patient', on_delete=models.CASCADE, default=1)
    medecin = models.ForeignKey('Medecin', related_name="medcin", on_delete=models.CASCADE, default=1)
    antecedents = models.TextField(blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', unique=True , default='default_qr')

    def save(self, *args, **kwargs):
        # Génère le QR code avant de sauvegarder
        if not self.qr_code:  # Vérifie si un QR code n'a pas déjà été assigné
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def generate_qr_code(self):
        """Génère et sauvegarde un QR code unique basé sur le NSS du patient."""
        if not self.patient or not self.patient.NSS:
            raise ValueError("Le NSS du patient est requis pour générer un QR code.")

        # Récupérer le prénom et le nom du patient
        nom_patient = self.patient.utilisateur.last_name
        prenom_patient = self.patient.utilisateur.first_name

        # Génération du QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.patient.NSS)  # Encode le NSS dans le QR code
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")

        # Génère un chemin unique pour le fichier avec prénom et nom
        unique_filename = f"qrcodes/{nom_patient}_{prenom_patient}_{self.patient.NSS}_qrcode_{uuid.uuid4().hex}.png"

        # Enregistre l'image générée dans le champ qr_code
        self.qr_code.save(unique_filename, ContentFile(buffer.getvalue()), save=False)

#comment
class Resume(models.Model):
    diagnostic = models.TextField(blank=True, null=True)
    symptomes = models.TextField(blank=True, null=True)
    antecedents = models.TextField(blank=True, null=True)
    autres_informations = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Résumé"
 

class Medicament(models.Model):
    id_medicament= models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()



    
class Ordonnance(models.Model):
    id_ordonnance = models.AutoField(primary_key=True)
    date_prescription = models.DateField()
    etat_ordonnance = models.BooleanField(default=False)
    

class Consultation(models.Model):
    id_consultation = models.AutoField(primary_key=True)
    dpi = models.ForeignKey('DPI', related_name="consultations", on_delete=models.CASCADE)
    date_consult = models.DateField()
    resume = models.OneToOneField('Resume', related_name="consultation", on_delete=models.CASCADE)
    ordonnance = models.OneToOneField(Ordonnance, related_name="Consultation", on_delete=models.CASCADE)
    
    # Add bilanRadiologue and bilanBiologique, allowing them to be null
    bilan_radiologue = models.ForeignKey('BilanRadiologique', related_name="consultations", on_delete=models.SET_NULL, null=True, blank=True)
    bilan_biologique = models.ForeignKey('BilanBiologique', related_name="consultations", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Consultation {self.id_consultation} pour DPI {self.dpi.id_dpi}"
    
    
class Prescription(models.Model):
    id_prescription = models.AutoField(primary_key=True)
    ordonnance = models.ForeignKey(Ordonnance, related_name="prescriptions", on_delete=models.CASCADE)
    dose = models.CharField(max_length=50)
    duree = models.CharField(max_length=50)
    medicament = models.OneToOneField(Medicament, related_name="prescription", on_delete=models.CASCADE,default=1)    

class BilanBiologique(models.Model):
    id_bilanbiologique = models.AutoField(primary_key=True)
    description = models.TextField(default="")
    parametres = models.ManyToManyField('ParametreBiologique', related_name="bilans_biologiques")
    laborantin = models.ForeignKey('Laborantin', related_name="bilanbiologiques", on_delete=models.CASCADE,null=True,)

class ParametreBiologique(models.Model):
    id_parametrebiologique = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    unite_mesure = models.CharField(max_length=20)
    valeur_normale = models.CharField(max_length=100)

class ParametreBioMesure(models.Model):
    id_parametrebiomesure = models.AutoField(primary_key=True)
    parametre_biologique = models.ForeignKey('ParametreBiologique', on_delete=models.CASCADE, related_name="mesures")
    valeur_mesuree = models.CharField(max_length=100)
    date_mesure = models.DateField()

class BilanRadiologique(models.Model):
    id_bilanradiologique = models.AutoField(primary_key=True)
    description = models.TextField(default="")
    type = models.TextField(default="")
    image = models.ImageField(upload_to="radiologies/")
    compte_rendu = models.TextField()
    radiologue = models.ForeignKey('Radiologue', related_name="bilanradiologiques", on_delete=models.CASCADE,null=True,)


class Soin(models.Model):
    id_soin = models.AutoField(primary_key=True)
    dpi = models.ForeignKey(DPI, related_name="soins", on_delete=models.CASCADE)
    infirmier = models.ForeignKey(Infirmier, related_name="soins", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)  # Description du soin
    date_soin = models.DateField()  # Date du soin
    observation = models.TextField()
