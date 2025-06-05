from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('danh-sach-mon-an/', views.danh_sach_mon_an_view, name='danh_sach_mon_an'),
    path('them-mon-an/', views.them_monan_view, name='them_monan'),
    path('them-loai-mon-an/', views.them_loaimonan_view, name='them_loaimonan'),
    path('capnhat-trangthai-mon-an/<int:monan_id>/', views.capnhat_trangthai_monan_view, name='capnhat_trangthai_monan'),
    path('xoa-mon-an/<int:monan_id>/', views.xoa_monan_view, name='xoa_monan'),
    path('sua-mon-an/<int:monan_id>/', views.sua_monan_view, name='sua_monan'),
    path('ban-an/', views.danh_sach_ban_an_view, name='danh_sach_ban_an'),
    path('them-khu/', views.them_khu_view, name='them_khu'),
    path('sua-khu/<int:khu_id>/', views.sua_khu_view, name='sua_khu'),
    path('xoa-khu/<int:khu_id>/', views.xoa_khu_view, name='xoa_khu'),
    path('them-ban-an/', views.them_ban_an_view, name='them_ban_an'),
    path('sua-ban-an/<int:ban_id>/', views.sua_ban_an_view, name='sua_ban_an'),
    path('xoa-ban-an/<int:ban_id>/', views.xoa_ban_an_view, name='xoa_ban_an'),
    path('logout/', views.logout_view, name='logout'),
    path('mo-ban/', views.mo_ban_view, name='mo_ban'),
    path('bieu-do-doanh-thu/', views.bieu_do_doanh_thu_view, name='bieu_do_doanh_thu'),
    path('nhan-vien/', views.danh_sach_nhan_vien_view, name='danh_sach_nhan_vien'),
    path('dat-ban/', views.danh_sach_dat_ban_view, name='danh_sach_dat_ban'),
    path('dat-ban/xac-nhan/<int:datban_id>/', views.xac_nhan_dat_ban_view, name='xac_nhan_dat_ban'),
    path('dat-ban/huy/<int:datban_id>/', views.huy_dat_ban_view, name='huy_dat_ban'),
]

