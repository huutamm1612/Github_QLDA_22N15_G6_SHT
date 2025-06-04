from django.shortcuts import render, get_object_or_404, redirect
from account.models import BanAn, MonAn, LoaiMonAn, HoaDon, ChiTietHoaDon
from django.http import HttpResponseForbidden, JsonResponse

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
