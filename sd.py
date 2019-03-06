#!/usr/bin/env python3

import select, socket, sys, queue, struct

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 3333))
server.listen(5)

server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server2.bind(('0.0.0.0', 5555))
server2.listen(5)

server3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server3.bind(('0.0.0.0', 1111))
server3.listen(5)

inputs = [server, server2, server3]
outputs = []
message_queues = {}

while inputs:
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs)
    for s in readable:
        fp = open("sd.log", "a")
        connection, client_address = s.accept()
        fp.write("CONN: {}\n".format(client_address))
        the_mix = []
        try:
            while(True):
                data = connection.recv(2048)
                if data:
                    #fp.write("DATA: {}\n".format(data))
                    #print("[{}]: {}\n".format(len(data), data))
                    try:
                        header1 = struct.unpack('!H', data[0:2])[0]
                        header2 = struct.unpack('!H', data[2:4])[0]
                        header3 = struct.unpack('!I', data[4:8])[0]
                        print("HEAD: [{}] [{}] [{}]\n".format(header1, header2, header3))
                        fp.write("HEAD: [{}] [{}] [{}]\n".format(header1, header2, header3))
                        for x in range(1, int(header2 / 8)):
                            molecule = struct.unpack('!IHH', data[8 * x:(8 * x) + 8])
                            #print("{}: {}\n".format(x + 1, molecule))
                            the_mix.append(molecule)    
                    except:
                        print("Could not unpack\n")
                    ds_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    ds_address = ('10.40.13.151', 1111)
                    ds_socket.connect(ds_address)
                    ds_socket.send(data)
                    ds_socket.close()
                    print("DATA: [{}] {}\n".format(len(the_mix), the_mix))
                    fp.write("DATA: [{}] {}\n".format(len(the_mix), the_mix))
                    clorine = 0
                    air = 0
                    for x in the_mix:
                        if x[1] == x[2] and x[0] is not 0:
                            clorine += 1
                        if x[0] == 0:
                            air += 1
                    print("Clorine percent {}%\n".format(clorine /len(the_mix)))
                    print("Air percent {}%\n".format(air /len(the_mix)))    
                else:
                    fp.write("CLOS: No more data on {}\n".format(client_address))
                    break
        finally:
            connection.close()
        fp.close()

    for s in writable:
        pass

    for s in exceptional:
        pass


