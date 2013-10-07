from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.anciliary_submission import *
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, message_state

#------------QuerySm Encoding And Decoding-----------------


def test_01_query_sm_encode():
    "Test Query Sm encoding"
    P = QuerySm()
    P. command_id = Integer(command_ids.query_sm, 4)
    P.message_id = CString("2")
    P.source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.source_addr_npi = Integer(NPI.ISDN, 1)
    P.source_addr = CString("ASMA")

    assert '00 00 00 19 00 00 00 03 00 00 00 00 00 00 00 01 32 00 01 01 41 53 4D 41 00 ' == hex_convert(P.encode(), 150)


def test_02_query_sm_decode():

    "Test Query Sm decoding"
    data = b'\x00\x00\x00\x19\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x012\x00\x01\x01ASMA\x00'

    P = QuerySm.decode(data)
    assert '00 00 00 19 00 00 00 03 00 00 00 00 00 00 00 01 32 00 01 01 41 53 4D 41 00 ' == hex_convert(P.encode(), 150)
 #-----------------------------------------------------------------------


def test_03_query_sm_resp_encode():
    "Test Query Sm Response Encoding"
    P = QuerySmResp()
    P.command_id = Integer(command_ids.query_sm_resp, 4)
    P.message_id = CString("2")
    P.final_date = CString("2013-10-07 00:00:00")
    P.message_state = Integer(message_state.SCHEDULED, 1)
    P.error_code = Integer(0, 1)
    assert '00 00 00 28 80 00 00 03 00 00 00 00 00 00 00 01 32 00 32 30 31 33 2D 31 30 2D 30 37 20 30 30 3A 30 30 3A 30 30 00 00 00 ' == hex_convert(P.encode(), 150)


def test_04_query_sm_resp_decode():
    "Test Query Response Sm Decoding"

    data = b'\x00\x00\x00(\x80\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x012\x002013-10-07 00:00:00\x00\x00\x00'

    P = QuerySmResp.decode(data)
    assert '00 00 00 28 80 00 00 03 00 00 00 00 00 00 00 01 32 00 32 30 31 33 2D 31 30 2D 30 37 20 30 30 3A 30 30 3A 30 30 00 00 00 ' ==  hex_convert(P.encode(), 150)

#---------------------------------------------------------------------------


#------------CancelSm Encoding And Decoding-----------------

def test_01_cancel_sm_encode():
    "Test Cancel Sm encoding"
    P = CancelSm()
    P.command_id = Integer(command_ids.cancel_sm, 4)
    P.service_type = CString("")
    P.message_id = CString("2")
    P.source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.source_addr_npi = Integer(NPI.ISDN, 1)
    P.source_addr = CString("ASMA")
    P.dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.dest_addr_npi = Integer(NPI.ISDN, 1)
    P.destination_addr = CString("+923005381993")
    assert '00 00 00 2A 00 00 00 08 00 00 00 00 00 00 00 01 00 32 00 01 01 41 53 4D 41 00 01 01 2B 39 32 33 30 30 35 33 38 31 39 39 33 00 ' == hex_convert(P.encode(), 150)


def test_02_cancel_sm_decode():

    "Test Cancel Sm decoding"
    data = b'\x00\x00\x00*\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x01\x002\x00\x01\x01ASMA\x00\x01\x01+923005381993\x00'

    P = CancelSm.decode(data)
    assert '00 00 00 2A 00 00 00 08 00 00 00 00 00 00 00 01 00 32 00 01 01 41 53 4D 41 00 01 01 2B 39 32 33 30 30 35 33 38 31 39 39 33 00 ' == hex_convert(P.encode(), 150)
 #-----------------------------------------------------------------------


def test_03_cancel_sm_resp_encode():
    "Test Cancel Sm Response Encoding"
    P = CancelSmResp()
    P.command_id = Integer(command_ids.cancel_sm_resp, 4)

    assert '00 00 00 10 80 00 00 08 00 00 00 00 00 00 00 01 ' == hex_convert(P.encode(), 150)


def test_04_cancel_sm_resp_decode():
    "Test Cancel Response Sm Decoding"

    data = b'\x00\x00\x00\x10\x80\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x01'

    P = CancelSmResp.decode(data)
    assert '00 00 00 10 80 00 00 08 00 00 00 00 00 00 00 01 ' == hex_convert(P.encode(), 150)

#---------------------------------------------------------------------------


#------------ReplaceSm Encoding And Decoding-----------------

def test_01_replace_sm_encode():
    "Test Replace Sm encoding"
    P = ReplaceSm()
    P.command_id = Integer(command_ids.replace_sm, 4)
    P.message_id = CString("2")
    P.source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.source_addr_npi = Integer(NPI.ISDN, 1)
    P.source_addr = CString("ASMA")
    P.schedule_delivery_time = CString("")
    P.validity_period = CString("")
    P.registered_delievery = Integer(0, 1)
    P.sm_default_msg_id = Integer(0, 1)
    P.sm_length = Integer(5, 1)                # page 134
    P.short_message = CString("hello")

    assert '00 00 00 24 00 00 00 07 00 00 00 00 00 00 00 01 32 00 01 01 41 53 4D 41 00 00 00 00 00 05 68 65 6C 6C 6F 00 ' == hex_convert(P.encode(), 150)


def test_02_replace_sm_decode():

    "Test Replace Sm decoding"
    data = b'\x00\x00\x00$\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x012\x00\x01\x01ASMA\x00\x00\x00\x00\x00\x05hello\x00'

    P = ReplaceSm.decode(data)
    assert '00 00 00 24 00 00 00 07 00 00 00 00 00 00 00 01 32 00 01 01 41 53 4D 41 00 00 00 00 00 05 68 65 6C 6C 6F 00 ' == hex_convert(P.encode(), 150)
    #-----------------------------------------------------------------------


def test_03_replace_sm_resp_encode():
    "Test Replace Sm Response Encoding"
    P = ReplaceSmResp()
    P.command_id = Integer(command_ids.replace_sm_resp, 4)

    assert '00 00 00 10 80 00 00 07 00 00 00 00 00 00 00 01 ' == hex_convert(P.encode(), 150)


def test_04_replace_sm_resp_decode():
    "Test Replace Response Sm Decoding"

    data = b'\x00\x00\x00\x10\x80\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x01'

    P = ReplaceSmResp.decode(data)
    assert '00 00 00 10 80 00 00 07 00 00 00 00 00 00 00 01 ' == hex_convert(P.encode(), 150)

#---------------------------------------------------------------------------
 
