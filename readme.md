# 🏛️ Sistem Informasi E-Filing Pajak (SPT Tahunan)

Sistem Informasi berbasis web untuk memfasilitasi simulasi pelaporan Surat Pemberitahuan (SPT) Tahunan Wajib Pajak Orang Pribadi. Aplikasi ini dirancang untuk menghitung pajak secara otomatis berdasarkan aturan tarif progresif terbaru (UU HPP) dan mencetak Bukti Penerimaan Elektronik (BPE) dalam format PDF.

Proyek ini dikembangkan menggunakan **Python (Django Framework)** dan diimplementasikan dengan metodologi **Waterfall**.

---

## ✨ Fitur Utama

- **Kalkulasi Pajak Progresif:** Menghitung otomatis Penghasilan Kena Pajak (PKP) dan Pajak Terutang sesuai persentase berlapis UU HPP (5%, 15%, 25%, 30%, 35%).
- **Validasi Status Ketetapan:** Menentukan status pelaporan secara presisi (Nihil, Kurang Bayar, atau Lebih Bayar) berdasarkan selisih Pajak Terutang dan Kredit Pajak.
- **Smart Form Selection:** Sistem secara otomatis menentukan jenis formulir yang sesuai (Formulir 1770 SS untuk penghasilan bruto $\le$ Rp 60 Juta, dan 1770 S untuk $>$ Rp 60 Juta).
- **Cetak BPE (PDF):** Menghasilkan Bukti Penerimaan Elektronik resmi yang siap diunduh atau dicetak menggunakan *library* `xhtml2pdf`.
- **Manajemen Wajib Pajak:** Sistem autentikasi (Daftar & Login) serta pelacakan riwayat pelaporan SPT untuk masing-masing pengguna.

---

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Database:** SQLite (Bawaan Django) / [Bisa diubah ke MySQL/PostgreSQL]
- **Library Tambahan:** `xhtml2pdf` (untuk export PDF)

---

## 🚀 Cara Menjalankan Proyek (Local Development)

Ikuti langkah-langkah berikut untuk menjalankan aplikasi di komputer lokal:

1. **Clone Repository**
   ```bash
   git clone https://github.com/FannKyoo/RPL_TAX_APP.git
   cd proyek_pajak