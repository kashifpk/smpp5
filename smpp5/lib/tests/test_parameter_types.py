from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String, TLV


def test_01_integer_encode():
    "Test to check 1, 2 and 4 byte integer encoding"

    assert '05 ' == hex_convert(Integer(5, 1).encode())
    assert 'A3 12 ' == hex_convert(Integer(41746, 2).encode())
    assert '01 D9 5E 1F ' == hex_convert(Integer(31022623, 4).encode())


def test_02_integer_decode():
    "Test to check 1, 2 and 4 byte integer decoding"

    assert 5 == Integer.decode(b'\x05').value
    assert 41746 == Integer.decode(b'\xa3\x12').value
    assert 31022623 == Integer.decode(b'\x01\xd9^\x1f').value


def test_03_cstring_encode():
    "Test to check CString encoding"

    assert '48 65 6C 6C 6F 00 ' == hex_convert(CString(b"Hello").encode())
    assert '31 32 33 34 35 36 37 38 39 00 ' == hex_convert(CString(b"123456789").encode())
    assert '41 32 46 35 45 44 32 37 38 46 43 00 ' == hex_convert(CString(b"A2F5ED278FC").encode())


def test_04_cstring_decode():
    "Test to check CString decoding"

    assert b"Hello" == CString.decode(b'Hello\x00').value
    assert b"123456789" == CString.decode(b'123456789\x00').value
    assert b"A2F5ED278FC" == CString.decode(b'A2F5ED278FC\x00').value


def test_05_string_encode():
    "Test to check CString encoding"

    assert b"Hello" == String(b"Hello").encode()


def test_06_string_decode():
    "Test to check CString decoding"

    assert b"Hello" == String.decode(b'Hello').value


def test_07_tlv_encode():
    "Test to check TLV encoding"

    assert '00 07 00 01 04 ' == hex_convert(TLV(0x0007, 0x04).encode())
    assert 1 == TLV(0x0007, 0x04).length.value


def test_08_tlv_decode():
    "Test to check TLV decoding"

    tlv = TLV.decode(b'\x00\x07\x00\x01\x04')
    assert 7 == tlv.tag.value
    assert 1 == tlv.length.value
    assert 4 == ord(tlv.value.value)
