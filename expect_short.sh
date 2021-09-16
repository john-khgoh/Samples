#!/usr/bin/expect -f
#!/bin/bash

#IP and passwords have been censored
set sv(1) [IP_censored].42.13
set sv(2) [IP_censored].42.14
set sv(3) [IP_censored].42.15
set sv(4) [IP_censored].42.170 
set sv(5) [IP_censored].42.171 

set pw(1) [password_censored]
set pw(2) [password_censored]
set pw(3) [password_censored]
set pw(4) [password_censored]
set pw(5) [password_censored]

set user(1) [username_censored]
set pass(1) [password_censored]

for { set i 1 } { $i <= 5} { incr i } {

spawn ssh root@$sv($i)  
expect "*?ssword:*"
send -- "$pw($i)\n"
expect << EOF
spawn passwd $user(1)
expect "New UNIX password:"
send -- "$pass(1)\r"
expect "Retype new UNIX password:"
send -- "$pass(1)\r"
expect eof;
}
EOF
