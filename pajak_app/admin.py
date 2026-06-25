from django.contrib import admin
from .models import WajibPajak, SPTTahunan

# Kustomisasi tampilan tabel Wajib Pajak di Admin
@admin.register(WajibPajak)
class WajibPajakAdmin(admin.ModelAdmin):
    list_display = ('npwp', 'nama', 'nik', 'jenis', 'password') # Kolom yang ditampilkan
    search_fields = ('npwp', 'nama', 'nik')         # Menambahkan kolom pencarian

# Kustomisasi tampilan tabel Transaksi SPT di Admin
@admin.register(SPTTahunan)
class SPTTahunanAdmin(admin.ModelAdmin):
    list_display = ('no_lapor', 'npwp', 'tahun', 'status', 'tgl_lapor') 
    list_filter = ('tahun', 'status')               # Menambahkan filter di samping kanan
    search_fields = ('no_lapor', 'npwp__nama')      # Pencarian berdasarkan nomor lapor atau nama