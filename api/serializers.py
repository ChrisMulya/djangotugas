# api/serializers.py

from rest_framework import serializers
from alatmusik_app.models import Provinsi, AlatMusik

class AlatMusikSerializer(serializers.ModelSerializer):
    # Field ini hanya untuk DIBACA (read-only).
    # Fungsinya untuk menampilkan nama dari provinsi yang terhubung saat GET request.
    # 'source' memberitahu serializer untuk mengambil nilai dari 'provinsi.nama'.
    provinsi_nama = serializers.CharField(source='provinsi.nama', read_only=True)

    class Meta:
        model = AlatMusik
        fields = [
            'id', 
            'nama', 
            'asal_daerah', 
            'deskripsi', 
            'provinsi',        # Field ini untuk MENULIS (write), menerima ID.
            'provinsi_nama'    # Field ini untuk MEMBACA (read), menampilkan nama.
        ]
        extra_kwargs = {
            # Aturan tambahan untuk field 'provinsi':
            # 1. hanya untuk input, jangan tampilkan di output JSON.
            # 2. field ini wajib diisi saat membuat data baru.
            'provinsi': {'write_only': True, 'required': True}
        }

class ProvinsiSerializer(serializers.ModelSerializer):
    # Serializer ini sudah benar, ia menampilkan daftar alat musik terkait.
    alat_musik = AlatMusikSerializer(many=True, read_only=True)

    class Meta:
        model = Provinsi
        fields = ['id', 'nama', 'alat_musik']