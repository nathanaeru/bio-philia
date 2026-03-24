from django.db import models

class ThemeSetting(models.Model):
    bg_color = models.CharField(max_length=20, default="#be185d")
    text_color = models.CharField(max_length=20, default="#ffffff")
    
    def __str__(self):
        return "Pengaturan Tema Global"