from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.session_management import BindTransmitter
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON


def test_01_bind_tr_encode():
    "Test Bind Transmitter encoding"
    P = BindTransmitter()

    P.system_id = CString("SMPP3TEST")
    P.password = CString("secret08")
    P.system_type = CString("SUBMIT1")
    P.interface_version = Integer(IV.SMPP_VERSION_5, 1)
    P.addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.addr_npi = Integer(NPI.ISDN, 1)
    P.address_range = CString('')

    assert '00 00 00 2F 00 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)


def test_02_bind_tr_decode():
    "Test Bind Transmitter decoding"
    data = b'\x00\x00\x00/\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00' + \
           b'SUBMIT1\x00P\x01\x01\x00'
    P = BindTransmitter.decode(data)
    assert '00 00 00 2F 00 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)

def test_01_bind_tr_rsp_encode():
    "Test Bind Transmitter Response encoding"
    P = BindTransmitter()

    P.system_id = CString("SMPP3TEST")
    P.password = CString("secret08")
    P.system_type = CString("SUBMIT1")
    P.interface_version = Integer(IV.SMPP_VERSION_5, 1)
    P.addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.addr_npi = Integer(NPI.ISDN, 1)
    P.address_range = CString('')

    assert '00 00 00 2F 00 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)


def test_02_bind_tr_rsp_decode():
    "Test Bind Transmitter Response decoding"
    data = b'\x00\x00\x00/\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00' + \
           b'SUBMIT1\x00P\x01\x01\x00'
    P = BindTransmitter.decode(data)
    assert '00 00 00 2F 00 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)


def test_01_bind_rcr_encode():
    "test Bind Receiver encoding"
    P = BindReceiver()
    
    P.system_id = CString("SMPP3TEST")
    P.password = CString("secret08")
    P.system_type = CString("SUBMIT1")
    P.interface_version = Integer(IV.SMPP_VERSION_5, 1)
    P.addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.addr_npi = Integer(NPI.ISDN, 1)
    P.address_range = CString('')


    assert '00 00 00 2F 00 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)
           
def test_02_bind_rcr_decode():
    "Test Bind Receiver decoding"
    data = b'\x00\x00\x00/\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00' + \
           b'SUBMIT1\x00P\x01\x01\x00'
    P = BindReceiver.decode(data)
    assert '00 00 00 2F 00 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)

def test_01_bind_tcr_encode():
    "test Bind Transceiver encoding"
    P = BindTransceiver()
    
    P.system_id = CString("SMPP3TEST")
    P.password = CString("secret08")
    P.system_type = CString("SUBMIT1")
    P.interface_version = Integer(IV.SMPP_VERSION_5, 1)
    P.addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.addr_npi = Integer(NPI.ISDN, 1)
    P.address_range = CString('')
    
    assert '00 00 00 2F 00 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)
           
def test_02_bind_tcr_decode():
    "Test Bind Transceiver decoding"
    data = b'\x00\x00\x00/\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00' + \
           b'SUBMIT1\x00P\x01\x01\x00'
    P = BindTransceiver.decode(data)
    assert '00 00 00 2F 00 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)
           
BindTransceiverResp
