from django.urls import path
from .views import DPICreationView ,QRCodeView 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('create-dpi/', DPICreationView.as_view(), name='create_dpi'),
    path('<int:dpi_id>/qrcode/', QRCodeView.as_view(), name='qr_code_download'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
