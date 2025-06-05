from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_user_view, name='home_user'),
    path('goi-mon/<int:ban_id>/', views.goi_mon_view, name='goi_mon'),
    path('hoa-don/<int:ban_id>/', views.xem_hoa_don_view, name='xem_hoa_don'),
    path('uu-dai/', views.uu_dai_view, name='uu_dai'),
    path('thuc-don/', views.thuc_don_view, name='thuc_don'),
    path('dat-ban/', views.dat_ban_view, name='dat_ban'),
]
