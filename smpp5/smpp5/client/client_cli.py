"""
SMPP CLIENT INTERFACE
"""

import sys
import time
from smpp5.lib.session import SMPPSession, SessionState
from smpp5.client.smpp_client import SMPPClient
import threading


def ui_loop(client):

    while True:
        try:
            print("\n********************** MAIN MENU **********************************")
            print()
            notification = client.session.notifications_4_client()
            if(notification == 0):
                pass
            else:
                print("*** You have pending  notifications...Press 6 to view them....")
            print("\nPress 1 to send Short Text Message")
            print("Press 2 to query the status of previously submitted short Text Message")
            print("Press 3 to cancel a previously submitted Short Text Message")
            print("Press 4 to replace a previously submitted Short Text Message")
            print("Press 5 to view Unread Smses")
            print("Press 6 to view pending notifications")
            print("Press 7 to check connectivity with server")
            print("Press 8 to exit")
            print("Press 9 to leave the valuable comments.")
            option = int(input())
            if(option == 1):
                recipient = input("Enter the Recipient               : ")
                message = input("Enter the Short Message to send    : ")
                recipientt = recipient[0:3]
                if not recipient.startswith('+'):
                    recipient = '+92' + recipient[1:]
                if recipientt == '033' or recipientt == '031':
                    client.session.send_sms(recipient, message, None)
                else:
                    print("Cnnot send message...prefix wrong")

            elif(option == 2):
                message_id = input("Enter the Message Id of Message whom Status is required   : ")
                client.session.query_status(message_id)

            elif(option == 3):
                message_id = system_id = input("Enter the Message Id of Message whom you want to cancel   : ")
                client.session.cancel_sms(message_id)

            elif(option == 4):
                message_id = input("Enter the Message Id of Message whom you want to replace              : ")
                message = input("Enter the Short Message to replace previous sumbitted short message      : ")
                client.session.replace_sms(message_id, message)

            elif(option == 5):
                client.session.view_smses()

                key = input("\nPress Enter To Continue.......")
                while key != '':
                    key = input("Press Enter To Continue.......")

            elif(option == 6):
                count = client.session.notifications_4_client()
                if(count == 0):
                    print("You have no any pending notification...")
                else:
                    while count > 0:
                        client.session.processing_recieved_pdus()
                        count = count - 1

                key = input("\nPress Enter To Continue.......")
                while key != '':
                    key = input("\nPress Enter To Continue.......")

            elif(option == 7):
                client.session.enquire_link()

            elif(option == 8):
                break

            else:
                print("\nInvalid Option......")
        except:
            print("\nInvalid option")
    client.session.unbind()
    time.sleep(1)
    while client.session.state != SessionState.UNBOUND:
        client.session.processing_recieved_pdus()
    client.sc.close()
    print("Thank You.....Good Bye!!")
    sys.exit()


def get_connect_info():
        ret = dict(ip=None, port=None)
        ret['ip'] = input("Enter the server IP to connect\t\t\t")
        ret['port'] = int(input("Enter the server PORT to connect\t\t"))

        return ret


def get_login_info():
    ret = dict(bind_type=None, system_id=None, password=None, system_type=None)
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

    ret['system_id'] = input("Enter the System Id       ")
    ret['password'] = input("Enter the Password        ")
    ret['system_type'] = input("Enter the System Type     ")

    return ret


if __name__ == '__main__':

    conn_info = get_connect_info()

    login = False

    client = SMPPClient(conn_info['ip'], conn_info['port'])

    if client.connect():
        print("\nConnection established successfully\n")
        background_thread = threading.Thread(target=client.session.storing_recieved_pdus, args=())  # to recieve response from server
        background_thread.start()
    else:
        print("\nConnection Refused...Try Again\n")
        sys.exit()

    while login is False:
        login_info = get_login_info()
        if client.login(login_info['bind_type'], login_info['system_id'], login_info['password'], login_info['system_type']):
            print("\nLogin successful")
            login = True
            ui_loop(client)  # to check if ui_loop method is functioning correct
            background_thread.join()
            client.sc.close()
            sys.exit()
        else:
            print("\nLogin Failed...Try Again\n")

    # if here then login was successful, now create a background thread for handling traffic from server
    # and run UI loop in the main process/thread for user interaction

    # Notes on background thread: It can either wait till there is data (blocking) or check if there is data
    # ready to read from socket periodically and sleep in the meanwhile (non-blocking). We need to go with the non-blocking
    # option since socket is shared between both threads and if it is blocked in socket.recv in the background thread we
    # cannot send data through it in the UI thread.
