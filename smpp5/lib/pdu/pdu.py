"""
This module contains some fun code to keep track of class properties in the order they are defined
including properties for the child classes. Aim is to make PDU subclass declaration very easy and
non-repetitive.

WARNING: Don't try to modify this code unless you understand what it does completely.
"""

from collections import OrderedDict
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from collections import OrderedDict


class OrderedMeta(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        return OrderedDict()                # OrderedDict tracks the insertion order

    def __new__(cls, name, bases, clsdict):
        c = type.__new__(cls, name, bases, clsdict)
        c._orderedKeys = clsdict.keys()
        return c


class PDU(metaclass=OrderedMeta):
    """
    Base class for all PDU classes. Contains the code encoding/decoding functionality along-with the
    header fields.

    Developers don't need to set a value for command_length either for the base PDU class or its
    child classes. Its calculated automatically during encode and decode operations.
    """

    command_length = Integer(0, 4)
    command_id = Integer(0, 4)
    command_status = Integer(0, 4)
    sequence_number = Integer(0, 4)

    def __init__(self, seq_num=1):

        self.sequence_number.value = seq_num

        if type != type(self.__class__.__bases__[0]):
            # if the constructor is being called for a child class's object
            # replace the child's attribute mappings OrderedDict with a new one
            # that also includes the parent attributes. This is required for
            # proper encode and decode functionality

            new_mapping = OrderedDict()
            new_mapping.update(self.__class__.__bases__[0]._orderedKeys._mapping)
            new_mapping.update(self._orderedKeys._mapping)
            self._orderedKeys._mapping = new_mapping

    def encode(self):
        "Encodes a PDU based on its properties"

        encoded_data = b''
        for member in self._orderedKeys:
            if not member.startswith("__") and not callable(getattr(self, member)):
                #print(member + " : " + str(getattr(self, member)))
                M = getattr(self, member)
                if type(M) in [Integer, CString, String, TLV]:
                    #print(member)
                    #print(M.encode())
                    if 'command_length' != member:
                        encoded_data += M.encode()

        # now calculate command length
        self.command_length.value = len(encoded_data) + 4
        encoded_data = self.command_length.encode() + encoded_data
        return encoded_data

    @classmethod
    def decode(cls, data):
        "Decodes the PDU from the given data bytes"

        new_pdu = cls()
        idx = 0
        for member in cls._orderedKeys:
            if not member.startswith("__") and not callable(getattr(cls, member)):
                M = getattr(cls, member)
                if Integer == type(M):  # in [Integer, CString, String, TLV]
                    s = data[idx:idx+M.length]
                    idx = idx + M.length
                    setattr(new_pdu, member, Integer.decode(s))
                elif CString == type(M):
                    # Need to find the next NULL character which is the string's end
                    try:
                        nidx = data.index(b'\x00', idx)
                        s = data[idx:nidx+1]
                        idx = nidx + 1
                        setattr(new_pdu, member, CString.decode(s))
                    except:
                        raise RuntimeError("Cannot find end for CString type")
                elif String == type(M):
                    # TODO: Since string fields can either be fixed length or have a corresponding
                    # length field specifying their length, decoding this requires some info to
                    # be passed from within the PDU class.
                    pass
                elif TLV == type(M):
                    pass

        return new_pdu
