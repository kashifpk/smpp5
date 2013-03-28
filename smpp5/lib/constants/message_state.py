# Message_State - SMPP v5.0, section 4.7.15, table 4-50, page 127-128
"'The MC returns the message_state value to the ESME as part of the query_sm_resp or query_broadcast_sm_resp  PDU."'

    SCHEDULED       =0     # Type : Intermediate, Description: The message is scheduled. Delivery has not yet been initiated.
    ENROUTE         =1     # Type : Intermediate, Description: The message is in enroute state.
    DELIVERED       =2     # Type : Final       , Description: Message is delivered to destination
    EXPIRED         =3     # Type : Final       , Description: Message validity period has expired.
    DELETED         =4     # Type : Final       , Description: Message has been deleted. 
    UNDELIVERABLE   =5     # Type : Final       , Description: Message is undeliverable.
    ACCEPTED        =6     # Type : Final       , Description: Message is in accepted state (i.e. has been manually read on behalf of the subscriber by customer service) 
    UNKNOWN         =7     # Type : N/A         , Description: Message is in invalid state
    REJECTED        =8     # Type : Final       , Description: Message is in a rejected state
    SKIPPED         =9     # Type : Final       , Description: The message was accepted but not transmitted or broadcast on the network.
    



   
