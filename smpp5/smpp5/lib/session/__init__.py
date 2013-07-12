"""
SMPP Session Implementation
===========================

SMPPSession class is used to handle SMPP Sessions between client and server, both client and
server create an instance of SMPPSession to communicate with each other.

"""

import socket
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.constants import *
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag
from smpp5.lib.constants.command_status import *
from smpp5.lib.pdu import command_mappings
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
        self._seq_num = 0

    def _next_seq_num(self):
        self._seq_num += 1
        return self._seq_num

    def get_pdu_from_socket(self):
        """
        Given a socket, returns a completed PDU
        """
        #First wait till 4 bytes a read from the socket (command_length)
        d = self.socket.recv(4, socket.MSG_WAITALL)
        command_length = Integer.decode(d)

        # get bytes specified by command_length - 4
        sock_data = self.socket.recv(command_length.value - 4, socket.MSG_WAITALL)
        sock_data = d + sock_data

        command_id = Integer.decode(sock_data[4:8])
        PDUClass = command_mappings[command_id.value]

        # decode PDU
        P = PDUClass.decode(sock_data)

        return P

    def bind(self, bind_type, system_id, password, system_type):
        """
        Used by the client to bind TX, RX or TRX with the server
        """
        # try sending the appropriate bind type PDU ('RX', 'TX', 'TRX') and fetch return value
        bind_types = dict(
            TX=dict(request=BindTransmitter, response=BindTransmitterResp),
            RX=dict(request=BindReceiver, response=BindReceiverResp),
            TRX=dict(request=BindTransceiver, response=BindTransceiverResp)
        )

        P = bind_types[bind_type]['request']()
        P.sequence_number = self._next_seq_num()
        P.system_id = CString(system_id)
        P.password = CString(password)
        P.system_type = CString(system_type)
        data = P.encode()

        self.socket.sendall(data)

    def handle_bind(self):
        """
        Used by the server to handle the incoming bind request
        """

        P = self.get_pdu_from_socket()
        print("Received PDU: " + P.__class__.__name__)
        print(P.system_id.value)
        print(P.password.value)
        print(P.system_type.value)

        #TODO: Validate this against DB here. Set session state according to validation results and
        # send appropriate response or generick nack PDU back through self.socket.

    #def send_sms(self, other_parameters):
    #
    #    if self.state not in ['bound_tx', 'bound_trx']:
    #        raise Exception("SMPP Session not in a state that allows sending SMSes")

