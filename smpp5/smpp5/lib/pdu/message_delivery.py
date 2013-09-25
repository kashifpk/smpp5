from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, dest_flag


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
    short_message = CString("")
    #TLV Submission operations


class DeliverSmResp(PDU):
    command_id = Integer(command_ids.deliver_sm_resp, 4)
    message_id = CString("")
    #message deliver response TLV




