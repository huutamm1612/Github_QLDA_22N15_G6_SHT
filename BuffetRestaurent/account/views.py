from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, MonAn, LoaiMonAn, KhuBanAn, BanAn, HoaDon, NhanVien
from django import forms
from django.conf import settings
import os
import qrcode
import io
import base64
from django.db.models import Sum
from django.db.models.functions import TruncDate

class MonAnForm(forms.ModelForm):
    class Meta:
        model = MonAn
        fields = ['IdLoaiMonAn', 'TenMonAn', 'Anh', 'DonGia', 'TrangThai']
        labels = {
            'IdLoaiMonAn': 'Loại món ăn',
            'TenMonAn': 'Tên món ăn',
            'Anh': 'Ảnh (tải lên)',
            'DonGia': 'Đơn giá',
            'TrangThai': 'Trạng thái (Còn/Hết)',
        }
    Anh = forms.ImageField(label='Ảnh (tải lên)', required=False)

    def save(self, commit=True):
        instance = super().save(commit=False)
        image = self.cleaned_data.get('Anh')
        if image:
            image_path = os.path.join('uploads', image.name)
            full_path = os.path.join(settings.MEDIA_ROOT, image_path)
            with open(full_path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            instance.Anh = os.path.join(settings.MEDIA_URL, image_path).replace('\\', '/')
        if commit:
            instance.save()
        return instance

class LoaiMonAnForm(forms.ModelForm):
    class Meta:
        model = LoaiMonAn
        fields = ['TenLoaiMon']
        labels = {'TenLoaiMon': 'Tên loại món ăn'}

class KhuBanAnForm(forms.ModelForm):
    class Meta:
        model = KhuBanAn
        fields = ['TenKhu']
        labels = {'TenKhu': 'Tên khu vực'}

class BanAnForm(forms.ModelForm):
    class Meta:
        model = BanAn
        fields = ['SoBan', 'TrangThai', 'Khu']
        labels = {
            'SoBan': 'Số bàn',
            'TrangThai': 'Trạng thái (Trống/Đã có người)',
            'Khu': 'Khu vực',
        }

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            account = Account.objects.get(username=username, password=password)
            # Đăng nhập thành công, chuyển hướng sang trang home
            request.session['account_id'] = account.id
            return redirect('home')
        except Account.DoesNotExist:
            error = 'Tên đăng nhập hoặc mật khẩu không đúng.'
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    request.session.flush()
    return redirect('login')

def danh_sach_mon_an_view(request):
    selected_loai = request.GET.get('loai', '')
    loai_monan_list = LoaiMonAn.objects.all().order_by('TenLoaiMon')
    data = []
    for loai in loai_monan_list:
        monan = MonAn.objects.filter(IdLoaiMonAn=loai).order_by('TenMonAn')
        data.append({'loai': loai, 'monan_list': monan})
    return render(request, 'danh_sach_mon_an.html', {
        'data': data,
        'all_loai_monan': loai_monan_list,
        'selected_loai': selected_loai
    })

def welcome_view(request):
    return render(request, 'welcome.html')

def them_monan_view(request):
    if request.method == 'POST':
        form = MonAnForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_mon_an')
    else:
        form = MonAnForm(initial={'TrangThai': True})
    return render(request, 'them_monan.html', {'form': form})

def them_loaimonan_view(request):
    if request.method == 'POST':
        form = LoaiMonAnForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_mon_an')
    else:
        form = LoaiMonAnForm()
    return render(request, 'them_loaimonan.html', {'form': form})

def capnhat_trangthai_monan_view(request, monan_id):
    monan = get_object_or_404(MonAn, id=monan_id)
    monan.TrangThai = not monan.TrangThai
    monan.save()
    return redirect('danh_sach_mon_an')

def xoa_monan_view(request, monan_id):
    monan = get_object_or_404(MonAn, id=monan_id)
    if request.method == 'POST':
        monan.delete()
        return redirect('danh_sach_mon_an')
    return redirect('danh_sach_mon_an')

def sua_monan_view(request, monan_id):
    monan = get_object_or_404(MonAn, id=monan_id)
    if request.method == 'POST':
        form = MonAnForm(request.POST, request.FILES, instance=monan)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_mon_an')
    else:
        form = MonAnForm(instance=monan)
    return render(request, 'them_monan.html', {'form': form, 'is_update': True, 'monan': monan})

def danh_sach_ban_an_view(request):
    khu_list = KhuBanAn.objects.all().order_by('TenKhu')
    data = []
    for khu in khu_list:
        banan = BanAn.objects.filter(Khu=khu).order_by('SoBan')
        data.append({'khu': khu, 'banan_list': banan})
    return render(request, 'danh_sach_ban_an.html', {'data': data, 'all_khu': khu_list})

def them_khu_view(request):
    if request.method == 'POST':
        form = KhuBanAnForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_ban_an')
    else:
        form = KhuBanAnForm()
    return render(request, 'them_khu.html', {'form': form})

def sua_khu_view(request, khu_id):
    khu = get_object_or_404(KhuBanAn, id=khu_id)
    if request.method == 'POST':
        form = KhuBanAnForm(request.POST, instance=khu)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_ban_an')
    else:
        form = KhuBanAnForm(instance=khu)
    return render(request, 'them_khu.html', {'form': form, 'is_update': True, 'khu': khu})

def xoa_khu_view(request, khu_id):
    khu = get_object_or_404(KhuBanAn, id=khu_id)
    if request.method == 'POST':
        khu.delete()
        return redirect('danh_sach_ban_an')
    return redirect('danh_sach_ban_an')

def them_ban_an_view(request):
    if request.method == 'POST':
        form = BanAnForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_ban_an')
    else:
        form = BanAnForm()
    return render(request, 'them_ban_an.html', {'form': form})

def sua_ban_an_view(request, ban_id):
    ban = get_object_or_404(BanAn, id=ban_id)
    if request.method == 'POST':
        form = BanAnForm(request.POST, instance=ban)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_ban_an')
    else:
        form = BanAnForm(instance=ban)
    return render(request, 'them_ban_an.html', {'form': form, 'is_update': True, 'ban': ban})

def xoa_ban_an_view(request, ban_id):
    ban = get_object_or_404(BanAn, id=ban_id)
    if request.method == 'POST':
        ban.delete()
        return redirect('danh_sach_ban_an')
    return redirect('danh_sach_ban_an')

def home_view(request):
    return render(request, 'home.html')

def mo_ban_view(request):
    khu_id = request.GET.get('khu')
    all_khu = KhuBanAn.objects.all().order_by('TenKhu')
    selected_khu = None
    banan_list = []
    qr_code_base64 = None
    goi_mon_url = None
    opened_ban = None
    success_message = None
    if khu_id:
        selected_khu = KhuBanAn.objects.filter(id=khu_id).first()
        if selected_khu:
            banan_list = BanAn.objects.filter(Khu=selected_khu).order_by('SoBan')
    context = {
        'all_khu': all_khu,
        'selected_khu': selected_khu,
        'banan_list': banan_list,
    }
    if request.method == 'POST':
        ban_id = request.POST.get('ban_id')
        so_nguoi = request.POST.get('so_nguoi')
        if ban_id and so_nguoi:
            ban = get_object_or_404(BanAn, id=ban_id)
            # Kiểm tra nếu bàn đã có hóa đơn chưa thanh toán thì không mở tiếp
            if HoaDon.objects.filter(Ban=ban, TrangThai=False).exists():
                context['error'] = f"Bàn {ban.SoBan} đã có hóa đơn chưa thanh toán!"
            else:
                ban.TrangThai = False
                ban.save()
                hoadon = HoaDon.objects.create(Ban=ban, SoLuongNguoi=so_nguoi, TrangThai=False)
                # Tạo link gọi món
                goi_mon_url = request.build_absolute_uri(f"/user/goi-mon/{ban.id}/")
                # Sinh QR code
                qr = qrcode.QRCode(box_size=8, border=2)
                qr.add_data(goi_mon_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                qr_code_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                opened_ban = ban
                success_message = f"Mở bàn {ban.SoBan} thành công! Quét mã QR để gọi món."
                # Cập nhật context để render luôn trang với QR code
                context.update({
                    'qr_code_base64': qr_code_base64,
                    'goi_mon_url': goi_mon_url,
                    'opened_ban': opened_ban,
                    'success_message': success_message,
                })
                return render(request, 'mo_ban.html', context)
    return render(request, 'mo_ban.html', context)

def bieu_do_doanh_thu_view(request):
    doanh_thu_ngay = (
        HoaDon.objects.filter(TrangThai=True)
        .annotate(ngay=TruncDate('timeout'))
        .values('ngay')
        .annotate(tong=Sum('TongTien'))
        .order_by('ngay')
    )
    labels = [str(dt['ngay']) for dt in doanh_thu_ngay]
    data = [float(dt['tong']) for dt in doanh_thu_ngay]
    return render(request, 'bieu_do_doanh_thu.html', {'labels': labels, 'data': data})

def danh_sach_nhan_vien_view(request):
    nhan_vien_list = NhanVien.objects.all().order_by('id')
    return render(request, 'danh_sach_nhan_vien.html', {'nhan_vien_list': nhan_vien_list})
