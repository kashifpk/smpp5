from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.session_management import BindTransmitter, BindTransmitterResp, BindReceiver, BindReceiverResp, BindTransceiver, BindTransceiverResp, OutBind, UnBind, UnBindResp
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


#------------SubmitSm Encoding And Decoding-----------------
def test_25_sbmit_sm_encode():
    "Test Submit Sm encoding"
    P = SubmitSm()

   
    service_type = CString('')
    source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    source_addr_npi = Integer(NPI.ISDN, 1)
    source_addr = CString("1616")
    dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    dest_addr_npi = Integer(NPI.ISDN, 1)
    destination_addr = CString('+33600000000')
    esm_class = Integer(esm_class.Default_mode, 1)
    protocol_id = Integer(0, 1) 
    priority_flag = Integer(0, 1) 
    schedule_delivery_time = CString('060401120000004+')
    validity_period = CString('060402120000004+')
    registered_delievery = Integer(0, 1) 
    replace_if_present_flag = Integer(0,1) 
    data_coding = Integer(0, 1) 
    sm_default_msg_id = Integer(0, 1) 
    sm_length = Integer(0, 1) 
    short_message = String('Message')

    assert '00 00 00 51 00 00 00 04 00 00 00 00 00 00 00 01 00 01 01 31 36 31 36 01 01 2B 33 33 36 30 30 30 30 30 30 30 30 00 00 00' + \
           '30 36 30 34 30 31 31 32 30 30 30 30 30 30 34 2B 30 36 30 34 30 32 31 32 30 30 30 30 30 30 34 2B 00 00 00 00 00 4D 65 73 73 61 67 65'== hex_convert(P.encode(), 150)


def test_26_sbmit_sm_decode():
    "Test Submit Sm decoding"
    
