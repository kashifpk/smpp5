# Esm_class - SMPP v5.0, section 4.7.12, table 4-48, page 125
"'Esm_class is use to indicate special message attributes'"




    Default_mode               =00000000            #Default MC Mode (e.g. Store and Forward)
    Datagram_mode              =00000001
    Forward_mode               =00000010            #Forward (i.e. Transaction) mode
    Store_and_forward_mode     =00000011            #Use to select Store and Forward mode if Default MC Mode is non Store and Forward
    Default_message_type       =00000000            #Normal message
    Mc_delivery_receipt        =00000100            #Short Message contains MC Delivery Receipt 
    Delivery_notification      =00100000            #Short Message contains Intermediate Delivery Notification
    Delivery_acknowledgement   =00001000            #Short Message contains Delievery Acknowledgement
    User_acknowledgement       =00010000            #Short Message contains Manual/User Acknowledgement
    Conversation_abort         =00011000            #Short Message contains Conversation Abort (Korean CDMA)
    Feature_none               =00000000
    UDHI_indicator             =01000000
    Feature_reply_path         =10000000             #Set Reply Path (only relevant for GSM network) 
    UDHI_and_reply_path        =11000000             #Set UDHI and Reply Path (only relevant for GSM) 


   
