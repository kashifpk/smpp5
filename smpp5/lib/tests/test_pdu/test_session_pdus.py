from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.session_management import BindTransmitter


def test_01_bind_tr_encode():
    "Test Bind Transmitter encoding"
    P = BindTransmitter()
    assert '00 00 00 2F 00 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)


def test_02_bind_tr_decode():
    "Test Bind Transmitter decoding"
    pass
