from io import BytesIO

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def generate_certificate(student_name, course_title, instructor_name, date):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Fondo
    pdf.setFillColor(colors.HexColor("#F8F5EF"))
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    # Marco exterior
    pdf.setStrokeColor(colors.HexColor("#1F3A5F"))
    pdf.setLineWidth(4)
    pdf.rect(
        1 * cm,
        1 * cm,
        width - 2 * cm,
        height - 2 * cm
    )

    # Marco interior
    pdf.setStrokeColor(colors.HexColor("#C9A227"))
    pdf.setLineWidth(2)
    pdf.rect(
        1.5 * cm,
        1.5 * cm,
        width - 3 * cm,
        height - 3 * cm
    )

    # Título
    pdf.setFillColor(colors.HexColor("#1F3A5F"))
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(
        width / 2,
        height - 90,
        "CERTIFICADO DE FINALIZACIÓN"
    )

    # Texto introductorio
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        height - 150,
        "Se certifica que"
    )

    # Nombre estudiante
    pdf.setFillColor(colors.HexColor("#C9A227"))
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        width / 2,
        height - 210,
        student_name
    )

    # Texto
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        width / 2,
        height - 270,
        "ha completado satisfactoriamente el curso"
    )

    # Nombre curso
    pdf.setFillColor(colors.HexColor("#1F3A5F"))
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(
        width / 2,
        height - 330,
        course_title
    )

    # Datos
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 14)

    pdf.drawCentredString(
        width / 2,
        height - 390,
        f"Instructor: {instructor_name}"
    )

    pdf.drawCentredString(
        width / 2,
        height - 420,
        f"Fecha de emisión: {date}"
    )

    # Línea de firma
    pdf.line(
        width / 2 - 120,
        120,
        width / 2 + 120,
        120
    )

    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        width / 2,
        100,
        "Plataforma de Cursos Online"
    )

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer