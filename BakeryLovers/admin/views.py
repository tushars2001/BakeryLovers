from . import models
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import validate_email
import json
from django.db import DatabaseError, IntegrityError
from .models import isInt
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.


@staff_member_required(login_url='/login/?message=You cannot access this.')
def home(request):
    return render(request, 'home-admin.html')


@staff_member_required
def create_session(request):
    ret = {'status': 'ok', 'message': ''}
    fields = {}
    if request.method == 'POST':
        if 'title' in request.POST and len(request.POST['title']) \
                and 'enddt' in request.POST and len(request.POST['enddt']) \
                and 'startdt' in request.POST and len(request.POST['startdt']):
            fields['title'] = request.POST['title']
            fields['startdt'] = request.POST['startdt']
            fields['enddt'] = request.POST['enddt']
            fields['details'] = ''
            fields['fee'] = None
            if 'details' in request.POST:
                fields['details'] = request.POST['details']
            if 'fee' in request.POST:
                fields['fee'] = request.POST['fee']
            ret = models.create_session(fields)
        else:
            ret = {'status': 'fail', 'message': 'Required Field Issue'}
    return render(request, 'create-session.html', {'formFields': fields, 'ret': ret})


@staff_member_required
def view_sessions(request):

    data = {}
    data = models.get_sessions()

    return render(request, 'view-session.html', {'data': data})


@staff_member_required
def select_session(request):

    data = {}
    data = models.get_sessions()

    return render(request, 'select-session.html', {'data': data})


@staff_member_required
def view_accounts(request):

    data = {}
    data = models.get_accounts()

    return render(request, 'view-accounts.html', {'data': data})


@staff_member_required
def view_session_students(request):
    data = {}
    session = {}
    sessionid = None
    if request.method == 'POST' and 'sessionid' in request.POST:
        sessionid = request.POST['sessionid']
        data = models.get_students(sessionid)
        session = models.get_session_by_id(sessionid)

    return render(request, 'view-session-students.html', {'data': data, 'session': session})


@staff_member_required
def assign_students(request):
    data = {}
    if request.method == 'POST' and 'sessionid' in request.POST and isInt(request.POST['sessionid']):
        data = models.get_accounts_with_session(request.POST['sessionid'])

    return render(request, 'select-accounts.html', {
        'data': data,
        'sessionid': request.POST['sessionid'],
        'title': request.POST['title'],
    })


@staff_member_required
def session_students(request):
    data = {}
    ret = {}
    data = models.get_sessions()
    message = "Some Issue! Sorryy!"
    if request.method == 'POST' and 'sessionid' in request.POST and isInt(request.POST['sessionid']) \
            and len(request.POST.getlist('username')):
        ret = models.link_session_students(request.POST['sessionid'], request.POST.getlist('username'))
        message = "Students assigned to Session ID: " + request.POST['sessionid']
    return redirect("/administration/select-session/?message=" + message)


@staff_member_required
def create_account(request):
    ret = {'status': 'ok', 'message': ''}

    if request.method == 'POST':
        if create_account_br(request.POST):
            try:
                user = User.objects.create_user(request.POST['phone'], None, request.POST['phone'])
                user = authenticate(request, username=request.POST['phone'], password=request.POST['phone'])
                if user is not None:
                    ret = {'status': 'ok', 'message': 'Account Created!'}
                    return render(request, 'create-account.html', {'ret': ret})
                else:
                    ret = {'status': 'fail', 'message': 'Error Creating Account'}
            except IntegrityError:
                ret = {'status': 'fail', 'message': 'Account Already Exists!'}
            except DatabaseError:
                ret = {'status': 'fail', 'message': 'Something Wrong!'}
        else:
            ret = {'status': 'fail', 'message': 'Invalid Data Provided!'}

    return render(request, 'create-account.html', {'ret': ret})


def create_account_br(params):
    if 'phone' in params \
            and len(params['phone']) == 10 \
            and isInt(params['phone']):
        return True
    else:
        return False

