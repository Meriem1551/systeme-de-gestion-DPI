from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import date

from .serializers import ConsultationSerializer, SoinSerializer, PatientSerializer
from gestiondpi.models import Soin, Consultation, Prescription, DPI, Patient, Infirmier
from authentification.models import User


# -------------------------------------------------------------------------------------------
# AjouterConsultation: Handles adding a consultation with nested data structures.
# Expected frontend data format:
# {
#     "nss": "1111111",
#     "resume": { "diagnostic": "string", "symptomes": "string", ... },
#     "ordonnance": { "prescription": [{ "dose": "string", ... }] },
#     "bilan_biologique": { "description": "string" },
#     "bilan_radiologue": { "description": "string", "type": "string" }
# }
class AjouterConsultation(APIView):
    def post(self, request):
        nss = request.data.pop('nss', None)
        patient = Patient.objects.get(NSS=nss)
        dpi = DPI.objects.get(patient=patient)
        request.data['dpi'] = dpi.id_dpi

        serializer = ConsultationSerializer(data=request.data)
        if serializer.is_valid():
            consultation = serializer.create(serializer.validated_data)
            consultation_serializer = ConsultationSerializer(consultation)
            return Response(consultation_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------------------------------------------------
# RemplirSoin: Handles adding a Soin for a patient.
# Expected frontend data format:
# {
#     "patient": 1,
#     "user": 2,
#     "description": "string",
#     "observation": "string"
# }
class RemplirSoin(APIView):
    def post(self, request):
        data = request.data.copy()
        data['dpi'] = data.pop('patient', None)
        data['date_soin'] = date.today().strftime('%Y-%m-%d')
        id_user = data.pop('user')

        user_infirmier = User.objects.get(id=id_user)
        infirmier = Infirmier.objects.get(utilisateur=user_infirmier)
        data['infirmier'] = infirmier.id_infirmier

        serializer = SoinSerializer(data=data)
        if serializer.is_valid():
            soin = serializer.create(serializer.validated_data)
            soin_serializer = SoinSerializer(soin)
            return Response(soin_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------------------------------------------------
# GetPatients: Fetches a list of all patients.
# Response format:
# [
#     { "id_patient": 1, "first_name": "Lokman", "last_name": "Djerfi" }
# ]
class GetPatients(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)


# -------------------------------------------------------------------------------------------
# GetSoins: Fetches Soins for a specific patient.
# Expected frontend data format: { "dpi": 1 }
# Response format:
# [
#     { "dpi": "", "infirmier": "", "description": "", "date_soin": "", "observation": "" }
# ]
class GetSoins(APIView):
    def get(self, request):
        #dpi = request.data.get('dpi')
        dpi = request.GET.get('dpi')

        if not dpi:
            return Response({"error": "dpi parameter is required"}, status=400)

        soins = Soin.objects.filter(dpi=dpi)
        serializer = SoinSerializer(soins, many=True)
        return Response(serializer.data)


# -------------------------------------------------------------------------------------------
# GetConsultations: Fetches consultations for a specific patient.
# Expected frontend data format: { "dpi": 1 }
# Response format:
# [
#     { "id_consult": 1, "date_consult": "2024-12-31", "ordonnance": true, ... }
# ]
class GetConsultations(APIView):
    def get(self, request):
        #dpi = request.data.get('dpi')
        dpi = request.GET.get('dpi')

        if not dpi:
            return Response({"error": "dpi parameter is required"}, status=400)

        consultations = Consultation.objects.filter(dpi=dpi)
        data = [
            {
                "id_consult": consultation.id_consultation,
                "date_consult": consultation.date_consult,
                "ordonnance": bool(consultation.ordonnance),
                "bilan_biologique": bool(consultation.bilan_biologique),
                "bilan_radiologique": bool(consultation.bilan_radiologue),
                "resume": bool(consultation.resume),
            } for consultation in consultations
        ]
        return Response(data)


# -------------------------------------------------------------------------------------------
# GetOrdonnance: Fetches prescription details for a specific consultation.
# Expected frontend data format: { "id_consult": 1 }
# Response format:
# [
#     { "medicament": "string", "dose": "string", "duree": "string" }
# ]
class GetOrdonnance(APIView):
    def get(self, request):
        # id_consult = request.data.get('id_consult')
        id_consult = request.GET.get('id_consult')

        if not id_consult:
            return Response({"error": "id_consult parameter is required"}, status=400)

        consultation = Consultation.objects.filter(id_consultation=id_consult).first()
        prescriptions = Prescription.objects.filter(ordonnance=consultation.ordonnance)

        data = [
            {
                "medicament": prescription.medicament,
                "dose": prescription.dose,
                "duree": prescription.duree
            } for prescription in prescriptions
        ]
        return Response(data)

# -------------------------------------------------------------------------------------------
# GetResume: Fetches the summary details for a specific consultation.
# Expected frontend data format: { "id_consult": 1 }
# Response format:
# {
#     "diagnostic": "string",
#     "symptomes": "string",
#     "antecedents": "string",
#     "autres_informations": "string"
# }
class GetResume(APIView):
    def get(self, request):
        #id_consult = request.data.get('id_consult')
        id_consult = request.GET.get('id_consult')

        if not id_consult:
            return Response({"error": "id_consult parameter is required"}, status=400)

        consultation = Consultation.objects.filter(id_consultation=id_consult).first()
        resume = consultation.resume
        data = {
            "diagnostic": resume.diagnostic,
            "symptomes": resume.symptomes,
            "antecedents": resume.antecedents,
            "autres_informations": resume.autres_informations
        }
        return Response(data)

# -------------------------------------------------------------------------------------------
# ValiderOrdonnance: Validates an ordonnance.
# Expected frontend data format:
# {
#     "valide": true/false,
#     "id_consult": 1
# }
class ValiderOrdonnance(APIView):
    def post(self, request):
        valide = request.data.get('valide')
        id_consult = request.data.get('id_consult')

        if valide is None or id_consult is None:
            return Response({"error": "Both 'valide' and 'id_consult' are required fields."}, status=400)

        consultation = get_object_or_404(Consultation, id_consultation=id_consult)
        ordonnance = consultation.ordonnance

        if valide:
            ordonnance.etat_ordonnance = True
            ordonnance.save()
            return Response({"message": "Ordonnance validated successfully."}, status=200)

        return Response({"error": "Invalid value for 'valide'. Must be true."}, status=400)

