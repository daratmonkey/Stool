#!/usr/bin/env python3

import struct

class Water:
    def __init__(self, data):
        liquid = True
        self.hazmat = []
        self.sludge = dict()
        self.mix = dict()
        self.trash = []

        for x in data:
            if x[1] > len(data) or x[2] > len(data):
                self.trash.append(x)
            else:
                if x[1] == 0:
                    if liquid is True:
                        a = 0
                    else:
                        a = 0xffff
                else:
                    a = data[x[1] - 1][0]
                if x[2] == 0:
                    if liquid is True:
                        b = 0
                    else:
                        b = 0xffff
                else:
                    b = data[x[2] - 1][0]

                    self.mix[x[0]] = [a, b]

        
    def treat_mercury(self):
        unreachable = set(self.mix.keys())
        for key,value in self.mix.items():
            unreachable.discard(value[0])
            unreachable.discard(value[1])

        if (len(unreachable) > 1):
            smallest = min(unreachable)
            self.hazmat.append(smallest)
            self.mix.pop(smallest)
            self.treat_mercury()
        

    def treat_trash(self):
        for x in self.mix:
            if self.mix[x][0] > len(self.mix) or self.mix[x][1] > len(self.mix):
                self.trash.append(x)

        for x in self.trash:
                self.mix.pop(x)

    def add_air(self):
        pass
    
    def serialize_water(self):
        water_final = b""
        for x in self.mix:
            try:
                a = list(self.mix.keys()).index(self.mix[x][0]) + 1
            except:
                a = 0
            try:
                b = list(self.mix.keys()).index(self.mix[x][1]) + 1
            except:
                b = 0
            water_final += struct.pack('!IHH', x, a, b)
        return water_final

    def serialize_trash(self):
        debris_final = b""
        for x in self.trash:
            debris_final += struct.pack('!IHH', x[0], 0, 0)
        return debris_final

    def serialize_hazmat(self):
        hazmat_final = b""
        for x in self.hazmat:
            hazmat_final += struct.pack('!II', x, 0)
        return hazmat_final