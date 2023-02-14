#Importar los modulos necesarios
import sys
import MySQLdb

#Conectar Base de Datos
def Conexion_BD(host,usuario,password,nombrebd):
    try:
        db = MySQLdb.connect(host,usuario,password,nombrebd)
        return db
    except MySQLdb.Error as e:
        print("No puedo conectar a la base de datos:",e)
        sys.exit(1)


#0. Desconectar 
def Dexconexion_BD(db):
    db.close()

#Menu
def MostrarMenu():
    menu='''
    1. Listar los participantes en la competición con toda su información y contar cuantos paises estan representados.
    2. - Buscar o filtrar información: 
    3. - Buscar información relacionada: 
    4. - Insertar información: 
    5. - Borrar información: 
    6. - Actualizar información: 
    0. Salir
    '''
    print(menu)
    while True:
        try:
            opcion=int(input("Opción:"))
            return opcion
        except:
            print("Opción incorrecta, el valor introducido debe cumplir el rango indicado.")


#1. Listar la informacion
def Listar(db):
    sql = "SELECT * from Participantes"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        for registro in registros:
            print(registro[0],registro[1],registro[2],registro[3],registro[4])
    except:
        print("Error en la consulta")
    db.close()
