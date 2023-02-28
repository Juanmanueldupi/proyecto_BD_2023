from MariaDBPython3 import *

db = Conexion_BD("localhost","juanmad","juanmad","Python3")

opcion=MostrarMenu()
while opcion != 0:
    if opcion == 1:
        Listar(db)
    elif opcion == 2:
        fecha = input("Introduce una fecha por pantalla: ")
        Buscar(db,fecha)
    elif opcion == 3:
        PaisOrigen= input("Introduce el nombre de tu pais de origen: ")
        BuscarRelacionada(db,PaisOrigen)
    elif opcion == 4:
        nuevo={}
        nuevo["NumAsociado"]=input("Introduce el numero de Asociado:")
        nuevo["NumCorrelativo_Pais"]=input("Introduce el codigo de tu Pais():")
        nuevo["Nombre"]=input("Introduce el Nombre")
        nuevo["Telefono"]=(input("Introduce el Telefono:"))
        nuevo["Direccion"]=input("Introduce la Direccion:")
        NuevoParticipante(db,nuevo)
    elif opcion == 5:
        borrar = input("Introduce el nombre de un pais: ")
        BorrarInformacion(db,borrar)
    elif opcion == 6:
        actualizar = float(input(""))
        ActualizarInformacion(db,actualizar)

    
    opcion=MostrarMenu()
Dexconexion_BD(db)