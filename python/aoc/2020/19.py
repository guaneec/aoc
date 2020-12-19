from .util import getinput
import re

from lark import Lark

s = getinput(19)

for p in (1, 2):
    rules, msgs = s.split('\n\n')
    if p == 2:
        rules = re.sub(r'^8\D.+$', '8: 42 | 42 8', rules, flags=re.M)
        rules = re.sub(r'^11\D.+$', '11: 42 31 | 42 11 31', rules, flags=re.M)
    msgs = msgs.splitlines()

    l = Lark(re.sub(r'(\d+)', r'r\1', f'start: 0\n{rules}'))

    def match(s):
        try:
            l.parse(s)
            return True
        except:
            return False

    print(sum(match(m) for m in msgs))