from rovcontroller import ROVControl, getDefaultPackets

if __name__ == "__main__":
	con = ROVControl(port=5000)
	packets = getDefaultPackets("./packets.json")
	i = 0
	while True:
            con.getClient()
            if i % 5 == 4:
                    con.getFlask(packets['dearflask'])
            i+=1
