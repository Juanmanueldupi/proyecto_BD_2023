#Importar los modulos necesarios
import sys
import MySQLdb

#Conectar Base de Datos
def Conexion_BD(host,usuario,password,nombrebd):
    try:
        db = MySQLdb.connect(host,usuario,password,nombrebd)
        print("conectado a la base de datos:")
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
    1. Lista los participantes en la competición con toda su información y cuenta cuantos países están representados.
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
        Participantes = cursor.fetchall()
        participantes_por_pais = {}
        for Participante in Participantes:
            print("Codigo Participante:", Participante[0], "Codigo Pais:", Participante[1], "Nombre:", Participante[2], "Telefono:", Participante[3], "Dirección:", Participante[4])
            if Participante[1] in participantes_por_pais:
                participantes_por_pais[Participante[1]] += 1
            else:
                participantes_por_pais[Participante[1]] = 1
        print("Número de participantes por país:")
        for pais, num_participantes in participantes_por_pais.items():
            print("El pais nº:",pais,"tiene:", num_participantes,"participantes.")
    except:
        print("Error en la consulta")
    db.close()



#2. Buscar o filtrar informacion:

def Buscar(db,fecha):
    sql="SELECT p.Nombre, a.Fecha_Alojamiento FROM Alojamiento a INNER JOIN Participantes p ON a.NumAsociado = p.NumAsociado INNER JOIN Pais pa ON p.NumCorrelativo_Pais = pa.NumCorrelativo_Pais WHERE a.Fecha_Alojamiento >= '2022-03-2';"
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
    except:
       print("Error en la consulta")


#3. Buscar información relacionada: 

#def BuscarRelacionada(db,PaisOrigen):
#    sql="SELECT p.Nombre, p.NumAsociado, a.Fecha_Alojamiento FROM Participantes p LEFT JOIN Alojamiento a ON p.NumAsociado = a.NumAsociado JOIN Pais pa ON p.NumCorrelativo_Pais = pa.NumCorrelativo_Pais WHERE pa.Nombre_Pais = 'Portugal';"



#4. Insertar información: 
def NuevoParticipante(db,nuevo):
    cursor = db.cursor()
    sql="INSERT into Participantes values (%s, '%s', '%s', %f )" % (nuevo["NumAsociado"],nuevo["NumCorrelativo_Pais"],nuevo["Nombre"],nuevo["Telefono"],nuevo["Direccion"])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print("Error al insertar.")
        db.rollback()


#5. Borrar información:
#def BorrarInformacion(db,borrar):
    sql="DELETE a, p FROM Alojamiento a INNER JOIN Participantes p ON a.NumAsociado = p.NumAsociado INNER JOIN Pais pa ON p.NumCorrelativo_Pais = pa.NumCorrelativo_Pais WHERE pa.Nombre_Pais = 'Portugal'"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        if cursor.rowcount==0:
            print("No hay participantes nacidos en ese pais")
    except:
        print("Error al borrar.")
        db.rollback()

#6.Actualizar información:

#def ActualizarInformacion(db,actualizar):
sql="UPDATE Pais SET NumParticipantes = NumParticipantes + 5 WHERE NumCorrelativo_Pais = ( SELECT NumCorrelativo_Pais FROM Participantes WHERE NumAsociado = 1);"