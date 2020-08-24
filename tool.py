import getpass
import telnetlib
import time
import serial
import pandas as pd
from BTCInput import *

df = pd.read_csv("ban.txt")
mach = int(input('Nhap vao mach muon ghi MAC va  SN: '))
def telnet():
    HOST = "192.168.1.254"
#     user = input("Enter your remote account: ")
#     password = getpass.getpass()
#     password = input("Enter your pass account: ")
   
    user = 'root'
    password = 'admin'
    tn = telnetlib.Telnet(HOST)
    
    tn.read_until(b"tc login: ")
    tn.write(user.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    time.sleep( 3 )
    tn.write('\x03'.encode())
    
    time.sleep( 5 )
#    tn.write(b"exit\n")
    tn.write(b"prolinecmd gponsn set " + df['gpon'][mach - 1].encode('ascii') + b"\n")
    tn.write(b"sys mac " + df['mac'][mach - 1].encode('ascii') + b" ifconfig br0"+b"\n")
    print(tn.read_all().decode('ascii'))

def show_info():
    HOST = "192.168.1.254"
#     user = input("Enter your remote account: ")
#     password = getpass.getpass()
#     password = input("Enter your pass account: ")
   
    user = 'root'
    password = 'admin'
    tn = telnetlib.Telnet(HOST)
    
    tn.read_until(b"tc login: ")
    tn.write(user.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    time.sleep( 3 )
    tn.write('\x03'.encode())
    time.sleep( 5 )
    tn.write(b"tcapi show GPON_ONU" + b"\n")
    time.sleep( 5 )
    tn.write(b"ifconfig br0" + b"\n")
    time.sleep( 5 )
    tn.write(b"exit\n")
    print(tn.read_all().decode('ascii'))
    print(df['gpon'][mach-1])
    print(df['mac'][mach-1])
    
    
menu = '''Tool write MAC/SN ONT G010
1. New Contact
2. Find Contact
3. Exit Program

Enter the command: '''
while True:
    command = read_int_ranged (prompt = menu, min_value = 1, max_value = 3)
    if command == 1:
        telnet()
    if command == 2:
        show_info()
    if command == 3:
        break    
   




