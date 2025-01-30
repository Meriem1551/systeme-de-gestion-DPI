from django.urls import path
from .views import AjouterConsultation,RemplirSoin,GetPatients,GetSoins,GetConsultations,GetOrdonnance,GetResume,ValiderOrdonnance

urlpatterns =[
    path('ajouterConsultation/',AjouterConsultation.as_view(),name='ajouter_consultation'),
    path('remplirSoin/',RemplirSoin.as_view(),name='remplir_Soin'),
    path('getPatients/',GetPatients.as_view(),name='get_patients'),
    path('getSoins/',GetSoins.as_view(),name='get_soins'),
    path('getConsultations/',GetConsultations.as_view(),name='get_consultations'),
    path('getOrdonnance/',GetOrdonnance.as_view(),name='get_ordonnance'),
    path('getResume/',GetResume.as_view(),name='get_resume'),
    path('validerOrdonnance/',ValiderOrdonnance.as_view(),name='valider_ordonnance')

]

