#!/usr/bin/env python3

import struct

def log_it(mtype, message):
    fp = open("sd.log", "a")
    fp.write("{}: {}\n".format(mtype, message))
    fp.close()
    print("{}: {}\n".format(mtype, message))

#https://stackoverflow.com/a/18833845

def is_prime(n):
    n = abs(int(n))
    if n < 2:
        return False
    if n == 2: 
        return True    
    if not n & 1: 
        return False
    for x in range(3, int(n**0.5) + 1, 2):
        if n % x == 0:
            return False
    return True

#https://github.com/brian-stout/water/blob/master/python_all/liquid.py
def is_undulating(x):
    last_digit = 0
    flip_bool = False
    string = str(x)

    if len(string) == 1:
        return True

    if len(string) >= 2:
        if string[0] == string[1]:
            return False
        elif string[0] > string[1]:
            flip_bool = False
        elif string[0] < string[1]:
            flip_bool = True

    for i in range(len(string)-1):
        if flip_bool == False:
            if int(string[i]) <= int(string[i+1]):
                return False
            else:
                flip_bool = True
        else:
            if int(string[i]) >= int(string[i+1]):
                return False
            else:
                flip_bool = False
    return True    

class Water:
    def __init__(self, data):
        liquid = True
        self.hazmat = []
        self.sludge = []
        self.mix = dict()
        self.trash = []
        self.data = data
        self.merc_level = 0
        self.chlorine = []

        for x in data:
            if x[1] == x[2] and x[1] is not 0:
                self.chlorine.append(x)
            if x[1] > len(data) or x[2] > len(data):
                self.trash.append(x)
            elif x[0] == 0:
                pass
            else:
                if x[1] == 0:
                    if liquid is True:
                        a = 0
                    else:
                        a = 0xffff
                elif data[x[1] - 1][0] > len(data):
                    a = 0
                else:
                    a = data[x[1] - 1][0]

                if x[2] == 0:
                    if liquid is True:
                        b = 0
                    else:
                        b = 0xffff
                elif data[x[2] - 1][0] > len(data):
                    b = 0
                else:
                    b = data[x[2] - 1][0]

                self.mix[x[0]] = [a, b]

    def __repr__(self):
        air = 0
        for x in self.data:
            if x[0] == 0:
                air += 1
        return '\x1b[0;30;33mdata\x1b[0m  : [\x1b[0;30;31m{}\x1b[0m] {}\n\x1b[0;30;33mmix\x1b[0m   \
: [\x1b[0;30;31m{}\x1b[0m] {}\n\x1b[0;30;33mtrash\x1b[0m : [\x1b[0;30;31m{}\x1b[0m] {}\n\x1b[0;30;33mhazmat\x1b[0m:\
 [\x1b[0;30;31m{}\x1b[0m] {}\n\x1b[0;30;33msludge\x1b[0m: [\x1b[0;30;31m{}\x1b[0m] {}\n\x1b[0;30;33mair\x1b[0m   \
: [\x1b[0;30;31m{}\x1b[0m]'.format(len(self.data), self.data, 
            len(self.mix), self.mix, 
            len(self.trash), self.trash, 
            len(self.hazmat), self.hazmat, 
            len(self.sludge), self.sludge,
            air)
        
    def treat_mercury(self):
        unreachable = set(self.mix.keys())
        for key,value in self.mix.items():
            unreachable.discard(value[0])
            unreachable.discard(value[1])

        if (len(unreachable) > 1):
            self.merc_level += 1
            smallest = min(unreachable)
            self.hazmat.append(smallest)
            self.mix.pop(smallest)
            self.treat_mercury()

    def treat_ammonia(self):
        ammonia_list = []
        for key in self.mix.keys():
            if is_undulating(key) == True and key is not 0:
                ammonia_list.append(key)
                self.sludge.append(key)
        for x in ammonia_list:
            self.mix.pop(x)
        return len(ammonia_list)

    def treat_trash_ammonia(self):
        trash_ammonia_list = []
        for x in self.trash:
            if is_undulating(x[0]) == True:
                trash_ammonia_list.append(x[0])
                self.sludge.append(x[0])
        for x in trash_ammonia_list:
            try:
                for y in self.trash:
                    if y[0] == x:
                        self.trash.remove(y)
                #self.trash.remove(x)
            except:
                log_it("ERRO", "Tried to remove invalid trash ammonia")
        return len(trash_ammonia_list)

    def treat_poop(self):
        poop_list = []
        for key in self.mix.keys():
            if is_prime(key) == True:
                poop_list.append(key)
                self.sludge.append(key)
        for x in poop_list:
            self.mix.pop(x, None)
        return len(poop_list)

    def treat_trash_poop(self):
        trash_poop_list = []
        for x in self.trash:
            if is_prime(x[0]) == True:
                trash_poop_list.append(x[0])
                self.sludge.append(x[0])
        for x in trash_poop_list:
            try:
                for y in self.trash:
                    if y[0] == x:
                        self.trash.remove(y)
                #self.trash.remove(x)
            except:
                log_it("ERRO", "Tried to remove invalid trash poop")
        return len(trash_poop_list)
    
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
        #for x in range(1, int((len(self.mix) / 20))):
        #    print("\x1b[0;30;36mADDING THAT AIR\x1b[0m")
        #    water_final += struct.pack('!IHH', 0, 0, 0)
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

    def serialize_sludge(self):
        sludge_final = b""
        for x in self.sludge:
            sludge_final += struct.pack('!IHH', x, 0, 0)
        return sludge_final

    def aerate(self, water_final, num=1):
        for x in range(0, num):
            water_final += struct.pack('!IHH', 0, 1, 0)
            return water_final