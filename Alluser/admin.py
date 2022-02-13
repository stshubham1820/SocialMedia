from django.contrib import admin
from .models import *
# Register your models here.
class upUser(admin.ModelAdmin):
    def __str__(self):
            return self.mobile
admin.site.register(User,upUser)