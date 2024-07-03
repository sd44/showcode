""" 删除CJK字符间非CJK特殊字符，默认空格

Examples:
  删除CJK间的空格或者 小写字母和空格::

    assert build_del_noncjk_pat('aha哈a  哈  的    你') == "aha哈a  哈的你"
    assert build_del_noncjk_pat('aha哈 a哈  的 a  你', '[a-z ]') == "aha哈哈的你"

"""

import re

""" UNICODE码表中的CJK字符区间

    参考https://www.unicode.org/versions/Unicode15.0.0/ch18.pdf Table18.1
"""
UNI_CJK = [[0x4E00, 0x9FFF], [0x3400, 0x4DBF], [0x20000, 0x2A6DF],
           [0x2A700, 0x2B73F], [0x2B740, 0x2B81F], [0x2B820, 0x2CEAF],
           [0x2CEB0, 0x2EBEF], [0x30000, 0x3134F], [0x31350, 0x323AF],
           [0xF900, 0xFAFF], [0x2F800, 0x2FA1F]]


def build_cjk_patstr():
    """ 返回CJK区间范围的regexp pattern """
    L = []
    for i in UNI_CJK:
        if isinstance(i, list):
            f, t = i
            f = chr(f)
            t = chr(t)
            L.append(f'{f}-{t}')
        else:
            L.append(chr(i))
    return f"[{''.join(L)}]"


def build_del_noncjk_pat(line, del_noncjk_pat=' '):
    """ 删除字符串

    Args:
        line: 输入的字符串。
        del_noncjk_pat: 要删除的CJK字符之间非CJK字符的正则表达式，默认为空格。
    Retruns:
        删除CJK字间非CJK字符(如空格后)后的字符串。

    """

    cjkpat = build_cjk_patstr()
    if re.search(cjkpat, del_noncjk_pat):
        raise ValueError(f"{del_noncjk_pat=}, it's can not be CJK char")
    pat = re.compile(r'({0}){1}+(?={0})'.format(cjkpat, del_noncjk_pat))
    # (?=...)是前视断言，只断言，不消耗 ...字符。
    result = pat.sub(r'\1', line)
    return result


def test_del_space():
    assert build_del_noncjk_pat('aha哈a  哈  的    你') == "aha哈a  哈的你"
    assert build_del_noncjk_pat('aha哈 a哈  的 a  你', '[a-z ]') == "aha哈哈的你"
    assert build_del_noncjk_pat('aha哈a   哈   的你') == "aha哈a   哈的你"
    assert build_del_noncjk_pat('aha哈a     哈   的 你') == "aha哈a     哈的你"
    assert build_del_noncjk_pat('aha 哈a   哈哇哟   的 你') == "aha 哈a   哈哇哟的你"
    assert build_del_noncjk_pat(
        'aha 哈a   哈  哇\n哟 的\n  哈哈   你') == "aha 哈a   哈哇\n哟的\n  哈哈你"
