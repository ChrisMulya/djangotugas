from rest_framework import serializers
from alatmusik_app.models import Provinsi, AlatMusik

class AlatMusikSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlatMusik
        fields = ['id', 'nama', 'asal_daerah', 'deskripsi', 'provinsi']

class ProvinsiSerializer(serializers.ModelSerializer):
    alat_musik = AlatMusikSerializer(many=True, read_only=True)

    class Meta:
        model = Provinsi
        fields = ['id', 'nama', 'alat_musik']