
from django.db import models
from authentification.models import User


class Patient(models.Model):
    id_patient = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    NSS = models.CharField(max_length=20, unique=True)
    codeQR = models.CharField(max_length=255, unique=True)
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
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE,default=1)
    medecin = models.ForeignKey(Medecin, related_name="medcin", on_delete=models.CASCADE,default=1)
    antecedents = models.TextField()


class Consultation(models.Model):
    id_consultation = models.AutoField(primary_key=True)
    dpi = models.ForeignKey(DPI, related_name="consultations", on_delete=models.CASCADE)
    date_consult = models.DateField()
    resume = models.TextField(blank=True, null=True)

class Ordonnance(models.Model):
    id_ordonnance = models.AutoField(primary_key=True)
    consultation = models.OneToOneField(Consultation, related_name="ordonnance", on_delete=models.CASCADE)
    date_prescription = models.DateField()
    etat_ordonnance = models.BooleanField(default=False)

class Prescription(models.Model):
    id_prescription = models.AutoField(primary_key=True)
    ordonnance = models.ForeignKey(Ordonnance, related_name="prescriptions", on_delete=models.CASCADE)
    dose = models.CharField(max_length=50)
    duree = models.CharField(max_length=50)
    medicament = models.OneToOneField('Medicament', related_name="prescription", on_delete=models.CASCADE,default=1)

class Medicament(models.Model):
    id_medicament= models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()


class Examen(models.Model):

    TYPE_CHOICES = [
        ('biologique', 'Biologique'),
        ('radiologique', 'Radiologique'),
    ]
    id_examen = models.AutoField(primary_key=True)
    consultation = models.ForeignKey(Consultation, related_name="examens", on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    date_prescription = models.DateField()

class BilanBiologique(models.Model):
    id_bilanbiologique = models.AutoField(primary_key=True)
    examen = models.OneToOneField(Examen, on_delete=models.CASCADE, related_name="bilan_biologique")
    parametres = models.ManyToManyField('ParametreBiologique', related_name="bilans_biologiques")
    laborantin = models.ForeignKey(Laborantin, related_name="bilanbiologiques", on_delete=models.CASCADE,default=1)

class ParametreBiologique(models.Model):
    id_parametrebiologique= models.AutoField(primary_key=True)
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
    examen = models.OneToOneField(Examen, on_delete=models.CASCADE, related_name="bilan_radiologique")
    image = models.ImageField(upload_to="radiologies/")
    compte_rendu = models.TextField()
    radiologue = models.ForeignKey(Radiologue, related_name="bilanradiologiques", on_delete=models.CASCADE,default=1)

class Soin(models.Model):
    id_soin = models.AutoField(primary_key=True)
    dpi = models.ForeignKey(DPI, related_name="soins", on_delete=models.CASCADE)
    infirmier = models.ForeignKey(Infirmier, related_name="soins", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)  # Description du soin
    date_soin = models.DateField()  # Date du soin
    observation = models.TextField()
