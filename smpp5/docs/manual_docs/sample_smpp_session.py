valid_session_states = ['open', 'bound_tx', 'bound_rx', 'bound_trx', 'unbound', 'closed', 'outbound']

class SMPPSession(object):
    
    state = 'closed' # can be one of
    socket = None
    sequence_number = 0
    ip = None
    port = None
    system_id = None
    password = None
    system_type = None

    def connect(self, ip, port):
        
        #open socket and connect and then set
        s = open_socket_here()
        self.socket = s
        s.state = 'open'
        
    def bind(self, bind_type, system_id, password, system_type):
        
        # try sending the appropriate bind type PDU ('RX', 'TX', 'TRX') and fetch return value
    
    def send_sms(self, other_parameters):
        
        if self.state not in ['bound_tx', 'bound_trx']:
            raise Exception("SMPP Session not in a state that allows sending SMSes")



if '__main__' == __name__:
    
    S = SMPPSession()
    S.connect('192.168.1.5', 3333)
    S.bind('TRX', 'abc', 'secret', 'test_server')
    
    S.send_sms(sms_related_parameters_here)
