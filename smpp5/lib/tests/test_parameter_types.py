from smpp5.lib.util.hex_print import hex_convert, hex_print
from smpp5.lib.parameter_types import Integer


def test_01_integer_encode():
    "Test to check 1, 2 and 4 byte integer encoding"

    assert '05 ' == hex_convert(Integer(5, 1).encode())
    assert 'a3 12 ' == hex_convert(Integer(41746, 2).encode())
    assert '01 d9 5e 1f ' == hex_convert(Integer(31022623, 4).encode())


def test_02_integer_decode():
    "Test to check 1, 2 and 4 byte integer decoding"

    assert 5 == Integer.decode('\x05').value
    assert 41746 == Integer.decode('\xa3\x12').value
    assert 31022623 == Integer.decode('\x01\xd9^\x1f').value
