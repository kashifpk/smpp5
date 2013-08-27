from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, dest_flag


class SubmitSm(PDU):
    "Submit Sm PDU type"

    command_id = Integer(command_ids.submit_sm, 4)
    service_type = CString("")
    source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    source_addr_npi = Integer(NPI.ISDN, 1)
    source_addr = CString("")
    dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    dest_addr_npi = Integer(NPI.ISDN, 1)
    destination_addr = CString("")
    esm_class = Integer(esm_class.Default_mode, 1)
    protocol_id = Integer(0, 1)              # page 129, its value is NULL
    priority_flag = Integer(0, 1)            # page 129
    schedule_delivery_time = CString("")
    validity_period = CString("")
    registered_delievery = Integer(0, 1)     # page 130
    replace_if_present_flag = Integer(0, 1)  # page 131
    data_coding = Integer(0, 1)              # page 123
    sm_default_msg_id = Integer(0, 1)        # page 134
    sm_length = Integer(0, 1)                # page 134
    short_message = CString("")
    #TLV Submission operations


class SubmitSmResp(PDU):
    "Submit Sm Response PDU type"

    command_id = Integer(command_ids.submit_sm_resp, 4)
    message_id = CString("")
    #message submission response TLV


class DataSm(PDU):
    "Data Sm PDU type"

    command_id = Integer(command_ids.data_sm, 4)
    service_type = CString("")
    source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    source_addr_npi = Integer(NPI.ISDN, 1)
    source_addr = CString("")
    dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    dest_addr_npi = Integer(NPI.ISDN, 1)
    destination_addr = CString("")
    esm_class = Integer(esm_class.Default_mode, 1)
    registered_delievery = Integer(0, 1)     # page 130
    data_coding = Integer(0, 1)              # page 123
    #TLV Submission operations


class DataSmResp(PDU):
    "Data Sm Response PDU type"

    command_id = Integer(command_ids.data_sm_resp, 4)
    message_id = CString("")
    #message submission response TLV


class SubmitMulti(PDU):
    "Submit Multi PDU type"

    command_id = Integer(command_ids.submit_multi, 4)
    service_type = CString("")
    source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    source_addr_npi = Integer(NPI.ISDN, 1)
    source_addr = CString("")
    number_of_dests = Integer(1, 1)           # page 72
    sme_dest_flag = Integer(dest_flag.SME_ADDRESS, 1)
    dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    dest_addr_npi = Integer(NPI.ISDN, 1)
    destination_addr = CString("")
    distribution_dest_flag = Integer(dest_flag.DISTRIBUTION_LIST_NAME, 1)
    dl_name = CString("")
    esm_class = Integer(esm_class.Default_mode, 1)
    protocol_id = Integer(0, 1)              # page 129, its value is NULL
    priority_flag = Integer(0, 1)            # page 129
    schedule_delivery_time = CString("")
    validity_period = CString("")
    registered_delievery = Integer(0, 1)     # page 130
    replace_if_present_flag = Integer(0, 1)  # page 131
    data_coding = Integer(0, 1)              # page 123
    sm_default_msg_id = Integer(0, 1)        # page 134
    sm_length = Integer(0, 1)                # page 134
    short_message = String("")
    #TLV Submission operations


class SubmitMultiResp(PDU):
    "Submit Multi Response PDU type"

    command_id = Integer(command_ids.submit_multi_resp, 4)
    message_id = CString("")
    no_unsuccess = Integer(0, 1)            # page 129
    dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    dest_addr_npi = Integer(NPI.ISDN, 1)
    destination_addr = CString("")
    error_status_code = Integer(command_status.ESME_ROK, 4)
    #message submission response TLV


class QuerySm(PDU):
    "Query Submission PDU type"
    
    command_id = Integer(command_ids.query_sm, 4)
    message_id = CString("")
    source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    source_addr_npi = Integer(NPI.ISDN, 1)
    source_addr = CString("")


class QuerySmResp(PDU):
    "Query Submission Response PDU type"
    
    command_id = Integer(command_ids.query_sm_resp, 4)
    message_id = CString("")
    final_date = CString("")
    message_state = Integer(0, 1)
    error_code = Integer(0, 1)


class CancelSm(PDU):
    "Cancel Message Submission PDU type"
    
    command_id = Integer(command_ids.cancel_sm, 4)
    service_type = CString("")
    message_id = CString("")
    source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    source_addr_npi = Integer(NPI.ISDN, 1)
    source_addr = CString("")
    dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    dest_addr_npi = Integer(NPI.ISDN, 1)
    destination_addr = CString("")


class CancelSmResp(PDU):
    "Cancel Message Response PDU type"
    
    command_id = Integer(command_ids.cancel_sm_resp, 4)


class ReplaceSm(PDU):
    "Replace Short Message PDU type"
    
    command_id = Integer(command_ids.replace_sm, 4)
    message_id = CString("")
    source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    source_addr_npi = Integer(NPI.ISDN, 1)
    source_addr = CString("")
    schedule_delivery_time = CString("")
    validity_period = CString("")
    registered_delievery = Integer(0, 1)
    sm_default_msg_id = Integer(0, 1)
    sm_length = Integer(0, 1)                # page 134
    short_message = CString("")              # This field should be CString


class ReplaceSmResp(PDU):
    "Replace Short Message Response PDU type"
    
    command_id = Integer(command_ids.replace_sm_resp, 4)

class DeliverSm(PDU):
    "Deliver Short Message "
    
    command_id = Integer(command_ids.deliver_sm, 4)
    service_type = CString("")
    source_addr_ton = Integer(TON.INTERNATIONAL, 1)
    source_addr_npi = Integer(NPI.ISDN, 1)
    source_addr = CString("")
    dest_addr_ton = Integer(TON.INTERNATIONAL, 1)
    dest_addr_npi = Integer(NPI.ISDN, 1)
    destination_addr = CString("")
    esm_class = Integer(esm_class.Default_mode, 1)
    protocol_id = Integer(0, 1)              # page 129, its value is NULL
    priority_flag = Integer(0, 1)            # page 129
    schedule_delivery_time = CString("")
    validity_period = CString("")
    registered_delievery = Integer(0, 1)     # page 130
    replace_if_present_flag = Integer(0, 1)  # page 131
    data_coding = Integer(0, 1)              # page 123
    sm_default_msg_id = Integer(0, 1)        # page 134
    sm_length = Integer(0, 1)                # page 134
    short_message = String("")
    #TLV Submission operations
    
class DeliverSmResp(PDU):
    command_id = Integer(command_ids.deliver_sm_resp, 4)
    message_id = CString("")
    #message deliver response TLV


    
