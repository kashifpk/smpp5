from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU


class BindTransmitter(PDU):
    "Bind Transmitter PDU type"

    example_field = String("ABC")
    another_filed = Integer(5, 2)
