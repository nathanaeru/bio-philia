from .models import ThemeSetting

DEFAULT_THEME = {
    "bg_color": "#be185d",
    "text_color": "#ffffff",
    "font_family": "Roboto, sans-serif",
    "background_image": "",
}

THEME_PRESETS = {
    "original": DEFAULT_THEME.copy(),
    "dark": {
        "bg_color": "#0f172a",
        "text_color": "#f8fafc",
        "font_family": "Roboto, sans-serif",
        "background_image": "",
    },
    "light": {
        "bg_color": "#f8fafc",
        "text_color": "#0f172a",
        "font_family": "Roboto, sans-serif",
        "background_image": "",
    },
}

AUTHORIZED_EMAILS = [
    'lhn4th4n@gmail.com',
    'arrdyana@gmail.com',
    'arisnrochelle@gmail.com',
    'hlee79394@gmail.com',
    'diraramadhani05@gmail.com'
]


def get_active_theme(request):
    theme_setting = ThemeSetting.objects.first()
    
    if not theme_setting:
        return DEFAULT_THEME.copy(), "original"

    mode = theme_setting.theme_mode

    if mode in THEME_PRESETS:
        return THEME_PRESETS[mode].copy(), mode
    elif mode == "custom":
        return {
            "bg_color": theme_setting.bg_color,
            "text_color": theme_setting.text_color,
            "font_family": theme_setting.font_family,
            "background_image": theme_setting.background_image.url if theme_setting.background_image else "",
        }, "custom"

    return DEFAULT_THEME.copy(), "original"

def website_theme(request):
    theme, theme_mode = get_active_theme(request)
    is_member = request.user.is_authenticated and request.user.email in AUTHORIZED_EMAILS

    theme_setting = ThemeSetting.objects.first()
    custom_theme_dict = {}
    if theme_setting:
        custom_theme_dict = {
            'bg_color': theme_setting.bg_color,
            'text_color': theme_setting.text_color,
            'font_family': theme_setting.font_family,
            'background_image': theme_setting.background_image.url if theme_setting.background_image else "",
        }

    return {
        'theme': theme, 
        'custom_theme': custom_theme_dict,
        'active_mode': theme_mode,
        'is_group_member': is_member,
        'can_customize_theme': is_member,
    }
