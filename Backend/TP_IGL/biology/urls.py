from django.urls import path
'''from .views import GetParametreBiologiquesForBilan

urlpatterns = [
  
    path('get-parametres-for-bilan/<int:bilan_id>/', GetParametreBiologiquesForBilan.as_view(), name='get_parametres_for_bilan'),
    
]'''
 
from .views import BilanBioMesureCreationView,Generergraph,GetBilanBiologiquesByDPI,GetBilanBiologiqueByConsultation,GetDPIsWithBiologie

urlpatterns = [
    path('create-bio-measures/', BilanBioMesureCreationView.as_view(), name='create_bio_measures'),
     path('generergraphic/<int:dpi_id>/<int:laborantin_id>/', Generergraph.as_view(), name='generergraphic'),
     path('dpi/<int:dpi_id>/bilans-biologiques/', GetBilanBiologiquesByDPI.as_view(), name='get_bilan_biologiques_by_dpi'),
      path('dpi/<int:consultation_id>/biobilansparconsult/', GetBilanBiologiqueByConsultation.as_view(), name='get_bilan_biologiques_by_CON'),
      path('dpis/', GetDPIsWithBiologie.as_view(), name='get_dpibio')

]

