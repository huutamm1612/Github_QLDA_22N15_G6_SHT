from django.db import models
from UserInterface.models import ChiNhanh

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

class KhuBanAn(models.Model):
    TenKhu = models.CharField(max_length=100)

    def __str__(self):
        return self.TenKhu

class BanAn(models.Model):
    SoBan = models.CharField(max_length=20)  # Số bàn hoặc mã bàn
    TrangThai = models.BooleanField(default=True)  # True: Trống, False: Đã có người
    Khu = models.ForeignKey(KhuBanAn, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bàn {self.SoBan} - {self.Khu.TenKhu}"

class HoaDon(models.Model):
    Ban = models.ForeignKey(BanAn, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    timeout = models.DateTimeField(null=True, blank=True)
    SoLuongNguoi = models.PositiveIntegerField(default=1)
    TongTien = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    TrangThai = models.BooleanField(default=False)  # False: chưa thanh toán, True: đã thanh toán

    def __str__(self):
        return f"Hóa đơn bàn {self.Ban.SoBan} - {'Đã thanh toán' if self.TrangThai else 'Chưa thanh toán'}"

class ChiTietHoaDon(models.Model):
    HoaDon = models.ForeignKey(HoaDon, on_delete=models.CASCADE, related_name='chi_tiet')
    MonAn = models.ForeignKey(MonAn, on_delete=models.CASCADE)
    SoLuong = models.PositiveIntegerField(default=1)
    GhiChu = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.HoaDon} - {self.MonAn} x {self.SoLuong}"

class NhanVien(models.Model):
    ten_nhan_vien = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=20)
    tai_khoan = models.CharField(max_length=100, unique=True)
    mat_khau = models.CharField(max_length=128, default='')
    chi_nhanh = models.ForeignKey(ChiNhanh, on_delete=models.SET_NULL, null=True, blank=True)
    TINH_TRANG_CHOICES = [
        ('on', 'Đang làm'),
        ('off', 'Không làm'),
        ('on_leave', 'Đang nghỉ phép'),
        ('quit', 'Đã nghỉ làm'),
    ]
    tinh_trang = models.CharField(max_length=10, choices=TINH_TRANG_CHOICES, default='off')

    def __str__(self):
        return f"{self.ten_nhan_vien} ({self.tai_khoan})"