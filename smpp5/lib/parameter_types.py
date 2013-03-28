"""
Parameter Type Definitions
==========================

SMPP supports 4 types of parameters, Integer, CString, String and TLV. This module contains
classes for encoding and decoding these parameter types
"""

import struct


class Integer(object):
    """
    Integer SMPP Parameter Type. Integers can be of length 1, 2 or 4 bytes/octets.
    """

    value = None
    length = None

    def __init__(self, value, length):
        self.value = value
        self.length = length

    def encode(self):
        "Encode the integer value to a byte-string"

        if 1 == self.length:
            return struct.pack('>B', self.value)
        elif 2 == self.length:
            return struct.pack('>H', self.value)
        elif 4 == self.length:
            return struct.pack('>L', self.value)

    @classmethod
    def decode(cls, string):
        "Decode from a string to an Integer object"

        l = None
        v = None
        if 1 == len(string):
            l = 1
            v = struct.unpack('>B', string)[0]
        elif 2 == len(string):
            l = 2
            v = struct.unpack('>H', string)[0]
        elif 4 == len(string):
            l = 4
            v = struct.unpack('>L', string)[0]

        if l and v:
            return Integer(v, l)
        else:
            raise RuntimeError("Invalid size/value for integer type")


class CString(object):
    "A null terminated string"

    value = None
    length = 0

    def __init__(self, value=None):
        self.value = value
        self.length = len(value)

    def encode(self):
        return self.value + '\x00'

    @classmethod
    def decode(cls, string):
        if string.endswith('\x00'):
            return CString(string[:-1])
        else:
            raise RuntimeError("Invalid CString value")


class String(object):
    "A null terminated string"

    value = None
    length = 0

    def __init__(self, value=None):
        self.value = value
        self.length = len(value)

    def encode(self):
        return self.value

    @classmethod
    def decode(cls, string):
        return CString(string)
