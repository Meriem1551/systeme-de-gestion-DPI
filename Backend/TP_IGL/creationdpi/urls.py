from django.urls import path

from .views import  SearchDPIByNSSView ,QRCodeScanView

from .views import DPICreationView ,QRCodeView , DPIListView ,DPIDetailView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-dpi/', DPICreationView.as_view(), name='create_dpi'),
    path('<int:dpi_id>/qrcode/', QRCodeView.as_view(), name='qr_code_download'),

    path('NssSearch/', SearchDPIByNSSView.as_view(), name='search-dpi-by-nss'),
    path('QRCodeSearch/', QRCodeScanView.as_view(), name='qr-code-search'),


    
    path('dpis/', DPIListView.as_view(), name='dpi-list'),
    path('dpis/<int:pk>/', DPIDetailView.as_view(), name='dpi-detail'),


    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
