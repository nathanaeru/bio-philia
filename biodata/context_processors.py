from .models import ThemeSetting

AUTHORIZED_EMAILS = [
    'lhn4th4n@gmail.com',
    'arrdyana@gmail.com',
    'arisnrochelle@gmail.com',
    'hlee79394@gmail.com',
]

def website_theme(request):
    try:
        theme = ThemeSetting.objects.first()
    except:
        theme = None

    is_member = False
    if request.user.is_authenticated and request.user.email in AUTHORIZED_EMAILS:
        is_member = True

    return {
        'theme': theme, 
        'is_group_member': is_member
    }