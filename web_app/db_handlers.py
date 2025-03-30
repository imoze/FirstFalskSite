import os

import psycopg2 as pg

DB_PASS = os.getenv("INJ_PASS")

def db_login(login, password):
    connection = pg.connect(user="postgres", password=DB_PASS, host="127.0.0.1", port="5432", database='SiteDB')

    cursor = connection.cursor()

    cursor.callproc('authentification', (login, password))
    res = cursor.fetchone()
    cursor.close()
    connection.close()
    return res[0]

def db_register(login, password):
    connection = pg.connect(user="postgres", password=DB_PASS, host="127.0.0.1", port="5432", database='SiteDB')
    cursor = connection.cursor()

    cursor.callproc('registration', (login, password))
    res = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return res[0]

def getClientData(user):
    connection = pg.connect(user="postgres", password=DB_PASS, host="127.0.0.1", port="5432", database='SiteDB')
    cursor = connection.cursor()

    cursor.callproc('getClientData', (user,))
    clientData = cursor.fetchone()
    cursor.close()
    clientData = {
        'Firstname': clientData[0] if clientData else '',
        'Lastname': clientData[1] if clientData else '',
        'BirthDate': clientData[2].strftime("%Y-%m-%d") if clientData else '',
        'Phone': clientData[3] if clientData else '',
        'Email': clientData[4] if clientData else '',
        'PersonalDiscount': clientData[5] if clientData else '',
        'DeliveryAdress': clientData[6] if clientData else ''
    }
    connection.close()
    return clientData


def setClientData(dataPull):
    connection = pg.connect(user="postgres", password=DB_PASS, host="127.0.0.1", port="5432", database='SiteDB')
    cursor = connection.cursor()

    cursor.callproc('setClientData', (*dataPull,))
    res = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return res

def orderSum(data):
    connection = pg.connect(user="postgres", password=DB_PASS, host="127.0.0.1", port="5432", database='SiteDB')
    cursor = connection.cursor()

    cursor.callproc('summ_for_order', (*data,))
    res = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return res

def placeOrder(data):
    connection = pg.connect(user="postgres", password=DB_PASS, host="127.0.0.1", port="5432", database='SiteDB')
    cursor = connection.cursor()

    cursor.callproc('place_order', (*data,))
    res = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return res

def getOrders(user):
    connection = pg.connect(user="postgres", password=DB_PASS, host="127.0.0.1", port="5432", database='SiteDB')
    cursor = connection.cursor()

    cursor.callproc('getOrders', (user,))
    res = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    res = [
        {
            'id': order[0],
            'model': order[1],
            'quantity': order[2],
            'order_date': order[3],
            'delivery_date': order[4],
            'total_amount': order[5],
            'completed': order[6]
        }
        for order in res 
    ]
    return res