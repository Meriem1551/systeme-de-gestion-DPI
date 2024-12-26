from django.urls import path
from .views import UpdateBilanRadiologiqueView

urlpatterns = [
    # Add your other paths here
    path('bilan_radiologique/<int:bilan_id>/update/', UpdateBilanRadiologiqueView.as_view(), name='update_bilan_radiologique'),
]

