from rest_framework import serializers
from alatmusik_app.models import Provinsi, AlatMusik

class AlatMusikSerializer(serializers.ModelSerializer):
    # TAMBAHKAN BARIS INI
    # Ini akan mengambil representasi string (__str__) dari model Provinsi, yaitu namanya.
    provinsi = serializers.StringRelatedField()

    class Meta:
        model = AlatMusik
        # Field 'provinsi' di sini akan merujuk ke StringRelatedField di atas
        fields = ['id', 'nama', 'asal_daerah', 'deskripsi', 'provinsi']

# PERBARUI SERIALIZER INI
class ProvinsiSerializer(serializers.ModelSerializer):
    # Baris ini akan mengambil semua alat musik yang terhubung
    # ke provinsi ini dan menampilkannya dalam daftar.
    alat_musik = AlatMusikSerializer(many=True, read_only=True)

    class Meta:
        model = Provinsi
        # Tambahkan 'alat_musik' ke dalam fields
        fields = ['id', 'nama', 'alat_musik']