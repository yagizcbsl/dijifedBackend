from django.contrib import admin

# Register your models here.

from .models import ProfileTable, extraUserFields

admin.site.register(ProfileTable)
admin.site.register(extraUserFields)