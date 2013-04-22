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

    assert '00 00 00 31 00 00 00 04 00 00 00 00 00 00 00 01 00 01 01 31 36 31 36 00 01 01 31 35 31 35 00 00 00 00 20 00 00 00 00 00 00 00 4D 65 73 73 61 67 65 ' == 

hex_convert(P.encode(), 150)
def test_26_sbmit_sm_decode():

    "Test Submit Sm decoding"
    data = b'\x00\x00\x00\x31\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x011616\x00\x01\x011515\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00Message'

    P = SubmitSm.decode(data)
    '00 00 00 31 00 00 00 04 00 00 00 00 00 00 00 01 00 01 01 31 36 31 36 00 01 01 31 35 31 35 00 00 00 00 20 00 00 00 00 00 00 00 4D 65 73 73 61 67 65 ' == 

hex_convert(P.encode(), 150)
