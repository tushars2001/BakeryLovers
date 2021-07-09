from django.http import JsonResponse
from django.shortcuts import render
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
# Create your views here.
from reportlab.lib.pagesizes import letter, A4, landscape
import pdb
from django.conf import settings
from reportlab.lib.units import inch
from reportlab.lib.colors import magenta, red, blue
from reportlab.pdfbase.pdfmetrics import stringWidth


def home(request):
    return render(request, 'home.html')


def pdftest(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    fname = request.POST['fname']
    lname = request.POST['lname']
    dt = request.POST['dt']
    course = request.POST['course']
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    p.drawInlineImage(str(settings.BASE_DIR) + "/BakeryLovers/static/cert.png", 0, 0, width, height)
    # p.drawString(100, height/2, "Hello world.")
    p.setFont("Times-Roman", 30)
    p.setFillColor(red)
    text = fname
    text_width = stringWidth(text, fontName="Times-Roman", fontSize=40)
    y = height/2  # wherever you want your text to appear
    p.drawString((width - text_width) / 2.0+8, y+10, text)
    p.setFillColor(magenta)

    p.setFont("Times-Roman", 30)
    p.setFillColor(red)
    text = lname
    text_width = stringWidth(text, fontName="Times-Roman", fontSize=40)
    y = height / 2  # wherever you want your text to appear
    p.drawString((width - text_width) / 2.0+8, y-30, text)
    p.setFillColor(magenta)

    p.setFont("Times-Roman", 25)
    p.setFillColor(blue)
    text = dt
    text_width = stringWidth(text, fontName="Times-Roman", fontSize=25)
    y = height / 2  # wherever you want your text to appear
    p.drawString((width - text_width) / 2.0+200, y - 190, text)
    p.setFillColor(blue)

    p.setFont("Times-Roman", 20)
    text = course
    text_width = stringWidth(text, fontName="Times-Roman", fontSize=20)
    y = height / 2  # wherever you want your text to appear
    p.drawString((width - text_width) / 2.0+9, y - 130, text)
    p.setFillColor(blue)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='barekyLovers_certificate_'+fname+'.pdf')

