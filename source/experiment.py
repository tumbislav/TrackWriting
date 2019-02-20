# chars = 'TCREHEA'
# pattern = [None, None, None, None, 'R']
import re


def enum_all(pattern, chars, flt=None):
    for ch in pattern:
        if ch != '?':
            i = chars.find(ch)
            chars = chars[:i] + chars[i+1:]
    total = enum_combos('', pattern, chars, flt)
    print(total)


def enum_combos(head: str, tail: str, chars: str, flt) -> int:
    if len(tail) == 0:
        if flt is not None and not flt.match(head):
            print(head)
            return 1
        else:
            return 0
    elif tail[0] == '?':
        count = 0
        for i, ch in enumerate(chars):
            count += enum_combos(head + ch, tail[1:], chars[:i] + chars[i + 1:], flt)
        return count
    else:
        return enum_combos(head + tail[0], tail[1:], chars, flt)


enum_all('????R', 'TCREHEA', re.compile('[EA]{3}|[CRT]{3}'))
