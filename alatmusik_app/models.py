from django.db import models 

class Provinsi(models.Model):
    nama = models.CharField(max_length=100, unique=True)
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Provinsi"

class AlatMusik(models.Model):
    nama = models.CharField(max_length=100)
    asal_daerah = models.CharField(max_length=100)
    deskripsi = models.TextField()
    provinsi = models.ForeignKey(Provinsi, related_name='alat_musik', on_delete=models.CASCADE)
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name_plural = "Alat Musik"