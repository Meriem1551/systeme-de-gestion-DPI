from django.urls import path
from .views import UpdateBilanRadiologiqueView,GetBilanRadiologiqueByDPI,GetBilanRadiologiqueByConsultation,GetDPIsWithRadio

urlpatterns = [
    # Add your other paths here
    path('bilan_radiologique/<int:bilan_id>/update/', UpdateBilanRadiologiqueView.as_view(), name='update_bilan_radiologique'),
    path('dpi/<int:dpi_id>/radiological-bilans/', GetBilanRadiologiqueByDPI.as_view(), name='get_bilan_radiologique_by_dpi'),
     path('dpi/<int:consultation_id>/bilanparconsult/', GetBilanRadiologiqueByConsultation.as_view(), name='get_bilan_byconsultation'),
       path('dpis/', GetDPIsWithRadio.as_view(), name='getdpiradio'),
     

]

