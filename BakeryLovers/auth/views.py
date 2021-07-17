from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import DatabaseError, IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as l
from . import models
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


# Create your views here.


def home(request):
    return render(request, "auth_login.html")


def create_account(request):
    context_data = {}

    if request.method == 'POST':
        if create_account_br(request.POST):
            try:
                user = User.objects.create_user(request.POST['phone'], request.POST['email'], request.POST['password'])
                user.first_name = request.POST['fname']
                user.last_name = request.POST['lname']
                user.save()
                user = authenticate(request, username=request.POST['phone'], password=request.POST['password'])
                if user is not None:
                    login(request, user)
                    # Redirect to a success page.
                    context_data = {"success": "Account created! <br>"
                                               + " You can update profile later and continue to use app from menu."}
                    return redirect('/my-account/?success=' + context_data['success'])
                else:
                    context_data = {"error": "Error Creating Account"}
            except IntegrityError:
                context_data = {"error": "This phone already exists. Try login or resetting password if you forgot."}
            except DatabaseError:
                context_data = {"error": "Something Wrong! Database didn't like it."}
        else:
            context_data = {"error": "Invalid values provided"}
    return render(request, "auth_create-account.html")


@login_required
def account_update(request):
    first_name = ''
    last_name = ''
    email = ''

    if request.method == 'POST':
        if 'fname' in request.POST:
            first_name = request.POST['fname']
        if 'lname' in request.POST:
            last_name = request.POST['lname']
        if 'email' in request.POST:
            email = request.POST['email']
        u = User.objects.get(username=request.user.username)
        u.first_name = first_name
        u.last_name = last_name
        u.email = email
        u.save()
    return redirect('/my/account/')


def reset_password(request):
    return render(request, "auth_reset_password.html")


@login_required
def my_account(request):
    return render(request, "auth_my_account.html")


def create_account_br(params):
    if 'phone' in params \
            and 'password' in params \
            and 'password_confirm' in params \
            and len(params['phone']) == 10 \
            and isInt(params['phone']) \
            and len(params['password']) >= 3 \
            and len(params['password_confirm']) >= 3 \
            and params['password_confirm'] == params['password']:
        return True
    else:
        return False


def logout(request):
    l(request)
    return redirect('/')


def login_user(request):
    message = ''
    if request.method == 'POST' and 'phone' in request.POST and 'password' in request.POST:
        user = authenticate(request, username=request.POST['phone'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('/my-account/')
        else:
            return redirect('/login/?message=Invalid User ID/Password')

    if request.method == 'GET' and 'message' in request.GET:
        message = request.GET['message']

    return render(request, "auth_login.html", {"message": message})


@login_required
def completed_courses(request):
    data = {}
    data = models.get_completed_by_account(request.user.username)

    return render(request, 'my_completed_courses.html', {'data': data})


@login_required
def enrollments(request):
    data = {}
    data = models.get_enrolled_by_account(request.user.username)

    return render(request, 'my_enrollments.html', {'data': data})


def certificate(request):
    if request.method == 'POST':
        if 'first_name' in request.POST and 'last_name' in request.POST and 'username' in request.POST \
                and 'enddt' in request.POST and 'title' in request.POST:
            if len(request.POST['first_name']) == 0:
                return HttpResponse(content="No Name. You need to update profile with name.")
        else:
            return HttpResponse(content="Invalid Request")
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        dt = request.POST['enddt']
        course = request.POST['title']
        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer, pagesize=landscape(A4))
        width, height = landscape(A4)
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.

        p.drawInlineImage(str(settings.BASE_DIR) + "/BakeryLovers/static/cert.png", 0, 0, width, height)
        # p.drawString(100, height/2, "Hello world.")
        lalign = 370
        p.setFont("Times-Roman", 30)
        p.setFillColor(red)
        text = fname
        text_width = stringWidth(text, fontName="Times-Roman", fontSize=40)
        y = height / 2  # wherever you want your text to appear
        p.drawString(lalign, y + 10, text)
        p.setFillColor(magenta)

        p.setFont("Times-Roman", 30)
        p.setFillColor(red)
        text = lname
        text_width = stringWidth(text, fontName="Times-Roman", fontSize=40)
        y = height / 2  # wherever you want your text to appear
        p.drawString(lalign, y - 30, text)
        p.setFillColor(magenta)

        p.setFont("Times-Roman", 25)
        p.setFillColor(blue)
        text = dt
        text_width = stringWidth(text, fontName="Times-Roman", fontSize=25)
        y = height / 2  # wherever you want your text to appear
        p.drawString(lalign + 210, y - 190, text)
        p.setFillColor(blue)

        p.setFont("Times-Roman", 20)
        text = course
        text_width = stringWidth(text, fontName="Times-Roman", fontSize=20)
        y = height / 2  # wherever you want your text to appear
        p.drawString(lalign, y - 130, text)
        p.setFillColor(blue)

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='barekyLovers_certificate_' + fname + '.pdf')
    else:
        return HttpResponse(content="Error!")


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
