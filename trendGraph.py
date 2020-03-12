#Durante la grafica se realizará la monitorizacion

import rrdtool
from time import sleep
import threading
from Notify import send_alert_attached

def crearGraficas(host):
    ultima_lectura = int(rrdtool.last(host+".rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 3600

    # grafica para CPU
    """rrdtool.graph(host+"CPU.png",
                  "--start", str(tiempo_inicial),
                  "--end", str(tiempo_final),
                  "--vertical-label=Carga CPU",
                  "--title=Uso de CPU",
                  "--color", "ARROW#009900",
                  '--vertical-label', "Uso de CPU (%)",
                  '--lower-limit', '0',
                  '--upper-limit', '100',
                  "DEF:carga="+host+".rrd:CPU:AVERAGE",
                  "AREA:carga#00FF00:Carga CPU",
                  "LINE1:30",
                  "AREA:5#ff000022:stack",
                  "VDEF:CPUlast=carga,LAST",
                  "VDEF:CPUmin=carga,MINIMUM",
                  "VDEF:CPUavg=carga,AVERAGE",
                  "VDEF:CPUmax=carga,MAXIMUM",

                  "COMMENT:Now          Min             Avg             Max",
                  "GPRINT:CPUlast:%12.0lf%s",
                  "GPRINT:CPUmin:%10.0lf%s",
                  "GPRINT:CPUavg:%13.0lf%s",
                  "GPRINT:CPUmax:%13.0lf%s",
                  "VDEF:m=carga,LSLSLOPE",
                  "VDEF:b=carga,LSLINT",
                  'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                  "LINE2:tendencia#FFBB00")"""

    # grafica RAM
    rrdtool.graph(host+"RAM.png",
                  "--start", str(tiempo_inicial),
                  "--end", str(tiempo_final),
                  "--vertical-label=Carga RAM",
                  "--title=Uso de RAM",
                  "--color", "ARROW#009900",
                  '--vertical-label', "Uso de RAM (%)",
                  '--lower-limit', '0',
                  '--upper-limit', '100',
                  "DEF:carga="+host+".rrd:RAM:AVERAGE",
                  "AREA:carga#00FF00:Carga RAM",
                  "LINE1:30",
                  "AREA:5#ff000022:stack",
                  "VDEF:RAMlast=carga,LAST",
                  "VDEF:RAMmin=carga,MINIMUM",
                  "VDEF:RAMavg=carga,AVERAGE",
                  "VDEF:RAMmax=carga,MAXIMUM",

                  "COMMENT:Now          Min             Avg             Max",
                  "GPRINT:RAMlast:%12.0lf%s",
                  "GPRINT:RAMmin:%10.0lf%s",
                  "GPRINT:RAMavg:%13.0lf%s",
                  "GPRINT:RAMmax:%13.0lf%s",
                  "VDEF:m=carga,LSLSLOPE",
                  "VDEF:b=carga,LSLINT",
                  'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                  "LINE2:tendencia#FFBB00")

    # grafica HDD
    """rrdtool.graph(host+"HDD.png",
                  "--start", str(tiempo_inicial),
                  "--end", str(tiempo_final),
                  "--vertical-label=Carga HDD",
                  "--title=Uso de HDD",
                  "--color", "ARROW#009900",
                  '--vertical-label', "Uso de HDD (%)",
                  '--lower-limit', '0',
                  '--upper-limit', '100',
                  "DEF:carga="+host+".rrd:HDD:AVERAGE",
                  "AREA:carga#00FF00:Carga HDD",
                  "LINE1:30",
                  "AREA:5#ff000022:stack",
                  "VDEF:HDDlast=carga,LAST",
                  "VDEF:HDDmin=carga,MINIMUM",
                  "VDEF:HDDavg=carga,AVERAGE",
                  "VDEF:HDDmax=carga,MAXIMUM",

                  "COMMENT:Now          Min             Avg             Max",
                  "GPRINT:HDDlast:%12.0lf%s",
                  "GPRINT:HDDmin:%10.0lf%s",
                  "GPRINT:HDDavg:%13.0lf%s",
                  "GPRINT:HDDmax:%13.0lf%s",
                  "VDEF:m=carga,LSLSLOPE",
                  "VDEF:b=carga,LSLINT",
                  'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                  "LINE2:tendencia#FFBB00")"""

    """hilo2 = threading.Thread(target=analizarCPU, args=[host])
    hilo2.start()"""

    hilo3 = threading.Thread(target=analizarRAM, args=[host])
    hilo3.start()

    """hilo4 = threading.Thread(target=analizarHDD, args=[host])
    hilo4.start()"""


def analizarCPU(host):
    while True:
        # calculos de tiempos basado en la ultima entrada de la base
        tiempo_final = int(rrdtool.last(host+".rrd"))
        tiempo_inicial = tiempo_final - 3600
        ret = rrdtool.graphv(host+"CPU.png",
                             "--start", str(tiempo_inicial),
                             "--end", str(tiempo_final),
                             "--title", "Carga del microprocesador",
                             "--vertical-label=Uso de CPU (%)",
                             '--lower-limit', '0',
                             '--upper-limit', '100',
                             "DEF:carga="+host+".rrd:CPU:AVERAGE",
                             "CDEF:umbral70=carga,70,LT,0,carga,IF",
                             "CDEF:umbral80=carga,80,LT,0,carga,IF",
                             "CDEF:umbral90=carga,90,LT,0,carga,IF",
                             "VDEF:cargaMAX=carga,MAXIMUM",
                             "VDEF:cargaMIN=carga,MINIMUM",
                             "VDEF:cargaSTDEV=carga,STDEV",
                             "VDEF:cargaLAST=carga,LAST",
                             "AREA:carga#00FF00:Carga del CPU",
                             "AREA:umbral70#1ECC0E:Tráfico de carga mayor que 70",
                             "AREA:umbral80#C97D02:Tráfico de carga mayor que 80",
                             "AREA:umbral90#FF0000:Tráfico de carga mayor que 90",
                             "HRULE:45#1ECC0E:Umbral 1 - 80%",
                             "HRULE:50#C97D02:Umbral 80 - 90%",
                             "HRULE:60#FF0000:Umbral 90 - 100%",
                             "PRINT:cargaMAX:%6.2lf %S",
                             "GPRINT:cargaMIN:%6.2lf %SMIN",
                             "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                             "GPRINT:cargaLAST:%6.2lf %SLAST",
                              #Y = MX + B
                             "VDEF:m=carga,LSLSLOPE",
                             "VDEF:b=carga,LSLINT",
                             "CDEF:Y=carga,POP,m,COUNT,*,b,+",
                             "LINE2:Y#FF0000"
                             )
        # print (ret)
        # print(ret.keys())
        # print(ret.items())

        ultimo_valor = float(ret['print[0]'])

        #print("Ultimo valor CPU: "+ str(ultimo_valor))
        if ultimo_valor >= 70 and ultimo_valor < 80:
            #send_alert_attached("Sobrepasa 45% del CPU", host, "CPU")
            print("Sobrepasa 45% del CPU")
            sleep(60)
        elif ultimo_valor >= 80 and ultimo_valor < 90:
            #send_alert_attached("Sobrepasa 50% del CPU, cuidado", host, "CPU")
            print("Sobrepasa 50% del CPU, cuidado")
            sleep(60)
        elif ultimo_valor >= 90 and ultimo_valor <= 100:
            send_alert_attached("Sobrepasa 60% del CPU, niveles criticos", host, "CPU")
            print("Sobrepasa 60% del CPU, niveles criticos")
            sleep(60)

        sleep(5)



def analizarRAM(host):
    
    while True:
        # calculos de tiempos basado en la ultima entrada de la base
        tiempo_final = int(rrdtool.last(host+".rrd"))
        tiempo_inicial = tiempo_final - 3600
        ret = rrdtool.graphv(host+"RAM.png",
                             "--start", str(tiempo_inicial),
                             "--end", str(tiempo_final),
                             "--title", "Carga de Memoria RAM",
                             "--vertical-label=Uso de RAM (%)",
                             '--lower-limit', '0',
                             '--upper-limit', '100',
                             "DEF:carga="+host+".rrd:RAM:AVERAGE",
                             "CDEF:umbral60=carga,60,LT,0,carga,IF",
                             "CDEF:umbral75=carga,75,LT,0,carga,IF",
                             "CDEF:umbral85=carga,85,LT,0,carga,IF",
                             "VDEF:cargaMAX=carga,MAXIMUM",
                             "VDEF:cargaMIN=carga,MINIMUM",
                             "VDEF:cargaSTDEV=carga,STDEV",
                             "VDEF:cargaLAST=carga,LAST",
                             "AREA:carga#00FF00:Carga de la RAM",
                             "AREA:umbral60#1ECC0E:Tráfico de carga mayor que 60",
                             "AREA:umbral75#C97D02:Tráfico de carga mayor que 75",
                             "AREA:umbral85#FF0000:Tráfico de carga mayor que 85",
                             "HRULE:60#1ECC0E:Umbral 1 - 75%",
                             "HRULE:75#C97D02:Umbral 75 - 85%",
                             "HRULE:85#FF0000:Umbral 85 - 100%",
                             "PRINT:cargaMAX:%6.2lf %S",
                             "GPRINT:cargaMIN:%6.2lf %SMIN",
                             "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                             "GPRINT:cargaLAST:%6.2lf %SLAST")
        # print (ret)
        # print(ret.keys())
        # print(ret.items())

        ultimo_valor = float(ret['print[0]'])

        print("Ultimo valor RAM: "+ str(ultimo_valor))
        if ultimo_valor >= 60 and ultimo_valor < 75:
            send_alert_attached("Sobrepasa 60% de la RAM", host, "RAM")
            print("Sobrepasa 60% de la RAM")
            sleep(60)
        elif ultimo_valor >= 75 and ultimo_valor < 85:
            send_alert_attached("Sobrepasa 75% de la RAM", host, "RAM")
            print("Sobrepasa 75% de la RAM, cuidado")
            sleep(60)
        elif ultimo_valor >= 90 and ultimo_valor <= 100:
            send_alert_attached("Sobrepasa 90% de la RAM, niveles criticos", host, "RAM")
            print("Sobrepasa 90% de la RAM, niveles criticos")
            sleep(60)

        sleep(5)

def analizarHDD(host):
    while True:
        # calculos de tiempos basado en la ultima entrada de la base
        tiempo_final = int(rrdtool.last(host+".rrd"))
        tiempo_inicial = tiempo_final - 3600
        ret = rrdtool.graphv(host+"HDD.png",
                             "--start", str(tiempo_inicial),
                             "--end", str(tiempo_final),
                             "--title", "Carga del disco duro",
                             "--vertical-label=Uso de HDD (%)",
                             '--lower-limit', '0',
                             '--upper-limit', '100',
                             "DEF:carga="+host+".rrd:HDD:AVERAGE",
                             "CDEF:umbral45=carga,45,LT,0,carga,IF",
                             "CDEF:umbral50=carga,50,LT,0,carga,IF",
                             "CDEF:umbral60=carga,60,LT,0,carga,IF",
                             "VDEF:cargaMAX=carga,MAXIMUM",
                             "VDEF:cargaMIN=carga,MINIMUM",
                             "VDEF:cargaSTDEV=carga,STDEV",
                             "VDEF:cargaLAST=carga,LAST",
                             "AREA:carga#00FF00:Carga del HDD",
                             "AREA:umbral45#1ECC0E:Tráfico de carga mayor que 45",
                             "AREA:umbral50#C97D02:Tráfico de carga mayor que 50",
                             "AREA:umbral60#FF0000:Tráfico de carga mayor que 60",
                             "HRULE:45#1ECC0E:Umbral 1 - 45%",
                             "HRULE:50#C97D02:Umbral 45 - 50%",
                             "HRULE:60#FF0000:Umbral 60 - 100%",
                             "PRINT:cargaMAX:%6.2lf %S",
                             "GPRINT:cargaMIN:%6.2lf %SMIN",
                             "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                             "GPRINT:cargaLAST:%6.2lf %SLAST")
        # print (ret)
        # print(ret.keys())
        # print(ret.items())

        ultimo_valor = float(ret['print[0]'])

        #print("Ultimo valor HDD: "+ str(ultimo_valor))
        if ultimo_valor >= 45 and ultimo_valor < 50:
            #send_alert_attached("Sobrepasa 45% del HDD", host, "HDD")
            print("Sobrepasa 45% del HDD")
            sleep(60)
        elif ultimo_valor >= 50 and ultimo_valor < 60:
            #send_alert_attached("Sobrepasa 50% del HDD, cuidado", host, "HDD")
            print("Sobrepasa 50% del HDD, cuidado")
            sleep(60)
        elif ultimo_valor >= 60 and ultimo_valor <= 100:
            send_alert_attached("Sobrepasa 60% del HDD, niveles criticos", host, "HDD")
            print("Sobrepasa 60% del HDD, niveles criticos")
            sleep(60)

        sleep(5)
