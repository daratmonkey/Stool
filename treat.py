#!/usr/bin/env python3

import select, socket, sys, struct
from water import Water

def log_it(mtype, message):
    fp = open("sd.log", "a")
    fp.write("{}: {}\n".format(mtype, message))
    fp.close()
    print("{}: {}\n".format(mtype, message))

def send_it(dest, port, data):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (dest, port)
        sock.connect(address)
        sock.send(data)
        sock.close()
    except:
        log_it("ERRO", "Could not send to downstream")

def main():
    downstream = "10.40.13.151"
    liquid = True
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
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for s in readable:
            connection, client_address = s.accept()
            print("----------------------------------------------")
            log_it("CONN", client_address)
            
            the_mix = []
            try:
                while(True):
                    data = connection.recv(2048)
                    if data:
                        try:
                            header1 = struct.unpack('!H', data[0:2])[0]
                            header2 = struct.unpack('!H', data[2:4])[0]
                            header3 = struct.unpack('!I', data[4:8])[0]
                            
                            log_it("HEAD", "type:{} size:{} custom:{}]".format(header1, header2, header3))
                            
                            for x in range(1, int(header2 / 8)):
                                molecule = struct.unpack('!IHH', data[8 * x:(8 * x) + 8])
                                the_mix.append(molecule)    
                            
                            log_it("DATA", "[{}] {}".format(len(the_mix), the_mix))

                        except:
                            log_it("ERRO", "Could not unpack data")
                        
                        ww = Water(the_mix)
                        #print(ww.mix)
                        print("Treat trash poop: {}".format(ww.treat_trash_poop()))
                        #print(ww.mix)
                        print("Treat poop      : {}".format(ww.treat_poop()))
                        #print(ww.mix)
                        print("Amount of debris: {}".format(len(ww.trash)))
                        print("Treat ammonia   : {}".format(ww.treat_ammonia()))
                        ww.treat_mercury()
                        print("Treat mercury   : {}".format(ww.merc_level))
                        #print(ww.mix)
                        
                        #print(ww.mix)
                        air = 0
                        for x in ww.data:
                            if x[0] == 0:
                                air += 1
                        print("Air             : {}".format(air))
                        #print("Send stuff")


                        if len(ww.trash) > 0:
                            debris_final = struct.pack('!HHI', 1, (len(ww.trash) * 8) + 8, 0)
                            debris_final += ww.serialize_trash()
                            send_it(downstream, 2222, debris_final)
                            log_it("DEBR", "[{}] {}".format(int((len(debris_final) - 8) / 8), debris_final))

                        if len(ww.hazmat) > 0:
                            hazmat_final = struct.pack('!HHI', 4, (len(ww.hazmat) * 8) + 8, 0)
                            hazmat_final += ww.serialize_hazmat()
                            send_it(downstream, 8888, hazmat_final)
                            log_it("HAZM", "[{}] {}".format(int((len(hazmat_final) - 8) / 8), hazmat_final))

                        if len(ww.mix) > 0:
                            water_final = struct.pack('!HHI', 0, (len(ww.mix) * 8) + 8, 0)
                            water_final += ww.serialize_water()
                            send_it(downstream, 1111, water_final)
                            log_it("WATR", "[{}] {}".format(int((len(water_final) - 8) / 8), water_final))
                        print("++++++++++++++++++++++++++++++++++++++++")
                        print(ww)
                        print("++++++++++++++++++++++++++++++++++++++++")

                    else:
                        break
            finally:
                connection.close()

if __name__ == "__main__":
    main()