from django.shortcuts import render, redirect
from django.http import HttpResponse
from clients.forms import ClientForm, PeroranganForm, PerusahaanForm
from .utils import match_banks_dynamic
from clients.models import ClientHistory
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


# =========================
# LOGIN (HARDCODE)
# =========================
VALID_USERNAME = "lmpremier2025"
VALID_PASSWORD = "premier@01"


def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            request.session["is_logged_in"] = True
            return redirect("choose_type")
        else:
            error = "Username atau password salah"

    return render(request, "matching/login.html", {"error": error})


# =========================
# PILIH TIPE CLIENT
# =========================
def choose_type(request):
    if not request.session.get("is_logged_in"):
        return redirect("login")

    if request.method == "POST":
        tipe = request.POST.get("tipe_client")

        # save to session
        request.session["tipe_client"] = tipe

        return redirect("input_client")

    return render(request, "matching/choose_type.html")

def set_type(request, tipe):
    request.session["tipe_client"] = tipe
    return redirect("input_client")

# =========================
# INPUT CLIENT
# =========================
def input_client(request):

    if not request.session.get("is_logged_in"):
        return redirect("login")

    tipe = request.session.get("tipe_client")

    if tipe == "PERUSAHAAN":
        FormClass = PerusahaanForm
    else:
        FormClass = PeroranganForm

    results = None

    if request.method == 'POST':
        form = FormClass(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.tipe_client = tipe  # 🔥 IMPORTANT
            client.save()

            results = match_banks_dynamic(client)

            request.session["last_results"] = results
            request.session["last_client"] = {
                "nama": client.nama,
                "umur": client.umur,
                "jenis_kelamin": client.jenis_kelamin,
                "tipe_client": client.tipe_client,
                "jenis_pinjaman": client.jenis_pinjaman,
                "jumlah_pinjaman": client.jumlah_pinjaman,
                "tenor": client.tenor,

                "pekerjaan": client.pekerjaan,
                "status_pekerjaan": client.status_pekerjaan,
                "lama_kerja": client.lama_kerja,

                "bentuk_perusahaan": client.bentuk_perusahaan,
                "bidang_usaha": client.bidang_usaha,

                "jaminan": client.jaminan,

                "sumber_penghasilan": client.sumber_penghasilan,
                "status_slik": client.status_slik,

                "join_income": client.join_income,
            }

    else:
        form = FormClass()

    return render(request, 'matching/input.html', {
        'form': form,
        'results': results,
        'tipe': tipe
    })


# =========================
# SAVE HISTORY
# =========================
def save_history(request):
    if request.method == "POST":

        client = request.session.get("last_client")
        results = request.session.get("last_results")

        print("CLIENT:", client)
        print("RESULTS:", results)

        if client and results:
            ClientHistory.objects.create(
                nama=client.get("nama"),
                umur=client.get("umur") or 0,
                jumlah_pinjaman=client.get("jumlah_pinjaman"),
                tenor=client.get("tenor"),

                jenis_kelamin=client.get("jenis_kelamin"),
                tipe_client=client.get("tipe_client"),
                jenis_pinjaman=client.get("jenis_pinjaman"),

                pekerjaan=client.get("pekerjaan"),
                status_pekerjaan=client.get("status_pekerjaan"),

                bentuk_perusahaan=client.get("bentuk_perusahaan"),
                bidang_usaha=client.get("bidang_usaha"),

                jaminan=client.get("jaminan"),

                sumber_penghasilan=client.get("sumber_penghasilan"),
                status_slik=client.get("status_slik"),

                join_income=client.get("join_income"),
                results=results
            )

    return redirect("history")


# =========================
# HISTORY LIST
# =========================
def history(request):
    if not request.session.get("is_logged_in"):
        return redirect("login")

    histories = ClientHistory.objects.all().order_by("-created_at")

    return render(request, "matching/history.html", {
        "histories": histories
    })


# =========================
# HISTORY DETAIL
# =========================
def history_detail(request, id):
    if not request.session.get("is_logged_in"):
        return redirect("login")

    history = ClientHistory.objects.get(id=id)
    print(history.__dict__)

    return render(request, "matching/history_detail.html", {
        "h": history
    })


# =========================
# DELETE HISTORY
# =========================
def delete_history(request, id):
    if not request.session.get("is_logged_in"):
        return redirect("login")

    history = ClientHistory.objects.get(id=id)
    history.delete()

    return redirect("history")


def download_history_pdf(request, id):
    if not request.session.get("is_logged_in"):
        return redirect("login")

    h = ClientHistory.objects.get(id=id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="history_{id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # =========================
    # TITLE
    # =========================
    elements.append(Paragraph("History Detail", styles['Title']))
    elements.append(Spacer(1, 12))

    # =========================
    # CLIENT DATA
    # =========================
    if h.nama:
        elements.append(Paragraph(f"Nama: {h.nama}", styles['Normal']))

    if h.umur:
        elements.append(Paragraph(f"Umur: {h.umur} tahun", styles['Normal']))

    if h.jenis_pinjaman:
        elements.append(Paragraph(
            f"Jenis Pinjaman: {h.get_jenis_pinjaman_display()}",
            styles['Normal']
        ))

    if h.jumlah_pinjaman:
        elements.append(Paragraph(f"Plafond: Rp {h.jumlah_pinjaman:,}", styles['Normal']))

    if h.tenor:
        elements.append(Paragraph(f"Tenor: {h.tenor} bulan", styles['Normal']))

    elements.append(Spacer(1, 12))

    # =========================
    # RESULTS
    # =========================
    elements.append(Paragraph("Hasil Rekomendasi:", styles['Heading2']))
    elements.append(Spacer(1, 10))

    for r in h.results:
        # Handle PKS
        bank_name = r.get("bank", "-")
        if r.get("is_pks"):
            bank_name += " (PKS)"

        elements.append(
            Paragraph(f"{bank_name} - Score: {r.get('score', 0)}", styles['Heading3'])
        )

        for reason in r.get("reasons", []):
            elements.append(
                Paragraph(f"- {reason}", styles['Normal'])
            )

        elements.append(Spacer(1, 10))

    doc.build(elements)

    return response