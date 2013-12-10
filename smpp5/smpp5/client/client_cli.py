"""
SMPP CLIENT INTERFACE
"""

import sys
import time
from smpp5.lib.session import SMPPSession
from smpp5.client.smpp_client import SMPPClient
import threading


def ui_loop(client):

    while True:
        print("\n********************** MAIN MENU **********************************")
        print()
        notification = client.session.notifications_4_client()
        if(notification == 0):
            pass
        else:
            print("* You have pending  notifications...Press 6 to view them....thank you....")
        print("\nPress 1 to send Short Text Message")
        print("Press 2 to query the status of previously submitted short Text Message")
        print("Press 3 to cancel a previously submitted Short Text Message")
        print("Press 4 to replace a previously submitted Short Text Message")
        print("Press 5 to view Unread Smses")
        print("Press 6 to view pending notifications")
        print("Press 7 to exit")
        option = int(input())
        if(option == 1):
            recipient = input("Enter the Recipient                                   ")
            message = input("Enter the Short Message to send      ")
            if not recipient.startswith('+'):
                recipient = '+92' + recipient[1:]
            client.session.send_sms(recipient, message)

        elif(option == 2):
            message_id = input("Enter the Message Id of Message whose Status is required    ")
            client.session.query_status(message_id)

        elif(option == 3):
            message_id = input("Enter the Message Id of Message which you want to cancel    ")
            client.session.cancel_sms(message_id)

        elif(option == 4):
            message_id = input("Enter the Message Id of Message which you want to replace    ")
            message = input("Enter the Short Message to replace previous sumbitted short message      ")
            client.session.replace_sms(message_id, message)

        elif(option == 5):
            client.session.view_smses()

        elif(option == 6):
            count = client.session.notifications_4_client()
            if(count == 0):
                print("You have no pending notifications...")
            else:
                while count > 0:
                    client.session.processing_recieved_pdus()
                    count = count - 1

        elif(option == 7):
            break

        else:
            print("\nInvalid Selection......")
    client.session.unbind()
    time.sleep(1)
    while client.session.state != 5:
        client.session.processing_recieved_pdus()
    client.sc.close()
    print("Thank You.....Good Bye!!")


def get_connect_info():
        ret = dict(ip=None, port=None, bind_type=None,
                   system_id=None, password=None, system_type=None)
        ret['ip'] = input("Enter the server IP to connect\t\t\t")
        ret['port'] = int(input("Enter the server PORT to connect\t\t"))

        print("**** Select Bind Type ****")
        bind_types = ['TX', 'RX', 'TRX']
        for bt in bind_types:
            print("%i. %s" % (bind_types.index(bt), bt))
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


def client_thread(client):
    while client.sc.is_open is True: #if shared socket and shared connection is open 
        client.session.storing_recieved_pdus()#call this method of session class via the object passed as parameter

if __name__ == '__main__':

    conn_info = get_connect_info()

    client = SMPPClient(conn_info['ip'], conn_info['port'], conn_info['bind_type'],
                        conn_info['system_id'], conn_info['password'], conn_info['system_type'])#passing connection information to client object

    if client.connect():
        print("Connection established successfully\n")
        background_thread = threading.Thread(target=client_thread, args=(client,))#creating a background thread for the client and giving name of method in target for execution
        background_thread.start()#starting the background thread
    else:
        print("Connection Refused...Try Again\n")
        sys.exit()

    if client.login():
        print("Login successful\n")
        ui_loop(client)#to check if ui_loop method is functioning correct
        print("Yes it is...")
        background_thread.join()#to assure that main thread should exit when background has completed all its operations
    else:
        print("Login Failed")
        background_thread.join()#to assure that main thread should exit when background has completed all its operations
        sys.exit()

    # if here then login was successful, now create a background thread for handling traffic from server
    # and run UI loop in the main process/thread for user interaction

    # Notes on background thread: It can either wait till there is data (blocking) or check if there is data
    # ready to read from socket periodically and sleep in the meanwhile (non-blocking). We need to go with the non-blocking
    # option since socket is shared between both threads and if it is blocked in socket.recv in the background thread we
    # cannot send data through it in the UI thread.
