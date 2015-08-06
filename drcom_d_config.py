#!/usr/bin/python
# -*- coding: utf-8 -*-

from binascii import hexlify
import re

def hexed(s):
    ret = ''
    for i in s:
        ret += '\\x' + hex(ord(i))[2:].rjust(2, '0')
    return ret

filename = 'dr.pcapng'
with open(filename, 'rb') as f:
	text = f.read()
offset = re.search('\xf0\x00\xf0\x00[\x00-\xFF]{4}\x03\x01', text).start() + 8
#print hexlify(text[offset:offset+330])
username_len = ord(text[offset+3]) - 20
username = text[offset+20:offset+20+username_len]
passwd = raw_input('Please input your password!\n')

server =  'server = \'%s\'' % '.'.join([str(ord(i)) for i in text[offset-12:offset-8]])
username = 'username = \'%s\'' % username
password = 'password = \'' + passwd + '\''
CONTROLCHECKSTATUS = 'CONTROLCHECKSTATUS = \'%s\'' % hexed(text[offset+56])
ADAPTERNUM = 'ADAPTERNUM = \'%s\'' % hexed(text[offset+57])
host_ip = 'host_ip = \'%s\'' % '.'.join(map(lambda x: str(ord(x)), text[offset+81:offset+85]))
IPDOG = 'IPDOG = \'%s\'' % hexed(text[offset+105])
host_name = 'host_name = \'%s\'' % 'DRCOMFUCKER'
PRIMARY_DNS = 'PRIMARY_DNS = \'%s\'' % '.'.join(map(lambda x: str(ord(x)), text[offset+142 :offset+146]))
dhcp_server = 'dhcp_server = \'%s\'' % '.'.join(map(lambda x: str(ord(x)), text[offset+146:offset+150]))
AUTH_VERSION = 'AUTH_VERSION = \'%s\'' % hexed(text[offset+310:offset+312])
mac = 'mac = 0x%s' % hexlify(text[offset+320:offset+326])
host_os = 'host_os = \'%s\'' % 'WINDIAOS'
KEEP_ALIVE_VERSION = [i for i in re.findall('\xf0\x00\xf0\x00....\x07.\x5c\x28\x00\x0b\x01(..)', text) if i != '\x0f\x27'][0]
KEEP_ALIVE_VERSION = 'KEEP_ALIVE_VERSION = \'%s\'' % hexed(KEEP_ALIVE_VERSION)

content = open('config.conf', 'w')
for args in [server,username,password,CONTROLCHECKSTATUS,ADAPTERNUM,host_ip,IPDOG,host_name,PRIMARY_DNS,dhcp_server,AUTH_VERSION,mac,host_os,KEEP_ALIVE_VERSION]:
    print args
    content.write(args+'\n')
content.close()
