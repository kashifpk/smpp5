import threading


def client_thread(session, connection):
    if session is '':
        print("Oops, There seems a disconnection from session")
    else:
        print("Yes it works!")
        background_thread = threading.Thread(target=thread, args=(session, connection))
        background_thread.start()


def thread(session, connection):
    while True:
        session.storing_recieved_pdus()
