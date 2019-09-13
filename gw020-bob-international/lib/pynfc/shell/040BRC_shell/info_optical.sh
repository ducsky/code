#!/usr/bin/expect
set timeout 10
set ip [lindex $argv 0]
set pw [lindex $argv 1]
spawn telnet $ip
expect "Login: "
send "admin\n"
sleep 0.5
expect "Password: "
send "gpon@Vnt00\n"
sleep 0.5
expect ">"
send "laser power --rxread\n"
expect ">"
send "ifconfig br0 | grep HWaddr\n"
expect ">"
sleep 1
send "laser power --txread\n"
expect ">"
sleep 1
send "laser temperature --read\n"
expect ">"
sleep 1
send "laser txbias      --read\n"
expect ">"
sleep 1
send "laser voltage     --read\n"
expect ">"
sleep 1
send "exit\n"
sleep 0.5
expect eof
#interact
