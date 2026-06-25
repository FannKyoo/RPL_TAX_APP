from django.db import models
from django.utils import timezone

class WajibPajak(models.Model):
    npwp = models.CharField(max_length=15, primary_key=True) 
    nik = models.CharField(max_length=16)
    nama = models.CharField(max_length=50)
    alamat = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    jenis = models.CharField(max_length=1) 

    def __str__(self):
        return f"{self.npwp} - {self.nama}"

    class Meta:
        db_table = 'tb_wajib_pajak'

class SPTTahunan(models.Model):
    no_lapor = models.CharField(max_length=20, primary_key=True)
    npwp = models.ForeignKey(WajibPajak, on_delete=models.CASCADE, db_column='npwp')
    tahun = models.CharField(max_length=4)
    bruto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    kredit_pajak = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    terutang = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    status = models.CharField(max_length=15)
    tgl_lapor = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"SPT {self.tahun} - {self.npwp.nama}"

    class Meta:
        db_table = 'tb_spt_tahunan'