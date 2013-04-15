from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON, esm_class, command_id, command_status, tlv_tag


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

class GenericNack(PDU):
    "Generic Nack PDU type"

    command_id = Integer(command_id.generic_nack, 4)

class SubmitSm(PDU):
    "Submit Sm PDU type"

    command_id = Integer(command_id.submit_sm, 4)
    service_type = CString("")
    source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    source_addr_npi = Integer(NPI.ISDN, 1)
    source_addr = CString("")
    dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    dest_addr_npi = Integer(NPI.ISDN, 1)
    destination_addr = CString("")
    esm_class = Integer(esm_class.Default_mode, 1)  
    protocol_id = Integer(0, 1)              #page 129, its value is NULL
    priority_flag = Integer(0, 1)            #page 129
    schedule_delivery_time = CString("")
    validity_period = CString("")
    registered_delievery = Integer(0, 1)     #page 130
    replace_if_present_flag = Integer(0,1)   #page 131
    data_coding = Integer(0, 1)              #page 123
    sm_default_msg_id = Integer(0, 1)        #page 134
    sm_length = Integer(0, 1)                #page 134
    short_message = String("")
    #TLV Submission operations

class SubmitSmResp(PDU):
    "Submit Sm Response PDU type"

    command_id = Integer(command_id.submit_sm_resp, 4)
    message_id = CString("")
    #message submission response TLV

class DataSm(PDU):
    "Data Sm PDU type"

    command_id = Integer(command_id.data_sm, 4)
    service_type = CString("")
    source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    source_addr_npi = Integer(NPI.ISDN, 1)
    source_addr = CString("")
    dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    dest_addr_npi = Integer(NPI.ISDN, 1)
    destination_addr = CString("")
    esm_class = Integer(esm_class.Default_mode, 1)  
    registered_delievery = Integer(0, 1)     #page 130
    data_coding = Integer(0, 1)              #page 123
    #TLV Submission operations

class DataSmResp(PDU):
    "Data Sm Response PDU type"

    command_id = Integer(command_id.data_sm_resp, 4)
    message_id = CString("")
    #message submission response TLV
    
class SubmitMulti(PDU):
    "Submit Multi PDU type"

    command_id = Integer(command_id.submit_multi, 4)
    service_type = CString("")
    source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    source_addr_npi = Integer(NPI.ISDN, 1)
    source_addr = CString("")
    number_of_dests = Integer(1, 1)           #page 72
    sme_dest_flag = Integer(command_id.dest_flag_value1, 1)
    dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    dest_addr_npi = Integer(NPI.ISDN, 1)
    destination_addr = CString("")
    distribution_dest_flag = Integer(command_id.dest_flag_value2, 1)
    dl_name = CString("") 
    esm_class = Integer(esm.Default_mode, 1)  
    protocol_id = Integer(0, 1)              #page 129, its value is NULL
    priority_flag = Integer(0, 1)            #page 129
    schedule_delivery_time = CString("")
    validity_period = CString("")
    registered_delievery = Integer(0, 1)     #page 130
    replace_if_present_flag = Integer(0,1)   #page 131
    data_coding = Integer(0, 1)              #page 123
    sm_default_msg_id = Integer(0, 1)        #page 134
    sm_length = Integer(0, 1)                #page 134
    short_message = String("")
    #TLV Submission operations
    
class SubmitMultiResp(PDU):
    "Submit Multi Response PDU type"

    command_id = Integer(command_id.submit_multi_resp, 4)
    message_id = CString("")
    no_unsuccess = Integer(0, 1)            #page 129
    dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    dest_addr_npi = Integer(NPI.ISDN, 1)
    destination_addr = CString("")
    error_status_code = Integer(command_status.ESME_ROK, 4)
    #message submission response TLV
    


    
    
