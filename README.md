# ListeNet

A network listening tool that notifies via mail whenever a new device is connected, providing IP, MAC addresses and the vendor as well
(read notes below)

## Description

This tool is a deamon that keeps track of the devices connected to the both wired and wireless local network and when a new one is connected the script immediately gets the IP address and, from it, the MAC address that uses to discover the device's vendor using a small local database (VMAC) and sends all the information to the given mail.
The new devices discovered are then saved into another database (MacLog) and the script compares every detected device with the device list in the database to check if it already exists.
(NOTE: By default the script works with gmail accounts as senders, if you want to use a different one just edit the smtp port in the script.)


## Getting Started

## Requirements
* Python 3.x
* If you use a gmail account, make sure to enable the Third-Party access to the sender account ([Guide Here](https://support.google.com/accounts/answer/3466521))

### Dependencies
* All imported libraries are default python libraries
* The script is developed in order to work on UNIX-Like systems

### Installing

How to install the program
 ```
 $ git clone https://github.com/aledipa/ListeNet.git
 $ cd ListeNet/
 ```

### Executing program
 
Execute as script
```
# Run the script
$ python3 ListeNet.py

# If you already used the script and want to keep the data, enter N
An old scan is available, do you want to override the latest scansion log? 
[y/N]
> n

# Enter the IP scan range: [min], [max]
> 172.20.10.1, 172.20.10.14

# Enter the seconds delay from a scan to anotehr
> 25

# Enter the password which sends the notifications, it's password and then the receiver mail
# (The sender must be a gmail address, the receiver could be everything)
# Syntax: [sendermail],[password],[receivermail] 
> sendermail@gmail.com, myMailPass123, target@mail.com
```

## Help
For other issues try to update your python version
```
# Check your python version (should be at least 3.0)
$ python -v

# Force execute the script using python 3 over python 2.x
$ python3 ListeNet.py
```

## Authors
Alessandro Di Pasquale: [@AleDipa](https://github.com/aledipa)

## Version History

* 0.1
    * Initial Release
    * See [commit change](https://github.com/aledipa/ListeNet/commits/main) or See [release history](https://github.com/aledipa/ListeNet/releases/)

## Notes
This project was developed a bunch of years ago when i was still learning the Python language, the current version may be a bit raw and maybe i'll update and improve it in the near future
