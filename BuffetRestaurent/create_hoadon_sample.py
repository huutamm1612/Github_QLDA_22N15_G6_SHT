import random
from datetime import datetime, timedelta
from account.models import BanAn, HoaDon, KhuBanAn

# Lấy hoặc tạo khu và bàn mẫu
khu, _ = KhuBanAn.objects.get_or_create(TenKhu="Khu A")
ban, _ = BanAn.objects.get_or_create(SoBan="1", Khu=khu, defaults={"TrangThai": True})

for i in range(7):
    ngay = datetime.now() - timedelta(days=6-i)
    tong_tien = random.randint(500_000, 3_000_000)
    HoaDon.objects.create(
        Ban=ban,
        time=ngay,
        timeout=ngay,
        SoLuongNguoi=random.randint(2, 8),
        TongTien=tong_tien,
        TrangThai=True
    )
print("Đã tạo dữ liệu hóa đơn cho 7 ngày gần nhất!")
