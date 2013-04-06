# -*- coding: utf-8 -*-
# Esm_class - SMPP v5.0, section 4.7.12, table 4-48, page 125
# Esm_class is use to indicate special message attributes

Default_mode = int('00000000', 2)                # Default MC Mode (e.g. Store and Forward)
Datagram_mode = int('00000001', 2)
Forward_mode = int('00000010', 2)                # Forward (i.e. Transaction) mode
Store_and_forward_mode = int('00000011', 2)      # Use to select Store and Forward mode if Default MC Mode is non Store and Forward
Default_message_type = int('00000000', 2)        # Normal message
Mc_delivery_receipt = int('00000100', 2)         # Short Message contains MC Delivery Receipt 
Delivery_notification = int('00100000', 2)       # Short Message contains Intermediate Delivery Notification
Delivery_acknowledgement = int('00001000', 2)    # Short Message contains Delievery Acknowledgement
User_acknowledgement = int('00010000', 2)        # Short Message contains Manual/User Acknowledgement
Conversation_abort = int('00011000', 2)          # Short Message contains Conversation Abort (Korean CDMA)
Feature_none = int('00000000', 2)
UDHI_indicator = int('01000000', 2)
Feature_reply_path = int('10000000', 2)          # Set Reply Path (only relevant for GSM network) 
UDHI_and_reply_path = int('11000000', 2)         # Set UDHI and Reply Path (only relevant for GSM) 
