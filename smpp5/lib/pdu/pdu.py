from collections import OrderedDict
from smpp5.lib.parameter_types import Integer, CString, String, TLV


class OrderedMeta(type):
    @classmethod
    def __prepare__(metacls, name, bases): 
        return OrderedDict()

    def __new__(cls, name, bases, clsdict):
        c = type.__new__(cls, name, bases, clsdict)
        c._orderedKeys = clsdict.keys()
        return c


class PDU(metaclass=OrderedMeta):
    """
    Base class for all PDU classes. Contains the code encoding/decoding functionality along-with the
    header fields
    """

    command_length = Integer(None, 4)
    command_id = Integer(None, 4)
    command_status = Integer(None, 4)
    sequence_number = Integer(None, 4)

    def encode(self):
        "Encodes a PDU based on its properties"
        for p, v in vars(self).iteritems():
            print(p + ": " + v)

    @classmethod
    def decode(cls, string):
        "Decodes the PDU from the given string"
        pass
