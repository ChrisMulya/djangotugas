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