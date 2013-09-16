"""
SMPP CLIENT INTERFACE
"""

import sys
from smpp5.lib.session import SMPPSession
from smpp5.client.smpp_client import SMPPClient


def ui_loop(client):

    while True:
        print("\n********************** MAIN MENU **********************************")
        print("\nPress 1 to send Short Text Message")
        print("Press 2 to query the status of previously submitted short Text Message")
        print("Press 3 to cancel a previously submitted Short Text Message")
        print("Press 4 to replace a previously submitted Short Text Message")
        print("Press 5 to exit")
        option = int(input())
        if(option == 1):
            recipient = input("Enter the Recipient                                   ")
            message = input("Enter the Short Message to send      ")
            if not recipient.startswith('+'):
                recipient = '+92' + recipient[1:]

            client.send_sms(recipient, message)

        elif(option == 2):
            message_id = input("Enter the Message Id of Message whom Status is required    ")
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
            print("\nInvalid Option......")


        self.client.logout()
        self.client.disconnect()
        print("Thank You.....Good Bye!!")


def get_connect_info():
        ret = dict(ip=None, port=None, bind_type=None,
                   system_id=None, password=None, system_type=None)
        ret['ip'] = input("Enter the server IP to connect\t\t\t")
        ret['port'] = int(input("Enter the server PORT to connect\t\t"))

        print("**** Select Bind Type ****")
        bind_types = ['TX', 'RX', 'TRX']
        for bt in bind_types:
            print("%i. %s" % (bind_types.index(bt), bt)

        option = int(input())
        try:
            ret['bind_type'] = bind_types[option]
        except IndexError:
            print("Invalid Option")
            return False

        ret['system_id'] = input("Enter the System Id        ")
        ret['password'] = input("Enter the Password        ")
        ret['system_type'] = input("Enter the System Type     ")

        return ret

if __name__ == '__main__':
    conn_info = get_connect_info()

    client = SMPPClient(conn_info['ip'], conn_info['port'], conn_info['bind_type'],
                        conn_info['system_id'], conn_info['password'], conn_info['system_type'])

    if client.connect():
        print("Connection established successfully\n")
    else:
        print("Connection Refused...Try Again\n")
        sys.exit()

    if client.login():
        print("Login successful\n")
    else:
        print("Login Failed")
        sys.exit()

    # if here then login was successful, now create a background thread for handling traffic from server
    # and run UI loop in the main process/thread for user interaction

    # Notes on background thread: It can either wait till there is data (blocking) or check if there is data
    # ready to read from socket periodically and sleep in the meanwhile (non-blocking). We need to go with the non-blocking
    # option since socket is shared between both threads and if it is blocked in socket.recv in the background thread we
    # cannot send data through it in the UI thread.


