from django.db import models

# Create your models here.

class KhachHang(models.Model):
    ten = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.ten} - {self.so_dien_thoai}"
