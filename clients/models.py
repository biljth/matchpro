from django.db import models


class Client(models.Model):

    # =========================
    # BASIC INFO
    # =========================
    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]

    nama = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    umur = models.IntegerField(blank=True, null=True)   

    CLIENT_TYPE_CHOICES = [
        ('PERORANGAN', 'Perorangan'),
        ('PERUSAHAAN', 'Perusahaan'),
    ]

    tipe_client = models.CharField(
        max_length=20,
        choices=CLIENT_TYPE_CHOICES,
        default='PERORANGAN'
    )


    # =========================
    # LOAN DATA
    # =========================
    LOAN_TYPE_CHOICES = [
        ('KPR_PRIMARY', 'KPR Primary'),
        ('KPR_SECONDARY', 'KPR Secondary'),
        ('FAST_TAKE_OVER_KPR', 'Fast / Instant Approval Take Over KPR'),
        ('MULTIGUNA', 'Multiguna / Refinancing'),
        ('TAKE_OVER_MURNI', 'Take Over Murni'),
        ('TAKE_OVER_JUAL_BELI', 'Take Over Jual Beli'),
        ('TAKE_OVER_SME', 'Take Over dari SME (Fasilitas & Jaminan atas nama perorangan)'),
        ('INVESTASI', 'Kredit Investasi'),
        ('PRK', 'Modal Kerja'),
        ('INVOICE', 'Kredit Invoice Financing'),
        ('SPK', 'Kredit PO / SPK Financing'),
        ('BPKB', 'BPKB Mobil'),
        ('MICRO', 'Micro'),
        ('KOST', 'Pembiayaan Kost-kostan'),
        ('BRIDGING_OL', 'Bridging OL'),
        ('DANA_TALANGAN_BPJS', 'Dana Talangan BPJS'),
        ('DANA_TALANGAN_GAJI', 'Dana Talangan Gaji (Payroll Financing)'),
        ('ITSI', 'Investasi Terikat Syariah Indonesia (ITSI)'),
        ('SEWA_PROPERTY', 'Sewa Property'),
        ('RENOVASI', 'Renovasi Properti'),
        ('KPA', 'Kredit Pemilikan Apartemen (KPA)'),
        ('LOGAM_MULIA', 'Cicil Logam Mulia'),
        ('KTA', 'Kredit Tanpa Agunan (KTA)'),
        ('KTA_ONLINE', 'KTA Online Seller'),
        ('DEPOSITO', 'Deposito Berjangka'),
    ]

    jenis_pinjaman = models.CharField(max_length=50, choices=LOAN_TYPE_CHOICES)
    jumlah_pinjaman = models.IntegerField()
    tenor = models.IntegerField()

    # =========================
    # JOB DATA
    # =========================
    JOB_CHOICES = [
        ('KARYAWAN', 'Karyawan'),
        ('WIRASWASTA', 'Wiraswasta'),
        ('PROFESIONAL', 'Profesional'),
        ('ASN', 'PNS / ASN / Pemerintah'),
        ('TNI_POLRI', 'TNI / POLRI'),
        ('LAWYER', 'Lawyer'),
        ('BADAN_USAHA', 'Badan Usaha / Perusahaan / Yayasan'),
    ]

    JOB_STATUS_CHOICES = [
        ('TETAP', 'Tetap'),
        ('KONTRAK', 'Kontrak'),
    ]

    nama_perusahaan = models.CharField(max_length=150, blank=True, null=True)
    bidang_usaha = models.CharField(max_length=100, blank=True, null=True)
    lama_usaha = models.IntegerField(blank=True, null=True)
    pekerjaan = models.CharField(max_length=50, choices=JOB_CHOICES, blank=True, null=True)
    status_pekerjaan = models.CharField(max_length=20, choices=JOB_STATUS_CHOICES, blank=True, null=True)
    lama_kerja = models.IntegerField(blank=True, null=True)

    # =========================
    # BUSINESS DATA
    # =========================
    COMPANY_TYPE_CHOICES = [
        ('PERORANGAN', 'Perorangan'),
        ('PT', 'PT'),
        ('CV', 'CV'),
        ('YAYASAN', 'Yayasan'),
        ('PEMERINTAH', 'Pemerintah'),
        ('RUMAH_SAKIT', 'Rumah Sakit'),
    ]

    # =========================
    # BUSINESS FIELD (OPTIONAL)
    # =========================
    BIDANG_USAHA_CHOICES = [
        ('PERTANIAN', 'Pertanian, Kehutanan dan Perikanan'),
        ('PERTAMBANGAN', 'Pertambangan dan Penggalian'),
        ('INDUSTRI', 'Industri Pengolahan'),
        ('LISTRIK_GAS', 'Pengadaan Listrik, Gas, Uap/Air Panas dan Udara Dingin'),
        ('PENGELOLAAN_AIR', 'Pengelolaan Air, Limbah, Sampah, dan Remediasi'),
        ('KONSTRUKSI', 'Konstruksi'),
        ('PERDAGANGAN', 'Perdagangan Besar dan Eceran; Reparasi Mobil & Motor'),
        ('AKOMODASI', 'Akomodasi dan Makan Minum'),
        ('INFORMASI', 'Informasi dan Komunikasi'),
        ('KEUANGAN', 'Aktivitas Keuangan dan Asuransi'),
        ('REALESTAT', 'Real Estat'),
        ('PROFESIONAL', 'Aktivitas Profesional, Ilmiah dan Teknis'),
        ('SEWA', 'Aktivitas Penyewaan & Penunjang Usaha'),
        ('PEMERINTAHAN', 'Administrasi Pemerintahan, Pertahanan & Jaminan Sosial'),
        ('PENDIDIKAN', 'Pendidikan'),
        ('KESEHATAN', 'Kesehatan dan Aktivitas Sosial'),
        ('HIBURAN', 'Kesenian, Hiburan dan Rekreasi'),
        ('JASA_LAIN', 'Aktivitas Jasa Lainnya'),
        ('RUMAH_TANGGA', 'Aktivitas Rumah Tangga'),
        ('INTERNASIONAL', 'Badan Internasional & Ekstra Internasional'),
    ]

    bidang_usaha = models.CharField(
        max_length=50,
        choices=BIDANG_USAHA_CHOICES,
        blank=True,
        null=True
    )

    bentuk_perusahaan = models.CharField(max_length=50, choices=COMPANY_TYPE_CHOICES, blank=True, null=True)
    # bidang_usaha = models.CharField(max_length=100, blank=True, null=True)

    # =========================
    # COLLATERAL
    # =========================
    COLLATERAL_CHOICES = [
        ('TANPA_JAMINAN', '-'),
        ('RUMAH', 'Rumah'),
        ('APARTEMEN', 'Apartemen'),
        ('RUKO', 'Ruko / Rukan'),
        ('TANAH', 'Tanah'),
        ('GUDANG', 'Gudang'),
        ('KIOS', 'Kios'),
        ('KOST', 'Kost'),
        ('VILA', 'Vila'),
        ('INVOICE', 'Invoice'),
        ('SPK', 'SPK / PO'),
        ('BPKB', 'BPKB Mobil'),
        ('SK_PNS', 'SK Pegawai Negeri'),
        ('OBJEK_PEMBIAYAAN', 'Objek Pembiayaan'),
        ('SIP', 'SIP (Surat Izin Praktek)'),
    ]

    CERTIFICATE_CHOICES = [
        ('SHM', 'SHM'),
        ('HGB', 'HGB'),
        ('SHRS', 'SHRS'),
        ('AJB', 'AJB'),
        ('GIRIK', 'Girik'),
    ]

    jaminan = models.CharField(max_length=50, choices=COLLATERAL_CHOICES)
    jenis_sertifikat = models.CharField(max_length=50, choices=CERTIFICATE_CHOICES, blank=True, null=True)

    # =========================
    # FINANCIAL
    # =========================
    INCOME_TYPE_CHOICES = [
        ('HASIL_USAHA_TERCERMIN', 'Hasil Usaha Tercermin'),
        ('HASIL_USAHA_TIDAK_TERCERMIN', 'Hasil Usaha Tidak Tercermin'),
        ('GAJI_TRANSFER', 'Gaji Transfer'),
        ('GAJI_TUNAI', 'Gaji Tunai'),
        ('CAMPURAN', 'Campuran'),
    ]

    SLIK_CHOICES = [
        ('KOL1', 'Kol 1'),
        ('KOL2', 'Kol 2'),
        ('KOL3', 'Kol 3'),
        ('KOL5', 'Kol 5'),
    ]

    RESTRUKTUR_CHOICES = [
        ('TIDAK', 'Tidak'),
        ('AKTIF', 'Aktif'),
        ('SELESAI', 'Selesai'),
    ]

    sumber_penghasilan = models.CharField(max_length=50, choices=INCOME_TYPE_CHOICES)
    status_slik = models.CharField(max_length=10, choices=SLIK_CHOICES)
    # restruktur = models.CharField(max_length=10, choices=RESTRUKTUR_CHOICES)

    # =========================
    # RELATION / EXTRA
    # =========================
    JOIN_INCOME_CHOICES = [
        ('TIDAK', 'Tidak'),
        ('PASANGAN', 'Pasangan'),
        ('ORANG_TUA', 'Orang Tua'),
    ]

    # jenis_pengajuan = models.CharField(
    #     max_length=20,
    #     choices=[
    #         ('BARU', 'Baru'),
    #         ('TAKEOVER', 'Take Over'),
    #     ]
    # )

    join_income = models.CharField(max_length=20, choices=JOIN_INCOME_CHOICES, blank=True, null=True)

    # =========================
    # META
    # =========================
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.tipe_client == "PERUSAHAAN":
            return self.nama_perusahaan or "Perusahaan"
        return self.nama
    
    def is_perusahaan(self):
        return self.tipe_client == "PERUSAHAAN"

class ClientHistory(models.Model):
    nama = models.CharField(max_length=255)
    umur = models.IntegerField(null=True, blank=True)
    jumlah_pinjaman = models.BigIntegerField()
    tenor = models.IntegerField()

    # 🔥 ADD THESE
    jenis_pinjaman = models.CharField(max_length=50, choices=Client.LOAN_TYPE_CHOICES, null=True, blank=True)
    tipe_client = models.CharField(max_length=20, choices=Client.CLIENT_TYPE_CHOICES, null=True, blank=True)
    jenis_kelamin = models.CharField(max_length=1, choices=Client.GENDER_CHOICES, null=True, blank=True)
    pekerjaan = models.CharField(max_length=50, choices=Client.JOB_CHOICES, null=True, blank=True)
    bidang_usaha = models.CharField(max_length=20, choices=Client.BIDANG_USAHA_CHOICES, null=True, blank=True)
    status_pekerjaan = models.CharField(max_length=20, choices=Client.JOB_STATUS_CHOICES, null=True, blank=True)
    bentuk_perusahaan = models.CharField(max_length=50, choices=Client.COMPANY_TYPE_CHOICES, null=True, blank=True)
    jaminan = models.CharField(max_length=50, choices=Client.COLLATERAL_CHOICES, null=True, blank=True)
    sumber_penghasilan = models.CharField(max_length=50, choices=Client.INCOME_TYPE_CHOICES, null=True, blank=True)
    status_slik = models.CharField(max_length=10, choices=Client.SLIK_CHOICES, null=True, blank=True)
    join_income = models.CharField(max_length=20, choices=Client.JOIN_INCOME_CHOICES, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    results = models.JSONField()
    def __str__(self):
        return f"History {self.id}"
