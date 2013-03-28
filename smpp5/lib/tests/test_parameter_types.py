from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer, CString, String


def test_01_integer_encode():
    "Test to check 1, 2 and 4 byte integer encoding"

    assert '05 ' == hex_convert(Integer(5, 1).encode())
    assert 'A3 12 ' == hex_convert(Integer(41746, 2).encode())
    assert '01 D9 5E 1F ' == hex_convert(Integer(31022623, 4).encode())


def test_02_integer_decode():
    "Test to check 1, 2 and 4 byte integer decoding"

    assert 5 == Integer.decode('\x05').value
    assert 41746 == Integer.decode('\xa3\x12').value
    assert 31022623 == Integer.decode('\x01\xd9^\x1f').value


def test_03_cstring_encode():
    "Test to check CString encoding"

    assert '48 65 6C 6C 6F 00 ' == hex_convert(CString("Hello").encode())
    assert '31 32 33 34 35 36 37 38 39 00 ' == hex_convert(CString("123456789").encode())
    assert '41 32 46 35 45 44 32 37 38 46 43 00 ' == hex_convert(CString("A2F5ED278FC").encode())


def test_04_cstring_decode():
    "Test to check CString decoding"

    assert "Hello" == CString.decode('Hello\x00').value
    assert "123456789" == CString.decode('123456789\x00').value
    assert "A2F5ED278FC" == CString.decode('A2F5ED278FC\x00').value


def test_05_string_encode():
    "Test to check CString encoding"

    assert "Hello" == String("Hello").encode()


def test_06_string_decode():
    "Test to check CString decoding"

    assert "Hello" == String.decode('Hello').value
