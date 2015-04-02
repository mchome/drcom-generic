# -*- coding: utf-8 -*-

from binascii import hexlify
import re

def hexed(s):
    ret = ''
    for i in s:
        ret += '\\x' + hex(ord(i))[2:].rjust(2, '0')
    return ret

filename = 'drp.pcapng'
f = open(filename, 'rb')
text = f.read()
offset = re.search('\x07[\x00-\xFF]\x60\x00\x03\x00', text).start()
#print hexlify(text[offset:offset+330])
server = 'server = \'%s\'' % '.'.join([str(ord(i)) for i in text[offset-12:offset-8]])
pppoe_flag = 'pppoe_flag = \'%s\'' % hexed(text[offset+19])
keep_alive2_flag = re.search('\x07.\x5c\x28\x00\x0b\x03(.)\x02', text).group(1)
keep_alive2_flag = 'keep_alive2_flag = \'%s\'' % hexed(keep_alive2_flag)

content = open('config.conf', 'w')
for args in [server,pppoe_flag,keep_alive2_flag]:
    print args
    content.write(args+'\n')
content.close()

