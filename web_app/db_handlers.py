import os

import psycopg2 as pg

DB_PASS = os.getenv("INJ_PASS")

def db_login(login, password):
    connection = pg.connect(user="postgres", password=DB_PASS, host="127.0.0.1", port="5432", database='injection')

    cursor = connection.cursor()

    cursor.callproc('authentification', (login, password))
    res = cursor.fetchone()
    cursor.close()
    connection.close()
    return res[0]

def db_register(login, password):
    connection = pg.connect(user="postgres", password=DB_PASS, host="127.0.0.1", port="5432", database='injection')
    cursor = connection.cursor()

    cursor.callproc('registration', (login, password))
    res = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return res[0]

def getClientData(user):
    connection = pg.connect(user="postgres", password=DB_PASS, host="127.0.0.1", port="5432", database='injection')
    cursor = connection.cursor()

    cursor.callproc('getClientData', (user,))
    clientData = cursor.fetchone()
    cursor.close()
    clientData = {
        'Firstname': clientData[0],
        'Lastname': clientData[1],
        'BirthDate': clientData[2].strftime("%Y-%m-%d"),
        'Phone': clientData[3],
        'Email': clientData[4],
        'PersonalDiscount': clientData[5],
        'DeliveryAdress': clientData[6]
    }
    connection.close()
    return clientData