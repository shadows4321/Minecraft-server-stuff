#!/bin/bash
#read -p 'server name:' name
server_name=$1
sleep=10
if [ $server_name = all ]
then
	./minecraft_stop_all.sh
else
output=$(screen -ls)
if [[ ! "$output" =~ "$server_name" ]]
	then
	echo the $server_name server is not running
	else
		if [ $server_name == waterfall ]; then
			screen -S $server_name -X stuff 'end'$(echo -ne '\015')
			echo stoping the $server_name server
			sleep $sleep
			echo the $server_name server has stoped
			screen -S $server_name -X stuff 'exit'$(echo -ne '\015')
			screen -ls
		else
			screen -S $server_name -X stuff 'stop'$(echo -ne '\015')
			echo stoping the $server_name server
			sleep $sleep
			echo the $server_name server has stoped
			screen -S $server_name -X stuff 'exit'$(echo -ne '\015')
			screen -ls
		fi
	fi
fi
