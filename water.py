#!/usr/bin/env python3

import struct

#https://www.codecademy.com/en/forum_questions/51f239449c4e9d4e3c001f43
def is_prime(x):
    if x < 2:
        return False
    else:
        for n in range(2,x):
            if x % n == 0:
               return False
        return True

class Water:
    def __init__(self, data):
        liquid = True
        self.hazmat = []
        self.sludge = []
        self.mix = dict()
        self.trash = []
        self.data = data

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

    def __repr__(self):
        return "data: {}\nmix: {}\ntrash: {}\nhazmat: {}\nsludge: {}".format(self.data, self.mix, self.trash, self.hazmat, self.sludge)
        
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

    def treat_poop(self):
        poop_list = []
        for key in self.mix:
            if is_prime(self.mix[key][0]) == True:
                poop_list.append(key)
                self.sludge.append(key)
        for x in poop_list:
            self.mix.pop(key, None)

    def treat_trash_poop(self):
        poop_list = []
        for x in self.trash:
            if is_prime(x[0]) == True:
                poop_list.append(x[0])
                self.sludge.append(x[0])
        for x in poop_list:
            self.trash.remove(x)

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

    