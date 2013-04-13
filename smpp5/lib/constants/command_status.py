# Command Status - SMPP v5.0, section 4.7.6, table 4-45, page 116-122
# The command_status represents the means by which an ESME or MC sends an error code to its peer.
# This field is only relevant in response PDUs.

ESME_ROK = int(0x00000000)         # description : No error
ESME_RINVMSGLEN = int(0x00000001)  # description : Message Length is invalid
ESME_RINVCMDLEN = int(0x00000002)  # description : Command Length is invalid
ESME_RINVCMDID = int(0x00000003)  # description: Invalid Command ID
ESME_RINVBNDSTS = int(0x00000004)  # description: Incorrect BIND Status for given command
ESME_RALYBND = int(0x00000005)        # description: ESME Already in bound state
ESME_RINVPRTFLG = int(0x00000006)     # description: Invalid priority flag
ESME_RINVREGDLVFLG = int(0x00000007)  # description: Invalid registered delivery flag
ESME_RSYSERR = int(0x00000008)  # description: System Error
ESME_RINVSRCADR = int(0x0000000A)  # description: Invalid source address
ESME_RINVDSTADR = int(0x0000000B)  # description: Invalid destination address
ESME_RINVMSGID = int(0x0000000C)  # description: Message ID is invalid
ESME_RBINDFAIL = int(0x0000000D)  # description: Bind failed
ESME_RINVPASWD = int(0x0000000E)  # description: Invalid password
ESME_RINVSYSID = int(0x0000000F)  # description: Invalid System ID
ESME_RCANCELFAIL = int(0x00000011)  # description: Cancel SM Failed
ESME_RREPLACEFAIL = int(0x00000013)  # description: Replace SM Failed
ESME_RMSGQFUL = int(0x00000014)  # description: Message queue full
ESME_RINVSERTYP = int(0x00000015)  # description: Invalid service type
ESME_RINVNUMDESTS = int(0x00000033)  # description: Invalid number of destinations
ESME_RINVDLNAME = int(0x00000034)  # description: Invalid distribution list name
ESME_RINVDESTFLAG = int(0x00000040)  # description: Destination flag is invalid (submit_multi)
ESME_RINVSUBREP = int(0x00000042)  # description: Invalid submit with replace request (i.e. submit_sm with replace_if_present_flag set)
ESME_RINVESMCLASS = int(0x00000043)  # description: Invalid esm_class field data
ESME_RCNTSUBDL = int(0x00000044)  # description: Cannot submit to distribution list
ESME_RSUBMITFAIL = int(0x00000045)  # description: submit_sm or submit_multi failed
ESME_RINVSRCTON = int(0x00000048)  # description: Invalid source address TON
ESME_RINVSRCNPI = int(0x00000049)  # description: Invalid source address NPI
ESME_RINVDSTTON = int(0x00000050)  # description: Invalid destination address TON
ESME_RINVDSTNPI = int(0x00000051)  # description: Invalid destination address NPI
ESME_RINVSYSTYP = int(0x00000053)  # description: Invalid system_type field
ESME_RINVREPFLAG = int(0x00000054)  # description: Invalid replace_if_present flag
ESME_RINVNUMMSGS = int(0x00000055)  # description: Invalid number of messages
ESME_RTHROTTLED = int(0x00000058)  # description: Throttling error (ESME has exceeded allowed message limits)
ESME_RINVSCHED = iint(nt(0x00000061)  # description: Invalid scheduled delivery time
ESME_RINVEXPIRY = int(0x00000062)  # description: Invalid message validity period (expiry time)
ESME_RINVDFTMSGID = int(0x00000063)  # description: Predefined message invalid or not found
ESME_RX_T_APPN = int(0x00000064)  # description: ESME Receiver Temporary App Error Code
ESME_RX_P_APPN = int(0x00000065)  # description: ESME Receiver Permanent App Error Code
ESME_RX_R_APPN = int(0x00000066)  # description: ESME Receiver Reject Message Error Code
ESME_RQUERYFAIL = int(0x00000067)  # description: query_sm request failed
ESME_RINVOPTPARSTREAM = int(0x000000C0)  # description: Error in the optional part of the PDU Body
ESME_ROPTPARNOTALLWD = int(0x000000C1)  # description: TLV not allowed
ESME_RINVPARLEN = int(0x000000C2)  # description: Invalid parameter length
ESME_RMISSINGOPTPARAM = int(0x000000C3)  # description: Expected TLV missing
ESME_RINVOPTPARAMVAL = int(0x000000C4)  # description: Invalid TLV Value
ESME_RDELIVERYFAILURE = int(0x000000FE)  # description: Transaction Delivery Failure (used for data_sm_resp)
ESME_RUNKNOWNERR = int(0x000000FF)  # description: Unknown error
ESME_RSERTYPUNAUTH = int(0x00000100)  # description: ESME Not authorised to use specified service_type
ESME_RPROHIBITED = int(0x00000101)  # description: ESME prohibited from using specified operation
ESME_RSERTYPUNAVAIL = int(0x00000102)  # description : Specified service_type is unavailable.
ESME_RSERTYPDENIED = int(0x00000103)  # description : Specified service_type is denied.
ESME_RINVDCS = int(0x00000104)  # description : Invalid Data Coding Scheme.
ESME_RINVSRCADDRSUBUNIT = int(0x00000105)  # description : Source Address Sub unit is Invalid.
ESME_RINVDSTADDRSUBUNIT = int(0x00000106)  # description : Destination Address Sub unit is Invalid
ESME_RINVBCASTFREQINT = int(0x00000107)  # description : Broadcast Frequency Interval is invalid.
ESME_RINVBCASTALIAS_NAME = int(0x00000108)  # description : Broadcast Alias Name is invalid.
ESME_RINVBCASTAREAFMT = int(0x00000109)  # description : Broadcast Area Format is invalid.
ESME_RINVNUMBCAST_AREAS = int(0x0000010A)  # description : Number of Broadcast Areas is invalid.
ESME_RINVBCASTCNTTYPE = int(0x0000010B)  # description : Broadcast Content Type is invalid. 
ESME_RINVBCASTMSGCLASS = int(0x0000010C)  # description : Broadcast Message Class is invalid.
ESME_RBCASTFAIL = int(0x0000010D)  # description : broadcast_sm operation failed. 
ESME_RBCASTQUERYFAIL = int(0x0000010E)  # description : query_broadcast_sm operation failed.
ESME_RBCASTCANCELFAIL = int(0x0000010F)  # description : cancel_broadcast_sm operation failed.
ESME_RINVBCAST_REP = int(0x00000110)  # description : Number of Repeated Broadcasts is invalid.
ESME_RINVBCASTSRVGRP = int(0x00000111)  # description : Broadcast Service Group is invalid. 
ESME_RINVBCASTCHANIND = int(0x00000112)  # description : Broadcast Channel Indicator is invalid.
