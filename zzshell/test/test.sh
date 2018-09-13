#!/usr/bin/expect
spawn ssh root@192.168.22.194
expect "*password:"
send "123\r"
expect "*#"
interact