from django.urls import path
from . import views

urlpatterns = [
    path('goi-mon/<int:ban_id>/', views.goi_mon_view, name='goi_mon'),
    path('hoa-don/<int:ban_id>/', views.xem_hoa_don_view, name='xem_hoa_don'),
]
