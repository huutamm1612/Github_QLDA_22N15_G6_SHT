from django.shortcuts import render, get_object_or_404, redirect
from account.models import BanAn, MonAn, LoaiMonAn, HoaDon, ChiTietHoaDon
from django.http import HttpResponseForbidden, JsonResponse
from .models import ChiNhanh, DatBan
from datetime import datetime
from django.utils import timezone

def goi_mon_view(request, ban_id):
    ban = get_object_or_404(BanAn, id=ban_id)
    # Chỉ cho phép truy cập nếu bàn đang mở (TrangThai=False)
    if ban.TrangThai:
        return HttpResponseForbidden('Bàn này chưa được mở!')
    # Kiểm tra nếu đã có thiết bị truy cập (dùng session)
    session_key = f"ban_{ban_id}_active"
    if not request.session.get(session_key):
        # Nếu chưa có session, đánh dấu thiết bị này là đang truy cập bàn này
        request.session[session_key] = True
    else:
        # Nếu đã có session, cho phép tiếp tục
        pass
    # Nếu có thiết bị khác truy cập (session khác), có thể kiểm tra thêm bằng DB nếu muốn
    # Lấy danh sách món ăn
    selected_loai = request.GET.get('loai', '')
    # Lấy hóa đơn chưa thanh toán của bàn này
    hoadon = HoaDon.objects.filter(Ban=ban, TrangThai=False).order_by('-time').first()
    if request.method == 'POST' and hoadon:
        monan_id = request.POST.get('monan_id')
        so_luong = int(request.POST.get('so_luong', 1))
        monan = get_object_or_404(MonAn, id=monan_id)
        # Nếu đã có món này trong hóa đơn thì cộng dồn số lượng
        chitiet, created = ChiTietHoaDon.objects.get_or_create(HoaDon=hoadon, MonAn=monan, defaults={'SoLuong': so_luong})
        if not created:
            chitiet.SoLuong += so_luong
            chitiet.save()
        return redirect(request.path + f'?loai={selected_loai}' if selected_loai else request.path)
    loai_monan_list = LoaiMonAn.objects.all().order_by('TenLoaiMon')
    data = []
    for loai in loai_monan_list:
        monan = MonAn.objects.filter(IdLoaiMonAn=loai, TrangThai=True)
        data.append({'loai': loai, 'monan_list': monan})
    context = {
        'ban': ban,
        'data': data,
        'selected_loai': selected_loai,
    }
    return render(request, 'goi_mon.html', context)

def xem_hoa_don_view(request, ban_id):
    ban = get_object_or_404(BanAn, id=ban_id)
    hoadon = HoaDon.objects.filter(Ban=ban, TrangThai=False).order_by('-time').first()
    if request.GET.get('ajax') == '1':
        if not hoadon:
            return JsonResponse({'success': False, 'message': 'Không có hóa đơn chưa thanh toán cho bàn này.'})
        items = []
        tong_tien = 0
        for ct in hoadon.chi_tiet.all():
            tt = ct.SoLuong * ct.MonAn.DonGia
            tong_tien += tt
            items.append({
                'ten': ct.MonAn.TenMonAn,
                'soluong': ct.SoLuong,
                'dongia': f"{ct.MonAn.DonGia:,.0f} VNĐ",
                'thanhtien': f"{tt:,.0f} VNĐ",
            })
        return JsonResponse({'success': True, 'items': items, 'tong_tien': f"{tong_tien:,.0f} VNĐ"})
    if request.GET.get('thanh_toan') == '1' and request.method == 'POST':
        if not hoadon:
            return JsonResponse({'success': False, 'message': 'Không có hóa đơn để thanh toán.'})
        # Tính lại tổng tiền thực tế các món
        tong_tien = 0
        for ct in hoadon.chi_tiet.all():
            tong_tien += ct.SoLuong * ct.MonAn.DonGia
        hoadon.TongTien = tong_tien
        from django.utils import timezone
        hoadon.timeout = timezone.now()  # Ghi nhận thời điểm thanh toán
        hoadon.TrangThai = True
        hoadon.save()
        ban.TrangThai = True
        ban.save()
        return JsonResponse({'success': True})
    chitiet_list = []
    tong_tien = 0
    if hoadon:
        chitiet_list = hoadon.chi_tiet.all()
        for ct in hoadon.chi_tiet.all():
            tt = ct.SoLuong * ct.MonAn.DonGia
            tong_tien += tt
            
    context = {'ban': ban, 'hoadon': hoadon, 'chitiet_list': hoadon.chi_tiet.all(), 'tong_tien': tong_tien}
    return render(request, 'xem_hoa_don.html', context)

def home_user_view(request):
    return render(request, 'home_user.html')

def uu_dai_view(request):
    return render(request, 'uu_dai.html')

def thuc_don_view(request):
    selected_loai = request.GET.get('loai')
    loai_monan_list = LoaiMonAn.objects.all().order_by('TenLoaiMon')
    if not selected_loai:
        bo_loai = LoaiMonAn.objects.filter(TenLoaiMon__icontains='bò').first()
        if bo_loai:
            selected_loai = bo_loai.id
        else:
            selected_loai = None
    if selected_loai:
        monan_list = MonAn.objects.filter(IdLoaiMonAn_id=selected_loai, TrangThai=True)
        try:
            selected_loai = int(selected_loai)
        except:
            selected_loai = None
    else:
        monan_list = MonAn.objects.filter(TrangThai=True)
        selected_loai = None
    context = {
        'loai_monan_list': loai_monan_list,
        'monan_list': monan_list,
        'selected_loai': selected_loai,
        'active_tab': 'thuc_don',
    }
    return render(request, 'thuc_don.html', context)

def dat_ban_view(request):
    if request.method == 'POST':
        ten_khach_hang = request.POST.get('ten_khach_hang')
        so_dien_thoai = request.POST.get('so_dien_thoai')
        thoi_gian = request.POST.get('thoi_gian')
        chi_nhanh_id = request.POST.get('chi_nhanh_id')
        try:
            chi_nhanh = ChiNhanh.objects.get(id=chi_nhanh_id)
            thoi_gian_dt = datetime.strptime(thoi_gian, "%Y-%m-%dT%H:%M")
            thoi_gian_aware = timezone.make_aware(thoi_gian_dt, timezone.get_current_timezone())
            DatBan.objects.create(
                ten_khach_hang=ten_khach_hang,
                so_dien_thoai=so_dien_thoai,
                thoi_gian=thoi_gian_aware,
                chi_nhanh=chi_nhanh,
                trang_thai='chua_den',
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    branches = ChiNhanh.objects.all()
    return render(request, 'dat_ban.html', {'branches': branches})
