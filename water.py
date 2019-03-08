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

        for x in data:
            if x[1] > len(data) or x[2] > len(data):
                self.trash.append(x)
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
        return "data  : [{}]{}\nmix   : [{}] {}\ntrash : [{}] {}\nhazmat: [{}] {}\nsludge: [{}] {}".format(len(self.data), self.data, 
            len(self.mix), self.mix, 
            len(self.trash), self.trash, 
            len(self.hazmat), self.hazmat, 
            len(self.sludge), self.sludge)
        
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
        for key in self.mix:
            if is_undulating(key) == True and key is not 0:
                ammonia_list.append(key)
                self.sludge.append(key)
        print("+++++++> {}".format(ammonia_list))
        for x in ammonia_list:
            print("-------> {}".format(x))
            self.mix.pop(x)
        return len(ammonia_list)

    def treat_poop(self):
        poop_list = []
        for key in self.mix:
            if is_prime(self.mix[key][0]) == True:
                poop_list.append(key)
                self.sludge.append(key)
        for x in poop_list:
            self.mix.pop(key, None)
        return len(poop_list)

    def treat_trash_poop(self):
        trash_poop_list = []
        for x in self.trash:
            if is_prime(x[0]) == True:
                trash_poop_list.append(x[0])
                self.sludge.append(x[0])
        for x in trash_poop_list:
            try:
                self.trash.remove(x)
            except:
                log_it("ERRO", "Tried to remove invalid trash poop")
        return len(trash_poop_list)

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

    