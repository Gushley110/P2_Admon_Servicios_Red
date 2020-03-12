from trendCreate import crearRRD
from trendUpdate import actualizarRRD
from trendGraph import *
from getSNMP import consultaSNMP
from reporte import crearPDF
from os import remove
import os.path
import threading

# Que revise si existe el archivo, si no, que lo cree
def agregarAgente():
    # Que reciba los datos: nombre host/dirrecion IP - version SNMP - nombre comunidad - puerto
    archivo = open('agentes.txt', 'ta')  # Archivo de texto - escritura al final
    direccion = str(input("Introduce el host/direccion IP: "))
    version = str(input("Introduce la version SNMP a usar: "))
    comunidad = str(input("Introduce el nombre de la comunidad: "))
    puerto = str(input("Introduce el puerto a usar: "))
    linea = str(direccion + " " + version + " " + comunidad + " " + puerto + "\n")

    archivo.write(linea)
    archivo.close()

    # Ya esta guardado en el archivo, hay que usar esos datos para crear la BD
    crearRRD(direccion)
    # actualizarRRD(direccion, version, comunidad, puerto)
    # Para que la actualizacion no bloquee el sistema, que se haga por medio de un hilo en segundo plano
    hilo = threading.Thread(target=actualizarRRD, args=(direccion, version, comunidad, puerto))
    hilo.start()

    # Vaya creando las imagnes del CPU, RAM y HDD para que haga la deteccion de uso
    # El reporte se genera cuando uno de los estatus es muy alto, o bien, cuando quiera el usuario
    # Primero, crear una grafica base y luego, actualizarlas
    hilo2 = threading.Thread(target=crearGraficas, args=[direccion])
    hilo2.start()

    print("Agente agregado\n")


def eliminarAgente():
    agente = str(input("Introduce el host/direccion IP del agente a eliminar: "))
    archivo = open('agentes.txt', 'r+')  # Archivo de texto - escritura al final

    texto = archivo.read()  # Tenemos el archivo completo
    lista = texto.split("\n")
    texto = ""
    for aux in lista:
        if aux.find(agente):  # No es
            texto += aux + "\n"
        else:  # Si es
            texto += ""

    archivo.seek(0)
    archivo.truncate()  # Borrando
    archivo.write(texto)
    archivo.close()
    print("Agente eliminado\n")

    # Tambien elimine lor archivos relacionados
    remove(agente + ".rrd")
    remove(agente + ".xml")
    if os.path.isfile("reporte-" + agente + ".pdf"):
        remove("reporte-" + agente + ".pdf")
    if os.path.isfile(agente + "_1.png"):
        remove(agente + "_1.png")
    if os.path.isfile(agente + "_2.png"):
        remove(agente + "_2.png")
    if os.path.isfile(agente + "_3.png"):
        remove(agente + "_3.png")
    if os.path.isfile(agente + "_4.png"):
        remove(agente + "_4.png")
    if os.path.isfile(agente + "_5.png"):
        remove(agente + "_5.png")


def generarReporte():
    direccion = str(input("Introduce el host/direccion del agente que quiera reporte: "))
    # Ademas de las graficas, lleva los datos:
    # nombre, version y logo del SO - ubicacion geografica - num puertos - actividad desde el ultimo reinicio - comunidad - IP
    #Las graficas siempre estan creadas. Solo es tomarlas
    crearPDF(direccion)
    print("Reporte generado\n")


def mostrarAgentes():
    archivo = open('agentes.txt', 'r')  # Archivo de texto - escritura al final
    texto = archivo.read()  # Tenemos el archivo completo
    print(texto + "\n")


def resumenAgentes():
    # agente[0] - host
    # agente[1] - version
    # agente[2] - comunidad
    # agente[3] - puerto
    archivo = open('agentes.txt', 'r')  # Archivo de texto - escritura al final
    texto = archivo.read()  # Tenemos el archivo completo
    lista = texto.split("\n")

    dispositivos = 0
    for aux in lista:
        agente = aux.split(" ")
        if agente[0] != "":
            dispositivos = dispositivos + 1
            print("\nAgente: " + agente[0])

            estatus_agente = str(
                consultaSNMP(agente[2], agente[0],
                             '1.3.6.1.2.1.2.2.1.7.' + agente[3]))
            if estatus_agente != 0:
                print("\tEstatus del agente: Up")
            else:
                print("\tEstatus del agente: Down")

            num_puertos = str(
                consultaSNMP(agente[2], agente[0],
                             '1.3.6.1.2.1.2.1.0'))
            print("\tNumero de puertos del agente: " + num_puertos)
    print("\nNumero total de dispositivos monitoreados: " + str(dispositivos) + "\n")
