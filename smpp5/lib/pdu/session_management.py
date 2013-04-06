from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON


class BindTransmitter(PDU):
    "Bind Transmitter PDU type"

    command_id = Integer(2, 4)
    system_id = CString("")
    password = CString("")
    system_type = CString("")
    interface_version = Integer(IV.SMPP_VERSION_5, 1)
    addr_ton = Integer(TON.INTERNATIONAL, 1)
    addr_npi = Integer(NPI.ISDN, 1)
    address_range = CString('')
