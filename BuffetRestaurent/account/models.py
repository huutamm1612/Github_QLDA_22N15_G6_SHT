from django.db import models

# Create your models here.

class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class LoaiMonAn(models.Model):
    TenLoaiMon = models.CharField(max_length=100)

    def __str__(self):
        return self.TenLoaiMon

class MonAn(models.Model):
    IdLoaiMonAn = models.ForeignKey(LoaiMonAn, on_delete=models.CASCADE)
    TenMonAn = models.CharField(max_length=100)
    Anh = models.CharField(max_length=255)  # Đổi sang CharField để lưu đường dẫn ảnh
    DonGia = models.DecimalField(max_digits=12, decimal_places=2)
    TrangThai = models.BooleanField(default=True)  # Luôn mặc định là còn

    def __str__(self):
        return self.TenMonAn
