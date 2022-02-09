title = '''
   __ _     _           __     _   
  / /(_)___| |_ ___  /\ \ \___| |_ 
 / / | / __| __/ _ \/  \/ / _ \ __|
/ /__| \__ \ ||  __/ /\  /  __/ |_ 
\____/_|___/\__\___\_\ \/ \___|\__|
                                   
'''

import os, subprocess, re, time, smtplib, sys
from email.mime.text import MIMEText

# Network Scan (MAC Address)
def MacScan():
	global MAC
	p = subprocess.Popen("arp -an | awk '{print $4}'", stdout=subprocess.PIPE, shell=True)
	MACs = p.communicate()
	MACs = ''.join(map(str, MACs))
	MACs = MACs[2:]
	MACs = MACs[:-5]
	MAC = MACs.split('\\n')
	del MAC[-1]
	return
	
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# Network Scan (IP Address)
def IpScan():
	global IP
	p = subprocess.Popen("arp -an | awk '{print $2}'", stdout=subprocess.PIPE, shell=True)
	IPs = p.communicate()
	IPs = ''.join(map(str, IPs))
	IPs = IPs[2:]
	IPs = IPs[:-5]
	IP = IPs.split('\\n')
	return

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

def JoinMacIp():
	global NET
	NET = []
	xMAC = MAC
	for i in range(len(xMAC)):
		xMAC[i] +=  '    '
		xMAC[i] += IP[i]
	NET = xMAC
	return

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# Identifies the manufacturer of the device
def FindVendor(MAC):
	with open("VMAC.txt", "r") as f:
		lines = f.readlines()
		f.close()

	MAC = MAC.split(":")
	for i in range(len(MAC)):
		if (len(MAC[i]) < 2):
			MAC[i] = "0" + MAC[i]
		else:
			pass
	MAC = ''.join(map(str, MAC))
	MAC = MAC[:6].upper()

	for i in range(len(lines)):
		if (MAC in lines[i]):
			vendor = lines[i][8:]
			break
		else:
			vendor = '\n'
	return vendor

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

def ListCheck():
	global NMAC

	# Reads MAC addresses present in the MacLog text file
	RMAC = []
	with open('MacLog.txt', 'r') as f:
		RMAC = f.readlines()
		f.close()
		RMAC = ''.join(map(str, RMAC))
		RMAC = RMAC.split('\n')
		del RMAC[-1]

	# Compare the addresses in the maclog file with those in the new scan
	NMAC = []
	x = 0
	for x in range(len(MAC)):
		y = MAC[x]
		if (y in RMAC):
			gg=0
		else:
			NMAC.append(MAC[x])
	return

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# Input commands prompt
def GetInput():
	global ft
	if (ft == False):
		print("An old scan is available, do you want to override the latest scansion log? [y/N]")
		edit = str(input('> '))
		if (edit == 'y' or edit == 'Y'):
			with open('MacLog.txt', 'w+') as f:
				f.close()
			ft = True
		else:
			pass
	else:
		pass
	print("Please enter the scan range \n(deault: '"+str(broadcast2)+" - "+str(broadcast)+"') \n{leave blank for default}\nSintax: [lowerIP],[higherIP] \n")
	scan_ran = str(input('> '))
	print("Please enter the refresh rate you prefer (in seconds)")
	try:
		sec_delay = int(input('> '))
	except:
		print("Not a valid delay value")
		sys.exit()
	print("Please enter the sender email (gmail) with it's password and the receiver email (free choice).\nSintax: [sendermail],[password],[receivermail] \n")
	creds = str(input('> '))
	creds = ''.join(map(str, creds))
	creds = creds.split(',')
	os.system("clear")
	print(str(title)+"\ndaemon started!\n(press ctrl+c to quit)\nlistening...")
	return scan_ran, sec_delay, creds

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# Sends the notifier email
def SendMail(smail, passw, rmail, new_connections):
    msg = MIMEText('New device connected to your local network! \n' + str(new_connections))

    me = smail
    you = rmail
    msg['Subject'] = 'ListeNet Warning!'
    msg['From'] = str(me)
    msg['To'] = str(you)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(me, str(passw))
    s.sendmail(me, [you], msg.as_string())
    s.quit
    print('Warning mail sent successfully.')
    return

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

def LastVal(ip):
	sez_ip = ip.split(".")
	lval = sez_ip[3]
	return lval

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

global broadcast, broadcast2
i=0
n=0
useless = ["(incomplete)", "1:0:5e:7f:ff:fa", "1:0:5e:0:0:fb", "ff:ff:ff:ff:ff:ff"]
print(title)

# Defines whether the program has been started for the first time or not
try:
	with open('MacLog.txt', 'r') as f:
		f.close()
	ft = False
except:
	with open('MacLog.txt', 'w+') as f:
		f.close()
	ft = True

# Automatically finds the netmask to operate on
p = subprocess.Popen("ifconfig | grep broadcast | awk '{print $6}' | head -1", stdout=subprocess.PIPE, shell=True)
broadcast = p.communicate()
broadcast = ''.join(map(str, broadcast))
broadcast = broadcast[2:][:-7]
broadcast_parts = broadcast.split(".")
broadcast_last = int(LastVal(broadcast))-1
broadcast = str(broadcast_parts[0]) + "." + str(broadcast_parts[1]) + "." + str(broadcast_parts[2] + "." + str(broadcast_last))
broadcast_prefix = str(broadcast_parts[0]) + "." + str(broadcast_parts[1]) + "." + str(broadcast_parts[2])
broadcast2 = str(broadcast_prefix) + ".1"

scan_ran, sec_delay, creds = GetInput()
try:
	crdt, crdt1, crdt2 = creds[0], creds[1], creds[2]
except:
	os.system("clear")
	print("Error: not valid credits")
	scan_ran, sec_delay, creds = GetInput()

if (len(scan_ran) > 6):
	scan_ran = scan_ran.split(",")
	minVal = LastVal(scan_ran[0])
	maxVal = LastVal(scan_ran[1])
	iprefix = scan_ran[0].split(".")
	iprefix = str(iprefix[0]) + "." + str(iprefix[1]) + "." + str(iprefix[2] + ".")
	try:
		os.system("for i in {"+str(minVal)+".."+str(maxVal)+"} ;do (ping "+str(iprefix)+".$i -c 1 -W 5  >/dev/null &) ;done")
	except:
		os.system("for i in {1.."+str(broadcast_last)+"} ;do (ping "+str(broadcast_prefix)+".$i -c 1 -W 5  >/dev/null &) ;done")
else:
	os.system("for i in {1.."+str(broadcast_last)+"} ;do (ping "+str(broadcast_prefix)+".$i -c 1 -W 5  >/dev/null &) ;done")

while True:
	if (ft == True):
		MacScan()
		IpScan()
		with open('MacLog.txt', 'a') as f:
			for i in range(len(MAC)):
				if (MAC[i] not in useless):
					f.write(str(IP[i][1:][:-1]))
					f.write('\t' + str(MAC[i]))
					vendor = FindVendor(MAC[i])
					f.write('\t' + str(vendor))
				else:
					pass
			f.close()
		JoinMacIp()
		ft = False
	else:
		MacScan()
		IpScan()
		with open('MacLog.txt', 'r') as f:
			lines = f.readlines()
			lines = ''.join(map(str, lines))
			lines = lines.split('\t')
			f.close()
		with open('MacLog.txt', 'a') as f:
			for i in range(len(MAC)):
				if (MAC[i] not in useless and MAC[i] not in lines):
					f.write(str(IP[i][1:][:-1]))
					f.write('\t' + str(MAC[i]))
					vendor = FindVendor(MAC[i])
					f.write('\t' + str(vendor))
					nw_dev = str(IP[i][1:][:-1]) + '\t' + str(MAC[i]) + '\t' + str(vendor)
					SendMail(crdt, crdt1, crdt2, nw_dev)
				else:
					pass
			f.close()
		ListCheck()
	time.sleep(sec_delay)
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
