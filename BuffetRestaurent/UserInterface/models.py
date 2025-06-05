from django.db import models

# Create your models here.

class KhachHang(models.Model):
    ten = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.ten} - {self.so_dien_thoai}"


class ChiNhanh(models.Model):
    ten_chi_nhanh = models.CharField(max_length=100)
    dia_chi = models.CharField(max_length=255)
    so_dien_thoai = models.CharField(max_length=20)
    gio_mo = models.TimeField()
    gio_dong = models.TimeField()

    def __str__(self):
        return self.ten_chi_nhanh


class DatBan(models.Model):
    TRANG_THAI_CHOICES = [
        ('chua_den', 'Chưa đến'),
        ('da_den', 'Đã đến'),
        ('da_huy', 'Đã hủy'),
    ]
    ten_khach_hang = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=20)
    thoi_gian = models.DateTimeField()
    chi_nhanh = models.ForeignKey('ChiNhanh', on_delete=models.CASCADE)
    trang_thai = models.CharField(max_length=10, choices=TRANG_THAI_CHOICES, default='chua_den')

    def __str__(self):
        return f"{self.ten_khach_hang} - {self.so_dien_thoai} ({self.get_trang_thai_display()})"
