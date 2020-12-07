from .util import getinput
import re

s = getinput(4)


def present(passport):
    return len(passport) == 7

def valid(passport):
    try:
        return bool(
            1920 <= int(passport['byr']) <= 2002 and
            2010 <= int(passport['iyr']) <= 2020 and
            2020 <= int(passport['eyr']) <= 2030 and
            (
                passport['hgt'][-2:] == 'cm' and 150 <= int(passport['hgt'][:-2]) <= 193 or
                passport['hgt'][-2:] == 'in' and 59 <= int(passport['hgt'][:-2]) <= 76
            ) and
            re.match('^#[0-9a-f]{6}$', passport['hcl']) and
            passport['ecl'] in 'amb blu brn gry grn hzl oth'.split() and
            re.match('^[0-9]{9}$', passport['pid'])
        )
    except:
        return False

a1 = 0
a2 = 0

for group in s.split('\n\n'):
    passport = {k: v for k, v in (kv.split(':') for kv in group.split()) if k != 'cid'}
    a1 += present(passport)
    a2 += valid(passport)

print(a1)
print(a2)
