from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.message_submission import *
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON, command_id, esm_class

#------------SubmitSm Encoding And Decoding-----------------
def test_25_sbmit_sm_encode():
    "Test Submit Sm encoding"
    P = SubmitSm()

   
    P.service_type = CString('')
    P.source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.source_addr_npi = Integer(NPI.ISDN, 1)
    P.source_addr = CString("1616")
    P.dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.dest_addr_npi = Integer(NPI.ISDN, 1)
    P.destination_addr = CString('1515')
    P.esm_class = Integer(esm_class.Default_mode, 1)
    P.protocol_id = Integer(0, 1) 
    P.priority_flag = Integer(0, 1) 
    P.schedule_delivery_time = CString(' ')
    P.validity_period = CString('')
    P.registered_delievery = Integer(0, 1) 
    P.replace_if_present_flag = Integer(0,1) 
    P.data_coding = Integer(0, 1) 
    P.sm_default_msg_id = Integer(0, 1) 
    P.sm_length = Integer(0, 1) 
    P.short_message = String('Message')

    assert '00 00 00 31 00 00 00 04 00 00 00 00 00 00 00 01 00 01 01 31 36 31 36 00 01 01 31 35 31 35 00 00 00 00 20 00 00 00 00 00 00 00 4D 65 73 73 61 67 65 ' == hex_convert(P.encode(), 150)
def test_26_sbmit_sm_decode():

    "Test Submit Sm decoding"
    data = b'\x00\x00\x00\x31\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x011616\x00\x01\x011515\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00Message'

    P = SubmitSm.decode(data)
    '00 00 00 31 00 00 00 04 00 00 00 00 00 00 00 01 00 01 01 31 36 31 36 00 01 01 31 35 31 35 00 00 00 00 20 00 00 00 00 00 00 00 4D 65 73 73 61 67 65 ' == hex_convert(P.encode(), 150)
 #-----------------------------------------------------------------------
 
def test_01_sbmit_sm_resp_encode():
    "Test Submit Sm Encoding"
    P = SubmitSmResp()
    P.message_id = CString("2468ACE")
    assert '00 00 00 18 80 00 00 04 00 00 00 00 00 00 00 01 32 34 36 38 41 43 45 00 ' ==  hex_convert(P.encode(), 150)
    
    
def test_01_sbmit_sm_resp_decode():
    "Test Submit Sm Decoding"
    
    data = b'\x00\x00\x00\x18\x80\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x012468ACE\x00'

    P = SubmitSmResp.decode(data)
    assert '00 00 00 18 80 00 00 04 00 00 00 00 00 00 00 01 32 34 36 38 41 43 45 00 ' ==  hex_convert(P.encode(), 150)
    
#---------------------------------------------------------------------------

def test_01_data_sm_encode():
    "Test Data Sm Encoding"
    
    P=DataSm()

    P.command_id = Integer(command_id.data_sm, 4)
    P.source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.source_addr_npi = Integer(NPI.ISDN, 1)
    P.source_addr = CString("1616")
    P.dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.dest_addr_npi = Integer(NPI.ISDN, 1)
    P.destination_addr = CString("1515")
    P.esm_class = Integer(esm_class.Default_mode, 1)  
    P.registered_delievery = Integer(0, 1)     
    P.data_coding = Integer(0, 1)
    
    assert '00 00 00 22 00 00 01 03 00 00 00 00 00 00 00 01 00 01 01 31 36 31 36 00 01 01 31 35 31 35 00 00 00 00 ' ==  hex_convert(P.encode(), 150)

    
def test_01_data_sm_decode():
    "Test Data Sm Decoding"
    data =  b'\x00\x00\x00\x22\x00\x00\x01\x03\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x011616\x00\x01\x011515\x00\x00\x00\x00'
    P = DataSm.decode(data)
    assert '00 00 00 22 00 00 01 03 00 00 00 00 00 00 00 01 00 01 01 31 36 31 36 00 01 01 31 35 31 35 00 00 00 00 ' ==  hex_convert(P.encode(), 150)

    
    
    
    
