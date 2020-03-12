#!/usr/bin/python3
from agente import *

while True:
    #Al agregar un agente, se cree una BD para ese agente y, empiece a guardar datos
    #Ahora, tambien almacenará datos del CPU, RAM y HDD, para notificar niveles altos de uso

    print("GESTOR DE REDES")
    print("1.- Agregar agente")
    print("2.- Eliminar agente")
    print("3.- Generar reporte")
    print("4.- Mostrar agentes (mostrar BD)")
    print("5.- Resumen agentes (info agentes)")

    opcion = int(input("Introduce una opcion: "))

    if opcion == 1:
        agregarAgente()
    elif opcion == 2:
        eliminarAgente()
    elif opcion == 3:
        generarReporte()
    elif opcion == 4:
        mostrarAgentes()
    elif opcion == 5:
        resumenAgentes()
    else:
        print("Escribre una opcion valida\n")
