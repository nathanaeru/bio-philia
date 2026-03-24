from django.shortcuts import render, redirect
from django.contrib import messages # <-- Import sistem pesan Django
from .models import ThemeSetting
from .context_processors import AUTHORIZED_EMAILS # <-- Import daftar email tadi

def edit_theme(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Silakan login terlebih dahulu untuk mengakses halaman tersebut.")
        return redirect('home_view')
        
    if request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, "Akses Ditolak: Anda tidak diperkenankan mengedit tema website ini.")
        return redirect('home_view')

    theme, created = ThemeSetting.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        theme.bg_color = request.POST.get('bg_color')
        theme.text_color = request.POST.get('text_color')
        theme.font_family = request.POST.get('font_family')
        theme.save()
        
        messages.success(request, "Tema berhasil diperbarui!")
        return redirect('home_view')
        
    return render(request, 'edit_theme.html', {'theme': theme})