import random
from datetime import datetime, timedelta
from account.models import BanAn, HoaDon, KhuBanAn, Account

Account.objects.create(username="admin", password="123456")
