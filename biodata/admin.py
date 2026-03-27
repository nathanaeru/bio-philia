from django.contrib import admin

from biodata.models import ProfilMember, ThemeSetting

# Register your models here.
admin.site.register(ThemeSetting)
admin.site.register(ProfilMember)