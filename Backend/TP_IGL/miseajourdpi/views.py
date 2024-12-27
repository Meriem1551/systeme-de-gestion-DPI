from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,request
from .serializers import ConsultationSerializer,SoinSerializer,DPISerializer
from gestiondpi.models import Soin,Consultation,Prescription,Medecin,DPI
from rest_framework import status
from django.shortcuts import get_object_or_404


# the expected format of the info from the frontend
# {
#     "dpi": 1, 
#     "resume": {
#         "diagnostic": "string", 
#         "symptomes": "string", 
#         "antecedents": "string", 
#         "autres_informations": "string"
#     },
#     
#           "ordonnance": {
#             "date_prescription": "2025-05-30",
#             "etat_ordonnance": true,
#             "prescription": [{
#                 "dose": "string",
#                 "duree": "string",
#                 "medicament": {
#                 "nom": "string",
#                 "description": "string",
#                 "prix": 10,
#                 "quantite": 5
#           }],
#         }
#     },
#     "bilan_biologique": {
#         "description": "string"
#     },
#     "bilan_radiologique": {
#         "description": "string",
#         "type": "string"
#     }
# }
class AjouterConsultation(APIView):
    def post(self, request):
        # Serialize the data from the frontend to create a new consultation
        serializer = ConsultationSerializer(data=request.data)  
        
        if serializer.is_valid():
            # Explicitly call the create method to handle the nested logic
            consultation = serializer.create(serializer.validated_data)
            
            # Serialize the consultation object again to return it as a response
            consultation_serializer = ConsultationSerializer(consultation)
            
            return Response(consultation_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#-------------------------------------------------------------------------------------------  
# the expected format of the info from the frontend
# {
#   "patient": 1,  //ID 
#   "infirmier": 2,  //ID
#   "description": "Administered medication to the patient.",  
#   "date_soin": "2023-12-21",  
#   "observation": "Patient showed positive reaction to the medication."  
# }
class RemplirSoin(APIView):
    def post(self, request):
        # Extract id_patient from the request data
        data = request.data.copy()
        if 'patient' in data:  # If id_patient is provided by the frontend
            data['dpi'] = data.pop('patient')  # Rename id_patient to dpi (since it's the field expected by the serializer)

        # Use the updated data to validate the request
        serializer = SoinSerializer(data=data)

        if serializer.is_valid():
            soin = serializer.create(serializer.validated_data)

            soin_serializer = SoinSerializer(soin)

            return Response(soin_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#-------------------------------------------------------------------------------------------  
# the data sent to the front end will be in this format (list of JSON data):
# [
#     {
#         "id_patient": 1,
#         "first_name": "Lokman",
#         "last_name": "Djerfi"
#     }
# ] 

#  the data sent from the front wiil be in the format 
# {"medecin_first_name" :  "Nadine",
# "medecin_last_name": "Bousdjira"
# }   
class GetPatients(APIView):
    def get(self, request):
        # Get first_name and last_name from query parameters
        first_name = request.data['medecin_first_name']
        last_name = request.data['medecin_last_name']
        
        if not first_name or not last_name:
            return Response({"error": "first_name and last_name are required"}, status=400)
        
        # Search for Medecin using both first_name and last_name
        try:
            medecin = Medecin.objects.get(utilisateur__first_name=first_name, utilisateur__last_name=last_name)
        except Medecin.DoesNotExist:
            return Response({"error": "Medecin not found"}, status=404)
        
        dpis = DPI.objects.filter(medecin=medecin)  # Get all patients
        serializer =DPISerializer(dpis, many=True)  # Serialize the queryset
        return Response(serializer.data)  # Return serialized data in the response


#-------------------------------------------------------------------------------------------  
# the data sent to the front end will be in this format (list of JSON data):
# [
# {'dpi': "",
#  'infirmier' : " ",
#  'description' : " ", 
# 'date_soin' : " ",
#  'observation' : " "}
#  ]   

#  the data sent from the front wiil be in the format 
# {"dpi" :  1}
class GetSoins(APIView):
    def get(self,request):
        dpi = request.data['dpi']
        data = []
        if dpi is None:
            return Response({"error": "dpi parameter is required"}, status=400)
        soins = Soin.objects.filter(dpi=dpi)  
        serializer = SoinSerializer(soins,many=True)
        return Response(serializer.data) 


#-------------------------------------------------------------------------------------------  
# the data sent to the front end will be in this format (list of JSON data):
# [
#     {
#         "num_consult": 1,
#         "date_consult": "2024-12-22",
#         "ordonnance": true,
#         "prescription": true,
#         "resume": true
#     }
# ]
# the data sent from the front will be i the format 
# {"dpi" :  1}
class GetConsultations(APIView):
    def get(self, request):
        dpi = request.data['dpi']
        data = []
        if dpi is None:
            return Response({"error": "dpi parameter is required"}, status=400)
        consultations = Consultation.objects.filter(dpi=dpi)
        for consultation in consultations:
            data.append({
               "num_consult": consultation.id_consultation,
               "date_consult": consultation.date_consult,
               "ordonnance": bool(consultation.ordonnance),
               "prescription": bool(Prescription.objects.filter(ordonnance=consultation.ordonnance).exists()),
               "resume": bool(consultation.resume),
            })
        return Response(data)

            
#-------------------------------------------------------------------------------------------  
# the data sent to the front end will be in this format (list of JSON data):
# [
#     {
#         "medicament": "string",
#         "dose": "string",
#         "duree": "string"
#     },
# ]
# the data sent from the front will be i the format 
# {"id_consult" :  1}
class GetOrdonnance(APIView):
    def get(self,request):
        id_consult = request.data['id_consult']
        data = []
        if id_consult is None:
            return Response({"error": "id_consult parameter is required"}, status=400)
        
        consultation = Consultation.objects.get(id_consultation=id_consult)
        ordonnance = consultation.ordonnance
        prescriptions = Prescription.objects.filter(ordonnance=ordonnance)
        for prescription in prescriptions :
            data.append(
                {
                    "medicament" : prescription.medicament.nom,
                    "dose" : prescription.dose,
                    "duree" : prescription.duree
                }
            )
        return Response(data)    
    
#-------------------------------------------------------------------------------------------
# the data sent to the front end will be in this format (JSON data):
# {
#     "diagnostic": "string",
#     "symptomes": "string",
#     "antecedents": "string",
#     "autres_informations": "string"
# }
# the data sent from the front will be i the format 
# {"id_consult" :  1}
class GetResume(APIView):
    def get(self,request):
        id_consult = request.data['id_consult']
        data ={}
        if id_consult is None:
            return Response({"error": "id_consult parameter is required"}, status=400)
        consultation = Consultation.objects.get(id_consultation=id_consult) 
        resume = consultation.resume
        data = {
            "diagnostic" : resume.diagnostic,
            "symptomes" : resume.symptomes,
            "antecedents" : resume.antecedents,
            "autres_informations" :resume.autres_informations
        }
        return Response(data)    

# the data sent from the SGPH will be in the format 
# {
# "valide" :  true/false,
# "id_consult" : 1
# }    


class ValiderOrdonnance(APIView):
    def post(self, request):
        valide = request.data.get('valide')
        id_consult = request.data.get('id_consult')
        
        if valide is None or id_consult is None:
            return Response(
                {"error": "Both 'valide' and 'id_consult' are required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            consultation = get_object_or_404(Consultation, id_consultation=id_consult)
            ordonnance = consultation.ordonnance
            
            if valide is True:
                ordonnance.etat_ordonnance = True
                ordonnance.save()
                return Response(
                    {"message": "Ordonnance validated successfully."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Invalid value for 'valide'. Must be true."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




