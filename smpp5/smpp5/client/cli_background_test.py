import threading


def client_thread(session, connection):
    if session is '':
        print("oh no")
    else:
        print("atleat yeh tou chala")
        background_thread = threading.Thread(target=thread, args=(session, connection))
        background_thread.start()


def thread(session, connection):
    while True:
        session.storing_recieved_pdus()
