"""
SMPP Session Implementation
===========================

SMPPSession class is used to handle SMPP Sessions between client and server, both client and
server create an instance of SMPPSession to communicate with each other.

"""

from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.constants import *
from smpp5.lib.constants import NPI, TON, esm_class, command_id, command_status, tlv_tag
from smpp5.lib.constants.command_status import *
from smpp5.lib.pdu.pdu import PDU
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


class SessionState(object):
    """
    Possible session states
    """

    CLOSED = 0
    OPEN = 1
    BOUND_TX = 2
    BOUND_RX = 3
    BOUNT_TRX = 4
    UNBOUND = 5
    OUTBOUND = 6


class SMPPSession(object):

    sequence_number = 0

    def __init__(self, session_end, socket):
        """
        Create SMPPSession object.

        :param session_end: Can either be 'client' or 'server'
        :param socket: open socket object to use for communication
        """

        assert session_end in ['client', 'server']
        self.session_end = session_end
        self.socket = socket
        self.state = SessionState.OPEN



    #def bind(self, bind_type, system_id, password, system_type):
    #
    #    # try sending the appropriate bind type PDU ('RX', 'TX', 'TRX') and fetch return value
    #
    #def send_sms(self, other_parameters):
    #
    #    if self.state not in ['bound_tx', 'bound_trx']:
    #        raise Exception("SMPP Session not in a state that allows sending SMSes")

