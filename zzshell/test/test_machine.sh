#!/usr/bin/expect
send "<----------------->\r"
send "测试机器是否能ssh上\r"
send "<----------------->\r"
#环境检查

set ipList(1) 192.168.10.46
set userList(1) bbase
set keywordList(1) byb123456
set ipList(2) 192.168.10.47
set userList(2) bbase
set keywordList(2) byb123456
set ipList(3) 192.168.10.48
set userList(3) bbase
set keywordList(3) byb123456
set ipList(4) 192.168.10.101
set userList(4) bbase
set keywordList(4) byb123456
set ipList(5) 192.168.10.102
set userList(5) bbase
set keywordList(5) byb123456
set ipList(6) 192.168.10.103
set userList(6) bbase
set keywordList(6) byb123456
set ipList(7) 192.168.10.187
set userList(7) bbase
set keywordList(7) byb123456
set ipList(8) 192.168.10.188
set userList(8) bbase
set keywordList(8) byb123456


set totalNum 999
set timeout -1
for {set i 1} {$i<=$totalNum} {incr i} {
    set IPAddress $ipList($i)
    set password $keywordList($i)
    set user $userList($i)
    spawn ssh $user@$IPAddress

    expect {
            -re "Permission denied, please try again." {
                    send_user "Error:Permission denied.\n"
                    exit
            }
            -re "Are you sure you want to continue connecting (yes/no)?" {
                    send "yes\r";exp_continue
            }
            -re "assword:" {
                    send "$password\r";exp_continue
            }
            -re "speedup is"{
            }
    }
}