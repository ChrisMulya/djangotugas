from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'
urlpatterns = [
    path('provinsi/', views.ProvinsiListCreate.as_view(), name='provinsi-list-create'),
    path('provinsi/<int:pk>/', views.ProvinsiDetail.as_view(), name='provinsi-detail'),
    path('alatmusik/', views.AlatMusikListCreate.as_view(), name='alatmusik-list-create'),
    path('alatmusik/<int:pk>/', views.AlatMusikDetail.as_view(), name='alatmusik-detail'),
]