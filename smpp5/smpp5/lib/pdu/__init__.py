from smpp5.lib.constants import command_ids
from smpp5.lib.pdu.session_management import (
    BindTransmitter,
    BindTransmitterResp,
    BindReceiver,
    BindReceiverResp,
    BindTransceiver,
    BindTransceiverResp,
    OutBind,
    UnBind,
    UnBindResp,
    EnquireLink,
    EnquireLinkResp,
    AlertNotification,
    GenericNack)
from smpp5.lib.pdu.message_submission import (
    SubmitSm,
    SubmitSmResp,
    DataSm,
    DataSmResp,
    SubmitMulti,
    SubmitMultiResp,
    QuerySm,
    QuerySmResp,
    CancelSm,
    CancelSmResp,
    ReplaceSm,
    ReplaceSmResp)

# command_id to PDU Class mappings
command_mappings = {
    command_ids.generic_nack: GenericNack,
    command_ids.bind_receiver: BindReceiver,
    command_ids.bind_receiver_resp: BindReceiverResp,
    command_ids.bind_transmitter: BindTransmitter,
    command_ids.bind_transmitter_resp: BindTransmitterResp,
    command_ids.bind_transceiver: BindTransceiver,
    command_ids.bind_transceiver_resp: BindTransceiverResp,
    command_ids.outbind: OutBind,
    command_ids.unbind: UnBind,
    command_ids.unbind_resp: UnBindResp,
    command_ids.enquire_link: EnquireLink,
    command_ids.enquire_link_resp: EnquireLinkResp,
    command_ids.alert_notification: AlertNotification,
    command_ids.submit_sm: SubmitSm,
    command_ids.submit_sm_resp: SubmitSmResp,
    command_ids.query_sm: QuerySm,
    command_ids.query_sm_resp : QuerySmResp,
    command_ids.cancel_sm : CancelSm,
    command_ids.cancel_sm_resp : CancelSmResp,
    command_ids.replace_sm : ReplaceSm,
    command_ids.replace_sm_resp : ReplaceSmResp
}
