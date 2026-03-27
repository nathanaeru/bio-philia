from django.db import models

class ThemeSetting(models.Model):
    bg_color = models.CharField(max_length=20, default="#be185d")
    text_color = models.CharField(max_length=20, default="#ffffff")
    
    def __str__(self):
        return "Pengaturan Tema Global"
    
class ProfilMember(models.Model):
    nama = models.CharField(max_length=100)
    npm = models.CharField(max_length=20, unique=True)
    jurusan = models.CharField(max_length=100)
    tanggal_lahir = models.DateField(help_text="Format: YYYY-MM-DD")
    hobi = models.CharField(max_length=255)
    quotes = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, help_text="Upload gambar profil")

    def __str__(self):
        return self.nama