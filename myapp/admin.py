from django.contrib import admin
from myapp.models import news, userData, userTempData, ris

# Register your models here.
admin.site.register(news)
admin.site.register(userData)
admin.site.register(userTempData)
admin.site.register(ris)
