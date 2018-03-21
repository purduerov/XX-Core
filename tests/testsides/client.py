from rovcontroller import ROVControl, getDefaultPackets

if __name__ == "__main__":
    con = ROVControl(port=5000)
    packets = getDefaultPackets("./packets.json")
    i = 0
    while True:
            print "XXXXXXXXXXXXXXXXXXXXXX", con.getClient()
            if i % 5 == 4:
                    print "XXXXXX", con.getFlask(packets['dearflask'])
            i+=1
