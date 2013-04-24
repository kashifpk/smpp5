# Interface_version - SMPP v5.0, section 4.7.13, table 4-49, page 126
# This parameter is used to indicate the version of the SMPP protocol

SMPP_VERSION_3_OR_OLDER = int(0x00)  # Indicates that the ESME supports version 3.3 or earlier of the SMPP protocol.
SMPP_VERSION_3_3 = int(0x33)         # Indicates that the ESME supports version 3.3 or earlier of the SMPP protocol.
SMPP_VERSION_3_4 = int(0x34)         # Indicates that the ESME is supporting SMPP version 3.4 
SMPP_VERSION_5 = int(0x50)           # Indicates that the ESME is supporting SMPP version 5.0 
