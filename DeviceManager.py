#!/usr/bin/env python
# -*- coding: utf-8 -*-
#qpy:kivy

import os,sys,struct,json
from locale import getdefaultlocale
from socket import *
from datetime import *
import hashlib

try:
	try:
		from tkinter import *
	except:
		from Tkinter import *
	try:
		from tkFileDialog import asksaveasfilename,askopenfilename
		from tkMessageBox import showinfo, showerror
		import ttk
	except:
		#Python 3.x
		from tkinter.filedialog import asksaveasfilename,askopenfilename
		from tkinter.messagebox import showinfo, showerror
		import tkinter.ttk as ttk
	GUI_TK=True
except:
	GUI_TK=False

try:
	from kivy.uix.floatlayout import FloatLayout
	from kivy.adapters.listadapter import ListAdapter
	from kivy.uix.listview import ListItemLabel,ListItemButton,CompositeListItem
	from kivy.metrics import dp
	from kivy.app import App
	from kivy.lang import Builder
	GUI_Kivy = True
except:
	GUI_Kivy = False
	class App:
		pass

devices = {}
log = "search.log"
icon = "R0lGODlhIAAgAPcAAAAAAAkFAgwKBwQBABQNBRAQDQQFERAOFA4QFBcWFSAaFCYgGAoUMhwiMSUlJCsrKyooJy8wLjUxLjkzKTY1Mzw7OzY3OEpFPwsaSRsuTRUsWD4+QCo8XQAOch0nYB05biItaj9ARjdHYiRMfEREQ0hIR0xMTEdKSVNOQ0xQT0NEUVFNUkhRXlVVVFdYWFxdXFtZVV9wXGZjXUtbb19fYFRda19gYFZhbF5wfWRkZGVna2xsa2hmaHFtamV0Ynp2aHNzc3x8fHh3coF9dYJ+eH2Fe3K1YoGBfgIgigwrmypajDtXhw9FpxFFpSdVpzlqvFNzj0FvnV9zkENnpUh8sgdcxh1Q2jt3zThi0SJy0Dl81Rhu/g50/xp9/x90/zB35TJv8DJ+/EZqzj2DvlGDrlqEuHqLpHeQp26SuhqN+yiC6imH/zSM/yqa/zeV/zik/1aIwlmP0mmayWSY122h3VWb6kyL/1yP8UGU/UiW/VWd/miW+Eqp/12k/1Co/1yq/2Gs/2qr/WKh/nGv/3er9mK3/3K0/3e4+4ODg4uLi4mHiY+Qj5WTjo+PkJSUlJycnKGem6ShnY2ZrKOjo6urrKqqpLi0prS0tLu8vMO+tb+/wJrE+bzf/sTExMfIx8zMzMjIxtrWyM/Q0NXU1NfY193d3djY1uDf4Mnj+931/OTk5Ozs7O/v8PLy8gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAgACAAAAj+AAEIHEiwoMGDCBMqXMiwocOHECNKnEixosWLGDNq3Mgx4iVMnTyJInVKlclSpD550nRpUqKGmD59EjWqlMlVOFWdIgWq0iNNoBIhSujokidPn0aNKrmqVStWqjxRumTqyI5KOxI5OpiIkiakNG2yelqK5alKLSAJgbBBB6RIjArmCKLIkV1HjyZNpTTJFKgSQoI4cGBiBxBIR6QM6TGQxooWL3LwMBwkSJEcLUq8YATDAZAdMkKh+GGpAo0cL1wInJuokSNIeqdeCgLBAoVMR2CEMkHDzAcnTCzsCAKERwsXK3wYKYLIdd6pjh4guCGJw5IpT7R8CeNlCwsikx7+JTJ+PAZlRHXxOgqBAQMTLXj0AAKkJw+eJw6CXGqJyAWNyT8QgZ5rsD2igwYEOOEGH38EEoghgcQhQgJAxISJI/8ZNoQUijiX1yM7NIBAFm3wUcghh9yBhQcCFEBDJ6V8MskKhgERxBGMMILXI7AhsoAAGSgRBRlliLHHHlZgMAAJmLByCiUnfGajFEcgotVzjkhggAYjjBHFFISgkoodSDAwAyStqDIJAELs4CYQQxChVSRTQcJCFWmUyAcghmzCCRgdXCEHEU69VJiNdDmnV0s4rNHFGmzgkUcfhgiShAd0nNHDVAc9YIEFFWxAQgkVpKAGF1yw4UYdc6AhhQohJFiwQAIRPQCHFlRAccMJFCRAgAAVJXDBBAsQEEBHDwUEADs="
help = """
	Usage: %s [-q] [-n] [Command];[Command];...
	-q				No output
	-n				No gui
	Command			Description
	
	help			This help
	echo			Just echo
	log [filename]		Set log file
	logLevel [0..100]	Set log verbosity
	search [brand]		Searching devices of [brand] or all
	table			Table of devices
	json			JSON String of devices
	device [MAC]		JSON String of [MAC]
	config [MAC] [IP] [MASK] [GATE] [Pasword]   - Configure searched divice
	"""%os.path.basename(sys.argv[0])
lang, charset = getdefaultlocale()
locale = {
	"ru_RU":{
		"Type help or ? to display help(q or quit to exit)":u"Введите help или ? для справки, для выхода q или quit",
		"Name":u"Наименование",
		"Vendor":u"Марка",
		"IP Address":u"IP Адрес",
		"Mask":"Маска сети",
		"Gateway":"Шлюз",
		"TCP Port":u"TCP Порт",
		"HTTP Port":u"HTTP Порт",
		"Port":u"Порт",
		"MAC Address":u"МАК Адрес",
		"SN":u"Серийный №",
		"As on PC":u"Как на ПК",
		"Password":u"Пароль",
		"Apply":u"Применить",
		"Search":u"Поиск",
		"Reset":u"Сброс",
		"Export":u"Экспорт",
		"Flash":u"Прошивка",
		"All files":u"Все файлы",
		"Text files":u"Текстовые файлы",
		"Searching %s, found %d devices":u"Поиск %s, нашли %d устройств",
		"Found %d devices":u"Найденно %d устройств",
		"All":"По всем",
		"Error":"Ошибка",
		},
	}
def _(msg):
	if lang in locale.keys():
		if msg in locale[lang].keys():
			return locale[lang][msg]
	return msg
CODES = {
	100:_("Success"),
	101:_("Unknown error"),
	102:_("Version not supported"),
	103:_("Illegal request"),
	104:_("User has already logged in"),
	105:_("User is not logged in"),
	106:_("Username or Password is incorrect"),
	107:_("Insufficient permission"),
	108:_("Timeout"),
	109:_("Find failed, file not found"),
	110:_("Find success, returned all files"),
	111:_("Find success, returned part of files"),
	112:_("User already exists"),
	113:_("User does not exist"),
	114:_("User group already exists"),
	115:_("User group does not exist"),
	116:_("Reserved"),
	117:_("Message is malformed"),
	118:_("No PTZ protocol is set"),
	119:_("No query to file"),
	120:_("Configured to be enabled"),
	121:_("Digital channel is not enabled"),
	150:_("Success, device restart required"),
	202:_("User is not logged in"),
	203:_("Incorrect password"),
	204:_("User is illegal"),
	205:_("User is locked"),
	206:_("User is in the blacklist"),
	207:_("User already logged in"),
	208:_("Invalid input"),
	209:_("User already exists"),
	210:_("Object not found"),
	211:_("Object does not exist"),
	212:_("Account in use"),
	213:_("Permission table error"),
	214:_("Illegal password"),
	215:_("Password does not match"),
	216:_("Keep account number"),
	502:_("Illegal command"),
	503:_("Talk channel has ben opened"),
	504:_("Talk channel is not open"),
	511:_("Update started"),
	512:_("Update did not start"),
	513:_("Update data error"),
	514:_("Update failed"),
	515:_("Update succeeded"),
	521:_("Failed to restore default config"),
	522:_("Device restart required"),
	523:_("Default config is illegal"),
	602:_("Application restart required"),
	603:_("System restart required"),
	604:_("Write file error"),
	605:_("Features are not supported"),
	606:_("Verification failed"),
	607:_("Configuration does not exist"),
	608:_("Configuration parsing error"),
}
def tolog(s):
	print(s)
	if logLevel >= 20:
		logfile = open(log, "a+")
		logfile.write(s)
		logfile.close()
def local_ip():
	ip = gethostbyname_ex(gethostname())[2][0]
	ipn = struct.unpack(">I",inet_aton(ip))
	return (inet_ntoa(struct.pack(">I",ipn[0]+10)),"255.255.255.0",inet_ntoa(struct.pack(">I",(ipn[0]&0xFFFFFF00)+1)))
def sofia_hash(msg):
	s = ""
	md5 = hashlib.md5(msg).digest()
	for n in range(8):
		c = (ord(md5[2*n])+ord(md5[2*n+1]))%62
		if c > 9:
			if c > 35:
				c += 61
			else:
				c += 55
		else:
			c += 48
		s += chr(c)
	return s

def GetIP(s):
	return inet_ntoa(struct.pack('I',int(s,16)))

def SetIP(ip):
	return "0x%08X"%struct.unpack('I',inet_aton(ip))

def SearchXM(devices):
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind(('',34569))
	server.settimeout(1)
	server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	server.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	server.sendto(struct.pack('BBHIIHHI',255,0,0,0,0,0,1530,0),("255.255.255.255", 34569))
	while True:
		try:
			data = server.recvfrom(1024)
			head,ver,typ,session,packet,info,msg,leng = struct.unpack('BBHIIHHI',data[0][:20])
			if (msg == 1531) and leng > 0:
				answer = json.loads(data[0][20:20+leng].replace(b'\x00',b''),encoding="utf8")
				if answer['NetWork.NetCommon']['MAC'] not in devices.keys():
					devices[answer['NetWork.NetCommon']['MAC']] = answer['NetWork.NetCommon']
					devices[answer['NetWork.NetCommon']['MAC']][u'Brand'] = u"xm"
		except:
			break
	server.close()
	return devices

def SearchDahua(devices):
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind(('',5050))
	server.settimeout(1)
	server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	server.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	server.sendto(b'\xa3\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',("255.255.255.255", 5050))
	while True:
		try:
			data = server.recvfrom(1024)
			if data[0][0] == '\xb3' and len(data[0]) > 137:
				answer = {}
				answer[u'Brand'] = u"dahua"
				info,name = struct.unpack('8s16s',data[0][32:56])
				answer[u'HostName'] = name.replace('\x00','')
				ip,mask,gate,dns,answer[u'TCPPort'] = struct.unpack('<IIII26xH',data[0][56:100])
				answer[u'HostIP'],answer[u'Submask'],answer[u'GateWay'],answer[u'DNS'] = "0x%08X"%ip,"0x%08X"%mask,"0x%08X"%gate,"0x%08X"%dns
				answer[u'MAC'] = data[0][120:137]
				answer[u'Model'] = data[0][137:]
				answer[u'HttpPort'] = 80
				answer[u'SN'] = ""
				if answer[u'MAC'] not in devices.keys():
					devices[answer[u'MAC']] = answer
		except:
			break
	server.close()
	return devices

def SearchFros(devices):
	server = socket(AF_INET, SOCK_DGRAM)
	server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	server.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	server.settimeout(1)
	server.sendto(b'MO_I\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x01', ("255.255.255.255", 10000))
	while True:
		try:
			data = server.recvfrom(1024)
			cmd, legth = struct.unpack('<4xh9xi4x',data[0][:23])
			ser, name = struct.unpack('<13s21s',data[0][23:57])
			ip, mask, gate, dns = struct.unpack('<IIII',data[0][57:73])
			ser = ser.replace('\x00','')
			mac = ser[:2]+':'+ser[2:4]+':'+ser[4:6]+':'+ser[6:8]+':'+ser[8:10]+':'+ser[10:12]
			name = name.replace('\x00','')
			ip,mask,gate,dns = "0x%08X"%ip,"0x%08X"%mask,"0x%08X"%gate,"0x%08X"%dns
			ver, webver = struct.unpack('<4s4s',data[0][77:85])
			ver = ".".join([str(ord(x)) for x in ver])
			webver = ".".join([str(ord(x)) for x in webver])
			if mac not in devices.keys():
				devices[mac] = { u'Brand':'fros',u'GateWay' : gate, u'DNS': dns, u'HostIP' : ip, u'HostName' : name, u'HttpPort' : 80, u'TCPPort': 80, u'MAC' : mac, u'MaxBps' : 0, u'MonMode' : u"HTTP", u'SN' : ser, u'Submask' : mask, u'SwVer': ver, u'WebVer': webver }
		except:
			break
	server.close()
	return devices

def SearchWans(devices):
	client = socket(AF_INET, SOCK_DGRAM)
	client.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	client.settimeout(1.3)
	client.sendto(b'DH\x01\x01',("255.255.255.255", 8600))
	while True:
		try:
			data = client.recvfrom(1024)
			mac = [0,0,0,0,0,0]
			head, pver, type, ip, mask, gate, dns2, dns, mac[0], mac[1], mac[2], mac[3], mac[4], mac[5], port, ser, name, ver, webver, user, passwd, dhcp = struct.unpack('2sBB16s16s16s16s16s6BH32s32s48x16s16s32s32sxB22x',data[0][:324])
			mac = "%02x:%02x:%02x:%02x:%02x:%02x"%(mac[0], mac[1], mac[2], mac[3], mac[4], mac[5])
			name,ser,ver,webver = name.replace('\x00',''),ser.replace('\x00',''),ver.replace('\x00',''),webver.replace('\x00','')
			ip,mask,gate,dns = SetIP(ip.replace('\x00','')),SetIP(mask.replace('\x00','')),SetIP(gate.replace('\x00','')),SetIP(dns.replace('\x00',''))
			if mac not in devices.keys():
				devices[mac] = { u"Brand":u"wans",u"GateWay" : gate, u"DNS": dns, u"HostIP" : ip, u"HostName" : name, u"HttpPort" : port, u"TCPPort": port, u"MAC" : mac, u"MaxBps" : 0, u"MonMode" : u"HTTP", u"SN" : ser, u"Submask" : mask, u"SwVer": ver, u"WebVer": webver }
		except:
			break
	client.close()
	return devices

def ConfigXM(data):
	config = {}
	config[u'DvrMac'] = devices[data[1]][u'MAC']
	config[u'EncryptType'] = 1
	config[u'GateWay'] = SetIP(data[4])
	config[u'HostIP'] = SetIP(data[2])
	config[u'HostName'] = devices[data[1]][u'HostName']
	config[u'HttpPort'] = devices[data[1]][u'HttpPort']
	config[u'MAC'] = devices[data[1]][u'MAC']
	config[u'MaxBps'] = devices[data[1]][u'MaxBps']
	config[u'MonMode'] = devices[data[1]][u'MonMode']
	config[u'SSLPort'] = devices[data[1]][u'SSLPort']
	config[u'Submask'] = SetIP(data[3])
	config[u'TCPMaxConn'] = devices[data[1]][u'TCPMaxConn']
	config[u'TCPPort'] = devices[data[1]][u'TCPPort']
	config[u'TransferPlan'] = devices[data[1]][u'TransferPlan']
	config[u'UDPPort'] = devices[data[1]][u'UDPPort']
	config[u'UseHSDownLoad'] = devices[data[1]][u'UseHSDownLoad']
	config[u'Username'] = 'admin'
	config[u'Password'] = sofia_hash(data[5])
	devices[data[1]][u'GateWay'] = config[u'GateWay']
	devices[data[1]][u'HostIP'] = config[u'HostIP']
	devices[data[1]][u'Submask'] = config[u'Submask']
	config = json.dumps(config, ensure_ascii=False, sort_keys=True, separators=(', ', ' : ')).encode('utf8')
	server = socket(AF_INET, SOCK_DGRAM)
	server.bind(('',34569))
	server.settimeout(1)
	server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	server.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	clen = len(config)
	server.sendto(struct.pack('BBHIIHHI%ds2s'%clen,255,0,254,0,0,0,1532,clen+2,config,b'\x0a\x00'),('255.255.255.255', 34569))
	answer = {"Ret":203}
	e=0
	while True:
		try:
			data = server.recvfrom(1024)
			head,ver,typ,session,packet,info,msg,leng = struct.unpack('BBHIIHHI',data[0][:20])
			if (msg == 1533) and leng > 0:
				answer = json.loads(data[0][20:20+leng].replace(b'\x00',b''),encoding='utf8')
				break
		except:
			e += 1
			if e > 3:
				break
	server.close()
	return answer
	
def ConfigFros(data):
	devices[data[1]][u'GateWay'] = SetIP(data[4])
	devices[data[1]][u'HostIP'] = SetIP(data[2])
	devices[data[1]][u'Submask'] = SetIP(data[3])
	client = socket(AF_INET, SOCK_DGRAM)
	client.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	client.sendto(struct.pack('<4sB10xB3xB6xB12sx12sx12sxIIIIxB','MO_I',2,61,61,1,devices[data[1]][u'MAC'].replace(':',''),'admin',data[5],int(SetIP(data[2]),16),int(SetIP(data[3]),16),int(SetIP(data[4]),16),int(SetIP(data[4]),16),80),("255.255.255.255", 10000))
	answer = {}
	while True:
		try:
			data = client.recvfrom(1024)
			if data[0][4] == '\x03':
				s, type, n, n, result = struct.unpack('<4sB10xB3xB3xBx',data[0])
				if result == 0:
					answer[u'Ret'] = 100
				else:
					answer[u'Ret'] = 101
			break
		except:
			break
			e = 1
	client.close()
	return answer

def ConfigWans(data):
	devices[data[1]][u'GateWay'] = SetIP(data[4])
	devices[data[1]][u'HostIP'] = SetIP(data[2])
	devices[data[1]][u'Submask'] = SetIP(data[3])
	devices[data[1]][u'TCPPort'] = devices[data[1]][u'HttpPort']
	client = socket(AF_INET, SOCK_DGRAM)
	#client.bind(('',8600))
	client.settimeout(1)
	client.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
	mac = [int(x,16) for x in data[1].split(":")]
	client.sendto(struct.pack('2sBB16s16s16s16s16s6BH32s32s48x16s16s32s32sxB22x','DH', 2, 1, data[2], data[3], data[4], '8.8.8.8', data[4], mac[0], mac[1], mac[2], mac[3], mac[4], mac[5], devices[data[1]][u'HttpPort'], devices[data[1]][u'SN'], devices[data[1]][u'HostName'], devices[data[1]][u'SwVer'], devices[data[1]][u'WebVer'], 'admin', data[5], 0),("255.255.255.255", 8600))
	answer = {}
	while True:
		try:
			data = client.recvfrom(1024)
			mac = [0,0,0,0,0,0]
			head, pver, type, ip, mask, gate, dns2, dns, mac[0], mac[1], mac[2], mac[3], mac[4], mac[5], port, ser, name, ver, webver, user, passwd, dhcp, err = struct.unpack('2sBB16s16s16s16s16s6BH32s32s48x16s16s32s32sxB22xB',data[0][:325])
			mac = "%02x:%02x:%02x:%02x:%02x:%02x"%(mac[0], mac[1], mac[2], mac[3], mac[4], mac[5])
			name,ser,ver,webver = name.replace('\x00',''),ser.replace('\x00',''),ver.replace('\x00',''),webver.replace('\x00','')
			ip,mask,gate,dns = SetIP(ip.replace('\x00','')),SetIP(mask.replace('\x00','')),SetIP(gate.replace('\x00','')),SetIP(dns.replace('\x00',''))
			devices[mac] = { u"Brand":u"wans",u"GateWay" : gate, u"DNS": dns, u"HostIP" : ip, u"HostName" : name, u"HttpPort" : port, u"TCPPort": port, u"MAC" : mac, u"MaxBps" : 0, u"MonMode" : u"HTTP", u"SN" : ser, u"Submask" : mask, u"SwVer": ver, u"WebVer": webver }
			if err == 0:
				answer[u'Ret'] = 100
			else:
				answer[u'Ret'] = 101
			break
		except:
			break
			e = 1
	client.close()
	return answer

def ProcessCMD(cmd):
	global log,logLevel,devices,searchers,configure,flashers
	if logLevel == 20:
		tolog(datetime.now().strftime("[%Y-%m-%d %H:%M:%S] >")+" ".join(cmd))
	if (cmd[0].lower() == 'q' or cmd[0].lower() == 'quit'):
		sys.exit(1)
	if cmd[0].lower() in ["help","?","/?","-h","--help"]:
		return help
	if cmd[0].lower() == "search":
		if len(cmd) > 1 and cmd[1].lower() in searchers.keys():
			try:
				devices = searchers[cmd[1].lower()](devices)
			except Exception as error:
				print(" ".join([str(x) for x in list(error.args)]))
			print(_("Searching %s, found %d devices")%(cmd[1],len(devices)))
		else:
			for s in searchers:
				tolog(_("Search")+" %s\r"%s)
				try:
					devices = searchers[s](devices)
				except Exception as error:
					print(" ".join([str(x) for x in list(error.args)]))
			tolog(_("Found %d devices")%len(devices))
		if len(devices) > 0:
			if logLevel > 0:
				cmd[0] = "table"
				print("")
	if cmd[0].lower() == "table":
		logs = _("Vendor")+"\t"+_("MAC Address")+"\t\t"+_("Name")+"\t"+_("IP Address")+"\t"+_("Port")+"\n"
		for dev in devices:
			logs += "%s\t%s\t%s\t%s\t%s\n"%(devices[dev]['Brand'],devices[dev]['MAC'],devices[dev]['HostName'],GetIP(devices[dev]['HostIP']),devices[dev]['TCPPort'])
		if logLevel >= 20: tolog(logs)
		if logLevel >= 10: return logs
	if cmd[0].lower() == "csv":
		logs = _("Vendor")+";"+_("MAC Address")+";"+_("Name")+";"+_("IP Address")+";"+_("Port")+";"+_("SN")+"\n"
		for dev in devices:
			logs += '%s;%s;%s;%s;%s;%s\n'%(devices[dev]['Brand'],devices[dev]['MAC'],devices[dev]['HostName'],GetIP(devices[dev]['HostIP']),devices[dev]['TCPPort'],devices[dev]['SN'])
		if logLevel >= 20: tolog(logs)
		if logLevel >= 10: return logs
	if cmd[0].lower() == "html":
		logs = "<table border=1><th>"+_("Vendor")+"</th><th>"+_("MAC Address")+"</th><th>"+_("Name")+"</th><th>"+_("IP Address")+"</th><th>"+_("Port")+"</th><th>"+_("SN")+"</th>\r\n"
		for dev in devices:
			logs += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\r\n"%(devices[dev]['Brand'],devices[dev]['MAC'],devices[dev]['HostName'],GetIP(devices[dev]['HostIP']),devices[dev]['TCPPort'],devices[dev]['SN'])
		logs += "</table>\r\n"
		if logLevel >= 20: tolog(logs)
		if logLevel >= 10: return logs
	if cmd[0].lower() == "json":
		logs = json.dumps(devices)
		if logLevel >= 20: tolog(logs)
		if logLevel >= 10: return logs
	if cmd[0].lower() == "device":
		if len(cmd) > 1 and cmd[1] in devices.keys():
			return json.dumps(devices[cmd[1]])
		else:
			return "device [MAC]"
	if cmd[0].lower() == "config":
		if len(cmd) > 5 and cmd[1] in devices.keys() and devices[cmd[1]]['Brand'] in configure.keys():
			return configure[devices[cmd[1]]['Brand']](cmd)
		else:
			return "config [MAC] [IP] [MASK] [GATE] [Pasword]"
	if cmd[0].lower() == "flash":
		if len(cmd) > 2 and cmd[1] in devices.key(s) and devices[cmd[1]]['Brand'] in flashers.keys():
			return flashers[devices[cmd[1]]['Brand']](cmd)
		else:
			return "flash [MAC] [file]"
	if cmd[0].lower() == "loglevel":
		if len(cmd) > 1:
			logLevel = int(cmd[1])
		else:
			return "loglevel [int]"
	if cmd[0].lower() == "log":
		if len(cmd) > 1:
			log = " ".join(cmd[1:])
		else:
			return "log [filename]"
	if cmd[0].lower() == "echo":
		if len(cmd) > 1:
			return " ".join(cmd[1:])
	return ""
class GUITk:
	def __init__(self,root):
		self.root=root
		self.root.wm_title(_("Device Manager"))
		self.root.tk.call('wm', 'iconphoto', root._w, PhotoImage(data=icon))
		self.f = ttk.Frame(self.root)
		self.f.pack(fill=BOTH, expand=YES)

		self.fr = ttk.Frame(self.f)
		self.fr.grid(row=0, column=0, columnspan=3, sticky="nsew")
		self.fr_tools = ttk.Frame(self.f)
		self.fr_tools.grid(row=1, column=0, columnspan=3, sticky="ew")
		self.fr_config = ttk.Frame(self.f)
		self.fr_config.grid(row=0, column=5, rowspan=2, sticky="nsew")

		self.table = ttk.Treeview(self.fr, show='headings', selectmode='browse', height=10)
		self.table.grid(column=0, row=0, sticky="nsew")
		self.table["columns"]=("ID","vendor","addr","port","name","mac","sn")
		self.table["displaycolumns"]=("vendor","addr","port","name","mac","sn")

		self.table.heading("vendor", text=_("Vendor"), anchor='w')
		self.table.heading("addr", text=_("IP Address"), anchor='w')
		self.table.heading("port", text=_("Port"), anchor='w')
		self.table.heading("name", text=_("Name"), anchor='w')
		self.table.heading("mac", text=_("MAC Address"), anchor='w')
		self.table.heading("sn", text=_("SN"), anchor='w')

		self.table.column("vendor", stretch=0, width=50)
		self.table.column("addr", stretch=0, width=100)
		self.table.column("port", stretch=0, width=50)
		self.table.column("name", stretch=0, width=100)
		self.table.column("mac", stretch=0, width=110)
		self.table.column("sn", stretch=0, width=120)

		self.scrollY = ttk.Scrollbar(self.fr, orient=VERTICAL)
		self.scrollY.config(command=self.table.yview)
		self.scrollY.grid(row=0, column=1, sticky="ns")
		self.scrollX = ttk.Scrollbar(self.fr, orient=HORIZONTAL)
		self.scrollX.config(command=self.table.xview)
		self.scrollX.grid(row=1, column=0, sticky="ew")
		self.table.config(yscrollcommand=self.scrollY.set,xscrollcommand=self.scrollX.set)

		self.table.bind('<ButtonRelease>', self.select)

		self.l0 = ttk.Label(self.fr_config, text=_("Name"))
		self.l0.grid(row=0, column=0,pady=3,padx=5,sticky=W+N)
		self.name = ttk.Entry(self.fr_config, width=15, font="6")
		self.name.grid(row=0, column=1,pady=3,padx=5,sticky=W+N)
		self.l1 = ttk.Label(self.fr_config, text=_("IP Address"))
		self.l1.grid(row=1, column=0,pady=3,padx=5,sticky=W+N)
		self.addr = ttk.Entry(self.fr_config, width=15, font="6")
		self.addr.grid(row=1, column=1,pady=3,padx=5,sticky=W+N)
		self.l2 = ttk.Label(self.fr_config, text=_("Mask"))
		self.l2.grid(row=2, column=0,pady=3,padx=5,sticky=W+N)
		self.mask = ttk.Entry(self.fr_config, width=15, font="6")
		self.mask.grid(row=2, column=1,pady=3,padx=5,sticky=W+N)
		self.l3 = ttk.Label(self.fr_config, text=_("Gateway"))
		self.l3.grid(row=3, column=0,pady=3,padx=5,sticky=W+N)
		self.gate = ttk.Entry(self.fr_config, width=15, font="6")
		self.gate.grid(row=3, column=1,pady=3,padx=5,sticky=W+N)
		self.aspc = ttk.Button(self.fr_config, text=_("As on PC"),command=self.addr_pc)
		self.aspc.grid(row=4, column=1,pady=3,padx=5,sticky="ew")
		self.l4 = ttk.Label(self.fr_config, text=_("HTTP Port"))
		self.l4.grid(row=5, column=0,pady=3,padx=5,sticky=W+N)
		self.http = ttk.Entry(self.fr_config, width=5, font="6")
		self.http.grid(row=5, column=1,pady=3,padx=5,sticky=W+N)
		self.l5 = ttk.Label(self.fr_config, text=_("TCP Port"))
		self.l5.grid(row=6, column=0,pady=3,padx=5,sticky=W+N)
		self.tcp = ttk.Entry(self.fr_config, width=5, font="6")
		self.tcp.grid(row=6, column=1,pady=3,padx=5,sticky=W+N)
		self.l6 = ttk.Label(self.fr_config, text=_("Password"))
		self.l6.grid(row=7, column=0,pady=3,padx=5,sticky=W+N)
		self.passw = ttk.Entry(self.fr_config, width=15, font="6")
		self.passw.grid(row=7, column=1,pady=3,padx=5,sticky=W+N)
		self.aply = ttk.Button(self.fr_config, text=_("Apply"),command=self.setconfig)
		self.aply.grid(row=8, column=1,pady=3,padx=5,sticky="ew")
		
		self.l7 = ttk.Label(self.fr_tools, text=_("Vendor"))
		self.l7.grid(row=0, column=0,pady=3,padx=5,sticky="wns")
		self.ven = ttk.Combobox(self.fr_tools, width=10)
		self.ven.grid(row=0, column=1,padx=5,sticky="w")
		self.ven['values'] = [_("All"), "XM", "Dahua", "Fros", "Wans"]
		self.ven.current(0)
		self.search = ttk.Button(self.fr_tools, text=_("Search"),command=self.search)
		self.search.grid(row=0, column=2,pady=5,padx=5,sticky=W+N)
		self.reset = ttk.Button(self.fr_tools, text=_("Reset"),command=self.clear)
		self.reset.grid(row=0, column=3,pady=5,padx=5,sticky=W+N)
		self.exp = ttk.Button(self.fr_tools, text=_("Export"),command=self.export)
		self.exp.grid(row=0, column=4,pady=5,padx=5,sticky=W+N)
		self.fl = ttk.Button(self.fr_tools, text=_("Flash"),command=self.flash)
		self.fl.grid(row=0, column=5,pady=5,padx=5,sticky=W+N)

	def addr_pc(self):
		_addr,_mask,_gate = local_ip()
		self.addr.delete(0, END)
		self.addr.insert(END, _addr)
		self.mask.delete(0, END)
		self.mask.insert(END, _mask)
		self.gate.delete(0, END)
		self.gate.insert(END, _gate)
	def search(self):
		self.clear()
		if self.ven['values'].index(self.ven.get()) == 0:
			ProcessCMD(["search"])
		else:
			ProcessCMD(["search",self.ven.get()])
		self.pop()
	def pop(self):
		for dev in devices:
			self.table.insert('', 'end', values=(dev,devices[dev]['Brand'], GetIP(devices[dev]['HostIP']), devices[dev]['TCPPort'], devices[dev]['HostName'], devices[dev]['MAC'],  devices[dev]['SN']))
	def clear(self):
		global devices
		for i in self.table.get_children():
			self.table.delete(i)
		devices = {}
	def select(self, event):
		if len(self.table.selection()) == 0:
			return
		dev = self.table.item(self.table.selection()[0], option='values')[0]
		if logLevel >= 20 : print(json.dumps(devices[dev], indent = 4, sort_keys = True))
		self.name.delete(0, END)
		self.name.insert(END, devices[dev]['HostName'])
		self.addr.delete(0, END)
		self.addr.insert(END, GetIP(devices[dev]['HostIP']))
		self.mask.delete(0, END)
		self.mask.insert(END, GetIP(devices[dev]['Submask']))
		self.gate.delete(0, END)
		self.gate.insert(END, GetIP(devices[dev]['GateWay']))
		self.http.delete(0, END)
		self.http.insert(END, devices[dev]['HttpPort'])
		self.tcp.delete(0, END)
		self.tcp.insert(END, devices[dev]['TCPPort'])
	def setconfig(self):
		dev = self.table.item(self.table.selection()[0], option='values')[0]
		devices[dev][u'TCPPort'] = int(self.tcp.get())
		devices[dev][u'HttpPort'] = int(self.http.get())
		devices[dev][u'HostName'] = self.name.get()
		result = ProcessCMD(["config",dev,self.addr.get(),self.mask.get(),self.gate.get(),self.passw.get()])
		if result['Ret'] == 100:
			self.table.item(self.table.selection()[0], values=(dev,devices[dev]['Brand'], GetIP(devices[dev]['HostIP']), devices[dev]['TCPPort'], devices[dev]['HostName'], devices[dev]['MAC'],  devices[dev]['SN']))
		else:
			showerror(_("Error"),CODES[result['Ret']])
	def export(self):
		filename = asksaveasfilename(filetypes = ((_("JSON files"), "*.json")
								,(_("HTML files"), "*.html;*.htm")
								,(_("Text files"), "*.csv;*.txt")
								,(_("All files"), "*.*") ))
		if filename == "":
			return
		ProcessCMD(["log",filename])
		ProcessCMD(["loglevel", str(100)])
		if ".json" in filename:
			ProcessCMD(["json"])
		elif ".csv" in filename:
			ProcessCMD(["csv"])
		elif ".htm" in filename:
			ProcessCMD(["html"])
		else:
			ProcessCMD(["table"])
		ProcessCMD(["loglevel", str(10)])
	def flash(self):
		filename = askopenfilename(filetypes = ((_("Flash"), "*.bin")
									,(_("All files"), "*.*") ))
		if filename == "":
			return
		if len(self.table.selection()) == 0:
			_mac="all"
		else:
			_mac = self.table.item(self.table.selection()[0], option='values')[4]
		result = ProcessCMD(["flash",_mac,filename])
		if hasattr(result, 'keys') and 'Ret' in result.keys() and result['Ret'] in CODES.keys(): showerror(_("Error"),CODES[result['Ret']])

class GUIKivy(App):
	def _(self,t):
		return _(t)
	def build(self):
		class IORedirector(object):
			def __init__(self,TEXT_INFO):
				self.TEXT_INFO = TEXT_INFO
			def write(self,str):
				if len(str) > 1: self.TEXT_INFO.text=str
		root = Builder.load_string('''
PageLayout:
    BoxLayout:
        orientation: 'vertical'
        canvas:
            Color:
                rgba: 0, 0, 0, 1
            Rectangle:
                pos: self.pos
                size: self.size
        BoxLayout:
            size_hint_y: None
            height: dp(20)
            canvas:
                Color:
                    rgba: .3, .3, .3, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                size_hint_x: .2
                text: app._("IP Address")
            Label:
                size_hint_x: .1
                text:app._("Vendor")
            Label:
                size_hint_x: .1
                text: app._("Port")
            Label:
                size_hint_x: .2
                text: app._("Name")
            Label:
                size_hint_x: .21
                text: app._("MAC Address")
            Label:
                size_hint_x: .22
                text: app._("SN")
        ListView:
            id: table
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            Spinner:
                id: ven
                size_hint_x: None
                width: dp(100)
                font_size: dp(18)
                text: app._('All')
                values: [app._('All'),'XM', 'Dahua', 'Fros','Wans']
            Button:
                size_hint_x: None
                width: dp(100)
                text: app._("Search")
                font_size: dp(18)
                on_release: app.search()
            Button:
                size_hint_x: None
                width: dp(100)
                text: app._("Reset")
                font_size: dp(18)
                on_release: app.clear()
            Button:
                size_hint_x: None
                width: dp(100)
                text: app._("Export")
                font_size: dp(18)
            Button:
                size_hint_x: None
                width: dp(100)
                text: app._("Flash")
                font_size: dp(18)
            Label:
                id: info
                font_size: dp(18)
                text: " "
    GridLayout:
        cols: 2
        row_force_default: True
        row_default_height:dp(30)
        spacing: [dp(30),dp(5)]
        padding: [dp(10), dp(10)]
        canvas:
            Color:
                rgba: .1, .1, .1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            halign: 'right'
            text: app._("Name")
        TextInput:
            id: name
            text: ""
        Label:
            halign: 'right'
            text: app._("IP Address")
        TextInput:
            id: addr
            text: ""
        Label:
            halign: 'right'
            text: app._("Mask")
        TextInput:
            id: mask
            text: ""
        Label:
            halign: 'right'
            text: app._("Gateway")
        TextInput:
            id: gate
            text: ""
        Label:
            halign: 'right'
            text: app._("HTTP Port")
        TextInput:
            id: http
            text: ""
        Label:
            halign: 'right'
            text: app._("TCP Port")
        TextInput:
            id: tcp
            text: ""
        Label:
            id: label2
            halign: 'right'
            text: app._("Password")
        TextInput:
            id: passw
            text: ""
        Button:
            text: app._("Apply")
''')
		self.table = root.ids.table
		self.table.adapter = ListAdapter(
						data=[], 
						cls=CompositeListItem, selection_mode='single', 
						args_converter=lambda row_index, rec: {'text': rec['mac'],'size_hint_y': None,'height': dp(35),
							'cls_dicts': [
								{'cls': ListItemButton,'kwargs': {'id':rec['mac'],'text': str(rec['addr']),'size_hint_x': .2,'font_size':dp(18)}},
								{'cls': ListItemLabel,'kwargs': {'text': rec['vendor'],'size_hint_x': .1,'padding':(dp(1),0),'font_size':dp(18)}},
								{'cls': ListItemLabel,'kwargs': {'text': str(rec['port']),'size_hint_x': .1,'padding':(dp(1),0),'font_size':dp(18)}},
								{'cls': ListItemLabel,'kwargs': {'text': rec['name'],'size_hint_x': .2,'padding':(dp(1),0),'font_size':dp(18)}},
								{'cls': ListItemLabel,'kwargs': {'text': rec['mac'],'size_hint_x': .21,'padding':(dp(1),0),'font_size':dp(18)}},
								{'cls': ListItemLabel,'kwargs': {'text': rec['sn'],'size_hint_x': .22,'is_representing_cls': True,'font_size':dp(18)}}
							]})
		self.table.adapter.bind(on_selection_change=self.select)
		#sys.stdout=IORedirector(root.ids.info)
		return root
	def search(self):
		self.clear()
		if self.root.ids.ven.values.index(self.root.ids.ven.text) == 0:
			ProcessCMD(["search"])
		else:
			ProcessCMD(["search",self.root.ids.ven.text])
		self.pop()
	def pop(self):
		for dev in devices:
			self.table.adapter.data.append({'addr':GetIP(devices[dev]['HostIP']),'vendor':devices[dev]['Brand'],'port':devices[dev]['TCPPort'],"name":devices[dev]['HostName'],"mac":devices[dev]['MAC'],"sn":devices[dev]['SN']})
	def clear(self):
		global devices
		self.table.adapter.data = []
		self.root.ids.info.text = ""
		devices = {}
	def select(self, event=None):
		if len(self.table.adapter.selection) == 0:
			return
		dev = self.table.adapter.selection[0].id
		if logLevel >= 20 : print(json.dumps(devices[dev], indent = 4, sort_keys = True))
		self.root.ids.name.text=devices[dev]['HostName']
		self.root.ids.addr.text=GetIP(devices[dev]['HostIP'])
		self.root.ids.mask.text=GetIP(devices[dev]['Submask'])
		self.root.ids.gate.text=GetIP(devices[dev]['GateWay'])
		self.root.ids.http.text=str(devices[dev]['HttpPort'])
		self.root.ids.tcp.text=str(devices[dev]['TCPPort'])
	def setconfig(self):
		if len(self.table.adapter.selection) == 0:
			return
		dev = self.table.adapter.selection[0].id
		devices[dev][u'TCPPort'] = int(self.root.ids.tcp.text)
		devices[dev][u'HttpPort'] = int(self.root.ids.http.text)
		devices[dev][u'HostName'] = self.root.ids.name.text
		result = ProcessCMD(["config",dev,self.root.ids.addr.text,self.root.ids.mask.text,self.root.ids.gate.text,self.root.ids.passw.text])
		if result['Ret'] == 100:
			for i in range(0,len(self.table.adapter.data)):
				if self.table.adapter.data[i]["mac"] == dev:
					self.table.adapter.data[i]["addr"]=GetIP(devices[dev]['HostIP'])
					self.table.adapter.data[i]["port"]=devices[dev]['TCPPort']
					self.table.adapter.data[i]["name"]=devices[dev]['HostName']
		else:
			showerror(_("Error"),CODES[result['Ret']])
	def export(self):
		filename = "dump.json"
		if filename == "":
			return
		ProcessCMD(["log",filename])
		ProcessCMD(["loglevel", str(100)])
		if ".json" in filename:
			ProcessCMD(["json"])
		elif ".csv" in filename:
			ProcessCMD(["csv"])
		elif ".htm" in filename:
			ProcessCMD(["html"])
		else:
			ProcessCMD(["table"])
		ProcessCMD(["loglevel", str(10)])
	def flash(self):
		filename = ""
		if filename == "":
			return
		if len(self.table.selection()) == 0:
			_mac="all"
		else:
			_mac = self.table.item(self.table.selection()[0], option='values')[4]
		result = ProcessCMD(["flash",_mac,filename])
		if hasattr(result, 'keys') and 'Ret' in result.keys() and result['Ret'] in CODES.keys(): showerror(_("Error"),CODES[result['Ret']])

searchers = {"wans":SearchWans,"xm":SearchXM,"dahua":SearchDahua,"fros":SearchFros,}
configure = {"wans":ConfigWans,"xm":ConfigXM,"fros":ConfigFros}#,"dahua":ConfigDahua
flashers  = {}#"xm":FlashXM,"dahua":FlashDahua,"fros":FlashFros
logLevel = 10
if __name__ == "__main__":
	if len(sys.argv) > 1:
		cmds = " ".join(sys.argv[1:])
		if cmds.find("-q ") != -1:
			cmds = cmds.replace("-q ","").replace("-n ","").strip()
			logLevel = 0
		for cmd in cmds.split(";"):
			ProcessCMD(cmd.split(" "))
	if GUI_TK and "-n" not in sys.argv:
		root = Tk()
		app = GUITk(root)
		#Style = ttk.Style()
		#ttk.Style.theme_use(Style, "clam")
		root.mainloop()
		sys.exit(1)
	if GUI_Kivy and "-n" not in sys.argv:
		app = GUIKivy()
		app.run()
		sys.exit(1)
	print(_("Type help or ? to display help(q or quit to exit)"))
	while True:
		data = raw_input("> ").split(";")
		for cmd in data:
			result = ProcessCMD(cmd.split(" "))
			if hasattr(result, 'keys') and 'Ret' in result.keys():
				print(CODES[result['Ret']])
			else:
				print(result)
	sys.exit(1)
