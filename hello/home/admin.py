from django.contrib import admin
from home.models import about
from home.models import CustomUser
# Register your models here.
admin.site.register(about)
admin.site.register(CustomUser)