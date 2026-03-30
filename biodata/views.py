from django.shortcuts import render, redirect
from django.contrib import messages
import re 
from .models import ThemeSetting
from .context_processors import AUTHORIZED_EMAILS

def edit_theme(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Silakan login terlebih dahulu untuk mengakses halaman tersebut.")
        return redirect('home_view')
        
    if request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, "Akses Ditolak: Anda tidak diperkenankan mengedit tema website ini.")
        return redirect('home_view')

    theme, created = ThemeSetting.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        if 'reset' in request.POST:
            theme.bg_color = '#be185d'
            theme.text_color = '#ffffff'
            theme.font_family = 'Roboto, sans-serif'
            theme.save()
            messages.success(request, "Tema berhasil dikembalikan ke pengaturan awal!")
        else:
            raw_bg = request.POST.get('bg_color', '')[:20]
            raw_text = request.POST.get('text_color', '')[:20]
            raw_font = request.POST.get('font_family', '')[:100]

            if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', raw_bg):
                raw_bg = '#be185d'
            if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', raw_text):
                raw_text = '#ffffff'

            clean_font = re.sub(r'[<>;&]', '', raw_font)

            theme.bg_color = raw_bg
            theme.text_color = raw_text
            theme.font_family = clean_font
            theme.save()
            
            messages.success(request, "Tema berhasil diperbarui!")
            
        return redirect('home_view')
        
    return render(request, 'edit_theme.html', {'theme': theme})