from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU


def test_01_pdu_encode():
    "Test PDU encoding"
    P = PDU()
    assert '00 00 00 10 00 00 00 00 00 00 00 00 00 00 00 01 ' == hex_convert(P.encode())


def test_02_pdu_decode():
    "Test PDU decoding"
    pass
