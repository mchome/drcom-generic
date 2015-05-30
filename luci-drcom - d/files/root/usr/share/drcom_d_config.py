#!/usr/bin/env python
# -*- coding: utf-8 -*-
from binascii import hexlify
import re
import subprocess

def hexed(s):
    ret = ''
    for i in s:
        ret += '\\x' + hex(ord(i))[2:].rjust(2, '0')
    return ret

filename = '/tmp/upload/dr.pcapng'
f = open(filename, 'rb')
text = f.read()
offset = re.search('\xf0\x00\xf0\x00[\x00-\xFF]{4}\x03\x01', text).start() + 8
#print hexlify(text[offset:offset+330])
username_len = ord(text[offset+3]) - 20
username = text[offset+20:offset+20+username_len]
# passwd = raw_input('Please input your password!\n')

server =  '%s' % '.'.join([str(ord(i)) for i in text[offset-12:offset-8]])
username = '%s' % username
# password = ''
CONTROLCHECKSTATUS = '%s' % hexed(text[offset+56])
ADAPTERNUM = '%s' % hexed(text[offset+57])
host_ip = '%s' % '.'.join(map(lambda x: str(ord(x)), text[offset+81:offset+85]))
IPDOG = '%s' % hexed(text[offset+105])
host_name = '%s' % 'DRCOMFUCKER'
PRIMARY_DNS = '%s' % '.'.join(map(lambda x: str(ord(x)), text[offset+142 :offset+146]))
dhcp_server = '%s' % '.'.join(map(lambda x: str(ord(x)), text[offset+146:offset+150]))
AUTH_VERSION = '%s' % hexed(text[offset+310:offset+312])
mac = '0x%s' % hexlify(text[offset+320:offset+326])
host_os = '%s' % 'WINDIAOS'
KEEP_ALIVE_VERSION = re.search('\xf0\x00\xf0\x00....\x07.\x5c\x28\x00\x0b\x01(..)', text).group(1)
KEEP_ALIVE_VERSION = '%s' % hexed(KEEP_ALIVE_VERSION)

subprocess.check_output(["uci", "set", "drcom.config.server="+server])
subprocess.check_output(["uci", "set", "drcom.config.username="+username])
subprocess.check_output(["uci", "set", "drcom.config.mac="+mac])
subprocess.check_output(["uci", "set", "drcom.config.CONTROLCHECKSTATUS="+CONTROLCHECKSTATUS])
subprocess.check_output(["uci", "set", "drcom.config.ADAPTERNUM="+ADAPTERNUM])
subprocess.check_output(["uci", "set", "drcom.config.host_ip="+host_ip])
subprocess.check_output(["uci", "set", "drcom.config.IPDOG="+IPDOG])
subprocess.check_output(["uci", "set", "drcom.config.host_name="+host_name])
subprocess.check_output(["uci", "set", "drcom.config.PRIMARY_DNS="+PRIMARY_DNS])
subprocess.check_output(["uci", "set", "drcom.config.dhcp_server="+dhcp_server])
subprocess.check_output(["uci", "set", "drcom.config.AUTH_VERSION="+AUTH_VERSION])
subprocess.check_output(["uci", "set", "drcom.config.host_os="+host_os])
subprocess.check_output(["uci", "set", "drcom.config.KEEP_ALIVE_VERSION="+KEEP_ALIVE_VERSION])