from django.contrib import admin
from django.urls import path
from pajak_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.halaman_form_spt, name='form_spt'),
    path('cetak/<str:no_lapor>/', views.cetak_pdf, name='cetak_pdf'),
    
    # Tambahkan dua baris ini:
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('daftar/', views.daftar, name='daftar'),
]