from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'
urlpatterns = [
    # URL untuk Provinsi
    path('provinsi/', views.ProvinsiListApiView.as_view(), name='provinsi-list'),
    # URL untuk Alat Musik
    path('alatmusik/', views.AlatMusikListApiView.as_view(), name='alatmusik-list'),
    path('alatmusik/<int:id>/', views.AlatMusikDetailApiView.as_view(), name='alatmusik-detail'),
]