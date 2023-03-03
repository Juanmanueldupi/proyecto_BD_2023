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
    1. - Lista los Paises y su información.
    2. - Lista los Alojamiento y su informacióm.
    3. - Lista los Participantes y cuentas cuantos participantes comparten la misma nacionalidad.
    4. - Buscar o filtrar información: Introduce una fecha por pantalla y muestra la informacion de los Alojamientos de ese dia.
    5. - Buscar información relacionada:  Introduce el nombre de un País y muestra el nombre y NumAsociado del participante y si se Alojo en un Hotel la fecha del mismo.
    6. - Insertar información: Inseta los datos de un nuevo participante.
    7. - Borrar información: Elimina la informacion de los participantes del pais que introduzcas por teclado.
    8. - Actualizar información: Introduce un NumAsociado e incrementa en 5 el numero de participantes que pueden acudir al torneo que sean de su misma nacionalidad.
    0. Salir
    '''
    print(menu)
    while True:
        try:
            opcion=int(input("Opción:"))
            if opcion not in range(9):
                print("Opción incorrecta, el valor introducido debe cumplir el rango indicado.")
            return opcion
        except:
            print("Opción incorrecta, el valor introducido debe cumplir el rango indicado.")
            print(menu)


# 1.listar Pais
def Listar_Pais(db):
    sql ="SELECT * FROM Pais"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        Paises = cursor.fetchall()
        print("La informacion almacenada respecto a los Paises es:" )
        print()
        for Pais in Paises:
            print("NumCorrelativo_Pais:", Pais[0], "Nombre_Pais:", Pais[1], "NumClubs:", Pais[2], "NumParticipantes:", Pais[3])
            print()
    except:
        print("Error en la consulta")


# 2. Listar Alojamiento
def Listar_Alojamiento(db):
    sql ="SELECT * FROM Alojamiento"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        Alojamientos = cursor.fetchall()
        print("La informacion almacenada respecto a los Alojamientos es:" )
        print()
        for Alojamiento in Alojamientos:
            print("Fecha_Alojamiento:", Alojamiento[0], "NumAsociado:", Alojamiento[1], "Codigo_Hotel:", Alojamiento[2])
            print()
    except:
        print("Error en la consulta")


#3. Listar la informacion
def Listar(db):
    sql = "SELECT * from Participantes"
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        Participantes = cursor.fetchall()
        participantes_por_pais = {}
        for Participante in Participantes:
            print("Los datos de los Participantes son:")
            print()
            print("Codigo Participante:", Participante[0], "Codigo Pais:", Participante[1], "Nombre:", Participante[2], "Telefono:", Participante[3], "Dirección:", Participante[4])
            if Participante[1] in participantes_por_pais:
                participantes_por_pais[Participante[1]] += 1
            else:
                participantes_por_pais[Participante[1]] = 1
        print()
        print("Número de participantes por país:")
        print()
        for pais, num_participantes in participantes_por_pais.items():
            print("El pais nº:",pais,"tiene:", num_participantes,"participantes.")
    except:
        print("Error en la consulta")



#4. Buscar o filtrar informacion:

def Buscar(db,fecha):
    sql="SELECT p.Nombre, a.Fecha_Alojamiento FROM Alojamiento a INNER JOIN Participantes p ON a.NumAsociado = p.NumAsociado INNER JOIN Pais pa ON p.NumCorrelativo_Pais = pa.NumCorrelativo_Pais WHERE a.Fecha_Alojamiento >= DATE('%s')"%(fecha)
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        if len(registros) == 0:
            print("No se encontraron registros para la fecha indicada")
        else:
            print("Estos son los registros del Pais introducido: ")
            print()
            for registro in registros:
                print(registro["Nombre"],registro["Fecha_Alojamiento"])
                return registro["Nombre"],registro["Fecha_Alojamiento"]
    except:
       print("Error en la consulta")



#5. Buscar información relacionada: 

def BuscarRelacionada(db,PaisOrigen):
    sql="SELECT p.Nombre, p.NumAsociado, a.Fecha_Alojamiento FROM Participantes p LEFT JOIN Alojamiento a ON p.NumAsociado = a.NumAsociado JOIN Pais pa ON p.NumCorrelativo_Pais = pa.NumCorrelativo_Pais WHERE pa.Nombre_Pais = '%s'"%(PaisOrigen)
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        print("Estos son los registros del Pais introducido: ")
        print()
        for registro in registros:
            if registro["Fecha_Alojamiento"] is not None:
                print ("Nombre:",registro["Nombre"],"Número de Asociado:",registro["NumAsociado"],"Fecha de Alojamiento:",registro["Fecha_Alojamiento"])
                print()
                return registro["Nombre"],registro["NumAsociado"],registro["Fecha_Alojamiento"]

    except:
       print("Error en la consulta")


#6. Insertar información: 
def NuevoParticipante(db, nuevo):
    sql = "INSERT INTO Participantes (NumAsociado, NumCorrelativo_Pais, Nombre, Telefono, Direccion) VALUES (%s, %s, %s, %s, %s)"
    try:
        with db.cursor() as cursor:
            cursor.execute(sql, (nuevo["NumAsociado"], nuevo["NumCorrelativo_Pais"], nuevo["Nombre"], nuevo["Telefono"], nuevo["Direccion"]))
            db.commit()
            print()
            print("Participante introducido correctamente.")
    except:
        print("Error al insertar.")
        db.rollback()

#7. Borrar información:
def BorrarInformacion(db, borrar):
    sql = "DELETE a, p FROM Participantes a INNER JOIN Participantes p ON a.NumAsociado = p.NumAsociado INNER JOIN Pais pa ON p.NumCorrelativo_Pais = pa.NumCorrelativo_Pais WHERE pa.Nombre_Pais = '%s'" % (borrar)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        if cursor.rowcount == 0:
            print("No hay participantes nacidos en ese país.")
        else:
            print(f"Se han eliminado {cursor.rowcount} participantes nacidos en {borrar}.")
    except:
        print("Error al borrar.")
        db.rollback()

#8.Actualizar información:

def ActualizarInformacion(db,actualizar):
    sql="UPDATE Pais SET NumParticipantes = NumParticipantes + 5 WHERE NumCorrelativo_Pais = ( SELECT NumCorrelativo_Pais FROM Participantes WHERE NumAsociado = '%s')"%(actualizar)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        if cursor.rowcount > 0:
            print(f"Se han actualizado los datos del Pais del participante con número asociado {actualizar}.")
        else:
            print(f"No se puede actualizar la informacion del participante con numero asociado {actualizar} .")
    
    except:
        print("Error al actualizar la informacion")
        db.rollback()
