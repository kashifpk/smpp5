from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.message_submission import *
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON, command_ids, esm_class

#------------SubmitSm Encoding And Decoding-----------------


def test_01_sbmit_sm_encode():
    "Test Submit Sm encoding"
    P = SubmitSm()
    P.service_type = CString("")
    P.source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.source_addr_npi = Integer(NPI.ISDN, 1)
    P.source_addr = CString("ASMA")
    P.dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.dest_addr_npi = Integer(NPI.ISDN, 1)
    P.destination_addr = CString("+923335111156")
    P.esm_class = Integer(esm_class.Default_mode, 1)
    P.protocol_id = Integer(0, 1)
    P.priority_flag = Integer(0, 1)
    P.schedule_delivery_time = CString("")
    P.validity_period = CString("")
    P.registered_delievery = Integer(0, 1)
    P.replace_if_present_flag = Integer(1, 1)
    P.data_coding = Integer(0, 1)
    P.sm_default_msg_id = Integer(0, 1)
    P.sm_length = Integer(5, 1)
    P.short_message = CString("hello")

    assert '00 00 00 38 00 00 00 04 00 00 00 00 00 00 00 01 00 01 01 41 53 4D 41 00 01 01 2B 39 32 33 33 33 35 31 31 31 31 35 36 00 00 00 00 00 00 00 01 00 00 05 \n68 65 6C 6C 6F 00 ' == hex_convert(P.encode(), 150)


def test_02_sbmit_sm_decode():

    "Test Submit Sm decoding"

    data = b'\x00\x00\x008\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01ASMA\x00\x01\x01+923335111156\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x05hello\x00'

    P = SubmitSm.decode(data)
    assert '00 00 00 38 00 00 00 04 00 00 00 00 00 00 00 01 00 01 01 41 53 4D 41 00 01 01 2B 39 32 33 33 33 35 31 31 31 31 35 36 00 00 00 00 00 00 00 01 00 00 05 \n68 65 6C 6C 6F 00 ' == hex_convert(P.encode(), 150)
    #-----------------------------------------------------------------------


def test_03_sbmit_sm_resp_encode():
    "Test Submit Sm Encoding"
    P = SubmitSmResp()
    P.message_id = CString("2468ACE")
    assert '00 00 00 18 80 00 00 04 00 00 00 00 00 00 00 01 32 34 36 38 41 43 45 00 ' == hex_convert(P.encode(), 150)


def test_04_sbmit_sm_resp_decode():
    "Test Submit Sm Decoding"

    data = b'\x00\x00\x00\x18\x80\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x012468ACE\x00'

    P = SubmitSmResp.decode(data)
    assert '00 00 00 18 80 00 00 04 00 00 00 00 00 00 00 01 32 34 36 38 41 43 45 00 ' == hex_convert(P.encode(), 150)

#---------------------------------------------------------------------------

def test_01_submit_multi_encode():
    "Test Submit Multi Encoding"

    P = SubmitMulti()
    P = SubmitMulti()
    P.source_addr = CString("ASMA")
    P.number_of_dests = Integer(2, 1)
    P.destination_addr = CString("+923005381993\n+923365195924")
    P.sm_length = Integer(5, 1)
    P.short_message = CString("hello")


    assert '00 00 00 4A 00 00 00 21 00 00 00 00 00 00 00 01 00 01 01 41 53 4D 41 00 02 01 01 01 2B 39 32 33 30 30 35 33 38 31 39 39 33 0A 2B 39 32 33 33 36 35 31 \n39 35 39 32 34 00 02 00 00 00 00 00 00 00 01 00 00 05 68 65 6C 6C 6F 00 ' == hex_convert(P.encode(), 150)


def test_02_submit_multi_decode():
    "Test Submit Multi Decoding"
    data = b'\x00\x00\x00J\x00\x00\x00!\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x01ASMA\x00\x02\x01\x01\x01+923005381993\n+923365195924\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x05hello\x00'
    P = SubmitMulti.decode(data)

    assert '00 00 00 4A 00 00 00 21 00 00 00 00 00 00 00 01 00 01 01 41 53 4D 41 00 02 01 01 01 2B 39 32 33 30 30 35 33 38 31 39 39 33 0A 2B 39 32 33 33 36 35 31 \n39 35 39 32 34 00 02 00 00 00 00 00 00 00 01 00 00 05 68 65 6C 6C 6F 00 ' == hex_convert(P.encode(), 150)

#-----------------------------------------------------------------------------------


def test_03_submit_multi_response_encode():

    "Test Submit Multi Response Encoding"
    P = SubmitMultiResp()
    P.destination_addr = CString("1515")
    assert '00 00 00 1D 80 00 00 21 00 00 00 00 00 00 00 01 00 00 01 01 31 35 31 35 00 00 00 00 00 ' == hex_convert(P.encode(), 150)


def test_04_submit_multi_response_decode():
    "Test Submit Multi Response Decoding"

    data = b'\x00\x00\x00\x1d\x80\x00\x00\x21\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x011515\x00\x00\x00\x00\x00'
    P = SubmitMultiResp.decode(data)
    assert '00 00 00 1D 80 00 00 21 00 00 00 00 00 00 00 01 00 00 01 01 31 35 31 35 00 00 00 00 00 ' == hex_convert(P.encode(), 150)


