from django.contrib import admin

# Register your models here.
from .models import Profile,CustomUser

admin.site.register(Profile)
admin.site.register(CustomUser)