import rrdtool

def crearRRD(host):
    ret = rrdtool.create(host+".rrd",
                         "--start", 'N',
                         "--step", '60',
                         "DS:CPU:GAUGE:600:U:U",
                         "DS:RAM:GAUGE:600:U:U",
                         "DS:HDD:GAUGE:600:U:U",
                         "RRA:AVERAGE:0.5:1:24")
    rrdtool.dump(host+".rrd", host+".xml")

    if ret:
        print(rrdtool.error())
