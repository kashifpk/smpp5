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
    
    
