import sys
import MySQLdb

def Conexion_BD(host,usuario,password,nombrebd):
    try:
        db = MySQLdb.connect(host,usuario,password,nombrebd)
        return db
    except MySQLdb.Error as e:
        print("No puedo conectar a la base de datos:",e)
        sys.exit(1)

def Dexconexion_BD(db):
    db.close()

def MostrarMenu():
    menu='''
    1. 
    2. 
    3.
    4. 
    5. 
    6. 
    0. Salir
    '''
    print(menu)
    while True:
        try:
            opcion=int(input("Opción:"))
            return opcion
        except:
            print("Opción incorrecta, el valor introducido debe cumplir el rango indicado.")


def Listar():