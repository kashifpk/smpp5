"""
SMPP Session Implementation
===========================

SMPPSession class is used to handle SMPP Sessions between client and server, both client and
server create an instance of SMPPSession to communicate with each other.

"""
import sys
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
from smpp5.lib.pdu.message_submission import (
    SubmitSm,
    SubmitSmResp,
    DataSm,
    DataSmResp,
    SubmitMulti,
    SubmitMultiResp)


class SessionState(object):
    """
    Possible session states
    """

    CLOSED = 0
    OPEN = 1
    BOUND_TX = 2
    BOUND_RX = 3
    BOUND_TRX = 4
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
        self.server_validate_method = ''

    def _next_seq_num(self):
        self._seq_num += 1
        return self._seq_num

    def get_pdu_from_socket(self):
        """
        Given a socket, returns a completed PDU and blocks until a PDU is received
        """
        #First wait till 4 bytes a read from the socket (command_length)
        d = self.socket.recv(4, socket.MSG_WAITALL)
        command_length = Integer.decode(d)  # decode first four bytes to get the command length via it 

        # get bytes specified by command_length - 4
        sock_data = self.socket.recv(command_length.value - 4, socket.MSG_WAITALL)
        sock_data = d + sock_data

        command_id = Integer.decode(sock_data[4:8])    # decode from 5th byte till 8th to get command_id
        PDUClass = command_mappings[command_id.value]  # get the class name via command_id

        # decode PDU
        P = PDUClass.decode(sock_data)

        return P

    def handle_pdu(self, P):
        """
        Given a PDU P, calls appropriate methods to handle it.
        """
        if command_ids.submit_sm == P.command_id:
            pass

    def close(self):
        # if session stat is one of the bound states, unbind it.
        if self.state in [SessionState.BOUND_TX, SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            P = UnBind()
            P.sequence_number = Integer(self._next_seq_num(), 4)
            self.socket.sendall(P.encode())
            self.state = SessionState.UNBOUND

        # wait for the server to send UnBindResp and then close the session
        resp_pdu = self.get_pdu_from_socket()
        #while resp_pdu.command_id != command_ids.unbind_resp:
        #    self.handle_pdu(resp_pdu)
        #    resp_pdu = self.get_pdu_from_socket()
        self.state = SessionState.CLOSED

    def bind(self, bind_type, system_id, password, system_type):
        """
        Used by the client to bind TX, RX or TRX with the server
        """
        # try sending the appropriate bind type PDU ('RX', 'TX', 'TRX') and fetch return value
        bind_types = dict(
            TX=dict(request=BindTransmitter, response=BindTransmitterResp, state=SessionState.BOUND_TX),
            RX=dict(request=BindReceiver, response=BindReceiverResp, state=SessionState.BOUND_RX),
            TRX=dict(request=BindTransceiver, response=BindTransceiverResp, state=SessionState.BOUND_TRX)
        )
        self.state = bind_types[bind_type]['state']
        P = bind_types[bind_type]['request']()
        P.sequence_number = Integer(self._next_seq_num(), 4)
        P.system_id = CString(system_id)
        P.password = CString(password)
        P.system_type = CString(system_type)
        data = P.encode()
        self.socket.sendall(data)
        print("    Bind pdu sent to server by client   ")
        # recieving the response from server
        P = self.get_pdu_from_socket()

    def handle_bind(self, validate):
        """
        Used by the server to handle the incoming bind request
        """
        #recieving bind pdu from client
        P = self.get_pdu_from_socket()
        self.server_validate_method = validate
        print("Received PDU: " + P.__class__.__name__)

        pdu = dict(
            BindTransmitter=dict(state=SessionState.BOUND_TX, response=BindTransmitterResp),
            BindReceiver=dict(state=SessionState.BOUND_RX, response=BindReceiverResp),
            BindTransceiver=dict(state=SessionState.BOUND_TRX, response=BindTransceiverResp)
        )
        #Validating the Credentials and sending response
        if(P.__class__.__name__ == BindTransmitter or BindReceiver or BindTransceiver):
            validate = self.server_validate_method(P.system_id.value, P.password.value, P.system_type.value)
            if(validate == 'True'):
                self.state = pdu[P.__class__.__name__]['state']
                R = pdu[P.__class__.__name__]['response']()
                R.sequence_number = Integer(P.sequence_number.value, 4)
                R.system_id = CString(P.system_id.value)
                data = R.encode()
                self.socket.sendall(data)
            else:
                R = GenericNack()
                R.sequence_number = Integer(P.sequence_number.value, 4)
                R.command_status = Integer(command_status.ESME_RBINDFAIL, 4)
                data = R.encode()
                self.socket.sendall(data)
        print("    Response pdu sent to client by server   ")
        print(P.system_id.value)
        print(P.password.value)
        print(P.system_type.value)

    def handle_unbind(self):
        """
        Used by the server to handle the incoming unbind request
        """
        P = self.get_pdu_from_socket()
        if self.state in [SessionState.BOUND_TX, SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            self.state = SessionState.UNBOUND
            R = UnBindResp()
            R.sequence_number = Integer(P.sequence_number.value, 4)
            data = R.encode()
            self.socket.sendall(data)

    #def send_sms(self, other_parameters):
      #if self.state not in ['bound_tx', 'bound_trx']:
           #raise Exception("SMPP Session not in a state that allows sending SMSes")

