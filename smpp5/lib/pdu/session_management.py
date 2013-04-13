from smpp5.lib.parameter_types import Integer, CString, String, TLV
from smpp5.lib.pdu.pdu import PDU
from smpp5.lib.constants import interface_version as IV
from smpp5.lib.constants import NPI, TON


class BindTransmitter(PDU):
    "Bind Transmitter PDU type"

    command_id = Integer(2, 4)
    system_id = CString("")
    password = CString("")
    system_type = CString("")
    interface_version = Integer(IV.SMPP_VERSION_5, 1)
    addr_ton = Integer(TON.INTERNATIONAL, 1)
    addr_npi = Integer(NPI.ISDN, 1)
    address_range = CString('')

class bind_transmitter_resp(PDU):
    "The SMPP bind_transmitter_resp PDU is used to reply to a bind_transmitter request"
    
    command_id = Integer(2, 4)
    command_status = Integer(0, 4)  # Indicates status (success or error code) of original bind_transmitter request.
    sequence_number = Integer(0, 4) # Set to sequence number of original bind_transmitter request.
    system_id = CString("")         # Message Center(MC) identifier.Identifies the MC to the ESME.
    sc_interface_version = Integer(IV.SMPP_VERSION_5, 1) # sc_interface_version
    
class bind_receiver(PDU):
    "SMPP bind_receiver PDU type"
    
    command_id = Integer(2, 4)
    command_status = Integer(0, 4)  # Indicates status (success or error code) of original bind_transmitter request.
    sequence_number = Integer(0, 4) # Set to a unique sequence number. The associated bind_receiver_resp PDU will echo the same sequence number.
    system_id = CString("")         # Identifies the ESME system requesting to bind as a receiver with the MC.
    password = CString("")          # The password may be used by the MC for security reasons to authenticate the ESME requesting to bind.
    system_type = CString("")       # Identifies the type of ESME system requesting to bind as a receiver with the MC
    interface_version = Integer(IV.SMPP_VERSION_5, 1) # Identifies the version of the SMPP protocol supported by the ESME.
    addr_ton = Integer(TON.INTERNATIONAL, 1) # Type of Number (TON) for ESME address(es) served via this SMPP receiver session.Set to NULL if not known.
    addr_npi = Integer(NPI.ISDN, 1) # Numbering Plan Indicator (NPI) for ESME address(es) served via this SMPP receiver session.Set to NULL if not known.   
    address_range = CString('')     # A single ESME address or a range of ESME addresses served via this SMPP receiver session.Set to NULL if not known.
    
class bind_receiver_resp(PDU):
    "SMPP bind_receiver_resp PDU type"
    
    command_id = Integer(2, 4)
    command_status = Integer(0, 4)  # Indicates status (success or error code) of original bind_receiver request.
    sequence_number = Integer(0, 4) # Set to sequence number of original bind_receiver request.
    system_id = CString("")         # Message Center(MC) identifier.Identifies the MC to the ESME.
    sc_interface_version = Integer(IV.SMPP_VERSION_5, 1) # SMPP version supported by MC
    
class bind_transceiver(PDU):
    "SMPP bind_transceiver PDU type"
    
    command_id = Integer(9, 4)
    command_status = Integer(0, 4)  # Indicates status (success or error code) of original bind_receiver request.
    sequence_number = Integer(0, 4) # Set to a unique sequence number.The associated bind_transceiver_resp PDU will echo the same sequence number.
    system_id = CString("")         # Identifies the ESME system requesting to bind as a transceiver with the MC.
    password = CString("")          # The password may be used by the MC to authenticate the ESME requesting to bind.
    system_type = CString("")       # Identifies the type of ESME system requesting to bind as a transceiver with the MC.
    interface_version = Integer(IV.SMPP_VERSION_5, 1) # Identifies the version of the SMPP protocol supported by the ESME.
    addr_ton = Integer(TON.INTERNATIONAL, 1)  # Type of Number (TON) for ESME address(es) served via this SMPP transceiver session. Set to NULL (Unknown) if not known.
    addr_npi = Integer(NPI.ISDN, 1) # Numbering Plan Indicator (NPI) for ESME address(es) served via this SMPP transceiver session. Set to NULL (Unknown) if not known.
    address_range = CString('')     # A single ESME address or a range of ESME addresses served via this SMPP transceiver session. Set to NULL if not known.
    
class bind_transceiver_resp(PDU):
    "SMPP bind_transceiver_resp type"
    
    command_id = Integer(9, 4)
    command_status = Integer(0, 4)  # Indicates status (success or error code) of original bind_transceiver request.
    sequence_number = Integer(0, 4) # Set to sequence number of original bind_transceiver request.
    system_id = CString("")         # MC identifier. Identifies the MC to the ESME.
    interface_version = Integer(IV.SMPP_VERSION_5, 1) # Identifies the version of the SMPP protocol supported by the ESME.
    
class outbind(PDU):
    '''SMPP outbind PDU type
    This operation is used by the MC to signal an ESME to originate a outbind request to the MC.'''
    
    command_id = Integer(11, 4)
    command_status = Integer(0, 4)  
    sequence_number = Integer(0, 4) # Set to a unique sequence number.
    system_id = CString("")         # MC identifier. Identifies the MC to the ESME.
    password = CString("")          # The password may be used by the ESME for security reasons to authenticate the MC originating the outbind.
    
class unbind(PDU):
    '''SMPP unbind PDU type
    The purpose of the SMPP unbind operation is to deregister an instance of an ESME from the MC 
    and inform the MC that the ESME no longer wishes to use this network connection for
    the submission or delivery of messages.
    Thus, the unbind operation may be viewed as a form of MC logoff request to close the
    current SMPP session.'''

    command_id = Integer(6, 4)
    command_status = Integer(0, 4)  
    sequence_number = Integer(0, 4) # Set to a unique sequence number.The associated unbind_resp PDU will echo the same sequence number.
    
class unbind_resp(PDU):
    '''SMPP unbind_resp PDU type
    The SMPP unbind_resp PDU is used to reply to an unbind request. It comprises the SMPP
    message header only.'''
    
    command_id = Integer(6, 4)
    command_status = Integer(0, 4)  # Indicates outcome of original unbind request.
    sequence_number = Integer(0, 4) # Set to sequence number of original unbind request.
    
'''Enquire Link Operation
This PDU can be originated by either the ESME or MC and is used to provide a confidencecheck
of the communication path between an ESME and a MC. On receipt of this request the
receiving party should respond with an enquire_link_resp, thus verifying that the application
level connection between the MC and the ESME is functioning. The ESME may also respond
by sending any valid SMPP primitive.'''
    
class enquire_link(PDU):
    '''This PDU can be originated by either the ESME or MC and is used to provide a confidencecheck
    of the communication path between an ESME and a MC.'''
    
    command_id = Integer(15, 4)
    command_status = Integer(0, 4)  
    sequence_number = Integer(0, 4) # Set to a unique sequence number. The associated enquire_link_resp PDU should echo the same sequence number
    
class enquire_link_resp(PDU):
    '''The enquire_link_resp PDU is used to reply to an enquire_link request.'''
    
    command_id = Integer(15, 4)
    command_status = Integer(0, 4)  
    sequence_number = Integer(0, 4) # Set to the same sequence number of original enquire_link PDU
    
'''Alert Notification Operation
The alert_notification PDU is sent by the MC to the ESME across a Receiver or Transceiver
session. It is sent when the MC has detected that a particular mobile subscriber has become
available and a delivery pending flag had been previously set for that subscriber by means of
the set_dpf TLV(ref. 4.8.4.52).

A typical use of this operation is to trigger a data content ‘Push’ to the subscriber from a WAP
Proxy Server.
Note: There is no associated alert_notification_resp PDU.'''

class alert_notification(PDU):
    '''SMPP alert_notification PDU type'''
