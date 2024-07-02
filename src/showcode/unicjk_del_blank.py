""" 删除两个CJK字符中间的非CJK特殊字符，默认空格

Examples:
  删除中文字符间的空格::

    a = build_del_space('aha哈a  哈  的    你')
    b = build_del_space('aha哈a   哈   的你')
    c = build_del_space('aha哈a     哈   的 你')
    d = build_del_space('aha 哈a     哈哇哟   的 你')

"""

import re

""" UNICODE码表中的CJK字符区间

    参考https://www.unicode.org/versions/Unicode15.0.0/ch18.pdf Table18.1
"""
UNI_CJK = [[0x4E00, 0x9FFF], [0x3400, 0x4DBF], [0x20000, 0x2A6DF],
           [0x2A700, 0x2B73F], [0x2B740, 0x2B81F], [0x2B820, 0x2CEAF],
           [0x2CEB0, 0x2EBEF], [0x30000, 0x3134F], [0x31350, 0x323AF],
           [0xF900, 0xFAFF], [0x2F800, 0x2FA1F]]


def ischn(chars):
    """ 判断chars是否含有CJK

    Args:
        chars: CJK字符或字符串
    Retruns:
        如果含有中文，返回一个re.Match object；否则返回None
    """
    L = []
    for i in UNI_CJK:
        if isinstance(i, list):
            f, t = i
            f = chr(f)
            t = chr(t)
            L.append(f'{f}-{t}')
        else:
            L.append(chr(i))
    chn_range = re.compile(f"[{''.join(L)}]")
    return re.search(chn_range, chars)


def build_del_space(line, deleted_chars=' '):
    """ 删除字符串

    Args:
        line: 输入的字符串。
        deleted_chars: 要删除的汉字之间的非汉字字符，默认为空格。
    Retruns:
        删除汉字间非汉字特殊字符如空格后的结果。
    """
    result = []
    line = line.strip()
    if len(line) <= 2:
        return line

    repeat_del = []
    len_line = len(line)

    i = 1
    while i < len_line:
        prev = line[i - 1]
        chn = True if ischn(prev) else False
        result.append(prev)

        while i < len_line and line[i] == deleted_chars:
            repeat_del.append(deleted_chars)
            i += 1

        if i == len_line:
            return ''.join(result)

        if len(repeat_del) > 0:
            if chn == False or not ischn(line[i]):
                result += repeat_del
            repeat_del.clear()

        i += 1

    result.append(line[-1])

    return ''.join(result)


def test_del_space():
    assert build_del_space('aha哈a  哈  的    你') == "aha哈a  哈的你"
    assert build_del_space('aha哈a   哈   的你') == "aha哈a   哈的你"
    assert build_del_space('aha哈a     哈   的 你') == "aha哈a     哈的你"
    assert build_del_space('aha 哈a   哈哇哟   的 你') == "aha 哈a   哈哇哟的你"
    assert build_del_space(
        'aha 哈a   哈  哇\n哟 的\n  哈哈   你') == "aha 哈a   哈哇\n哟的\n  哈哈你"
