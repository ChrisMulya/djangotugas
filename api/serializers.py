from rest_framework import serializers
from alatmusik_app.models import Provinsi, AlatMusik

class AlatMusikSerializer(serializers.ModelSerializer):
    provinsi_nama = serializers.CharField(source='provinsi.nama', read_only=True)

    class Meta:
        model = AlatMusik
        fields = [
            'id', 
            'nama', 
            'asal_daerah', 
            'deskripsi', 
            'provinsi',
            'provinsi_nama' 
        ]
        extra_kwargs = {
            'provinsi': {'write_only': True, 'required': True}
        }

class ProvinsiSerializer(serializers.ModelSerializer):
    alat_musik = AlatMusikSerializer(many=True, read_only=True)

    class Meta:
        model = Provinsi
        fields = ['id', 'nama', 'alat_musik']