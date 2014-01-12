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
import transaction
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
        'submit_multi': [SessionState.BOUND_TRX, SessionState.BOUND_TX],
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
        self.comp_pdus = {}
        self.unread_smses = []
        self.server_validate_method = ''
        self.server_db_store = ''
        self.server_query_result = ''
        self.server_cancel_result = ''
        self.server_replace_result = ''
        self.server_commit_db = ''
        self.sever_fetch_sms = ''
        self.user_id = None
        self.smses = {}

    def _can_do(self, action):
        
        "Validates if an action can be performed in current session state or not."
        
        if self.state in self.allowed_actions[action]:
            return True
        else:
            return False

    def _next_seq_num(self):
        """
        This method is responsible to return sequence number
        """

        self._seq_num += 1
        return self._seq_num

    def process_request(self):
        """
        Server background thread uses this method to receive requests or response pdus sent by client over the socket.
        """

        while self.socket.is_open is True:
            P = self.socket.get_pdu_from_socket()
            if P is not None:
                # If command id sent by client is that of deliever sms response pass it.
                if(P.command_id.value == command_ids.deliver_sm_resp):
                    pass
                else:
                    # Updates the dictionary and add request pdu sent by the client and it works like a queue.
                    self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})

    def handle_pdu(self):
        """
        This method check for client request and calls appropriate methods to handle it.
        """

        isempty = (self.pdus and True) or False
        if isempty is not False:
            seq_no, pdu = self.pdus.popitem()
            if pdu['resp'] == '':
                P = pdu['req']
                if(command_ids.bind_transmitter == P.command_id.value):
                    self.handle_bind(P)
                elif(command_ids.bind_receiver == P.command_id.value):
                    self.handle_bind(P)
                elif(command_ids.bind_transceiver == P.command_id.value):
                    self.handle_bind(P)
                elif command_ids.submit_sm == P.command_id.value:
                    self.process_sms(P)
                elif command_ids.submit_multi == P.command_id.value:
                    self.process_multiple_sms(P)
                elif(command_ids.query_sm == P.command_id.value):
                    self.process_query(P)
                elif(command_ids.cancel_sm == P.command_id.value):
                    self.process_sms_cancelling(P)
                elif(command_ids.replace_sm == P.command_id.value):
                    self.process_replace_sms(P)
                elif(command_ids.enquire_link == P.command_id.value):
                    self.enquire_link_response(P)
                elif(command_ids.unbind == P.command_id.value):
                    self.handle_unbind(P)
                else:
                    R = GenericNack()
                    R.sequence_number = Integer(P.sequence_number.value, 4)
                    R.command_status = Integer(command_status.ESME_RINVCMDID, 4)
                    self.socket.send(R.encode())

    def storing_recieved_pdus(self):
        '''
        Client background thread uses this method to recieve response/request PDU's and storing them in dictionary.
        '''
        while self.socket.is_open is True:
            R = self.socket.get_pdu_from_socket()
            if(R is not None):
                if R.command_id.value == command_ids.deliver_sm:
                    self.deliver_sms_response(R)
                elif(self.pdus[R.sequence_number.value]):
                    self.comp_pdus[R.sequence_number.value] = self.pdus[R.sequence_number.value]
                    self.comp_pdus[R.sequence_number.value]['resp'] = R

    def processing_recieved_pdus(self):
        """
        Client use this method to process pdus responses by calling appropriate method.
        """
        isempty = (self.comp_pdus and True) or False
        if isempty is not False:
            seq_no, pdu = self.comp_pdus.popitem()  # first element from dictionary has been popped up and deleted from dict.
            if pdu['resp'] != '':
                R = pdu['resp']
                if(command_ids.generic_nack == R.command_id.value):
                    if(command_status.ESME_RINVCMDID == R.command_status.value):
                        print("You have sent invalid PDU which is not recognized by SMSC. ")
                if(self.state == SessionState.OPEN):
                    if(command_ids.bind_transmitter_resp == R.command_id.value):
                        self.binding_response_handling(R)
                    elif(command_ids.bind_receiver_resp == R.command_id.value):
                        self.binding_response_handling(R)
                    elif(command_ids.bind_transceiver_resp == R.command_id.value):
                        self.binding_response_handling(R)
                else:
                    if(command_ids.submit_sm_resp == R.command_id.value):
                        self.send_sms_response(R)
                    elif(command_ids.submit_multi_resp == R.command_id.value):
                        self.send_multiple_sms_response(R)
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
                    elif(command_ids.unbind_resp == R.command_id.value):
                        self.unbind_response(R)
            pdu['read'] = 'true'

    def notifications_4_client(self):
        """
        This method is used by client to view that either there are pending notifications or not..
        """
        notification = 0
        for seq_no in self.pdus:
            if self.pdus[seq_no]['read'] == 'false' and self.pdus[seq_no]['resp'] != '':
                notification = notification+1
        return notification

    def bind(self, bind_type, system_id, password, system_type):
        """
        Used by the client to bind TX, RX or TRX with the server
        """

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

    def handle_bind(self, P):
        """
        Used by the server to handle the incoming bind request
        """

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
                print("  Logged in Client is :   " + self.user_id)
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

    def enquire_link(self):
        """
        This method is used by client to ensure the connectivity with server.
        """
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
            print("Connection with server exists.")
        else:
            print("Connection with server not exists")

    def send_sms(self, recipient, message, sender):
        """
        This method is responsible for taking the Sumbit short message request send by client and writes it to
        the socket to be read by server.
        """
        try:
            if not self._can_do('submit_sm'):
                raise InvalidSessionState("SMPP Session not in a state that allows sending SMSes.")
            msg_length = int(len(message))
            P = SubmitSm()
            P.sequence_number = Integer(self._next_seq_num(), 4)
            if sender:
                P.source_addr = CString(sender)
            P.destination_addr = CString(recipient)
            P.schedule_delivery_time = CString("")
            P.validity_period = CString("")
            P.sm_default_msg_id = Integer(0, 1)
            if(msg_length < 255):
                P.sm_length = Integer(msg_length, 1)
                P.short_message = CString(str(message))
            else:
                P.message_payload = TLV(tlv_tag.message_payload, message)
            data = P.encode()
        #storing pdu in dictionary named responses
            self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})
            self.socket.send(data)
        except InvalidSessionState as e:
            print(e.value)

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
                db_storage = self.server_db_store(P.destination_addr.value, message, self.user_id, P.source_addr.value)
            # in db_storage the message id of sms is returned
                R.message_id = CString(str(db_storage))
        else:
            R = SubmitSmResp()
            R.sequence_number = Integer(P.sequence_number.value, 4)
            R.command_status = Integer(command_status.ESME_RINVBNDSTS, 4)
        data = R.encode()
        self.socket.send(data)

    def send_sms_response(self, P):
        """
        This method is responsible to process submit sm response send by server...
        """
        if(P.command_status.value == 0):
            message_id = P.message_id.value.decode(encoding='ascii')
            print("Message having message id " + str(message_id) + " has been scheduled for sending.")
        elif(P.command_status.value == command_status.ESME_RINVMSGLEN):
            print("Sorry message having message id " + str(message_id) + "cannot be send due to invalid message length.")
        elif(P.command_status.value == command_status.ESME_RINVBNDSTS):
            print("Sorry message cannot be send because Sending Sms is not allowed in this session state.")

    def send_multiple_sms(self, recipient, message, sender, total_recipient):
        """
        This method is responsible for taking the Sumbit short message request send by client and writes it to
        the socket to be read by server.
        """
        try:
            if not self._can_do('submit_multi'):
                raise InvalidSessionState("SMPP Session not in a state that allows sending SMSes.")
            msg_length = int(len(message))
            P = SubmitMulti()
            P.sequence_number = Integer(self._next_seq_num(), 4)
            if sender:
                P.source_addr = CString(sender)
            P.number_of_dests = Integer(total_recipient, 1)
            P.destination_addr = CString(recipient)
            P.schedule_delivery_time = CString("")
            P.validity_period = CString("")
            P.sm_default_msg_id = Integer(0, 1)
            if(msg_length < 255):
                P.sm_length = Integer(msg_length, 1)
                P.short_message = CString(str(message))
            else:
                P.message_payload = TLV(tlv_tag.message_payload, message)
            data = P.encode()
        #storing pdu in dictionary named responses
            self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})
            self.socket.send(data)
        except InvalidSessionState as e:
            print(e.value)

    def process_multiple_sms(self, P):
        """
        This method is responsible for handling the request sent by client and sending the response pdu to the client
        for successfull submission
        """
        if self.state in [SessionState.BOUND_TX, SessionState.BOUND_TRX]:
            R = SubmitMultiResp()
            R.sequence_number = Integer(P.sequence_number.value, 4)
            if(P.sm_length.value > 255):
                R.command_status = Integer(command_status.ESME_RINVMSGLEN, 4)
            else:
                if(P.short_message.value):
                    message = P.short_message.value.decode(encoding='ascii')
                else:
                    message = P.message_payload.value.value
                db_storage = self.server_db_store(P.destination_addr.value, message, self.user_id, P.source_addr.value)
            # in db_storage the message id of sms is returned
                R.message_id = CString(str(db_storage))
        else:
            R = SubmitSmResp()
            R.sequence_number = Integer(P.sequence_number.value, 4)
            R.command_status = Integer(command_status.ESME_RINVBNDSTS, 4)
        data = R.encode()
        self.socket.send(data)

    def send_multiple_sms_response(self, P):
        if(P.command_status.value == 0):
            message_id = P.message_id.value
            message_ids = P.message_id.value.decode(encoding='ascii').splitlines()
            for i in range(len(message_ids)):
                print("Message having message id " + str(message_ids[i]) + " has been scheduled for sending.")
        elif(P.command_status.value == command_status.ESME_RINVMSGLEN):
            print("Sorry message having message id " + str(message_id) + "cannot be send due to invalid message length.")
        elif(P.command_status.value == command_status.ESME_RINVBNDSTS):
            print("Sorry message cannot be send because Sending Sms is not allowed in this session state.")

    def query_status(self, message_id):
        """
        This method is responsible for querying the status of message that either it is delievered or still
        scheduled
        """
        try:
            if not self._can_do('query_sm'):
                raise InvalidSessionState("SMPP Session not in a state that allows querying SMSes.")

            P = QuerySm()
            P.sequence_number = Integer(self._next_seq_num(), 4)
            P.message_id = CString(str(message_id))
            self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})
            data = P.encode()
            self.socket.send(data)
        except InvalidSessionState as e:
            print(e.value)

    def process_query(self, P):
        """
        This message is responsible for handling querying request and returning status of message
        """
        R = QuerySmResp()
        R.sequence_number = Integer(P.sequence_number.value, 4)
        query_result = self.server_query_result(P.message_id.value, self.user_id)
        R.message_id = CString(P.message_id.value)
        if(query_result == command_status.ESME_RINVMSGID):
            R.command_status = Integer(command_status.ESME_RINVMSGID, 4)
        else:
            R.final_date = CString(str(query_result['final_date']))
            R.message_state = Integer(query_result['state'], 1)
        data = R.encode()
        self.socket.send(data)

    def query_sms_response(self, P):
        """
        This method is responsible to process query sm response send by server...
        """
        if(P.command_status.value == 0):
            msg_state = P.message_state.value
            if(msg_state == message_state.SCHEDULED):
                print("Message having message id " + str(P.message_id.value) + " is secheduled and ready to deliever")
            elif(msg_state == message_state.DELIVERED):
                print("Message having message id " + str(P.message_id.value) + " has been delievered to destination")
            elif(msg_state == message_state.EXPIRED):
                print("Sorry,message having message id " + str(P.message_id.value) + "validity period has been expired")
        elif(P.command_status.value == command_status.ESME_RINVMSGID):
            print("Message having message id " + str(P.message_id.value) + " cannot be quered because provided message id is invalid")

    def cancel_sms(self, message_id):
        """
        This method is responsible for requesting the cancelling of particular message
        """
        try:
            if not self._can_do('query_sm'):
                raise InvalidSessionState("SMPP Session not in a state that allows cancelling SMSes")

            P = CancelSm()
            P.sequence_number = Integer(self._next_seq_num(), 4)
            P.message_id = CString(str(message_id))
            source_addr = CString(str(self.user_id))
            destination_addr = CString("")
            self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})
            self.socket.send(P.encode())
        except InvalidSessionState as e:
            print(e.value)

    def process_sms_cancelling(self, P):
        """
        This method is responsible for handling cancel request and cancels the message if it is not yet delivered
        """
        cancel_result = self.server_cancel_result(P.message_id.value, self.user_id)
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
        except InvalidSessionState as e:
            print(e.value)

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
            replace_sms = self.server_replace_result(P.message_id.value, P.short_message.value, self.user_id)
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

    def deliver_sms(self):
        """
        This method is used by server to deliver the incoming smses if any to currently logged in client.
        """

        try:
            # Checks if action is not allowed in current bind state.
            if not self._can_do('deliver_sm'):
                raise InvalidSessionState("Oops! Client has terminated the connection.")
        except InvalidSessionState as e:
            print(e.value)
            
        # Pass currently logged-in user id to to fetch incoming sms method in server which checks the database for incoming smses
        # and return them here.
        sms = self.sever_fetch_sms(self.user_id)  
        if(sms is None):  # If there are no incoming smses for the client pass
            pass
        else:  # If there are incoming smses for the client
            msg_length = int(len(sms.msg))  # Take the message length and convert it into integer.
            P = DeliverSm()  # Make the class instance.
            
            # Set the class fields to compose the pdu.
            P.sequence_number = Integer(self._next_seq_num(), 4)  # Set the sequence number of the pdu.
            P.source_addr = CString(str(sms.sms_from))  # Server address
            P.destination_addr = CString(str(sms.sms_to))  # Client address
            P.schedule_delivery_time = CString(str(sms.schedule_delivery_time))  # By default its current time.
            P.validity_period = CString("")  # By default its 1 day
            if(msg_length < 5000):
                P.sm_length = Integer(msg_length, 1)  # Convert length into integer which is the desired type
                P.short_message = CString(str(sms.msg))  # Convert message body to string and then to Cstring format
            else:
                P.message_payload = TLV(tlv_tag.message_payload, message)
            data = P.encode()  # Encode the pdu
            self.socket.send(data)  # Send the pdu to the socket.
            # Call gets back to deliver sms method in server.

    def deliver_sms_response(self, P):
        """
        This method is used by client to ensure the recieving of delivered message by sending response to server.
        """

        R = DeliverSmResp()
        R.sequence_number = Integer(P.sequence_number.value, 4)
        data = R.encode()
        self.smses.update({P.sequence_number.value: {'pdu': P, 'read': 'false'}})
        self.socket.send(data)

    def view_smses(self):
        """
        This method is used by client to view all unread smses delivered by server.
        """

        if self.state in [SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            isempty = (self.smses and True) or False
            if isempty is False:
                print("Sorry, No Unread Smses For You........")
            else:
                while isempty is True:
                    seq_no, pdu = self.smses.popitem()
                    P = pdu['pdu']
                    print("******* SMSES DELIVERY*********** ")
                    print("** Sms From :" + str(P.source_addr.value))
                    print("   Sms      :" + str(P.short_message.value))
                    isempty = (self.smses and True) or False
        else:
            print("SMPP Session not in a state that allows you to view SMSes")

    def unbind(self):
        """
        This method is used by client to send Unbind request to server....
        """

        if self.state in [SessionState.BOUND_TX, SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            P = UnBind()
            P.sequence_number = Integer(self._next_seq_num(), 4)
            self.pdus.update({P.sequence_number.value: {'req': P, 'resp': '', 'read': 'false'}})
            self.socket.send(P.encode())

    def handle_unbind(self, P):
        """
        Used by the server to handle the incoming unbind request and ensure unbinding.
        """

        if self.state in [SessionState.BOUND_TX, SessionState.BOUND_RX, SessionState.BOUND_TRX]:
            self.state = SessionState.UNBOUND
            R = UnBindResp()
            R.sequence_number = Integer(P.sequence_number.value, 4)
            data = R.encode()
            self.socket.send(data)

    def unbind_response(self, R):
        """
        This method is used by client to perform action based on response of unbind request.
        """

        self.state = SessionState.UNBOUND

