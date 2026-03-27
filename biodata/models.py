from django.db import models
from django.contrib.auth.models import User

class ThemeSetting(models.Model):
    bg_color = models.CharField(max_length=20, default="#be185d")
    text_color = models.CharField(max_length=20, default="#ffffff")
    
    def __str__(self):
        return "Pengaturan Tema Global"
    
class Biodata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    npm = models.CharField(max_length=10)
    jurusan = models.CharField(max_length=50)
    
    def get_avatar_url(self):
        return f"https://api.dicebear.com/7.x/adventurer/svg?seed={self.npm}"

    def __str__(self):
        return self.nama