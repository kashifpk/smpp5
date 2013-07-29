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
        if(self.client.status == 'success'):
            print("****Enter the Binding PDU****")
            print("1 . Press 1 for Bind Transmitter PDU Type")
            print("2 . Press 2 for Bind Receiver PDU Type")
            print("3 . Press 3 for Bind Transceiver PDU Type")
            option = int(input())
            if(option == 1):
                self.bind_type = 'TX'
            elif(int(option) == 2):
                self.bind_type = 'RX'
            elif(int(option) == 3):
                self.bind_type = 'TRX'

        # Ask for credentials
            self.system_id = input("Enter the System Id\t\t\t")
            self.password = input("Enter the Password\t\t\t\t")
            self.system_type = input("Enter the System Type\t\t\t")
            self.client.login(self.bind_type, self.system_id, self.password, self.system_type)

        # If cresentials validated successfully then menu is displayed to client
            if(self.client.status == 'success'):
                print("Successfully Login\n")
                ch = 'Y'
                while ch == 'Y':
                    print("1. Press 1 to send Short Text Message")
                    print("2. Press 2 to query the status of previously submitted short Text Message")
                    print("3. Press 3 to cancel a previously submitted Short Text Message")
                    option = int(input())
                    if(option == 1):
                        self.recipient = input("Enter the Recipient     ")
                        self.message = input("Enter the Short Message to send      ")
                    print("Do you want to exit......reply with Y/N")
                    ch = input()
            else:
                print("Oops! Login Failed...Try Again")

        self.client.logout()
        self.client.disconnect()
        print("Thank You.....Good Bye!!")

if __name__ == '__main__':
    client_handler = ClientHandler()
    client_handler.connect_info()



