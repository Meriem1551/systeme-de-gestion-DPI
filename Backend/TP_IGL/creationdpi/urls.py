from django.urls import path
from .views import DPICreationView ,QRCodeView , SearchDPIByNSSView ,QRCodeScanView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('create-dpi/', DPICreationView.as_view(), name='create_dpi'),
    path('<int:dpi_id>/qrcode/', QRCodeView.as_view(), name='qr_code_download'),
    path('NssSearch/', SearchDPIByNSSView.as_view(), name='search-dpi-by-nss'),
    path('QRCodeSearch/', QRCodeScanView.as_view(), name='qr-code-search'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)