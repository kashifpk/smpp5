from smpp5.client.smpp_client import SMPPClient
import unittest


class Test(unittest.TestCase):
    def setUp(self):
        self.client = SMPPClient('127.0.0.1', 1337, 'TX',
                                 'ASMA', 'secret08', 'SUBMIT1')
        self.client.connect()
        self.client.login()

    def tearDown(self):
        self.client.session.unbind()

    def test_01_connection(self):
        assert self.client.connect() is True

    def test_02_login1(self):
        self.client.connect()
        assert self.client.login() is True

    def test_03_login2(self):
        client = SMPPClient('127.0.0.1', 1337, 'TX',
                            'ASMA', 'secret09', 'SUBMIT1')
        client.connect()

        assert client.login() is False

    def test_04_enquireconnection(self):

        assert self.client.session.enquire_link() is None

    def test_05_sendsms(self):

        assert self.client.session.send_sms('+923005381993', 'hello') is None

    def test_06_querysms(self):

        assert self.client.session.query_status(2) is None

    def test_07_replacesms(self):

        assert self.client.session.replace_sms(2, 'hello') is None

    def test_08_cancelesms(self):

        assert self.client.session.cancel_sms(2) is None

    def test_09_unbind(self):

        assert self.client.session.unbind() is None

