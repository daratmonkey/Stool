#!/usr/bin/env python3

import socket
import sys
import struct
import os

def main(dest):
    for x in range(1,6):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('10.40.{}.{}'.format(int(os.getuid()) - 3000, dest), 1111)
        sock.connect(server_address)
        try:
            sent_type = 0
            sent_size = 80
            sent_custom = 1
            message = struct.pack('>HHI', sent_type, sent_size, sent_custom)

            payload = b""
            for y in range(1,10):
                pay_data = x * y
                if y == 3:
                    pay_left = 7
                    pay_right = 7
                elif y == 4:
                    pay_data = 0
                    pay_left = 0
                    pay_right = 0
                else:
                    pay_left = 1
                    pay_right = 2
                payload = payload + struct.pack('>IHH', pay_data, pay_left, pay_right)
            print("{}\n".format(payload))
            sent = sock.sendto(message + payload, server_address)
        finally:
            pass
        sock.close()


if __name__ == "__main__":

    try:
        dest = int(sys.argv[1])
    except:
        dest = 130

    main(dest)

