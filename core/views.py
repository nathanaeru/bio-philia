import os
import subprocess
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt 
def github_webhook(request):
    if request.method == 'POST':
        try:
            repo_dir = str(settings.BASE_DIR)
            subprocess.run(['git', 'pull'], cwd=repo_dir, check=True)
            
            wsgi_file = '/var/www/nathanaeru_pythonanywhere_com_wsgi.py'
            if os.path.exists(wsgi_file):
                os.utime(wsgi_file, None)
            
            return HttpResponse("Kode berhasil ditarik dan server di-reload!", status=200)
        
        except subprocess.CalledProcessError:
            return HttpResponse("Gagal melakukan git pull.", status=500)
            
    return HttpResponseForbidden("Akses ditolak.")