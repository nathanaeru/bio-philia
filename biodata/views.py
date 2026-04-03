import re
import time
from pathlib import Path

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.contrib import messages
from django.shortcuts import render, redirect

from biodata.models import ThemeSetting

from .context_processors import AUTHORIZED_EMAILS, DEFAULT_THEME, THEME_PRESETS

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UsernameChangeForm 

@login_required
def change_username(request):
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Username kamu sudah berhasil diganti.")
            return redirect('/')
    else:
        form = UsernameChangeForm(instance=request.user)
    
    return render(request, 'change_username.html', {'form': form})

def edit_theme(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Silakan login terlebih dahulu untuk mengakses halaman tersebut.")
        return redirect('home_view')

    if request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, "Akses Ditolak: Anda tidak diperkenankan mengedit tema website ini.")
        return redirect('home_view')

    theme_setting, created = ThemeSetting.objects.get_or_create(id=1)

    if request.method == 'POST':
        if 'reset' in request.POST:
            theme_setting.theme_mode = 'original'
            theme_setting.bg_color = DEFAULT_THEME['bg_color']
            theme_setting.text_color = DEFAULT_THEME['text_color']
            theme_setting.font_family = DEFAULT_THEME['font_family']
            if theme_setting.background_image:
                theme_setting.background_image.delete(save=False)
            theme_setting.save()
            messages.success(request, "Tema berhasil di-reset ke pengaturan awal!")
            return redirect('home_view')

        selected_mode = request.POST.get('theme_mode', 'original')
        if selected_mode not in ('original', 'dark', 'light', 'custom'):
            selected_mode = 'original'

        theme_setting.theme_mode = selected_mode

        if selected_mode in THEME_PRESETS:
            theme_setting.save()
            messages.success(request, f"Tema {selected_mode} berhasil diterapkan!")
        else:
            raw_bg = request.POST.get('bg_color', '')[:20]
            raw_text = request.POST.get('text_color', '')[:20]
            raw_font = request.POST.get('font_family', '')[:100]

            if re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', raw_bg):
                theme_setting.bg_color = raw_bg
            if re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', raw_text):
                theme_setting.text_color = raw_text

            theme_setting.font_family = re.sub(r'[<>;&]', '', raw_font) or DEFAULT_THEME["font_family"]

            if 'remove_background_image' in request.POST:
                if theme_setting.background_image:
                    theme_setting.background_image.delete(save=False)

            uploaded_background = request.FILES.get('background_image')
            if uploaded_background:
                allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
                extension = Path(uploaded_background.name).suffix.lower()
                if extension not in allowed_extensions:
                    messages.error(request, "File background harus berupa JPG, JPEG, PNG, atau WEBP.")
                    return redirect('edit_theme')
                
                img = Image.open(uploaded_background)
                
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                    

                max_size = (1920, 1080)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                output_buffer = BytesIO()
                
                img.save(output_buffer, format='WEBP', quality=75)
                output_buffer.seek(0)

                unique_filename = f"bg_{int(time.time())}.webp"
                
                compressed_bg = InMemoryUploadedFile(
                    output_buffer, 
                    'ImageField', 
                    unique_filename,
                    'image/webp', 
                    output_buffer.tell(), 
                    None
                )

                if theme_setting.background_image:
                    theme_setting.background_image.delete(save=False) 

                theme_setting.background_image = compressed_bg

            theme_setting.save()
            messages.success(request, "Tema custom berhasil diperbarui!")

        return redirect('home_view')

    return render(request, 'edit_theme.html')