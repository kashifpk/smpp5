from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, dest_flag


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
