from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import ThemeSetting

# Daftar email anggota kelompok (Authorization List)
AUTHORIZED_EMAILS = [
    'lhn4th4n@gmail.com',
    # Nanti email teman kelompok yang lain ditambahkan ke sini
]

# Fungsi pengecekan otorisasi
def is_group_member(user):
    return user.is_authenticated and user.email in AUTHORIZED_EMAILS

# Lindungi View ini menggunakan decorator
# Jika user gagal tes (bukan anggota), dia akan dilempar kembali ke halaman '/'
@user_passes_test(is_group_member, login_url='/')
def edit_theme(request):
    # Ambil pengaturan tema pertama, jika belum ada di DB, buatkan secara otomatis
    theme, created = ThemeSetting.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        # Simpan warna baru dari form HTML
        theme.bg_color = request.POST.get('bg_color')
        theme.text_color = request.POST.get('text_color')
        theme.save()
        return redirect('home_view') # Kembali ke halaman utama
        
    return render(request, 'edit_theme.html', {'theme': theme})