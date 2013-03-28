from smpp5.lib.util.hex_print import hex_convert, hex_print


def test_01_hex_convert():
    "Test to check hex_convert"

    assert '48 65 6c 6c 6f 20 57 6f 72 6c 64 21 ' == hex_convert("Hello World!")


def test_02_hex_convert_with_line_size():
    "Test to check hex_convert with a given line size"

    assert '48 65 6c 6c \n6f 20 57 6f \n72 6c 64 21 \n' == hex_convert("Hello World!", 12)
