from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON, esm_class, command_ids, command_status, tlv_tag

'''Session Management Operations
These operations are used to establish and maintain a SMPP session.

Bind Operation
The purpose of the SMPP bind operation is to register an instance of an ESME with the MC
system and request a SMPP session over this network connection for the submission or
delivery of messages. Thus, the Bind operation may be viewed as a form of MC login request
to authenticate the ESME entity wishing to establish a connection.

An ESME may bind to the MC as a Transmitter (called ESME
Transmitter), a Receiver (called ESME Receiver), or a Transceiver (called ESME
Transceiver). There are three SMPP bind PDUs to support the various modes of operation,
namely bind_transmitter, bind_transceiver and bind_receiver. The command_id field setting
specifies which PDU is being used.'''


class BindTransmitter(PDU):
    "Bind Transmitter PDU type"

    command_id = Integer(command_ids.bind_transmitter, 4)
    system_id = CString("")        # Identifies the ESME system requesting to bind as a transmitter with the MC.
    password = CString("")         # The password may be used by the MC to authenticate the ESME requesting to bind.
    system_type = CString("")      # Identifies the type of ESME system requesting to bind as a transmitter with the MC.
    interface_version = Integer(IV.SMPP_VERSION_5, 1)  # Indicates the version of the SMPP protocol supported by the ESME.
    addr_ton = Integer(TON.INTERNATIONAL, 1)  # Indicates Type of Number of the ESME address. If not known set to NULL.
    addr_npi = Integer(NPI.ISDN, 1)  # Numbering Plan Indicator for ESME address. If not known set to NULL.
    address_range = CString('')      # A single ESME address or a range of ESME addresses served via this SMPP transmitter session.Set to NULL if not known.


class BindTransmitterResp(PDU):
    "The SMPP bind_transmitter_resp PDU is used to reply to a bind_transmitter request"

    command_id = Integer(command_ids.bind_transmitter_resp, 4)
    system_id = CString("")         # Message Center(MC) identifier.Identifies the MC to the ESME.
    sc_interface_version = Integer(IV.SMPP_VERSION_5, 1)  # sc_interface_version


class BindReceiver(PDU):
    "SMPP bind_receiver PDU type"

    command_id = Integer(command_ids.bind_receiver, 4)
    system_id = CString("")         # Identifies the ESME system requesting to bind as a receiver with the MC.
    password = CString("")          # The password may be used by the MC for security reasons to authenticate the ESME requesting to bind.
    system_type = CString("")       # Identifies the type of ESME system requesting to bind as a receiver with the MC
    interface_version = Integer(IV.SMPP_VERSION_5, 1) # Identifies the version of the SMPP protocol supported by the ESME.
    addr_ton = Integer(TON.INTERNATIONAL, 1) # Type of Number (TON) for ESME address(es) served via this SMPP receiver session.Set to NULL if not known.
    addr_npi = Integer(NPI.ISDN, 1) # Numbering Plan Indicator (NPI) for ESME address(es) served via this SMPP receiver session.Set to NULL if not known.   
    address_range = CString('')     # A single ESME address or a range of ESME addresses served via this SMPP receiver session.Set to NULL if not known.


class BindReceiverResp(PDU):
    "SMPP bind_receiver_resp PDU type"

    command_id = Integer(command_ids.bind_receiver_resp, 4)
    system_id = CString("")         # Message Center(MC) identifier.Identifies the MC to the ESME.
    sc_interface_version = Integer(IV.SMPP_VERSION_5, 1) # SMPP version supported by MC


class BindTransceiver(PDU):
    "SMPP bind_transceiver PDU type"

    command_id = Integer(command_ids.bind_transceiver, 4)
    system_id = CString("")         # Identifies the ESME system requesting to bind as a transceiver with the MC.
    password = CString("")          # The password may be used by the MC to authenticate the ESME requesting to bind.
    system_type = CString("")       # Identifies the type of ESME system requesting to bind as a transceiver with the MC.
    interface_version = Integer(IV.SMPP_VERSION_5, 1) # Identifies the version of the SMPP protocol supported by the ESME.
    addr_ton = Integer(TON.INTERNATIONAL, 1)  # Type of Number (TON) for ESME address(es) served via this SMPP transceiver session. Set to NULL (Unknown) if not known.
    addr_npi = Integer(NPI.ISDN, 1) # Numbering Plan Indicator (NPI) for ESME address(es) served via this SMPP transceiver session. Set to NULL (Unknown) if not known.
    address_range = CString('')     # A single ESME address or a range of ESME addresses served via this SMPP transceiver session. Set to NULL if not known.


class BindTransceiverResp(PDU):
    "SMPP bind_transceiver_resp type"

    command_id = Integer(command_ids.bind_transceiver_resp, 4)
    system_id = CString("")         # MC identifier. Identifies the MC to the ESME.
    interface_version = Integer(IV.SMPP_VERSION_5, 1) # Identifies the version of the SMPP protocol supported by the ESME.


class OutBind(PDU):
    '''SMPP outbind PDU type
    This operation is used by the MC to signal an ESME to originate a outbind request to the MC.'''

    command_id = Integer(command_ids.outbind, 4)
    system_id = CString("")         # MC identifier. Identifies the MC to the ESME.
    password = CString("")          # The password may be used by the ESME for security reasons to authenticate the MC originating the outbind.


class UnBind(PDU):
    '''SMPP unbind PDU type
    The purpose of the SMPP unbind operation is to deregister an instance of an ESME from the MC 
    and inform the MC that the ESME no longer wishes to use this network connection for
    the submission or delivery of messages.
    Thus, the unbind operation may be viewed as a form of MC logoff request to close the
    current SMPP session.'''

    command_id = Integer(command_ids.unbind, 4)


class UnBindResp(PDU):
    '''SMPP unbind_resp PDU type
    The SMPP unbind_resp PDU is used to reply to an unbind request. It comprises the SMPP
    message header only.'''

    command_id = Integer(command_ids.unbind_resp, 4)

'''Enquire Link Operation
This PDU can be originated by either the ESME or MC and is used to provide a confidencecheck
of the communication path between an ESME and a MC. On receipt of this request the
receiving party should respond with an enquire_link_resp, thus verifying that the application
level connection between the MC and the ESME is functioning. The ESME may also respond
by sending any valid SMPP primitive.'''


class EnquireLink(PDU):
    '''This PDU can be originated by either the ESME or MC and is used to provide a confidencecheck
    of the communication path between an ESME and a MC.'''

    command_id = Integer(command_ids.enquire_link, 4)


class EnquireLinkResp(PDU):
    '''The enquire_link_resp PDU is used to reply to an enquire_link request.'''

    command_id = Integer(command_ids.enquire_link_resp, 4)

'''Alert Notification Operation
The alert_notification PDU is sent by the MC to the ESME across a Receiver or Transceiver
session. It is sent when the MC has detected that a particular mobile subscriber has become
available and a delivery pending flag had been previously set for that subscriber by means of
the set_dpf TLV(ref. 4.8.4.52).

A typical use of this operation is to trigger a data content ‘Push’ to the subscriber from a WAP
Proxy Server.
Note: There is no associated alert_notification_resp PDU.'''


class AlertNotification(PDU):
    '''SMPP alert_notification PDU type'''

    command_id = Integer(command_ids.alert_notification, 4)
    source_addr_ton = Integer(0, 1)  # Type of Number for alert SME.
    source_addr_npi = Integer(0, 1)  # Numbering Plan Indicator for alert SME.
    source_addr = CString("")        # Address of alert SME.
    esme_addr_ton = Integer(0, 1)    # Type of Number for ESME address which requested the alert
    esme_addr_npi = Integer(0, 1)    # Numbering Plan Indicator for ESME address which requested the alert
    esme_addr = CString("")          # Address for ESME which requested the alert
    ms_availability_status = TLV(tlv_tag.ms_availability_status, 0)  # The status of the mobile station

'''Generic NACK Operation
The generic_nack PDU is used to acknowledge the submission of an unrecognized or
corrupt PDU.'''


class GenericNack(PDU):
    "SMPP generic_nack PDU type"

    command_id = Integer(command_ids.generic_nack, 4)
