from django.shortcuts import render

'''# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from gestiondpi.models import BilanBiologique
from .serializers import BilanBiologiqueSerializer, ParametreBiologiqueSerializer

class GetParametreBiologiquesForBilan(APIView):
    def get(self, request, bilan_id):
        # Retrieve the BilanBiologique instance
        try:
            bilan = BilanBiologique.objects.get(id_bilanbiologique=bilan_id)
        except BilanBiologique.DoesNotExist:
            return Response({"error": "BilanBiologique not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the BilanBiologique instance, including linked ParametreBiologique instances
        bilan_serializer = BilanBiologiqueSerializer(bilan)

        return Response(bilan_serializer.data, status=status.HTTP_200_OK)'''
        
        
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from gestiondpi.models import BilanBiologique, ParametreBioMesure, Laborantin,DPI,Consultation
from .serializers import BilanBiologiqueSerializer, ParametreBioMesureSerializer,DPISerializer

class StaticTableHelper:
    @staticmethod
    def get_static_table():
        return [
            {'id': 1, 'nom': 'Glucose', 'unite_mesure': 'mg/dL', 'valeur_normale': '70-99'},
            {'id': 2, 'nom': 'Cholesterol', 'unite_mesure': 'mg/dL', 'valeur_normale': '125-200'},
            {'id': 3, 'nom': 'Blood Pressure', 'unite_mesure': 'mmHg', 'valeur_normale': '120/80'},
            {'id': 4, 'nom': 'Body Temperature', 'unite_mesure': '°C', 'valeur_normale': '36.5-37.5'},
            {'id': 5, 'nom': 'Heart Rate', 'unite_mesure': 'bpm', 'valeur_normale': '60-100'},
            {'id': 6, 'nom': 'Oxygen Saturation', 'unite_mesure': '%', 'valeur_normale': '95-100'},
            {'id': 7, 'nom': 'Weight', 'unite_mesure': 'kg', 'valeur_normale': '60-80'},
        ]
''' test  {
  "bilan_id": 1,
  "laborantin_id": 1,
  "mesure": [
    {"id-mesure": 1, "valeur_mesure": "85", "date_mesure": "2024-12-26"},
    {"id-mesure": 2, "valeur_mesure": "180", "date_mesure": "2024-12-26"}
  ]
}    the response must be something like this {
    "message": "ParametreBioMesure instances created and linked successfully.",
    "created_mesures": [
        {
            "id_parametrebiomesure": 7,
            "nom": "Glucose",
            "unite_mesure": "mg/dL",
            "valeur_normale": "70-99",
            "valeur_mesuree": "85",
            "date_mesure": "2024-12-26",
            "bilan_biologique": 3
        },
        {
            "id_parametrebiomesure": 8,
            "nom": "Cholesterol",
            "unite_mesure": "mg/dL",
            "valeur_normale": "125-200",
            "valeur_mesuree": "180",
            "date_mesure": "2024-12-26",
            "bilan_biologique": 3
        }
    ]
}'''
class BilanBioMesureCreationView(APIView):
    def post(self, request):
        data = request.data
        bilan_id = data.get('bilan_id')
        laborantin_id = data.get('laborantin_id')
        mesure_table = data.get('mesure')

        # Validate that BilanBiologique and Laborantin exist
        try:
            bilan = BilanBiologique.objects.get(id_bilanbiologique=bilan_id)
        except BilanBiologique.DoesNotExist:
            return Response({'error': 'BilanBiologique not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            laborantin = Laborantin.objects.get(id_laborantin=laborantin_id)
        except Laborantin.DoesNotExist:
            return Response({'error': 'Laborantin not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Get static table
        static_table = StaticTableHelper.get_static_table()

        # Process each element in mesure_table
        created_mesures = []
        for mesure in mesure_table:
            id_mesure = mesure.get('id-mesure')
            valeur_mesuree = mesure.get('valeur_mesure')
            date_mesure = mesure.get('date_mesure')

            # Find matching element in the static table
            static_element = next((item for item in static_table if item['id'] == id_mesure), None)
            if not static_element:
                return Response({'error': f'No static element found for id-mesure {id_mesure}.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Create ParametreBioMesure
            parametre_bio_mesure = ParametreBioMesure.objects.create(
                bilan_biologique=bilan,
                nom=static_element['nom'],
                unite_mesure=static_element['unite_mesure'],
                valeur_normale=static_element['valeur_normale'],
                valeur_mesuree=valeur_mesuree,
                date_mesure=date_mesure
            )
            created_mesures.append(parametre_bio_mesure)

        # Link created mesures to BilanBiologique
        bilan.laborantin = laborantin
        bilan.save()

        return Response({
            'message': 'ParametreBioMesure instances created and linked successfully.',
            'created_mesures': ParametreBioMesureSerializer(created_mesures, many=True).data,
        }, status=status.HTTP_201_CREATED)
        
''' applying last function on bilanid =1 and bilanid 2 then test'''       

class Generergraph(APIView):
    def get(self, request, dpi_id, laborantin_id):
        try:
            # Check if the laborantin exists
            laborantin_exists = Laborantin.objects.filter(id_laborantin=laborantin_id).exists()
            if not laborantin_exists:
                return Response({'error': 'Laborantin not found'}, status=status.HTTP_404_NOT_FOUND)

            # Check if the DPI exists
            dpi = DPI.objects.filter(id_dpi=dpi_id).first()
            if not dpi:
                return Response({'error': 'DPI not found'}, status=status.HTTP_404_NOT_FOUND)

            # Get consultations for the given DPI
            consultations = Consultation.objects.filter(dpi=dpi)

            # Initialize list to collect BilanBiologique data
            bilan_biologiques = []
            counter =0 
            bilan_ids=[]

            # Loop through consultations to collect bilan data
            for consultation in consultations:
                bilan_biologique = consultation.bilan_biologique
                if bilan_biologique:  # Ensure bilan_biologique exists
                    # Serialize the BilanBiologique object
                    serializer = BilanBiologiqueSerializer(bilan_biologique)
                    bilan_id = serializer.data.get('id_bilanbiologique')
                    parametres = ParametreBioMesure.objects.filter(bilan_biologique=bilan_id)
                    
                    if parametres.exists():
                      counter+=1
                      bilan_ids.append(bilan_id)
                      
     # Based on the counter, return appropriate response
            if counter == 0:
                return Response({'error': 'No parametres found for the given DPI'}, status=status.HTTP_404_NOT_FOUND)
            
            if counter == 1:
                # Only one BilanBiologique with parametres, return parametres
                bilan_id = bilan_ids[0]  # We can safely access since counter is 1
                parametres = ParametreBioMesure.objects.filter(bilan_biologique=bilan_id)
                parametres_data = [{'nom': param.nom, 'valeur_mesuree': param.valeur_mesuree} for param in parametres]
                parametre_serializer = ParametreBioMesureSerializer(parametres, many=True)
                return Response({
                    'type': 'unaire',
                    'parametres': parametres_data
                })
            if counter > 1:
    # More than one BilanBiologique with parametres
    # Sort and get the two largest IDs
                bilan_ids.sort()
                bilanid1, bilanid2 = bilan_ids[-2], bilan_ids[-1]  # Get the two largest IDs
    
    # Fetch the corresponding BilanBiologique instances
                bilan1 = BilanBiologique.objects.get(id_bilanbiologique=bilanid1)
                bilan2 = BilanBiologique.objects.get(id_bilanbiologique=bilanid2)
    
    # Serialize the BilanBiologique instances
                bilan1_serialized = BilanBiologiqueSerializer(bilan1).data
                bilan2_serialized = BilanBiologiqueSerializer(bilan2).data
  
    # Fetch the corresponding ParametreBioMesure instances
                parametres_bilan1 = ParametreBioMesure.objects.filter(bilan_biologique=bilanid1)
                parametres_bilan2 = ParametreBioMesure.objects.filter(bilan_biologique=bilanid2)
    
    # Create dictionaries for easy comparison
                params_bilan1 = {param.nom: param for param in parametres_bilan1}
                params_bilan2 = {param.nom: param for param in parametres_bilan2}
    
    # Find common noms and build the result table
                common_params = []
                for nom in params_bilan1.keys() & params_bilan2.keys():  # Intersection of keys (common noms)
                         common_params.append({
                              'nom': nom,
                               'mesurebefore': params_bilan1[nom].valeur_mesuree,
                                'mesureafter': params_bilan2[nom].valeur_mesuree,
                             })
    
    # Return the response with the common parameters and serialized bilans
                return Response({
                                     'type': 'binaire',
                                     'parametres': common_params,
                                     'bilan1': bilan1_serialized,
                                      'bilan2': bilan2_serialized
                                      })

             

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        

class GetBilanBiologiquesByDPI(APIView):
    def get(self, request, dpi_id):
        try:
            # Get all consultations for the specified DPI
            consultations = Consultation.objects.filter(dpi_id=dpi_id)

            # Extract all associated BilanBiologique objects from consultations
            bilan_biologiques = BilanBiologique.objects.filter(
                consultations__in=consultations
            ).distinct()  # Avoid duplicates

            # Check if any bilans exist
            if not bilan_biologiques.exists():
                return Response(
                    {'message': 'No biological bilans found for the given DPI.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize and return the BilanBiologiques
            #serializer = BilanBiologiqueSerializer(bilan_biologiques, many=True)
            response_data = [
                {
                    "bilan": BilanBiologiqueSerializer(bilan).data,
                    "consultation_id": Consultation.objects.filter(
                        bilan_biologique=bilan
                    ).values_list('id_consultation', flat=True).first()  # Assuming one consultation per bilan
                }
                for bilan in bilan_biologiques
            ]
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class GetBilanBiologiqueByConsultation(APIView):
    def get(self, request, consultation_id):
        try:
            # Fetch the consultation by ID
            consultation = Consultation.objects.filter(id_consultation=consultation_id).first()

            if not consultation:
                return Response(
                    {'message': 'Consultation not found.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Fetch associated biological bilan
            bilan_biologique = consultation.bilan_biologique

            # Prepare the response
            response_data = {
                "consultation_id": consultation_id,
                "bilan_biologique": BilanBiologiqueSerializer(bilan_biologique).data if bilan_biologique else None,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class GetDPIsWithBiologie(APIView):
    def get(self, request):
        try:
            # Fetch all DPIs with at least one consultation linked to a biological bilan
            dpis_with_biologique = DPI.objects.filter(
                consultations__bilan_biologique__isnull=False
            ).distinct()

            # Check if any DPIs exist
            if not dpis_with_biologique.exists():
                return Response(
                    {'message': 'No DPIs found with biological bilans.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize the DPIs
            serializer = DPISerializer(dpis_with_biologique, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


                