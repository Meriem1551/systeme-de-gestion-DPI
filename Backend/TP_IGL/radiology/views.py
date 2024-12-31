from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from gestiondpi.models import BilanRadiologique, RadiologyImage,Consultation,DPI
from .serializers import BilanRadiologiqueSerializer, RadiologyImageSerializer,ConsultationSerializer,DPISerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser

''' for testing add to headers Content-Type  key with value  multipart/form-data then test on formdata not row
the response must be something like this {
    "bilan_radiologique": {
        "id_bilanradiologique": 1,
        "description": "'descriptionupdated'",
        "type": "'xray'",
        "compte_rendu": "\"conmpte rendu\"",
        "radiologue": "1",
        "images": [
            {
                "id_image": 1,
                "image": "/media/radiologies/meeer.PNG"
            },
            {
                "id_image": 2,
                "image": "/media/radiologies/meeer_yEP1Lm7.PNG"
            },
            {
                "id_image": 3,
                "image": "/media/radiologies/merde.PNG"
            },
            {
                "id_image": 4,
                "image": "/media/radiologies/merde_SmcOkot.PNG"
            },
            {
                "id_image": 5,
                "image": "/media/radiologies/merde_zks5PNV.PNG"
            },
            {
                "id_image": 6,
                "image": "/media/radiologies/merde_Ed9tBdc.PNG"
            },
            {
                "id_image": 7,
                "image": "/media/radiologies/radio5.png"
            },
            {
                "id_image": 8,
                "image": "/media/radiologies/radio4.png"
            },
            {
                "id_image": 9,
                "image": "/media/radiologies/radio4_eY11HkY.png"
            },
            {
                "id_image": 10,
                "image": "/media/radiologies/radio4_8nboQdy.png"
            },
            {
                "id_image": 11,
                "image": "/media/radiologies/radio3.png"
            },
            {
                "id_image": 12,
                "image": "/media/radiologies/radio3_5AlA0Jw.png"
            }
        ]
    },
    "images": [
        "/media/radiologies/meeer.PNG",
        "/media/radiologies/meeer_yEP1Lm7.PNG",
        "/media/radiologies/merde.PNG",
        "/media/radiologies/merde_SmcOkot.PNG",
        "/media/radiologies/merde_zks5PNV.PNG",
        "/media/radiologies/merde_Ed9tBdc.PNG",
        "/media/radiologies/radio5.png",
        "/media/radiologies/radio4.png",
        "/media/radiologies/radio4_eY11HkY.png",
        "/media/radiologies/radio4_8nboQdy.png",
        "/media/radiologies/radio3.png",
        "/media/radiologies/radio3_5AlA0Jw.png"
    ]
}

'''

class UpdateBilanRadiologiqueView(APIView):
    def put(self, request, bilan_id):
        try:
            # Get the BilanRadiologique instance
            bilan = BilanRadiologique.objects.get(id_bilanradiologique=bilan_id)

            # Update `compte_rendu` and `radiologue` fields if provided
            if 'compte_rendu' in request.data:
                bilan.compte_rendu = request.data['compte_rendu']
            if 'radiologue' in request.data:
                bilan.radiologue_id = request.data['radiologue']
            bilan.save()

            # Handle the image field
            if 'image' in request.FILES:
                image = request.FILES['image']
                RadiologyImage.objects.create(image=image, bilan_radiologique=bilan)

            # Serialize the updated instance
            
            
            related_images = RadiologyImage.objects.filter(bilan_radiologique=bilan)
            image_urls = [f"{settings.MEDIA_URL}{image.image}" for image in related_images]
            serializer = BilanRadiologiqueSerializer(bilan)
            return Response({
                "bilan_radiologique": serializer.data,
                "images": image_urls  # URLs of all related images
            }, status=status.HTTP_200_OK)

        except BilanRadiologique.DoesNotExist:
            return Response({'error': 'BilanRadiologique not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetBilanRadiologiqueByDPI(APIView):
    def get(self, request, dpi_id):
        try:
            # Get consultations for the given DPI that have a bilan_radiologique
            consultations_with_bilan = Consultation.objects.filter(
                dpi_id=dpi_id, bilan_radiologue__isnull=False
            )

            if not consultations_with_bilan.exists():
                return Response(
                    {'message': 'No radiological bilans found for the given DPI.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Extract the associated bilan radiologique objects
           
            bilans_radiologiques = [
                {
                    "consultation_id": consultation.id_consultation,
                    "bilan_radiologique": BilanRadiologiqueSerializer(
                        consultation.bilan_radiologue
                    ).data
                }
                for consultation in consultations_with_bilan
            ]

            # Serialize the bilans
            #serializer = BilanRadiologiqueSerializer(bilans_radiologiques, many=True)
            return Response( bilans_radiologiques, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class GetBilanRadiologiqueByConsultation(APIView):
    def get(self, request, consultation_id):
        try:
            # Fetch the consultation by ID
            consultation = Consultation.objects.filter(id_consultation=consultation_id).first()

            if not consultation:
                return Response(
                    {'message': 'Consultation not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Fetch associated radiological bilan
            bilan_radiologique = consultation.bilan_radiologue

            # Prepare the response
            response_data = {
                "consultation_id": consultation_id,
                "bilan_radiologique": BilanRadiologiqueSerializer(bilan_radiologique).data if bilan_radiologique else None,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



'''

class GetDPIsWithRadiologicalBilans(APIView):
    def get(self, request):
        try:
            # Fetch all DPIs with at least one consultation linked to a radiological bilan
            dpis_with_bilan = DPI.objects.filter(
                consultations__bilan_radiologue__isnull=False
            ).distinct()

            # Check if any DPIs exist
            if not dpis_with_bilan.exists():
                return Response(
                    {'message': 'No DPIs found with radiological bilans.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize the DPIs
            dpis_data = [{"id_dpi": dpi.id_dpi} for dpi in dpis_with_bilan]

            return Response(dpis_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)'''


class GetDPIsWithRadio(APIView):
    def get(self, request):
        try:
            # Fetch all DPIs with at least one consultation linked to a radiological bilan
            dpis_with_bilan = DPI.objects.filter(
                consultations__bilan_radiologue__isnull=False
            ).distinct()

            # Check if any DPIs exist
            if not dpis_with_bilan.exists():
                return Response(
                    {'message': 'No DPIs found with radiological bilans.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize the DPIs with nested patient and utilisateur details
            serializer = DPISerializer(dpis_with_bilan, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
