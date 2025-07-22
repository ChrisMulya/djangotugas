from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'
urlpatterns = [
    # Provinsi
    path('provinsi/', views.ProvinsiListApiView.as_view(), name='provinsi-list'),
    path('provinsi/<int:id>/', views.ProvinsiDetailApiView.as_view(), name='provinsi-detail'),

    # Alat Musik
    path('alatmusik/', views.AlatMusikListApiView.as_view(), name='alatmusik-list'),
    path('alatmusik/<int:id>/', views.AlatMusikDetailApiView.as_view(), name='alatmusik-detail'),
]