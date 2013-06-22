from smpp5.lib.util.hex_print import hex_convert, hex_print


def test_01_hex_convert():
    "Test to check hex_convert"

    assert '48 65 6C 6C 6F 20 57 6F 72 6C 64 21 ' == hex_convert("Hello World!")


def test_02_hex_convert_with_line_size():
    "Test to check hex_convert with a given line size"

    assert '48 65 6C 6C \n6F 20 57 6F \n72 6C 64 21 \n' == hex_convert("Hello World!", 12)
