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


def get_original_theme():
    theme = ThemeSetting.objects.first()
    if theme:
        return {
            "bg_color": theme.bg_color or DEFAULT_THEME["bg_color"],
            "text_color": theme.text_color or DEFAULT_THEME["text_color"],
            "font_family": theme.font_family or DEFAULT_THEME["font_family"],
            "background_image": "",
        }
    return DEFAULT_THEME.copy()


def get_active_theme(request):
    original_theme = get_original_theme()

    if not request.user.is_authenticated:
        return original_theme, "original"

    if request.user.email not in AUTHORIZED_EMAILS:
        return original_theme, "original"

    theme_mode = request.session.get("theme_mode", "original")
    if theme_mode == "custom":
        custom_theme = request.session.get("custom_theme", {})
        return {
            "bg_color": custom_theme.get("bg_color", original_theme["bg_color"]),
            "text_color": custom_theme.get("text_color", original_theme["text_color"]),
            "font_family": custom_theme.get("font_family", original_theme["font_family"]),
            "background_image": custom_theme.get("background_image", ""),
        }, "custom"

    if theme_mode in THEME_PRESETS and theme_mode != "original":
        preset = THEME_PRESETS[theme_mode].copy()
        preset["background_image"] = ""
        return preset, theme_mode

    return original_theme, "original"

def website_theme(request):
    theme, theme_mode = get_active_theme(request)

    is_member = False
    if request.user.is_authenticated and request.user.email in AUTHORIZED_EMAILS:
        is_member = True

    return {
        'theme': theme, 
        'is_group_member': is_member,
        'theme_mode': theme_mode,
        'can_customize_theme': is_member,
    }
