#!/bin/bash
#read -p 'server name: ' name
server_name=$1
output=$(screen -ls)
if [[ "$output" =~ "$server_name" ]]
then
    echo 'the server is running'
else
    screen -dmS $server_name
    echo starting $server_name
    screen -S $server_name -X stuff 'cd /var/opt/minecraft/server/'$server_name/''$(echo -ne '\015')
    screen -S $server_name -X stuff '/var/opt/minecraft/server/'$server_name/'start.sh'$(echo -ne '\015')
    screen -ls | grep $server_name
fi