from django.db import models
from django.db import connection, transaction, DatabaseError, IntegrityError, OperationalError

# Create your models here.


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_completed_by_account(username):
    response = {"data": {}, 'status': 200}
    where = ''

    sql = """SELECT s.* FROM bakerylovers.auth_user a, bakerylovers.classes c, bakerylovers.sessions s
            where a.username = c.username and c.sessionid = s.sessionid
            and a.username = %(username)s
            and s.enddt < current_date()
         """ + where

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, {'username': username})
            data = dict_fetchall(cursor)
            cursor.close()

    except OperationalError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-ADMIN-MODEL-GET-SESSIONS'}
        response['status'] = 400

    except DatabaseError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-ADMIN-MODEL-GET-SESSIONS'}
        response['status'] = 500

    if len(data):
        response['data'] = {'session_details': data}
    else:
        response = {"data": {}, 'status': 204}

    return response


def get_enrolled_by_account(username):
    response = {"data": {}, 'status': 200}
    where = ''

    sql = """SELECT s.* FROM bakerylovers.auth_user a, bakerylovers.classes c, bakerylovers.sessions s
            where a.username = c.username and c.sessionid = s.sessionid
            and a.username = %(username)s
            and s.startdt >= current_date()
         """ + where

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, {'username': username})
            data = dict_fetchall(cursor)
            cursor.close()

    except OperationalError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-ADMIN-MODEL-GET-SESSIONS'}
        response['status'] = 400

    except DatabaseError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-ADMIN-MODEL-GET-SESSIONS'}
        response['status'] = 500

    if len(data):
        response['data'] = {'session_details': data}
    else:
        response = {"data": {}, 'status': 204}
    return response
