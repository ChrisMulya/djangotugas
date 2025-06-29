# api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from alatmusik_app.models import Provinsi, AlatMusik
from .serializers import ProvinsiSerializer, AlatMusikSerializer

class AlatMusikListApiView(APIView):
    def get(self, request, *args, **kwargs):
        alat_musik_list = AlatMusik.objects.all()
        serializer = AlatMusikSerializer(alat_musik_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # PERBAIKAN: Langsung teruskan semua data dari request ke serializer.
        # Ini lebih sederhana dan akan bekerja dengan serializer kompleks kita.
        serializer = AlatMusikSerializer(data=request.data)
        
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
    def get_object(self, id):
        try:
            return AlatMusik.objects.get(id=id)
        except AlatMusik.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        alat_musik_instance = self.get_object(id)
        if not alat_musik_instance:
            return Response(
                {"status": status.HTTP_404_NOT_FOUND, "message": "Data alat musik tidak ditemukan."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AlatMusikSerializer(alat_musik_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        alat_musik_instance = self.get_object(id)
        if not alat_musik_instance:
            return Response(
                {"status": status.HTTP_404_NOT_FOUND, "message": "Data alat musik tidak ditemukan."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # PERBAIKAN: Langsung teruskan request.data untuk update.
        # 'partial=True' memungkinkan ini berfungsi sebagai PATCH juga.
        serializer = AlatMusikSerializer(instance=alat_musik_instance, data=request.data, partial=True)
        
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
        # Memanggil method put yang sudah fleksibel
        return self.put(request, id, *args, **kwargs)

    def delete(self, request, id, *args, **kwargs):
        alat_musik_instance = self.get_object(id)
        if not alat_musik_instance:
            return Response(
                {"status": status.HTTP_404_NOT_FOUND, "message": "Data alat musik tidak ditemukan."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        alat_musik_instance.delete()
        response = {
            'status': status.HTTP_200_OK,
            'message': 'Data alat musik berhasil dihapus.'
        }
        return Response(response, status=status.HTTP_200_OK)

# --- Kelas untuk Provinsi sudah benar, tidak perlu diubah ---

class ProvinsiListApiView(APIView):
    def get(self, request, *args, **kwargs):
        provinsi_list = Provinsi.objects.all()
        serializer = ProvinsiSerializer(provinsi_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProvinsiSerializer(data=request.data)
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
        provinsi_instance = self.get_object(id)
        if not provinsi_instance:
            return Response(
                {"status": 404, "message": "Data provinsi tidak ditemukan."},
                status=status.HTTP_404_NOT_FOUND
            )
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
        provinsi_instance = self.get_object(id)
        if not provinsi_instance:
            return Response(
                {"status": 404, "message": "Data provinsi tidak ditemukan."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProvinsiSerializer(instance=provinsi_instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 200,
                'message': 'Data provinsi berhasil diperbarui.',
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, *args, **kwargs):
        return self.put(request, id, *args, **kwargs)