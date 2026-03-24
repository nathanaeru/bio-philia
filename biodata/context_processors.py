from .models import ThemeSetting

def website_theme(request):
    # Mencegah error jika database belum dimigrasi
    try:
        theme = ThemeSetting.objects.first()
    except:
        theme = None
    return {'theme': theme}