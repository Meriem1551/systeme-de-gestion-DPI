from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DPICreationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from gestiondpi.models import DPI ,Patient
from .serializers import QRCodeSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from pyzbar.pyzbar import decode
from PIL import Image

from .serializers import SearchDPIByNSSSerializer
from .serializers import QRSearchSerializer
class DPICreationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DPICreationSerializer(data=request.data)
        if serializer.is_valid():
            dpi = serializer.save()
            return Response(
                {
                    "message": "DPI created successfully",
                    "dpi_id": dpi.id_dpi,
                    "qr_code": dpi.qr_code.url,  # URL of the generated QR code
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class QRCodeView(APIView):
    def get(self, request, dpi_id):
        # Récupérer le DPI par son ID
        dpi = get_object_or_404(DPI, id_dpi=dpi_id)

        # Sérialiser l'objet DPI pour obtenir l'URL du QR code
        serializer = QRCodeSerializer(dpi)

        return Response(serializer.data, status=status.HTTP_200_OK)

class SearchDPIByNSSView(APIView):
    def get(self, request):
        # Get the NSS from the query parameters
        nss = request.query_params.get('nss')

        if not nss:
            return Response({"error": "NSS parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the patient using the NSS
            patient = Patient.objects.get(NSS=nss)

            # Retrieve the associated DPI
            dpi = DPI.objects.get(patient=patient)

            # Prepare patient details
            patient_details = {
                "id_patient": patient.id_patient,
                "nom_patient": patient.utilisateur.first_name,
                "prenom_patient": patient.utilisateur.last_name,
                "nss": patient.NSS,
                "date_de_naissance": patient.date_de_naissance,
                "adresse": patient.adresse,
                "telephone": patient.telephone,
                "mutuelle": patient.mutuelle,
                "personne_a_contacter": patient.personne_a_contacter
            }

            # Prepare response data
            response_data = {
                "id_dpi": dpi.id_dpi,
                "antecedents": dpi.antecedents,
                "qr_code_url": dpi.qr_code.url if dpi.qr_code else None,
            }

            # Combine patient details and DPI details
            response_data.update(patient_details)

            return Response(response_data, status=status.HTTP_200_OK)

        except Patient.DoesNotExist:
            return Response({"error": "Patient with this NSS does not exist."}, status=status.HTTP_404_NOT_FOUND)

        except DPI.DoesNotExist:
            return Response({"error": "DPI not found for this patient."}, status=status.HTTP_404_NOT_FOUND)

class QRCodeScanView(APIView):
    # Allow image file upload
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # Get the uploaded QR code image
        uploaded_file = request.FILES.get('file')  # 'file' is the key for the uploaded image

        if not uploaded_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Open the uploaded image and decode the QR code
            image = Image.open(uploaded_file)
            decoded_objects = decode(image)

            # Check if QR code is decoded successfully
            if not decoded_objects:
                return Response({"error": "No QR code found in the image."}, status=status.HTTP_400_BAD_REQUEST)

            # Extract the NSS from the decoded QR code data
            nss = decoded_objects[0].data.decode('utf-8')  # Get the decoded NSS

            # Retrieve the corresponding patient using the decoded NSS
            try:
                patient = Patient.objects.get(NSS=nss)  # Get the patient by NSS

                # Now, retrieve the associated DPI for that patient
                dpi = DPI.objects.get(patient=patient)

                # Serialize the DPI data along with the Patient details
                serializer = QRSearchSerializer(dpi)

                # Get Patient details
                patient_details = {
                    "id_patient": patient.id_patient,
                    "nom_patient": patient.utilisateur.first_name,
                    "prenom_patient": patient.utilisateur.last_name,
                    "nss": patient.NSS,
                    "date_de_naissance": patient.date_de_naissance,
                    "adresse": patient.adresse,
                    "telephone": patient.telephone,
                    "mutuelle": patient.mutuelle,
                    "personne_a_contacter": patient.personne_a_contacter
                }

                # Add patient details to DPI response
                response_data = serializer.data
                response_data.update(patient_details)

                return Response(response_data, status=status.HTTP_200_OK)

            except Patient.DoesNotExist:
                return Response({"error": "Patient not found for this QR code."}, status=status.HTTP_404_NOT_FOUND)
            except DPI.DoesNotExist:
                return Response({"error": "DPI not found for this patient."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
