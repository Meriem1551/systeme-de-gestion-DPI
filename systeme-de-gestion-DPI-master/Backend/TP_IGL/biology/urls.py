from django.urls import path
'''from .views import GetParametreBiologiquesForBilan

urlpatterns = [
  
    path('get-parametres-for-bilan/<int:bilan_id>/', GetParametreBiologiquesForBilan.as_view(), name='get_parametres_for_bilan'),
    
]'''
 
from .views import BilanBioMesureCreationView,Generergraph

urlpatterns = [
    path('create-bio-measures/', BilanBioMesureCreationView.as_view(), name='create_bio_measures'),
     path('generergraphic/<int:dpi_id>/<int:laborantin_id>/', Generergraph.as_view(), name='generergraphic'),
]

