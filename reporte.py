#!/usr/bin/python3
from getSNMP import consultaSNMP
from reportlab.pdfgen import canvas

def crearPDF(host):
    # A sacar el agente del TXT
    archivo = open('agentes.txt', 'r')  # Archivo de texto - escritura al final
    texto = archivo.read()  # Tenemos el archivo completo
    lista = texto.split("\n")
    for aux in lista:
        agente = aux.split(" ")
        if agente[0] == host:
            break

    #agente[0] - host
    #agente[1] - version
    #agente[2] - comunidad
    #agente[3] - puerto

    # sysDescr
    sistema_operativo = consultaSNMP(agente[2].replace(" ", ""), host.replace(" ", ""),
                     '1.3.6.1.2.1.1.1.0')

    if sistema_operativo != "Linux":
        sistema_operativo = "Windows"

    tiempo_actividad = int(
        consultaSNMP(agente[2].replace(" ", ""), host.replace(" ", ""),
                     '1.3.6.1.2.1.1.3.0'))
    horas = int(tiempo_actividad / 3600)
    tiempo_actividad = tiempo_actividad - horas*3600

    minutos = int(tiempo_actividad / 60)
    tiempo_actividad = tiempo_actividad - minutos*60

    num_puertos = str(
        consultaSNMP(agente[2].replace(" ", ""), host.replace(" ", ""),
                     '1.3.6.1.2.1.2.1.0'))

    pdf = canvas.Canvas("reporte-"+host+".pdf")
    pdf.setLineWidth(.3)
    pdf.setFont('Helvetica', 12)

    pdf.drawString(30, 750, "Sistema operativo: " + sistema_operativo)
    pdf.drawString(30, 735, "Numero de puertos: " + num_puertos)
    pdf.drawString(30, 720, "Tiempo de actividad desde el ultimo reinicio: " +str(horas)+ " horas, " +str(minutos)+ " minutos, " +str(tiempo_actividad)+ " segundos" )
    pdf.drawString(30, 705, "Comunidad: " + agente[2])
    pdf.drawString(30, 690, "IP: " + agente[0])

    pdf.drawImage(agente[0] + "RAM.png", 30, 555, 250, 100)
    #pdf.drawString(30, 500, "El uso de la RAM ha llegado a niveles alto. Por favor, verificar su estado")

    if sistema_operativo == "Linux":
        pdf.drawImage("linux.png", 400, 750, 75, 75)
    else:
        pdf.drawImage("windows.png", 450, 700, 75, 50)

    pdf.save()
