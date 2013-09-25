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
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, message_state
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
    SubmitMultiResp,
    QuerySm,
    QuerySmResp,
    CancelSm,
    CancelSmResp,
    ReplaceSm,
    ReplaceSmResp,
    DeliverSm,
    DeliverSmResp)


class InvalidSessionState(Exception):
    def __init__(self):
        print(Exception)


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

    allowed_actions = {
        'submit_sm': [SessionState.BOUND_TRX, SessionState.BOUND_TX],
        'query_sm': [SessionState.BOUND_TRX, SessionState.BOUND_TX],
        'cancel_sm': [SessionState.BOUND_TRX, SessionState.BOUND_TX],
        'replace_sm': [SessionState.BOUND_TRX, SessionState.BOUND_TX],
        'deliver_sm': [SessionState.BOUND_TRX, SessionState.BOUND_RX]
    }

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
        self.responses = {}
        self.unread_smses = []
        self.server_validate_method = ''
        self.server_db_store = ''
        self.server_query_result = ''
        self.server_cancel_result = ''
        self.server_replace_result = ''
        self.user_id = None

    def _can_do(self, action):
        "Validates if an action can be performed in current session state or not"
        if self.state in self.allowed_actions[action]:
            return True
        else:
            return False

    def _next_seq_num(self):
        self._seq_num += 1
        return self._seq_num

    def get_pdu_from_socket(self):
        """
        Given a socket, returns a completed PDU and blocks until a PDU is received

        For non-blocking sockets see:

        * http://docs.python.org/2/howto/sockets.html#non-blocking-sockets
        * http://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
        * http://docs.python.org/2/library/select.html#select.select
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
        if command_ids.submit_sm == P.command_id.value:
            self.process_sms(P)
        elif(command_ids.query_sm == P.command_id.value):
            self.process_query(P)
        elif(command_ids.cancel_sm == P.command_id.value):
            self.process_sms_cancelling(P)
        elif(command_ids.replace_sm == P.command_id.value):
            self.process_replace_sms(P)

    def close(self):
        P = self.get_pdu_from_socket()
        if self.state in [SessionState.BOUND_TX, SessionState.BOUND_TRX]:
            while P.command_id.value != command_ids.unbind:
                self.handle_pdu(P)
                P = self.get_pdu_from_socket()
        self.handle_unbind(P)

    def client_recieve_pdus(self):
        '''
        Client use this method to recieve response PDU's and calls appropriate methods to handle it.
        '''

        while True:
            P = self.get_pdu_from_socket()
            if(responses[R.sequence_number]):
                if(command_ids.submit_sm_resp == R.command_id.value):
                    self.send_sms_response(P)
                elif(command_ids.query_sm_resp == R.command_id.value):
                    self.query_sms_response(P)
                elif(command_ids.replace_sm_resp == R.command_id.value):
                    self.replace_sms_response(P)
                elif(command_ids.cancel_sm_resp == R.command_id.value):
                    self.cancel_sms_response(P)
                elif(command_ids.unbind_resp == R.command_id.value):
                    self.state = SessionState.UNBOUND
            del responses[R.sequence_number]

    def unbind(self):
        if self.state in [SessionState.BOUND_TX, SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            P = UnBind()
            P.sequence_number = Integer(self._next_seq_num(), 4)
            self.responses.update({P.sequence_number.value: P})
            self.socket.sendall(P.encode())

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
        P = bind_types[bind_type]['request']()
        P.sequence_number = Integer(self._next_seq_num(), 4)
        P.system_id = CString(system_id)
        P.password = CString(password)
        P.system_type = CString(system_type)
        data = P.encode()
        self.socket.sendall(data)
        # recieving the response from server
        P = self.get_pdu_from_socket()
        if(P.command_status.value == 0):
            self.state = bind_types[bind_type]['state']

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
                self.validation_status = 'success'
                self.user_id = P.system_id.value.decode(encoding='ascii')
                print(self.user_id)
                self.state = pdu[P.__class__.__name__]['state']
                R = pdu[P.__class__.__name__]['response']()
                R.sequence_number = Integer(P.sequence_number.value, 4)
                R.system_id = CString(P.system_id.value)
                data = R.encode()
                self.socket.sendall(data)
            else:
                self.validation_status = 'fail'
                R = GenericNack()
                R.sequence_number = Integer(P.sequence_number.value, 4)
                R.command_status = Integer(command_status.ESME_RBINDFAIL, 4)
                data = R.encode()
                self.socket.sendall(data)
        print("    Response pdu sent to client by server   ")
        print(P.system_id.value)
        print(P.password.value)
        print(P.system_type.value)

    def send_sms(self, recipient, message):
        """
        This method is responsible for taking the Sumbit short message request send by client and writes it to
        the socket to be read by server.
        """

        if not self._can_do('submit_sm'):
            raise InvalidSessionState("SMPP Session not in a state that allows sending SMSes")

        P = SubmitSm()
        P.sequence_number = Integer(self._next_seq_num(), 4)
        P.source_addr = CString(str(self.user_id))
        P.destination_addr = CString(recipient)
        P.short_message = CString(str(message))
        data = P.encode()
        #storing pdu in dictionary named responses
        self.responses.update({P.sequence_number.value: P})
        self.socket.sendall(data)

    def process_sms(self, P):
        """
        This method is responsible for handling the request sent by client and sending the response pdu to the client
        for successfull submission
        """
        if self.state in [SessionState.BOUND_TX, SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            db_storage = self.server_db_store(P.destination_addr.value, P.short_message.value, self.user_id)
            # in db_storage the message id of sms is returned
            R = SubmitSmResp()
            R.sequence_number = Integer(P.sequence_number.value, 4)
            R.message_id = CString(str(db_storage))
            data = R.encode()
            self.socket.sendall(data)

    def send_sms_response(self, P):
        message_id = P.message_id.value

    def query_status(self, message_id):
        """
        This method is responsible for querying the status of message that either it is delievered or still
        scheduled
        """
        if not self._can_do('submit_sm'):
            raise InvalidSessionState("SMPP Session not in a state that allows querying SMSes")

        P = QuerySm()
        P.sequence_number = Integer(self._next_seq_num(), 4)
        P.message_id = CString(str(message_id))
        self.responses.update({P.sequence_number.value: P})
        self.socket.sendall(P.encode())

    def process_query(self, P):
        """
        This message is responsible for handling querying request and returning status of message
        """
        query_result = self.server_query_result(P.message_id.value)
        R = QuerySmResp()
        R.sequence_number = Integer(P.sequence_number.value, 4)
        R.message_id = CString(P.message_id.value)
        R.final_date = CString("")
        R.message_state = Integer(query_result, 1)
        data = R.encode()
        self.socket.sendall(data)

    def query_sms_response(self, P):
        message_state = P.message_state.value

    def cancel_sms(self, message_id):
        """
        This method is responsible for requesting the cancelling of particular message
        """
        if not self._can_do('submit_sm'):
            raise InvalidSessionState("SMPP Session not in a state that allows cancelling SMSes")

        P = CancelSm()
        P.sequence_number = Integer(self._next_seq_num(), 4)
        P.message_id = CString(str(message_id))
        self.responses.update({P.sequence_number.value: P})
        self.socket.sendall(P.encode())

    def process_sms_cancelling(self, P):
        """
        This method is responsible for handling cancel request and cancels the message if it is not yet delivered
        """
        cancel_result = self.server_cancel_result(P.message_id.value)
        R = CancelSmResp()
        R.sequence_number = Integer(P.sequence_number.value, 4)
        if(cancel_result is False):
            R.command_status = Integer(command_status.ESME_RCANCELFAIL, 4)
        data = R.encode()
        self.socket.sendall(data)

    def cancel_sms_response(self, P):
        command_state = P.command_status.value

    def replace_sms(self, message_id, message):
        """
        This method is responsible for requesting the replacing of particular short message.
        """
        if not self._can_do('submit_sm'):
            raise InvalidSessionState("SMPP Session not in a state that allows replacing SMSes")

        P = ReplaceSm()
        P.message_id = CString(str(message_id))
        P.sequence_number = Integer(self._next_seq_num(), 4)
        P.short_message = CString(message)
        self.responses.update({P.sequence_number.value: P})
        self.socket.sendall(P.encode())

    def process_replace_sms(self, P):
        """
        This method is responsible for handling replacing request and replace short message if it is not
        yet delivered.
        """
        replace_sms = self.server_replace_result(P.message_id.value, P.short_message.value)
        R = ReplaceSmResp()
        R.sequence_number = Integer(P.sequence_number.value, 4)
        if(replace_sms is False):
            R.command_status = Integer(command_status.ESME_RREPLACEFAIL, 4)
        data = R.encode()
        self.socket.sendall(data)

    def replace_sms_response(self, P):
        command_state = P.command_status.value

    def handle_unbind(self, P):
        """
        Used by the server to handle the incoming unbind request
        """
        if self.state in [SessionState.BOUND_TX, SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            self.state = SessionState.UNBOUND
            R = UnBindResp()
            R.sequence_number = Integer(P.sequence_number.value, 4)
            data = R.encode()
            self.socket.sendall(data)


