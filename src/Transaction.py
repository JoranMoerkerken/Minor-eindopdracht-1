#!/usr/bin/env python3
""" 
The goal of this exercise is to complete the transaction module.
In this exercise you need to add a __repr__() function that will be used
to show the details of transaction. 

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code 
    * run the test of this exercise located in same folder.

To test run 'TxBlock_t.py' in your command line

Notes:
    * do not change class structure or method signature to not break unit tests
    * Check previous tutorials for more information on this topic
"""


from Signature import *

class Tx:
    inputs = None
    outputs =None
    sigs = None
    reqd = None
    def __init__(self, type = "NORMAL"):
        self.type = type
        self.inputs = []
        self.outputs = []
        self.sigs = []
        self.reqd = []

    def add_input(self, from_addr, amount):
        self.inputs.append((from_addr, amount))

    def add_output(self, to_addr, amount):
        self.outputs.append((to_addr, amount))

    def add_reqd(self, addr):
        self.reqd.append(addr)

    def sign(self, private):
        message = self.__gather()
        newsig = sign(message, private)
        self.sigs.append(newsig)
               
    def is_valid(self):
        
        if self.type == REWARD:
            if len(self.inputs)!=0 and len(self.outputs)!=1:
                return False
            return True
        else:
            total_in = 0
            total_out = 0
            message = self.__gather()
            for addr,amount in self.inputs:
                found = False
                for s in self.sigs:
                    if verify(message, s, addr):
                        found = True
                if not found:
                    # print ("No good sig found for " + str(message))
                    return False
                if amount < 0:
                    return False
                total_in = total_in + amount
            for addr in self.reqd:
                found = False
                for s in self.sigs:
                    if verify(message, s, addr):
                        found = True
                if not found:
                    return False
            for addr,amount in self.outputs:
                if amount < 0:
                    return False
                total_out = total_out + amount

            if total_out > total_in:
                # print("Outputs exceed inputs")
                return False
            
            return True

    def __gather(self):
        data=[]
        data.append(self.inputs)
        data.append(self.outputs)
        data.append(self.reqd)
        return data

    def __repr__(self):
        repr_str = "Inputs:\n"
        for addr, amt in self.inputs:
            repr_str += str(amt) + " from " + str(addr) + "\n"
        repr_str += "Outputs:\n"
        for addr, amt in self.outputs:
            repr_str += str(amt) + " to " + str(addr) + "\n"
        repr_str += "Extra Required Signatures:\n"
        for r in self.reqd:
            repr_str += str(r) + "\n"
        repr_str += "Signatures:\n"
        for s in self.sigs:
            repr_str += str(s) + "\n"
        return repr_str