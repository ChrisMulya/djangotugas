# alatmusik_app/api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from alatmusik_app.models import Provinsi, AlatMusik
from .serializers import ProvinsiSerializer, AlatMusikSerializer

# ===============================================
# Views untuk Alat Musik
# ===============================================

class AlatMusikListApiView(APIView):
    """
    API View untuk menampilkan daftar semua alat musik (GET) dan
    membuat entri alat musik baru (POST).
    """

    def get(self, request, *args, **kwargs):
        """
        Mengembalikan daftar semua objek AlatMusik.
        """
        alat_musik_list = AlatMusik.objects.all()
        serializer = AlatMusikSerializer(alat_musik_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Membuat objek AlatMusik baru.
        """
        data = {
            'nama': request.data.get('nama'),
            'asal_daerah': request.data.get('asal_daerah'),
            'deskripsi': request.data.get('deskripsi'),
            'provinsi': request.data.get('provinsi'),
        }
        serializer = AlatMusikSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_201_CREATED,
                'message': 'Data alat musik berhasil dibuat.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlatMusikDetailApiView(APIView):
    """
    API View untuk mengambil (GET), memperbarui (PUT), dan menghapus (DELETE)
    satu objek AlatMusik.
    """

    def get_object(self, id):
        """
        Helper method untuk mendapatkan objek berdasarkan ID atau mengembalikan None.
        """
        try:
            return AlatMusik.objects.get(id=id)
        except AlatMusik.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        """
        Mengambil dan mengembalikan satu objek AlatMusik.
        """
        alat_musik_instance = self.get_object(id)
        if not alat_musik_instance:
            return Response(
                {"status": status.HTTP_404_NOT_FOUND, "message": "Data alat musik tidak ditemukan.", "data": {}},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AlatMusikSerializer(alat_musik_instance)
        response = {
            'status': status.HTTP_200_OK,
            'message': 'Data alat musik berhasil diambil.',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        """
        Memperbarui satu objek AlatMusik.
        """
        alat_musik_instance = self.get_object(id)
        if not alat_musik_instance:
            return Response(
                {"status": status.HTTP_404_NOT_FOUND, "message": "Data alat musik tidak ditemukan.", "data": {}},
                status=status.HTTP_404_NOT_FOUND
            )
        
        data = {
            'nama': request.data.get('nama'),
            'asal_daerah': request.data.get('asal_daerah'),
            'deskripsi': request.data.get('deskripsi'),
            'provinsi': request.data.get('provinsi'),
        }
        
        # `partial=True` memungkinkan pembaruan PATCH (hanya field tertentu)
        serializer = AlatMusikSerializer(instance=alat_musik_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_200_OK,
                'message': 'Data alat musik berhasil diperbarui.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        return self.put(request, id, *args, **kwargs)

    def delete(self, request, id, *args, **kwargs):
        """
        Menghapus satu objek AlatMusik.
        """
        alat_musik_instance = self.get_object(id)
        if not alat_musik_instance:
            return Response(
                {"status": status.HTTP_404_NOT_FOUND, "message": "Data alat musik tidak ditemukan.", "data": {}},
                status=status.HTTP_404_NOT_FOUND
            )
        
        alat_musik_instance.delete()
        response = {
            'status': status.HTTP_200_OK,
            'message': 'Data alat musik berhasil dihapus.'
        }
        return Response(response, status=status.HTTP_200_OK)

# ===============================================
# Views untuk Provinsi (Opsional, tapi direkomendasikan)
# ===============================================

class ProvinsiListApiView(APIView):
    """
    API View untuk menampilkan daftar semua provinsi (GET) dan
    membuat entri provinsi baru (POST).
    """
    def get(self, request, *args, **kwargs):
        provinsi_list = Provinsi.objects.all()
        serializer = ProvinsiSerializer(provinsi_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {'nama': request.data.get('nama')}
        serializer = ProvinsiSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': status.HTTP_201_CREATED,
                'message': 'Data provinsi berhasil dibuat.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProvinsiDetailApiView(APIView):
    def get_object(self, id):
        try:
            # Kita ingin mengambil provinsi beserta data alat musik terkait
            return Provinsi.objects.prefetch_related('alat_musik').get(id=id)
        except Provinsi.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        provinsi_instance = self.get_object(id)
        if not provinsi_instance:
            return Response({"status": 404, "message": "Provinsi tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProvinsiSerializer(provinsi_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id, *args, **kwargs):
        """
        Menghapus satu objek Provinsi.
        """
        provinsi_instance = self.get_object(id)
        if not provinsi_instance:
            return Response(
                {"status": 404, "message": "Data provinsi tidak ditemukan."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Cek apakah ada Alat Musik yang masih terhubung
        if provinsi_instance.alat_musik.count() > 0:
            return Response(
                {"status": 400, "message": "Hapus Gagal: Masih ada data alat musik yang terhubung ke provinsi ini."},
                status=status.HTTP_400_BAD_REQUEST
            )

        provinsi_instance.delete()
        response = {
            'status': 200,
            'message': 'Data provinsi berhasil dihapus.'
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        """
        Memperbarui satu objek Provinsi.
        """
        provinsi_instance = self.get_object(id)
        if not provinsi_instance:
            return Response(
                {"status": 404, "message": "Data provinsi tidak ditemukan."},
                status=status.HTTP_404_NOT_FOUND
            )

        data = {'nama': request.data.get('nama')}
        serializer = ProvinsiSerializer(instance=provinsi_instance, data=data, partial=True)
        
        # Cek apakah serializer valid
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 200,
                'message': 'Data provinsi berhasil diperbarui.',
                'data': serializer.data
            }
            # Jika valid, kembalikan respons sukses
            return Response(response, status=status.HTTP_200_OK)

        # PASTIKAN BARIS INI ADA DAN INDENTASINYA BENAR
        # Jika tidak valid, kembalikan respons error dari serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        """
        Memanggil method PUT untuk menangani PATCH request.
        """
        return self.put(request, id, *args, **kwargs)