from django.db import models
from django.db import connection, transaction, DatabaseError, IntegrityError, OperationalError

# Create your models here.


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def create_session(fields):
    response = {"data": {}, 'status': 'ok', 'message': ''}
    data = {}
    if not isInt(fields['fee']):
        fields['fee'] = 0
    sql = """insert into sessions(title, startdt, enddt, details,fee) values (
        %(title)s,%(startdt)s,%(enddt)s,%(details)s,%(fee)s
    ) """
    sql_last_id = "SELECT LAST_INSERT_ID()"
    sessionid = None

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, fields)
            cursor.execute(sql_last_id)
            data = cursor.fetchall()
            cursor.close()
            sessionid = data[0][0]
            response['message'] = 'Session Created : ' + str(sessionid)
            response['data'] = sessionid

    except OperationalError as e:
        response['status'] = 'fail'
        response['message'] = str(e).split(",")[1].replace("'", "")

    except DatabaseError as e:
        response['status'] = 'fail'
        response['message'] = str(e).split(",")[1].replace("'", "")

    return response


def get_sessions():
    response = {"data": {}, 'status': 200}
    where = ''

    sql = """SELECT `sessions`.`sessionid`,
        `sessions`.`title`,
        `sessions`.`startdt`,
        `sessions`.`enddt`,
        `sessions`.`fee`,
        `sessions`.`videolinks`,
        `sessions`.`details`
        FROM `bakerylovers`.`sessions`;
     """ + where

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
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


def get_session_by_id(sessionid):
    response = {"data": {}, 'status': 200}
    where = ' where sessionid = %(sessionid)s'

    sql = """SELECT `sessions`.`sessionid`,
        `sessions`.`title`,
        `sessions`.`startdt`,
        `sessions`.`enddt`,
        `sessions`.`fee`,
        `sessions`.`videolinks`,
        `sessions`.`details`
        FROM `bakerylovers`.`sessions`
     """ + where

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, {'sessionid': sessionid})
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


def get_accounts():
    response = {"data": {}, 'status': 200}
    where = ''

    sql = """SELECT username, first_name,last_name, email, is_staff, is_active, date_joined FROM bakerylovers.auth_user
     """ + where

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            data = dict_fetchall(cursor)
            cursor.close()

    except OperationalError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-ADMIN-MODEL-GET-ACCOUNTS'}
        response['status'] = 400

    except DatabaseError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-ADMIN-MODEL-GET-ACCOUNTS'}
        response['status'] = 500

    if len(data):
        response['data'] = {'account_details': data}
    else:
        response = {"data": {}, 'status': 204}

    return response


def get_accounts_with_session(sessionid):
    response = {"data": {}, 'status': 200}

    sql = """SELECT a.*, case when recordid is not null then 1 else 0 end is_present FROM bakerylovers.auth_user a 
    left outer join  bakerylovers.classes c on a.username = c.username and c.sessionid=%(sessionid)s """

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, {'sessionid': sessionid})
            data = dict_fetchall(cursor)
            cursor.close()

    except OperationalError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-ADMIN-MODEL-GET-ACCOUNTS'}
        response['status'] = 400

    except DatabaseError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-ADMIN-MODEL-GET-ACCOUNTS'}
        response['status'] = 500

    if len(data):
        response['data'] = {'account_details': data}
    else:
        response = {"data": {}, 'status': 204}

    return response


def get_students(sessionid):
    response = {"data": {}, 'status': 200}
    where = ' where username in (select username from bakerylovers.classes where sessionid = %(sessionid)s)'

    sql = """SELECT username, first_name,last_name, email, is_staff, is_active, date_joined FROM bakerylovers.auth_user
     """ + where

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, {'sessionid': sessionid})
            data = dict_fetchall(cursor)
            cursor.close()

    except OperationalError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-INVALID-REQUEST-ADMIN-MODEL-GET-ACCOUNTS'}
        response['status'] = 400

    except DatabaseError as e:
        data = {'error': str(e).split(",")[1].replace("'", ""), 'code': 'DB-ADMIN-MODEL-GET-ACCOUNTS'}
        response['status'] = 500

    if len(data):
        response['data'] = {'account_details': data}
    else:
        response = {"data": {}, 'status': 204}

    return response


def link_session_students(sessionid, usernames):
    response = {"data": {}, 'status': 'ok', 'message': 'Students assigned to Session ID: ' + sessionid}
    sql_delete = "delete from bakerylovers.classes where sessionid = %(sessionid)s"

    with connection.cursor() as cursor:
        cursor.execute(sql_delete, {'sessionid': sessionid})
        cursor.close()

    for username in usernames:
        sql = "insert into bakerylovers.classes(sessionid, username) values (%(sessionid)s, %(username)s)"

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, {'sessionid': sessionid, 'username': username})
                cursor.close()

        except OperationalError as e:
            response['status'] = response['status'] + 'fail,'
            response['message'] = response['message'] + "," + str(e).split(",")[1].replace("'", "")

        except DatabaseError as e:
            response['status'] = response['status'] + 'fail,'
            response['message'] = response['message'] + "," + str(e).split(",")[1].replace("'", "")

    return response


def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
