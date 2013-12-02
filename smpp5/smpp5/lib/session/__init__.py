"""
SMPP Session Implementation
===========================

SMPPSession class is used to handle SMPP Sessions between client and server, both client and
server create an instance of SMPPSession to communicate with each other.

"""
import sys
import socket
import time
import datetime
from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.constants import *
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag, message_state
from smpp5.lib.constants.command_status import *
from smpp5.lib.pdu import command_mappings
from smpp5.lib.pdu.pdu import PDU
from smpp5.lib.session.shared_connection import SharedConnection
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
from smpp5.lib.pdu.anciliary_submission import (
    QuerySm,
    QuerySmResp,
    CancelSm,
    CancelSmResp,
    ReplaceSm,
    ReplaceSmResp)
from smpp5.lib.pdu.message_delivery import (
    DeliverSm,
    DeliverSmResp)


class InvalidSessionState(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


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
        self._msg_id = 0
        self.pdus = {}
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

    #def get_pdu_from_socket(self):
    #    """
    #    Given a socket, returns a completed PDU and blocks until a PDU is received
    #
    #    For non-blocking sockets see:
    #
    #    * http://docs.python.org/2/howto/sockets.html#non-blocking-sockets
    #    * http://stackoverflow.com/questions/2719017/how-to-set-timeout-on-pythons-socket-recv-method
    #    * http://docs.python.org/2/library/select.html#select.select
    #    """
    #    #First wait till 4 bytes a read from the socket (command_length)
    #    d = self.socket.recv(4, socket.MSG_WAITALL)
    #    command_length = Integer.decode(d)  # decode first four bytes to get the command length via it
    #
    #    # get bytes specified by command_length - 4
    #    sock_data = self.socket.recv(command_length.value - 4, socket.MSG_WAITALL)
    #    sock_data = d + sock_data
    #
    #    command_id = Integer.decode(sock_data[4:8])    # decode from 5th byte till 8th to get command_id
    #    PDUClass = command_mappings[command_id.value]  # get the class name via command_id
    #
    #    # decode PDU
    #    P = PDUClass.decode(sock_data)
    #
    #    return P

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
        elif(command_ids.enquire_link == P.command_id.value):
            self.enquire_link_response(P)
        else:
            R = GenericNack()
            R.sequence_number = Integer(P.sequence_number.value, 4)
            R.command_status = Integer(command_status.ESME_RINVCMDID, 4)
            self.socket.send(R.encode())

    def close(self):
        P = self.socket.get_pdu_from_socket()
        if P is not None:
            if self.state in [SessionState.BOUND_TX, SessionState.BOUND_TRX]:
                while P.command_id.value != command_ids.unbind:
                    self.handle_pdu(P)
                    P = self.socket.get_pdu_from_socket()
            self.handle_unbind(P)

    def storing_recieved_pdus(self):
        '''
        Client background thread use this method to recieve response PDU's and storing them in dictionary.
        '''
        while True:
            R = self.socket.get_pdu_from_socket()
            if(R is not None):
                print(R)
                if(self.pdus[R.sequence_number.value]):
                    self.pdus[R.sequence_number.value]['resp'] = R
                    time.sleep(1)

    def processing_recieved_pdus(self):
        """
        Client use this method to process pdus responses by calling appropriate method
        """
        for seq_no in self.pdus:
            if self.pdus[seq_no]['read'] == 'false' and self.pdus[seq_no]['resp'] != '':
                R = self.pdus[seq_no]['resp']
                if(command_ids.generic_nack == R.command_id.value):
                    if(command_status.ESME_RINVCMDID == R.command_status.value):
                        print("You have sent invalid PDU which is not recognized by SMSC ")
                elif(command_ids.bind_transmitter_resp == R.command_id.value):
                    self.binding_response_handling(R)
                elif(command_ids.bind_receiver_resp == R.command_id.value):
                    self.binding_response_handling(R)
                elif(command_ids.bind_transceiver_resp == R.command_id.value):
                    self.binding_response_handling(R)
                elif(command_ids.submit_sm_resp == R.command_id.value):
                    self.send_sms_response(R)
                elif(command_ids.query_sm_resp == R.command_id.value):
                    self.query_sms_response(R)
                elif(command_ids.replace_sm_resp == R.command_id.value):
                    self.replace_sms_response(R)
                elif(command_ids.cancel_sm_resp == R.command_id.value):
                    self.cancel_sms_response(R)
                elif(command_ids.unbind_resp == R.command_id.value):
                    self.state = SessionState.UNBOUND
                elif(command_ids.cancel_sm_resp == R.command_id.value):
                    self.cancel_sms_response(R)
                elif(command_ids.enquire_link_resp == R.command_id.value):
                    self.process_enquire_link_response(R)
            self.pdus[seq_no]['read'] = 'true'

    def notifications_4_client(self):
        """
        This method is used by client to view that either there are pending notifications or not..
        """
        notification = 0
        for seq_no in self.pdus:
            if self.pdus[seq_no]['read'] == 'false' and self.pdus[seq_no]['resp'] != '':
                notification = notification+1
        return notification

    def unbind(self):
        """
        This method is used by client to Unbind with the server....
        """
        if self.state in [SessionState.BOUND_TX, SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            P = UnBind()
            P.sequence_number = Integer(self._next_seq_num(), 4)
            self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})
            self.socket.send(P.encode())

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
        P.sequence_number = Integer(self._next_seq_num(), 4)
        P.system_id = CString(system_id)
        P.password = CString(password)
        P.system_type = CString(system_type)
        data = P.encode()
        self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})
        self.socket.send(data)
        # recieving the response from server
        #P = self.get_pdu_from_socket()

    def binding_response_handling(self, R):
        """
        This method is reaponsible to process bind transmitter or receiver or transceiver responses send by server...
        """
        if(R.command_status.value == 0):
            if(R.command_id.value == command_ids.bind_transmitter_resp):
                self.state = SessionState.BOUND_TX
            elif(R.command_id.value == command_ids.bind_receiver_resp):
                self.state = SessionState.BOUND_RX
            elif(R.command_id.value == command_ids.bind_transceiver_resp):
                self.state = SessionState.BOUND_TRX

    def handle_bind(self, validate):
        """
        Used by the server to handle the incoming bind request
        """
        #recieving bind pdu from client
        P = self.socket.get_pdu_from_socket()
        print(P)
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
                self.socket.send(data)
            else:
                self.validation_status = 'fail'
                R = GenericNack()
                R.sequence_number = Integer(P.sequence_number.value, 4)
                R.command_status = Integer(command_status.ESME_RBINDFAIL, 4)
                data = R.encode()
                self.socket.send(data)
        print("    Response pdu sent to client by server   ")
        print(P.system_id.value)
        print(P.password.value)
        print(P.system_type.value)

    def enquire_link(self):
            P = EnquireLink()
            P.sequence_number = Integer(self._next_seq_num(), 4)
            data = P.encode()
            self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})
            self.socket.send(data)

    def enquire_link_response(self, P):
        R = EnquireLinkResp()
        R.sequence_number = Integer(P.sequence_number.value, 4)
        data = R.encode()
        self.socket.send(data)

    def process_enquire_link_response(self, P):
        if (P):
            return True
        else:
            return False

    def send_sms(self, recipient, message):
        """
        This method is responsible for taking the Sumbit short message request send by client and writes it to
        the socket to be read by server.
        """
        try:
            if not self._can_do('submit_sm'):
                raise InvalidSessionState("SMPP Session not in a state that allows sending SMSes")
        except InvalidSessionState as e:
            print(e.value)

        msg_length = int(len(message))
        P = SubmitSm()
        P.sequence_number = Integer(self._next_seq_num(), 4)
        P.source_addr = CString(str(self.user_id))
        P.destination_addr = CString(recipient)
        P.schedule_delivery_time = CString("")
        P.validity_period = CString("")
        P.sm_default_msg_id = Integer(0, 1)
        if(msg_length < 255):
            P.sm_length = Integer(msg_length, 1)                # page 134
            P.short_message = CString(str(message))
        else:
            P.message_payload = TLV(tlv_tag.message_payload, message)
            print(P.message_payload.value.value)
        data = P.encode()
        #storing pdu in dictionary named responses
        self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})
        time.sleep(2)
        self.socket.send(data)

    def process_sms(self, P):
        """
        This method is responsible for handling the request sent by client and sending the response pdu to the client
        for successfull submission
        """
        if self.state in [SessionState.BOUND_TX, SessionState.BOUND_TRX]:
            R = SubmitSmResp()
            R.sequence_number = Integer(P.sequence_number.value, 4)
            if(P.sm_length.value > 255):
                R.command_status = Integer(command_status.ESME_RINVMSGLEN, 4)
            else:
                if(P.short_message.value):
                    message = P.short_message.value.decode(encoding='ascii')
                else:
                    message = P.message_payload.value.value
                db_storage = self.server_db_store(P.destination_addr.value, message, self.user_id)
            # in db_storage the message id of sms is returned
                R.message_id = CString(str(db_storage))
        else:
            R = SubmitSmResp()
            R.sequence_number = Integer(P.sequence_number.value, 4)
            R.command_status = Integer(command_status.ESME_RINVBNDSTS, 4)
        data = R.encode()
        time.sleep(2)
        self.socket.send(data)

    def send_sms_response(self, P):
        """
        This method is responsible to process submit sm response send by server...
        """
        if(P.command_status.value == 0):
            message_id = P.message_id.value
            print("Message having message id " + str(message_id) + "has been sent successfully")
        elif(P.command_status.value == command_status.ESME_RINVMSGLEN):
            print("Sorry message cannot be send due to invalid message length")
        elif(P.command_status.value == command_status.ESME_RINVBNDSTS):
            print("Sorry message cannot be send because Sending Sms is not allowed in this session state")

    def query_status(self, message_id):
        """
        This method is responsible for querying the status of message that either it is delievered or still
        scheduled
        """
        try:
            if not self._can_do('query_sm'):
                raise InvalidSessionState("SMPP Session not in a state that allows querying SMSes")
        except InvalidSessionState as e:
            print(e.value)

        P = QuerySm()
        P.sequence_number = Integer(self._next_seq_num(), 4)
        P.message_id = CString(str(message_id))
        self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})
        self.socket.send(P.encode())

    def process_query(self, P):
        """
        This message is responsible for handling querying request and returning status of message
        """
        R = QuerySmResp()
        R.sequence_number = Integer(P.sequence_number.value, 4)
        query_result = self.server_query_result(P.message_id.value)
        if(query_result == command_status.ESME_RINVMSGID):
            R.command_status = Integer(command_status.ESME_RINVMSGID, 4)
        else:
            R.message_id = CString(P.message_id.value)
            R.final_date = CString(str(query_result['final_date']))
            R.message_state = Integer(query_result['state'], 1)
            data = R.encode()
        self.socket.send(data)

    def query_sms_response(self, P):
        """
        This method is responsible to process query sm response send by server...
        """
        if(P.command_status == 0):
            message_state = P.message_state.value
            if(message_state == message_state.SCHEDULED):
                print("Message is secheduled and ready to delievered")
            elif(message_state.value == message_state.DELIVERED):
                print("Message has been delievered to destination")
            elif(message_state.value == message_state.EXPIRED):
                print("Sorry, message validity period has been expired")
        elif(P.command_status.value == command_status.ESME_RINVMSGID):
            print("Message cannot be quered because provided message id is invalid")

    def cancel_sms(self, message_id):
        """
        This method is responsible for requesting the cancelling of particular message
        """
        try:
            if not self._can_do('cancel_sm'):
                raise InvalidSessionState("SMPP Session not in a state that allows cancelling SMSes")
        except InvalidSessionState as e:
            print(e.value)

        P = CancelSm()
        P.sequence_number = Integer(self._next_seq_num(), 4)
        P.message_id = CString(str(message_id))
        source_addr = CString(str(self.user_id))
        destination_addr = CString("")
        self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})
        self.socket.send(P.encode())

    def process_sms_cancelling(self, P):
        """
        This method is responsible for handling cancel request and cancels the message if it is not yet delivered
        """
        cancel_result = self.server_cancel_result(P.message_id.value)
        R = CancelSmResp()
        R.sequence_number = Integer(P.sequence_number.value, 4)
        if(cancel_result is False):
            R.command_status = Integer(command_status.ESME_RINVMSGID, 4)
        elif(cancel_result is command_status.ESME_RCANCELFAIL):
            R.command_status = Integer(command_status.ESME_RCANCELFAIL, 4)
        data = R.encode()
        self.socket.send(data)

    def cancel_sms_response(self, P):
        """
        This method is responsible to process cancel sm response send by server...
        """
        if(P.command_status.value == 0):
            print("Message has been cancelled successfully...")
        elif(P.command_status.value == command_status.ESME_RINVMSGID):
            print("Message cannot be cancelled because provided message id is invalid")
        elif(P.command_status.value == command_status.ESME_RCANCELFAIL):
            print("Message cannot be cancelled because message has been already delievered")

    def replace_sms(self, message_id, message):
        """
        This method is responsible for requesting the replacing of particular short message.
        """
        try:
            if not self._can_do('replace_sm'):
                raise InvalidSessionState("SMPP Session not in a state that allows replacing SMSes")
        except InvalidSessionState as e:
            print(e.value)

        P = ReplaceSm()
        P.message_id = CString(str(message_id))
        P.sequence_number = Integer(self._next_seq_num(), 4)
        source_addr = CString(str(self.user_id))
        schedule_delivery_time = CString("")
        validity_period = CString("")
        sm_default_msg_id = Integer(0, 1)
        sm_length = Integer(len(message), 1)
        P.short_message = CString(message)
        self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})
        self.socket.send(P.encode())

    def process_replace_sms(self, P):
        """
        This method is responsible for handling replacing request and replace short message if it is not
        yet delivered.
        """
        R = ReplaceSmResp()
        R.sequence_number = Integer(P.sequence_number.value, 4)
        if(P.sm_length.value >= 255):
            R.command_status = Integer(command_status.ESME_RINVMSGLEN, 4)
        else:
            replace_sms = self.server_replace_result(P.message_id.value, P.short_message.value)
            if(replace_sms is False):
                R.command_status = Integer(command_status.ESME_RINVMSGID, 4)
            elif(replace_sms is command_status.ESME_RREPLACEFAIL):
                R.command_status = Integer(command_status.ESME_RREPLACEFAIL, 4)
        data = R.encode()
        self.socket.send(data)

    def replace_sms_response(self, P):
        """
        This method is responsible to process replace sm response send by server...
        """
        if(P.command_status.value == 0):
            print("Message has been replaced successfully...")
        elif(P.command_status.value == command_status.ESME_RINVMSGID):
            print("Message cannot be replaced because provided message id is invalid")
        elif(P.command_status.value == command_status.ESME_RREPLACEFAIL):
            print("Message cannot be replaced because message has been already delievered")

    def handle_unbind(self, P):
        """
        Used by the server to handle the incoming unbind request
        """
        if self.state in [SessionState.BOUND_TX, SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            self.state = SessionState.UNBOUND
            R = UnBindResp()
            R.sequence_number = Integer(P.sequence_number.value, 4)
            data = R.encode()
            self.socket.send(data)


