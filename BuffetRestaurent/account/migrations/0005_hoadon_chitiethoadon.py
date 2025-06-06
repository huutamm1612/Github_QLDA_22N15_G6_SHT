# Generated by Django 5.1.1 on 2025-06-04 06:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_khubanan_banan'),
    ]

    operations = [
        migrations.CreateModel(
            name='HoaDon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('timeout', models.DateTimeField(blank=True, null=True)),
                ('SoLuongNguoi', models.PositiveIntegerField(default=1)),
                ('TongTien', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('TrangThai', models.BooleanField(default=False)),
                ('Ban', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.banan')),
            ],
        ),
        migrations.CreateModel(
            name='ChiTietHoaDon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SoLuong', models.PositiveIntegerField(default=1)),
                ('GhiChu', models.CharField(blank=True, max_length=255, null=True)),
                ('MonAn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.monan')),
                ('HoaDon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chi_tiet', to='account.hoadon')),
            ],
        ),
    ]
