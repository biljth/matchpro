from django import forms
from .models import Client

class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'
       
    def __init__(self, *args, **kwargs):
        tipe_client = kwargs.pop('tipe_client', None)
        super().__init__(*args, **kwargs)

        if tipe_client == "PERUSAHAAN":
            self.fields.pop('jenis_kelamin', None)
        else:
            self.fields.pop('bentuk_perusahaan', None)  


class PeroranganForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'nama',
            'jenis_kelamin',
            'umur',
            'jenis_pinjaman',
            'jumlah_pinjaman',
            'tenor',
            'pekerjaan',
            'status_pekerjaan',
            'lama_kerja',
            'jaminan',
            'sumber_penghasilan',
            'instant_approval',
            'status_slik',
            'join_income',
        ]
        labels = {
            'tenor': 'Tenor (bulan)',
            'lama_kerja': 'Lama kerja / usaha (tahun)',
            'jumlah_pinjaman': 'Jumlah Pinjaman (Rp)',
        }


class PerusahaanForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'nama',
            'bentuk_perusahaan',
            'bidang_usaha',
            'lama_usaha',
            'jenis_pinjaman',
            'jumlah_pinjaman',
            'tenor',
            'jaminan',
            'jenis_sertifikat',
            'sumber_penghasilan',
            'status_slik',
        ]
        labels = {
            'tenor': 'Tenor (bulan)',
            'jumlah_pinjaman': 'Jumlah Pinjaman (Rp)',
        }
    