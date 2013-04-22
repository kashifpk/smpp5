from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.session_management import *
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.pdu.session_management import BindTransmitter, BindTransmitterResp, BindReceiver, BindReceiverResp, BindTransceiver, BindTransceiverResp, OutBind, 

UnBind, UnBindResp, EnquireLink, EnquireLinkResp, AlertNotification, GenericNack
from smpp5.lib.constants import *

#--------------------------------------------------------------------------------

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

    assert '00 00 00 2F 00 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == 

hex_convert(P.encode(), 150)


def test_02_bind_tr_decode():
    "Test Bind Transmitter decoding"
    data = b'\x00\x00\x00/\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00' + \
            b'SUBMIT1\x00P\x01\x01\x00'
    P = BindTransmitter.decode(data)
    assert '00 00 00 2F 00 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == 

hex_convert(P.encode(), 150)


#--------------------------------------------------------------------------------

def test_01_bind_tr_rsp_encode():
    "Test Bind Transmitter Response encoding"
    P = BindTransmitterResp()

    P.system_id = CString("SMPP3TEST")
    P.interface_version = Integer(IV.SMPP_VERSION_5, 1)
    
    assert '00 00 00 1B 80 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 50 ' == hex_convert(P.encode(), 150)


def test_02_bind_tr_rsp_decode():
    "Test Bind Transmitter Response decoding"
    data = b'\x00\x00\x00\x1B\x80\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00\x50'
    P = BindTransmitterResp.decode(data)
    assert '00 00 00 1B 80 00 00 02 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 50 ' == hex_convert(P.encode(), 150)

#--------------------------------------------------------------------------------

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


    assert '00 00 00 2F 00 00 00 01 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == 

hex_convert(P.encode(), 150)


def test_02_bind_rcr_decode():
    "Test Bind Receiver decoding"
    data = b'\x00\x00\x00/\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00SUBMIT1\x00P\x01\x01\x00'
    P = BindReceiver.decode(data)
    assert '00 00 00 2F 00 00 00 01 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == 

hex_convert(P.encode(), 150)

#--------------------------------------------------------------------------------

def test_01_bind_rcr_rsp_encode():
    "Test Bind Receiver Response encoding"
    P = BindReceiverResp()

    P.system_id = CString("SMPP3TEST")
    P.interface_version = Integer(IV.SMPP_VERSION_5, 1)
    
    assert '00 00 00 1B 80 00 00 01 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 50 ' == hex_convert(P.encode(), 150)


def test_02_bind_rcr_rsp_decode():
    "Test Bind Receiver Response decoding"
    data = b'\x00\x00\x00\x1B\x80\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00\x50'
    P = BindReceiverResp.decode(data)
    assert '00 00 00 1B 80 00 00 01 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 50 ' == hex_convert(P.encode(), 150)

#--------------------------------------------------------------------------------

def test_01_bind_tcr_encode():
    "test Bind Transceivr encoding"
    P = BindTransceiver()
    
    P.system_id = CString("SMPP3TEST")
    P.password = CString("secret08")
    P.system_type = CString("SUBMIT1")
    P.interface_version = Integer(IV.SMPP_VERSION_5, 1)
    P.addr_ton = Integer(TON.INTERNATIONAL, 1)
    P.addr_npi = Integer(NPI.ISDN, 1)
    P.address_range = CString('')
    
    assert '00 00 00 2F 00 00 00 09 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == 

hex_convert(P.encode(), 150)


def test_02_bind_tcr_decode():
    "Test Bind Transceiver decoding"
    data = data = b'\x00\x00\x00/\x00\x00\x00\x09\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00' + \
           b'SUBMIT1\x00P\x01\x01\x00'
    P = BindTransceiver.decode(data)
    assert '00 00 00 2F 00 00 00 09 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38 00 53 55 42 4D 49 54 31 00 50 01 01 00 ' == 

hex_convert(P.encode(), 150)

#--------------------------------------------------------------------------------

def test_01_bind_tcr_rsp_encode():
    "Test Bind Transceiver Response encoding"
    P = BindTransceiverResp()

    P.system_id = CString("SMPP3TEST")
    P.interface_version = Integer(IV.SMPP_VERSION_5, 1)
    
    assert '00 00 00 1B 80 00 00 09 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 50 ' == hex_convert(P.encode(), 150)

def test_02_bind_tcr_rsp_decode():
    "Test Bind Transceiver Response decoding"
    data = b'\x00\x00\x00\x1b\x80\x00\x00\x09\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00P'


    P = BindTransceiverResp.decode(data)
    assert '00 00 00 1B 80 00 00 09 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 50 ' == hex_convert(P.encode(), 150)

#--------------------------------------------------------------------------------

def test_01_outbind_encode():
    "Test Out Bind encoding"
    P = OutBind()

    P.system_id = CString("SMPP3TEST")
    P.password = CString("secret08")
    
    assert '00 00 00 23 00 00 00 0B 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74 30 38 00 ' == hex_convert(P.encode(), 150)


def test_02_outbind_decode():
    "Test Out Bind decoding"
    data = b'\x00\x00\x00\x23\x00\x00\x00\x0B\x00\x00\x00\x00\x00\x00\x00\x01SMPP3TEST\x00secret08\x00'
    P = OutBind.decode(data)
    assert '00 00 00 23 00 00 00 0B 00 00 00 00 00 00 00 01 53 4D 50 50 33 54 45 53 54 00 73 65 63 72 65 74' +\
           ' 30 38 00 ' == hex_convert(P.encode(), 150)

#--------------------------------------------------------------------------------

def test_01_unbind_encode():
    "Test UnBind encoding"
    P = UnBind()
    
    assert '00 00 00 10 00 00 00 06 00 00 00 00 00 00 00 01 '  == hex_convert(P.encode(),150)
    
def test_02_unbind_decode():
    "Test UnBind decoding"
    
    data = b'\x00\x00\x00\x10\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x01'

    P = UnBind.decode(data)
    assert '00 00 00 10 00 00 00 06 00 00 00 00 00 00 00 01 ' == hex_convert(P.encode(),150)

#--------------------------------------------------------------------------------

def test_01_unbind_rsp_encode():
    "Test UnBindResp encoding"
    
    P = UnBindResp()
    #P.command_id = Integer(command_id.unbind_resp, 4)
    
    assert '00 00 00 10 80 00 00 06 00 00 00 00 00 00 00 01 ' == hex_convert(P.encode(), 150)
    
def test_02_unbind_rsp_decode():
    "Test UnBindResp decoding"
    
    data = b'\x00\x00\x00\x10\x80\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x01'
    P = UnBindResp.decode(data)
    assert '00 00 00 10 80 00 00 06 00 00 00 00 00 00 00 01 ' == hex_convert(P.encode(), 150)

#--------------------------------------------------------------------------------

def test_01_enquirelink_encode():
    "Test EnquireLink encoding"
    P = EnquireLink()
    
    assert '00 00 00 10 00 00 00 15 00 00 00 00 00 00 00 01 '  == hex_convert(P.encode(),150)
    
def test_02_enquirelink_decode():
    "Test EnquireLink decoding"
    
    data = b'\x00\x00\x00\x10\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00\x01'

    P = EnquireLink.decode(data)
    assert '00 00 00 10 00 00 00 15 00 00 00 00 00 00 00 01 ' == hex_convert(P.encode(),150)

#--------------------------------------------------------------------------------

def test_01_enquirelink_rsp_encode():
    "Test EnquireLinkResp encoding"
    P = EnquireLinkResp()
    
    assert '00 00 00 10 80 00 00 15 00 00 00 00 00 00 00 01 '  == hex_convert(P.encode(),150)
    
def test_02_enquirelink_rsp_decode():
    "Test EnquireLinkResp decoding"
    
    data =b'\x00\x00\x00\x10\x80\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00\x01'
    P = EnquireLinkResp.decode(data)
    assert '00 00 00 10 80 00 00 15 00 00 00 00 00 00 00 01 ' == hex_convert(P.encode(),150)

#--------------------------------------------------------------------------------

#def test_01_alert_notification_encode():
 #   "Test Alert Notification encoding"
  #  P = AlertNotification()
    
   # P.source_addr_ton = Integer(TON.INTERNATIONAL, 1)
   # P.source_addr_npi = Integer(NPI.ISDN, 1)
   # P.source_addr = CString("")
   # P.esme_addr_ton = Integer(TON.INTERNATIONAL, 1)
   # P.esme_addr_npi = Integer(NPI.ISDN, 1)
   # P.esme_addr = CString("")
    #P.ms_availability_status=TLV(1058,1)
   

    #assert '00 00 00 2a 00 00 01 02 00 00 00 00 00 00 00 01' + \
     #      ' 01 01 00 01 01 00 ' == hex_convert(P.encode(),150)
            
#def test_02_alert_notification_decode():
 #   "Test Alert Notification decoding"
  #   data = b'\x00\x00\x00\x2a\x00\x00\x01\x02\x00\x00\x00\x00\x00\x00\x00\x01' + \
   #        b'\x01\x01\x00\x01\x01\x00'
   #   P =  AlertNotification.decode(data)
      #assert '00 00 00 2a 00 00 01 02 00 00 00 00 00 00 00 01' + \
     #        ' 01 01 00 01 01 00' == hex_convert(P.encode(),150)
           
#--------------------------------------------------------------------------------

def test_01_generic_nack_encode():
    "Test Generic_Nack encoding"
    P = GenericNack()
    
    assert '00 00 00 10 80 00 00 00 00 00 00 00 00 00 00 01 '  == hex_convert(P.encode(), 150)
def test_02_generic_nack_decode():
    "Test Generic_Nack decoding"
    
    data = b'\x00\x00\x00\x10\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
    P = GenericNack.decode(data)
    assert '00 00 00 10 80 00 00 00 00 00 00 00 00 00 00 01 ' == hex_convert(P.encode(), 150)
    
#------------------------------------------------------------
