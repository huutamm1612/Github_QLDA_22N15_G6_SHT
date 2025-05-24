from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('danh-sach-mon-an/', views.danh_sach_mon_an_view, name='danh_sach_mon_an'),
    path('them-mon-an/', views.them_monan_view, name='them_monan'),
    path('them-loai-mon-an/', views.them_loaimonan_view, name='them_loaimonan'),
    path('capnhat-trangthai-mon-an/<int:monan_id>/', views.capnhat_trangthai_monan_view, name='capnhat_trangthai_monan'),
    path('xoa-mon-an/<int:monan_id>/', views.xoa_monan_view, name='xoa_monan'),
    path('sua-mon-an/<int:monan_id>/', views.sua_monan_view, name='sua_monan'),
]
