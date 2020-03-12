from time import sleep
import rrdtool
from getSNMP import consultaSNMP

MEMORIA = 16


def actualizarRRD(host, version, comunidad, puerto):
    while 1:
        cpu = int(
            consultaSNMP(comunidad, host,
                         '1.3.6.1.2.1.25.3.3.1.2.196608'))

        ramTotal = float(
            consultaSNMP(comunidad, host,
                         '1.3.6.1.4.1.2021.4.5.0'))
        ramLibre = float(
            consultaSNMP(comunidad, host,
                         '1.3.6.1.4.1.2021.4.11.0')
        )
        porcentaje_ram = float(((ramTotal-ramLibre)*100)/ramTotal)

        """ram = int(
            consultaSNMP(comunidad, host,
                         '1.3.6.1.4.1.2021.4.5.0'))
        porcentaje_ram = ((8-ram)*100)/ram"""

        """ram = int(
            consultaSNMP(comunidad, host,
                         '1.3.6.1.4.21.'+puerto))
        porcentaje_ram = (ram*100)/float(16)"""

        hdd = float(
            consultaSNMP(comunidad, host,
                         '1.3.6.1.2.1.25.2.3.1.6.1'))
        porcentaje_hdd = hdd / (1024 * 1024)

        valor = "N:" + str(cpu) + ":" + str(porcentaje_ram) + ":" + str(porcentaje_hdd)
        # print(valor)
        rrdtool.update(host + ".rrd", valor)
        rrdtool.dump(host + ".rrd", host + ".xml")
        sleep(1)
