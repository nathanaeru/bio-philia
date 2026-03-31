import re
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect

from .context_processors import AUTHORIZED_EMAILS, DEFAULT_THEME, THEME_PRESETS, get_active_theme, get_original_theme

def edit_theme(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Silakan login terlebih dahulu untuk mengakses halaman tersebut.")
        return redirect('home_view')

    if request.user.email not in AUTHORIZED_EMAILS:
        messages.error(request, "Akses Ditolak: Anda tidak diperkenankan mengedit tema website ini.")
        return redirect('home_view')

    original_theme = get_original_theme()
    theme, active_mode = get_active_theme(request)

    if request.method == 'POST':
        selected_mode = 'original' if 'reset' in request.POST else request.POST.get('theme_mode', 'original')
        if selected_mode not in ('original', 'dark', 'light', 'custom'):
            selected_mode = 'original'

        if selected_mode == 'original':
            request.session['theme_mode'] = 'original'
            messages.success(request, "Tema original berhasil diterapkan.")
        elif selected_mode in THEME_PRESETS:
            request.session['theme_mode'] = selected_mode
            messages.success(request, f"Tema {selected_mode} berhasil diterapkan.")
        else:
            raw_bg = request.POST.get('bg_color', '')[:20]
            raw_text = request.POST.get('text_color', '')[:20]
            raw_font = request.POST.get('font_family', '')[:100]

            if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', raw_bg):
                raw_bg = original_theme["bg_color"]
            if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', raw_text):
                raw_text = original_theme["text_color"]

            clean_font = re.sub(r'[<>;&]', '', raw_font) or DEFAULT_THEME["font_family"]
            custom_theme = {
                'bg_color': raw_bg,
                'text_color': raw_text,
                'font_family': clean_font,
                'background_image': request.session.get('custom_theme', {}).get('background_image', ''),
            }

            if 'remove_background_image' in request.POST:
                custom_theme['background_image'] = ''

            uploaded_background = request.FILES.get('background_image')
            if uploaded_background:
                allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
                extension = Path(uploaded_background.name).suffix.lower()
                if extension not in allowed_extensions:
                    messages.error(request, "File background harus berupa JPG, JPEG, PNG, atau WEBP.")
                    return redirect('edit_theme')

                file_name = f"theme_backgrounds/user_{request.user.id}{extension}"
                if default_storage.exists(file_name):
                    default_storage.delete(file_name)
                saved_path = default_storage.save(file_name, uploaded_background)
                custom_theme['background_image'] = settings.MEDIA_URL + saved_path.replace("\\", "/")

            request.session['theme_mode'] = 'custom'
            request.session['custom_theme'] = custom_theme
            messages.success(request, "Tema custom berhasil diperbarui.")

        return redirect('home_view')

    custom_theme = request.session.get('custom_theme', {})
    context = {
        'theme': theme,
        'active_mode': active_mode,
        'original_theme': original_theme,
        'custom_theme': {
            'bg_color': custom_theme.get('bg_color', original_theme['bg_color']),
            'text_color': custom_theme.get('text_color', original_theme['text_color']),
            'font_family': custom_theme.get('font_family', original_theme['font_family']),
            'background_image': custom_theme.get('background_image', ''),
        },
    }
    return render(request, 'edit_theme.html', context)
