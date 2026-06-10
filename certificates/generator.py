from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas


def generate_certificate(student_name, course_title, instructor_name, date):
    buffer = BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(width / 2, height - 100, "CERTIFICADO DE FINALIZACIÓN")

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(width / 2, height - 160, "Se certifica que")

    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(width / 2, height - 210, student_name)

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(width / 2, height - 260, "completó satisfactoriamente el curso")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(width / 2, height - 310, course_title)

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(width / 2, height - 370, f"Instructor: {instructor_name}")
    pdf.drawCentredString(width / 2, height - 400, f"Fecha: {date}")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer