#!/usr/bin/env python3

import socket
import sys
import struct
import os

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('10.40.{}.130'.format(int(os.getuid()) - 3000), 1111)

    for x in range(1,6):
        try:
            sent_type = 0
            sent_size = 1
            sent_custom = 1
            message = struct.pack('HHI', sent_type, sent_size, sent_custom)

            pay_data = x
            pay_left = 0
            pay_right = 0

            payload = struct.pack('IHH', pay_data, pay_left, pay_right)

            sent = sock.sendto(message + payload, server_address)
        finally:
            pass

    sock.close()


if __name__ == "__main__":
    main()

