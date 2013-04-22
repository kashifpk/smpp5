from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.session_management import BindTransmitter, BindTransmitterResp, BindReceiver, BindReceiverResp, BindTransceiver, BindTransceiverResp, OutBind, UnBind, UnBindResp, EnquireLink, EnquireLinkResp, AlertNotification, GenericNack

from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON, command_id, esm_class

#------------Bind Transmitter Encoding And Decoding-----------------
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

#------------Bind Transmitter Response Encoding And Decoding-----------------

def test_03_bind_tr_rp_encode():
    "Test Bind Transmitter Response encoding"
    P = BindTransmitterResp()

    P.system_id = CString("SMPP3TEST")

    assert '00 00 00 1A 80 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 ' == hex_convert(P.encode(), 150)


def test_04_bind_tr_rp_decode():
    "Test Bind Transmitter Response decoding"
    #decode function


#------------Bind Receiver Encoding And Decoding-----------------

def test_05_bind_rsvr_encode():
    "Test Bind Receiver encoding"
    P = BindReceiver()

    P.system_id = CString("SMPP3TEST")
    P.password = CString("secret08")
    P.system_type = CString("SUBMIT1")
    P.address_range = CString('')

    assert '00 00 00 2F 00 00 00 01 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)

def test_06_bind_rsvr_decode():
    "Test Bind Receiver decoding"
    data = b'\x00\x00\x00/\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00' + \
           b'SUBMIT1\x00P\x01\x01\x00'
    P = BindReceiver.decode(data)
    assert '00 00 00 2F 00 00 00 01 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)

#------------Bind Receiver Response Encoding And Decoding-----------------

def test_07_bind_rsvr_resp_encode():
    "Test Bind Receiver Response encoding"
    P = BindReceiverResp()

    P.system_id = CString("SMPP3TEST")

    assert '00 00 00 1A 80 00 00 01 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 ' == hex_convert(P.encode(), 150)

def test_08_bind_rsvr_resp_decode():
    "Test Bind Receiver Response decoding"
    #decode function

#------------Bind Transceiver Encoding And Decoding-----------------
def test_09_bind_trsvr_encode():
    "Test Bind Transceiver encoding"
    P = BindTransceiver()

    P.system_id = CString("SMPP3TEST")
    P.password = CString("secret08")
    P.system_type = CString("SUBMIT1")
    P.address_range = CString('')

    assert '00 00 00 2F 00 00 00 09 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)

def test_10_bind_trsvr_decode():
    "Test Bind Transceiver decoding"
    data = b'\x00\x00\x00/\x00\x00\x00\x09\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00' + \
           b'SUBMIT1\x00P\x01\x01\x00'
    P = BindTransceiver.decode(data)
    assert '00 00 00 2F 00 00 00 09 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == hex_convert(P.encode(), 150)

#------------Bind Transceiver Response Encoding And Decoding-----------------
def test_11_bind_trsvr_resp_encode():
    "Test Bind Transceiver Response encoding"
    P = BindTransceiverResp()

    P.system_id = CString("SMPP3TEST")

    assert '00 00 00 1A 80 00 00 09 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 ' == hex_convert(P.encode(), 150)

def test_12_bind_trsvr_resp_decode():
    "Test Bind Trabsceiver Response decoding"
    #decode function


#------------OutBind Encoding And Decoding-----------------
def test_13_outbind_encode():
    "Test OutBind encoding"
    P = OutBind()

    P.system_id = CString("SMPP3TEST")
    P.password = CString("secret08")
    

    assert '00 00 00 23 00 00 00 0B 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           '00' == hex_convert(P.encode(), 150)

def test_14_outbind_decode():
    "Test OutBind decoding"
    data = b'\x00\x00\x00/\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08'
           
    P = OutBind.decode(data)
    assert '00 00 00 23 00 00 00 0B 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38' + \
           ' 00 '== hex_convert(P.encode(), 150)

#------------Unbind Encoding And Decoding-----------------
def test_15_unbind_encode():
    "Test UnBind encoding"
    P = UnBind()
    assert '00 00 00 10 00 00 00 06 00 00 00 00 00 00 00 01' == hex_convert(P.encode(), 150)

def test_16_unbind_decode():
    "Test UnBind decoding"
    data = b'\x00\x00\x00/\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00'
           
    P = UnBind.decode(data)
    assert '00 00 00 10 00 00 00 06 00 00 00 00 00 00 00 01' == hex_convert(P.encode(), 150)

#------------Unbind Response Encoding And Decoding-----------------
def test_17_unbind_resp_encode():
    "Test UnBind Response encoding"
    P = UnBindResp()
    assert '00 00 00 10 80 00 00 06 00 00 00 00 00 00 00 01' == hex_convert(P.encode(), 150)

def test_18_unbind_decode():
    "Test UnBind Response decoding"
    data = b'\x00\x00\x00/\x80\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00'
           
    P = UnBind.decode(data)
    assert '00 00 00 10 80 00 00 06 00 00 00 00 00 00 00 01' == hex_convert(P.encode(), 150)

#------------Enquire Link Encoding And Decoding-----------------
def test_19_enqr_lnk_encode():
    "Test Enquire Link encoding"
    P = EnquireLink()
    assert '00 00 00 10 00 00 00 15 00 00 00 00 00 00 00 01' == hex_convert(P.encode(), 150)

def test_20_enqr_lnk_decode():
    "Test Enquire Link decoding"
    data = b'\x00\x00\x00/\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00'
           
    P = EnquireLink.decode(data)
    assert '00 00 00 10 00 00 00 15 00 00 00 00 00 00 00 01' == hex_convert(P.encode(), 150)

#------------Enquire Link Response Encoding And Decoding-----------------
def test_21_enqr_lnk_resp_encode():
    "Test Enquire Link Response encoding"
    P = UnBindResp()
    assert '00 00 00 10 80 00 00 15 00 00 00 00 00 00 00 01' == hex_convert(P.encode(), 150)

def test_22_enqr_lnk_resp_decode():
    "Test Enquire Link Response decoding"
    data = b'\x00\x00\x00/\x80\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00'
           
    P = UnBind.decode(data)
    assert '00 00 00 10 80 00 00 15 00 00 00 00 00 00 00 01' == hex_convert(P.encode(), 150)

#------------Generic Nack Encoding And Decoding-----------------
def test_23_genrc_nak_encode():
    "Test Generic Nack encoding"
    P = GenericNack()
    assert '00 00 00 10 80 00 00 00 00 00 00 00 00 00 00 01' == hex_convert(P.encode(), 150)

def test_24_genrc_nak_decode():
    "Test Generic Nack decoding"
    data = b'\x00\x00\x00/\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
           
    P = GenericNack.decode(data)
    assert '00 00 00 10 80 00 00 00 00 00 00 00 00 00 00 01' == hex_convert(P.encode(), 150)

