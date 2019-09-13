#!/usr/bin/expect
set timeout 10
set ip [lindex $argv 0]
spawn telnet $ip
expect "Login: "
send "admin\n"
sleep 0.5
expect "Password: "
send "gpon@Vnt00\n"
sleep 0.5
expect ">"
send "ifconfig br0 | grep HW\n"
expect ">"
send "swversion\n"
expect ">"
send "swversion -b\n"
expect ">"
send "exit\n"
sleep 0.5
expect eof
#interact
