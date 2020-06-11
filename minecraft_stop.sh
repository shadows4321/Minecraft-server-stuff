#!/bin/bash
#read -p 'server name: ' name
server_name=$1
sleep=10

output=$(screen -ls)
if [[ ! "$output" =~ "$server_name" ]]
then
	echo the server $server_name is not running
else
	if [ $server_name == waterfall ]; then
		screen -S $server_name -X stuff 'end'$(echo -ne '\015')
		echo server $server_name stoping
		sleep $sleep
		echo server $server_name has stoped
		screen -S $server_name -X stuff 'exit'$(echo -ne '\015')
	else
		screen -S $server_name -X stuff 'stop'$(echo -ne '\015')
		echo server $server_name stoping
		sleep $sleep
		echo server $server_name has stoped
	screen -S $server_name -X stuff 'exit'$(echo -ne '\015')
	fi
fi
