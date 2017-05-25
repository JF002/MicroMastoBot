import pycom
pycom.heartbeat(True)

import machine
from network import WLAN
import utime
import urequest
import gc
import ujson

tootUser=""
sendToot = False

def onData(r):
	global tootUser
	global sendToot
	ret = True

	strInput = r.text()
	if strInput[0] == ':':
		return ret

	print("Message received : ")
	print(str(r.text()))
	strInput = strInput[6:-1]
	obj = ujson.loads(strInput)

	remoteUser = obj['account']['acct']
	print("This message is from " + remoteUser)

	m = obj['status']['mentions'][0]['acct']
	if m != None:
		print("Mention : " + m)

	if obj['status']['mentions'][0]['acct'] == 'LopyBoard2':
		sendToot = True
		ret = False
		tootUser = remoteUser
		print("This message is for me!")

	return ret

wlan = WLAN()
if machine.reset_cause != machine.SOFT_RESET:
	wlan.init(mode=WLAN.STA)

if not wlan.isconnected():
	wlan.connect(ssid='WIFI_SSID', auth=(WLAN.WPA2, '********'))
	while not wlan.isconnected():
		utime.sleep_ms(10)

print(wlan.ifconfig())

print("Request instance information")
r = urequest.get("https://mastodon.codingfield.com/api/v1/instance", headers={'Authorization': 'Bearer 1111111122222222333333334444444455555555666666667777777788888888'}	)
if r is not None:
	print(r.text)
else:
	print("No response")

while(True):
	print("Listening for messages from instance...")
	r = urequest.get("https://mastodon.codingfield.com/api/v1/streaming/user", headers={'Authorization': 'Bearer 1111111122222222333333334444444455555555666666667777777788888888'}, stream=onData	)
	if r is not None:
		print(r.text)
	else:
		print("No response")

	if sendToot :
		print("Sending a toot")
		sendToot = False
		rr = urequest.post('https://mastodon.codingfield.com/api/v1/statuses?status=Hello+@'+tootUser+',+this+toot+was+sent+by+a+Lopy+board+based+on+ESP32+and+running+Micropython&visibility=direct', headers={'Authorization': 'Bearer 1111111122222222333333334444444455555555666666667777777788888888'})
		if rr is not None:
			print(rr.text)
		else:
			print("No response")

print("END")
