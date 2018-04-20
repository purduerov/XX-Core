from rovcontroller import ROVControl, getDefaultPackets

if __name__ == "__main__":
    con = ROVControl(IP="10.42.0.177",port=5000)
    packets = getDefaultPackets("./packets.json")
    i = 0
    while True:
            print "XXXXXXXXXXXXXXXXXXXXXX", con.getClient()
            packets['dearflask']['manipulator'] = -0.1
            packets['dearflask']['obs_tool'] = 0.1
            packets['dearflask']['transmitter'] = True
            packets['dearflask']['magnet'] = True
            packets['dearflask']['maincam_angle'] = 0
            if i % 5 == 4:
                    print "XXXXXX", con.getFlask(packets['dearflask'])
            i+=1
