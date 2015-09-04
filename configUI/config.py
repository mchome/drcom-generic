#!/usr/bin/python
# -*- coding: utf-8 -*-

from binascii import hexlify
import re

def hexed(s):
	ret = ''
	for i in s:
		ret += '\\x' + hex(ord(i))[2:].rjust(2, '0')
	return ret

def config_d(filepath):
	with open(filepath, 'rb') as f:
		text = f.read()
	try:
		offset = re.search('\xf0\x00\xf0\x00[\x00-\xFF]{4}\x03\x01', text).start() + 8
		username_len = ord(text[offset+3]) - 20
		username = text[offset+20:offset+20+username_len]
		passwd = ''
		server =  'server = \'%s\'' % '.'.join([str(ord(i)) for i in text[offset-12:offset-8]])
		username = 'username = \'%s\'' % username
		password = 'password = \'' + passwd + '\''
		CONTROLCHECKSTATUS = 'CONTROLCHECKSTATUS = \'%s\'' % hexed(text[offset+56])
		ADAPTERNUM = 'ADAPTERNUM = \'%s\'' % hexed(text[offset+57])
		host_ip = 'host_ip = \'%s\'' % '.'.join(map(lambda x: str(ord(x)), text[offset+81:offset+85]))
		IPDOG = 'IPDOG = \'%s\'' % hexed(text[offset+105])
		host_name = 'host_name = \'%s\'' % 'fuyumi'
		PRIMARY_DNS = 'PRIMARY_DNS = \'%s\'' % '.'.join(map(lambda x: str(ord(x)), text[offset+142 :offset+146]))
		dhcp_server = 'dhcp_server = \'%s\'' % '.'.join(map(lambda x: str(ord(x)), text[offset+146:offset+150]))
		AUTH_VERSION = 'AUTH_VERSION = \'%s\'' % hexed(text[offset+310:offset+312])
		mac = 'mac = 0x%s' % hexlify(text[offset+320:offset+326])
		host_os = 'host_os = \'%s\'' % 'Windows 8.1'
		KEEP_ALIVE_VERSION = [i for i in re.findall('\xf0\x00\xf0\x00....\x07.\x5c\x28\x00\x0b\x01(..)', text) if i != '\x0f\x27'][0]
		KEEP_ALIVE_VERSION = 'KEEP_ALIVE_VERSION = \'%s\'' % hexed(KEEP_ALIVE_VERSION)
	
		with open('drcom.conf', 'w') as content:
			for args in [server,username,password,CONTROLCHECKSTATUS,ADAPTERNUM,host_ip,IPDOG,host_name,PRIMARY_DNS,dhcp_server,AUTH_VERSION,mac,host_os,KEEP_ALIVE_VERSION]:
				# print args
				content.write(args+'\n')
		return 'Success!'
	except Exception, e:
		return str(e)
	
def config_p(filepath):
	with open(filepath, 'rb') as f:
		text = f.read()
	try:
		offset = re.search('\x07[\x00-\xFF]\x60\x00\x03\x00', text).start()
		server = 'server = \'%s\'' % '.'.join([str(ord(i)) for i in text[offset-12:offset-8]])
		pppoe_flag = 'pppoe_flag = \'%s\'' % hexed(text[offset+19])
		keep_alive2_flag = re.search('\x07.\x5c\x28\x00\x0b\x03(.)\x02', text).group(1)
		keep_alive2_flag = 'keep_alive2_flag = \'%s\'' % hexed(keep_alive2_flag)

		with open('drcom.conf', 'w') as content:
			for args in [server,pppoe_flag,keep_alive2_flag]:
				# print args
				content.write(args+'\n')
		return 'Success!'
	except Exception, e:
		return str(e)

def main():
	filepath = 'dr.pcapng'
	config_d(filepath)
	# config_p(filepath)

if __name__ == '__main__':
	main()