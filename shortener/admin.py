from django.contrib import admin

# Register your models here.
from .models import LongToShort, checkUserAuthentication


admin.site.register((LongToShort, checkUserAuthentication))