"""
Print hexadecimal representation of a string
"""


def hex_convert(string, line_width=80):
    "Given a string returns each byte's hexadecimal representation separated by a single space."

    hex_str = ""
    for ch in string:
        hex_str += hex(ord(ch))[2:].zfill(2) + " "
        if (len(hex_str) - hex_str.count("\n")) % line_width < 3:
            hex_str += "\n"

    return hex_str


def hex_print(string, line_width=80):
    """
    Given a string prints each byte's hexadecimal representation separated by a single space.
    Line width determines the maximum info to print in one line.
    """

    print(hex_convert(string, line_width))
