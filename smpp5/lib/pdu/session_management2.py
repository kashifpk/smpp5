from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON, esm_class, command_id, command_status, tlv_tag, dest_flag


class BindTransmitter(PDU):
    "Bind Transmitter PDU type"

    command_id = Integer(command_id.bind_transmitter, 4)
    system_id = CString("")
    password = CString("")
    system_type = CString("")
    interface_version = Integer(IV.SMPP_VERSION_5, 1)
    addr_ton = Integer(TON.INTERNATIONAL, 1)
    addr_npi = Integer(NPI.ISDN, 1)
    address_range = CString('')

class BindTransmitterResp(PDU):
    "Bind Transmitter Response PDU type"

    command_id = Integer(command_id.bind_transmitter_resp, 4)
    system_id = CString("")
    interface_version = Integer(IV.SMPP_VERSION_5, 1)
    

class BindReceiver(PDU):
    "Bind receiver PDU type"

    command_id = Integer(command_id.bind_receiver, 4)
    system_id = CString("")
    password = CString("")
    system_type = CString("")
    interface_version = Integer(IV.SMPP_VERSION_5, 1)
    addr_ton = Integer(TON.INTERNATIONAL, 1)
    addr_npi = Integer(NPI.ISDN, 1)
    address_range = CString('')

class BindReceiverResp(PDU):
    "Bind Receiver Response PDU type"

    command_id = Integer(command_id.bind_receiver_resp, 4)
    system_id = CString("")
    interface_version = Integer(IV.SMPP_VERSION_5, 1)
    

class BindTransceiver(PDU):
    "Bind Transceiver PDU type"

    command_id = Integer(command_id.bind_transceiver, 4)
    system_id = CString("")
    password = CString("")
    system_type = CString("")
    interface_version = Integer(IV.SMPP_VERSION_5, 1)
    addr_ton = Integer(TON.INTERNATIONAL, 1)
    addr_npi = Integer(NPI.ISDN, 1)
    address_range = CString('')

class BindTransceiverResp(PDU):
    "Bind Transceiver Respinse PDU type"

    command_id = Integer(command_id.bind_transceiver_resp, 4)
    system_id = CString("")
    interface_version = Integer(IV.SMPP_VERSION_5, 1)
    

class OutBind(PDU):
    "OutBind PDU type"

    command_id = Integer(command_id.outbind, 4)
    system_id = CString("")
    password = CString("")
    

class UnBind(PDU):
    "UnBind PDU type"

    command_id = Integer(command_id.unbind, 4)

class UnBindResp(PDU):
    "UnBind Response PDU type"

    command_id = Integer(command_id.unbind_resp, 4)

class EnquireLink(PDU):
    "Enquire_Link PDU type"

    command_id = Integer(command_id.enquire_link, 4)

class EnquireLinkResp(PDU):
    "Enquire_Link Response PDU type"

    command_id = Integer(command_id.enquire_link_resp, 4)
    
class AlertNotification(PDU):
    "Alert Notification PDU type"

    command_id = Integer(command_id.alert_notification, 4)
    system_id = CString("")
    password = CString("")
    system_type = CString("")
    source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    source_addr_npi = Integer(NPI.ISDN, 1)
    source_addr = CString("")
    esme_addr_ton = Integer(TON.INTERNATIONAL, 1)
    esme_addr_npi = Integer(NPI.ISDN, 1)
    esme_addr = CString("")
    ms_availability_status=TLV(1058,0)

class Generic_Nack(PDU):
    "Generic Nack Response PDU type"

    command_id = Integer(command_id.generic_nack, 4)

