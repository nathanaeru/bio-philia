import os
import json
import subprocess
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from biodata.models import ProfilMember

def home_view(request):
    members = ProfilMember.objects.all()
    return render(request, 'home.html', {'members': members})

@csrf_exempt 
def github_webhook(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            
            # Cek apakah push terjadi di branch 'main'
            if payload.get('ref') == 'refs/heads/main':
                repo_dir = str(settings.BASE_DIR)
                
                # Tarik kode terbaru dari GitHub
                subprocess.run(['git', 'pull'], cwd=repo_dir, check=True)
                
                # Aktifkan venv dan jalankan build.sh
                build_cmd = f"cd {repo_dir} && source env/bin/activate && bash build.sh"
                subprocess.run(build_cmd, cwd=repo_dir, shell=True, executable='/bin/bash', check=True)
                
                # Reload server PythonAnywhere
                wsgi_file = '/var/www/nathanaeru_pythonanywhere_com_wsgi.py'
                if os.path.exists(wsgi_file):
                    os.utime(wsgi_file, None)
                
                return HttpResponse("Sukses: Kode ditarik, build dieksekusi, dan server di-reload!", status=200)
            else:
                return HttpResponse("Diabaikan: Push bukan dari branch main.", status=200)
                
        except json.JSONDecodeError:
            return HttpResponse("Error: Payload JSON tidak valid.", status=400)
        except subprocess.CalledProcessError as e:
            # Menangkap error jika git pull atau build.sh gagal (misal: error saat migrate)
            return HttpResponse(f"Error: Proses terminal gagal. Detail: {str(e)}", status=500)
            
    return HttpResponseForbidden("Akses ditolak.")