"""
SMPP CLIENT INTERFACE
"""

from smpp5.lib.session import SMPPSession
from smpp5.client.smpp_client import SMPPClient


class ClientHandler(object):

    ip = None
    port = None
    system_id = None
    password = None
    system_type = None
    client = None
    bind_type = None
    status = None
    recipient = None
    message = None

    def __init__(self):
        pass

    def connect_info(self):
        self.ip = input("Enter the server IP to connect\t\t\t")
        self.port = input("Enter the server PORT to connect\t\t")
        self.client = SMPPClient()
        self.client.connect(self.ip, int(self.port))

        # If connection successfull then binding pdu is sent
        if(self.client.conn_status == 'connected'):
            print("****Enter the Binding PDU****")
            print("1 . Press 1 for Bind Transmitter PDU Type")
            print("2 . Press 2 for Bind Receiver PDU Type")
            print("3 . Press 3 for Bind Transceiver PDU Type")
            option = int(input())
            if(option == 1):
                self.bind_type = 'TX'
            elif(option == 2):
                self.bind_type = 'RX'
            elif(option == 3):
                self.bind_type = 'TRX'
            else:
                print("Invalid Option.....")

        # Ask for credentials
            self.system_id = input("Enter the System Id        ")
            self.password = input("Enter the Password        ")
            self.system_type = input("Enter the System Type     ")
            self.client.login(self.bind_type, self.system_id, self.password, self.system_type)

        # If cresentials validated successfully then menu is displayed to client
            if(self.client.validation_status == 'success'):
                print("\nSuccessfully Login")
                while True:
                    print("\n********************** MAIN MENU **********************************")
                    print("\nPress 1 to send Short Text Message")
                    print("Press 2 to query the status of previously submitted short Text Message")
                    print("Press 3 to cancel a previously submitted Short Text Message")
                    print("Press 4 to replace a previously submitted Short Text Message")
                    print("Press 5 to exit")
                    option = int(input())
                    if(option == 1):
                        self.recipient = input("Enter the Recipient (Kindly add +92)                  ")
                        self.message = input("Enter the Short Message to send      ")
                        self.client.send_sms(self.recipient, self.message, self.system_id)
                    elif(option == 2):
                        message_id = system_id = input("Enter the Message Id of Message whom Status is required    ")
                        self.client.query_status(message_id)
                    elif(option == 3):
                        message_id = system_id = input("Enter the Message Id of Message whom you want to cancel    ")
                        self.client.cancel_sms(message_id)
                    elif(option == 4):
                        message_id = input("Enter the Message Id of Message whom you want to replace    ")
                        self.message = input("Enter the Short Message to replace previous sumbitted short message      ")
                        self.client.replace_sms(message_id, self.message,)
                    elif(option == 5):
                        break

            else:
                print("Oops! Login Failed...Try Again")

        self.client.logout()
        self.client.disconnect()
        print("Thank You.....Good Bye!!")

if __name__ == '__main__':
    client_handler = ClientHandler()
    client_handler.connect_info()



