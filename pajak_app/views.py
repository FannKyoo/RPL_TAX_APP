from django.shortcuts import render, get_object_or_404, redirect
from .models import WajibPajak, SPTTahunan
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from decimal import Decimal
from django.contrib import messages

def halaman_form_spt(request):
    # 1. Siapkan wadah kosong
    context = {}
    
    # 2. LOGIKA AMBIL RIWAYAT (Taruh di luar POST biar selalu jalan saat buka web)
    if request.session.get('npwp'):
        npwp_login = request.session.get('npwp')
        # Tarik semua data SPT milik NPWP ini dari database, urutkan dari yang terbaru
        context['riwayat'] = SPTTahunan.objects.filter(npwp__npwp=npwp_login).order_by('-tgl_lapor')

    # 3. PROSES JIKA TOMBOL SIMPAN DIKLIK
    if request.method == 'POST':
        npwp_input = request.POST.get('npwp')
        nama_input = request.POST.get('nama')
        tahun = request.POST.get('tahun')

        # 1. Tangkap input dan ubah jadi tipe Decimal agar tidak error
        bruto = Decimal(request.POST.get('bruto', 0))
        kredit_pajak = Decimal(request.POST.get('kredit_pajak', 0))

        # --- LOGIKA PENENTUAN FORMULIR DINAMIS ---
        if bruto <= Decimal('60000000'):
            jenis_formulir = "Formulir 1770 SS"
        else:
            jenis_formulir = "Formulir 1770 S"
        # -----------------------------------------

        # 2. Aturan PTKP Standar (Lajang/TK-0 = 54 Juta)
        ptkp = Decimal('54000000')

        # 3. Hitung Penghasilan Kena Pajak (PKP)
        pkp = bruto - ptkp

        # Jika gaji di bawah 54 juta, PKP tidak boleh minus, kita set jadi 0
        if pkp < 0:
            pkp = Decimal('0') 

        # 4. Hitung Pajak Terutang (Tarif progresif sesuai UU HPP)
        if pkp <= Decimal('60000000'):
            terutang = pkp * Decimal('0.05')
        elif pkp <= Decimal('250000000'):
            terutang = (Decimal('60000000') * Decimal('0.05')) + ((pkp - Decimal('60000000')) * Decimal('0.15'))
        elif pkp <= Decimal('500000000'):
            terutang = (Decimal('60000000') * Decimal('0.05')) + (Decimal('190000000') * Decimal('0.15')) + ((pkp - Decimal('250000000')) * Decimal('0.25'))
        elif pkp <= Decimal('5000000000'):
            terutang = (Decimal('60000000') * Decimal('0.05')) + (Decimal('190000000') * Decimal('0.15')) + (Decimal('250000000') * Decimal('0.25')) + ((pkp - Decimal('500000000')) * Decimal('0.30'))
        else:
            terutang = (Decimal('60000000') * Decimal('0.05')) + (Decimal('190000000') * Decimal('0.15')) + (Decimal('250000000') * Decimal('0.25')) + (Decimal('4500000000') * Decimal('0.30')) + ((pkp - Decimal('5000000000')) * Decimal('0.35'))

        # 5. Tentukan Status Ketetapan (Kurang Bayar / Lebih Bayar / Nihil)
        # Perbaikan logika: Pajak Terutang dikurangi Pajak yang sudah dipotong (Kredit Pajak)
        selisih = terutang - kredit_pajak

        if selisih == 0:
            status = "Nihil"
        elif selisih > 0:
            status = "Kurang Bayar"
        else:
            status = "Lebih Bayar"
            
        wp, created = WajibPajak.objects.get_or_create(
            npwp=npwp_input,
            defaults={'nik': '0000000000000000', 'nama': nama_input, 'jenis': 'P'}
        )
        
        no_lapor_baru = f"SPT-{tahun}-{timezone.now().strftime('%H%M%S')}"
        
        spt = SPTTahunan(
            no_lapor=no_lapor_baru,
            npwp=wp,
            tahun=tahun,
            kredit_pajak=kredit_pajak,
            bruto=bruto,
            terutang=terutang,
            status=status
        )
        spt.save()
        
        # 4. TAMBAHKAN PESAN SUKSES & VARIABEL FORMULIR KE CONTEXT
        context['berhasil'] = True
        context['bruto'] = int(bruto)
        context['terutang'] = int(terutang)
        context['kredit_pajak'] = int(kredit_pajak)
        context['status'] = status
        context['no_lapor'] = no_lapor_baru
        context['jenis_formulir'] = jenis_formulir # <-- Variabel baru untuk HTML
        
        # Biar riwayatnya langsung update nambah 1 setelah submit, kita tarik ulang datanya
        if request.session.get('npwp'):
            context['riwayat'] = SPTTahunan.objects.filter(npwp__npwp=npwp_login).order_by('-tgl_lapor')

    return render(request, 'form_spt.html', context)
    
# --- FUNGSI 2: CETAK PDF ---
def cetak_pdf(request, no_lapor):
    # Ambil data SPT dari database berdasarkan nomor lapor
    spt = get_object_or_404(SPTTahunan, no_lapor=no_lapor)
    template_path = 'cetak_spt.html'
    context = {'spt': spt}
    
    # Render HTML ke PDF
    response = HttpResponse(content_type='application/pdf')
    # Kalau mau langsung terdownload, hapus tanda # di bawah ini:
    # response['Content-Disposition'] = f'attachment; filename="Bukti_Lapor_{no_lapor}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Ada error saat membuat PDF')
    return response

# --- FUNGSI LOGIN ---
def login_view(request):
    if request.method == 'POST':
        npwp_input = request.POST.get('npwp')
        password_input = request.POST.get('password')
        
        try:
            # Cek apakah NPWP dan Password cocok di database
            user = WajibPajak.objects.get(npwp=npwp_input, password=password_input)
            
            # Jika cocok, simpan data ke "Session" (seperti ID Card sementara)
            request.session['npwp'] = user.npwp
            request.session['nama'] = user.nama
            return redirect('form_spt') # Pindah ke halaman form
            
        except WajibPajak.DoesNotExist:
            # Jika salah, kembalikan ke halaman login dengan pesan error
            return render(request, 'login.html', {'error': 'NPWP atau Password tidak valid!'})
            
    return render(request, 'login.html')

# --- FUNGSI LOGOUT ---
def logout_view(request):
    request.session.flush() # Hapus semua data sesi
    return redirect('login_view')

def daftar(request):
    if request.method == 'POST':
        npwp_input = request.POST.get('npwp')
        nik_input = request.POST.get('nik')
        nama_input = request.POST.get('nama')
        alamat_input = request.POST.get('alamat')
        email_input = request.POST.get('email')
        password_input = request.POST.get('password')
        jenis_input = request.POST.get('jenis') # Misal: 'P' untuk Pribadi, 'B' untuk Badan

        # Validasi: Cek apakah NPWP sudah ada di database
        if WajibPajak.objects.filter(npwp=npwp_input).exists():
            messages.error(request, 'NPWP ini sudah terdaftar! Silakan langsung login.')
            return redirect('daftar')

        try:
            # Simpan Wajib Pajak baru ke database
            WajibPajak.objects.create(
                npwp=npwp_input,
                nik=nik_input,
                nama=nama_input,
                alamat=alamat_input,
                email=email_input,
                password=password_input, # Disimpan sesuai model kamu saat ini
                jenis=jenis_input
            )
            messages.success(request, 'Akun berhasil dibuat! Silakan login dengan NPWP dan Password kamu.')
            return redirect('login_view') # Pastikan name 'login' sesuai dengan yang ada di urls.py kamu
            
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
            return redirect('daftar')

    # Jika method GET, tampilkan form HTML
    return render(request, 'daftar.html')