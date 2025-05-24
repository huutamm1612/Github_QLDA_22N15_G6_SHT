from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, MonAn, LoaiMonAn
from django import forms
from django.conf import settings
import os

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

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            account = Account.objects.get(username=username, password=password)
            # Đăng nhập thành công, chuyển hướng sang trang danh sách món ăn
            return redirect('danh_sach_mon_an')
        except Account.DoesNotExist:
            error = 'Tên đăng nhập hoặc mật khẩu không đúng.'
    return render(request, 'login.html', {'error': error})

def danh_sach_mon_an_view(request):
    # Lấy tất cả loại món ăn và các món ăn tương ứng
    loai_monan_list = LoaiMonAn.objects.all().order_by('TenLoaiMon')
    data = []
    for loai in loai_monan_list:
        monan = MonAn.objects.filter(IdLoaiMonAn=loai).order_by('TenMonAn')
        data.append({'loai': loai, 'monan_list': monan})
    return render(request, 'danh_sach_mon_an.html', {'data': data})

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
