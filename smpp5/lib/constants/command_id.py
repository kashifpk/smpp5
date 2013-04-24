# Command IDs - SMPP v5.0, section 4.7.5, table 4-44, page 115-116
# SMPP V5.0 4.7.5 command_id pg 115

bind_receiver = int(0x00000001)
bind_transmitter = int(0x00000002)
query_sm = int(0x00000003)
submit_sm = int(0x00000004)
deliver_sm = int(0x00000005)
unbind = int(0x00000006)
replace_sm = int(0x00000007)
cancel_sm = int(0x00000008)
bind_transceiver = int(0x00000009)
outbind = int(0x0000000B)
enquire_link = int(0x00000015)
submit_multi = int(0x00000021)
alert_notification = int(0x00000102)
data_sm = int(0x00000103)
broadcast_sm = int(0x00000111)
query_broadcast_sm = int(0x00000112)
cancel_broadcast_sm = int(0x00000113)
generic_nack = int(0x80000000)
bind_receiver_resp = int(0x80000001)
bind_transmitter_resp = int(0x80000002)
query_sm_resp = int(0x80000003)
submit_sm_resp = int(0x80000004)
deliver_sm_resp = int(0x80000005)
unbind_resp = int(0x80000006)
replace_sm_resp = int(0x80000007)
cancel_sm_resp = int(0x80000008)
bind_transceiver_resp = int(0x80000009)
enquire_link_resp = int(0x80000015)
submit_multi_resp = int(0x80000021)
data_sm_resp = int(0x80000103)
broadcast_sm_resp = int(0x80000111)
query_broadcast_sm_resp = int(0x80000112)
cancel_broadcast_sm_resp = int(0x80000113)


# 4.7.9 dest_flag
# A flag, which will identify whether destination address is a Distribution List (DL) name or SME
# address. pg 124

dest_flag_value1 = int(0x01)  # SME Address
dest_flag_value2 = int(0x02)  # Distribution List Name
