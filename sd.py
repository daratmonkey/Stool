#!/usr/bin/env python3

import select, socket, sys, queue, struct

def de_merc(mix_dict):
    nums = []
    for x in mix_dict:
        nums.append(0)

    for i, x in enumerate(mix_dict):
        for y in mix_dict:
            if x is not y:
                if mix_dict[y][0] == x or mix_dict[y][1] == x:
                    nums[i] += 1    

    print("MERC: {}".format(nums))

    m_list = []
    for i, x in enumerate(nums):
        if x == 0:
            m_list.append(list(mix_dict.keys())[i])
    m_list.sort()
    print("-->: {}".format(m_list))
    for x in m_list:
        print("    {}".format(x))

    if len(m_list) > 1:
        merc_final = struct.pack('!HHI', 4, ((len(m_list) - 1) * 8) + 8, 0)
        for x in range(0, len(m_list) - 1):
            merc_final += struct.pack('!II', x, 0)
            print("MERCURY: {}".format(x))
        merc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        merc_adress = ('10.40.13.151', 8888)
        merc_socket.connect(merc_adress)
        merc_socket.send(merc_final)
        merc_socket.close()
    else:
        print("NO MERCURY")


def main():
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
                            print("----------------------------------------------")
                            print("HEAD: [{}] [{}] [{}]".format(header1, header2, header3))
                            fp.write("HEAD: [{}] [{}] [{}]\n".format(header1, header2, header3))
                            for x in range(1, int(header2 / 8)):
                                molecule = struct.unpack('!IHH', data[8 * x:(8 * x) + 8])
                                #print("{}: {}\n".format(x + 1, molecule))
                                the_mix.append(molecule)    
                        except:
                            print("Could not unpack\n")
                        
                        debris = []
                        mix_dict = {}
                        for x in the_mix:
                            if x[1] > len(the_mix) or x[2] > len(the_mix):
                                pass
                            else:
                                if x[1] == 0:
                                    if liquid is True:
                                        a = 0
                                    else:
                                        a = 0xffff
                                else:
                                    a = the_mix[x[1] - 1][0]
                                if x[2] == 0:
                                    if liquid is True:
                                        b = 0
                                    else:
                                        b = 0xffff
                                else:
                                    b = the_mix[x[2] - 1][0]

                                mix_dict[x[0]] = [a, b]

                        remove_list = []
                        for x in mix_dict:
                            if mix_dict[x][0] not in mix_dict or mix_dict[x][1] not in mix_dict:
                                remove_list.append(x)

                        for x in remove_list:
                            mix_dict.pop(x)

                        try:
                            mix_dict.pop(0)
                        except:
                            pass

                        print("DICT: {}\n".format(mix_dict))

                        print("TEST: ", end="")
                        for x in mix_dict:
                            try:
                                a = list(mix_dict.keys()).index(mix_dict[x][0]) + 1
                            except:
                                a = 0
                            try:
                                b = list(mix_dict.keys()).index(mix_dict[x][1]) + 1
                            except:
                                b = 0
                            print(" {}: {} {}".format(x, a, b), end=" ")

                        print()
                        de_merc(mix_dict)

                        print()
                        for x in the_mix:
                            if x[1] > len(the_mix) or x[2] > len(the_mix):
                                # print("{} {} {}<-".format(x, x[1], x[2]))
                                debris.append(x)
                                the_mix.remove(x)
                                #adjust the indexes


                        debris_final = struct.pack('!HHI', 1, (len(debris) * 8) + 8, 0)
                        for x in debris:
                            debris_final += struct.pack('!IHH', x[0], 0, 0) 

                        if len(debris) > 0:
                            debris_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            debris_adress = ('10.40.13.151', 2222)
                            debris_socket.connect(debris_adress)
                            debris_socket.send(debris_final)
                            debris_socket.close()
                            fp.write("DEBR: {}\n".format(debris_final))
                            print("DEBR: {}\n".format(debris_final))

                        water_final = struct.pack('!HHI', 0, (len(the_mix) * 8) + 8, 0)
                        for y in the_mix:
                            water_final += struct.pack('!IHH', y[0], y[1], y[2])

                        ds_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        ds_address = ('10.40.13.151', 1111)
                        ds_socket.connect(ds_address)
                        ds_socket.send(water_final)
                        print("SEND: {}\n".format(water_final))
                        ds_socket.close()

                        print("DATA: [{}] {}".format(len(the_mix), the_mix))
                        fp.write("DATA: [{}] {}\n".format(len(the_mix), the_mix))
                        clorine = 0
                        air = 0
                        for x in the_mix:
                            if x[1] == x[2] and x[0] is not 0 and x[1] is not 0:
                                clorine += 1
                            if x[0] == 0:
                                air += 1
                        print("Clorine percent {}%".format(clorine /len(the_mix)))
                        print("Air percent {}%".format(air /len(the_mix)))    
                    else:
                        fp.write("CLOS: No more data on {}\n".format(client_address))
                        break
                    print("----------------------------------------------")
            finally:
                connection.close()
            fp.close()

        for s in writable:
            pass

        for s in exceptional:
            pass


if __name__ == "__main__":
    main()