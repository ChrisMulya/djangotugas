# alatmusik_app/api/serializers.py

from rest_framework import serializers
from alatmusik_app.models import Provinsi, AlatMusik

class AlatMusikSerializer(serializers.ModelSerializer):
    # Field ini hanya untuk DIBACA (GET).
    provinsi_nama = serializers.CharField(source='provinsi.nama', read_only=True)

    class Meta:
        model = AlatMusik
        fields = [
            'id', 
            'nama', 
            'asal_daerah', 
            'deskripsi', 
            'provinsi',        # Field ini untuk MENULIS (POST/PUT), menerima ID.
            'provinsi_nama'    # Field ini untuk MEMBACA (GET), menampilkan nama.
        ]
        extra_kwargs = {
            'provinsi': {'write_only': True, 'required': True}
        }

class ProvinsiSerializer(serializers.ModelSerializer):
    alat_musik = AlatMusikSerializer(many=True, read_only=True)

    class Meta:
        model = Provinsi
        fields = ['id', 'nama', 'alat_musik']