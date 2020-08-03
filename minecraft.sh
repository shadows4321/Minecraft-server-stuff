#!/bin/bash

function start(){
clear
cd ~
echo "~~~~~~~~~~~~~~~"
echo "[0] cancel"
echo "[1] start server"
echo "[2] stop server"
echo "[3] create server"
echo "[4] list started servers"
echo "[5] connect to server"
echo "~~~~~~~~~~~~~~~"

read -p "select option:" option
if [ $option -eq '0' ]
then
 exit 0
 elif [ $option -eq '1' ]
 then
 read -p "what server do you want to start:" server
 ./startserver.sh $server
 pause
 start

 elif [ $option -eq '2' ]
 then
 read -p "what server do you want to stop:" server
 ./stopserver.sh $server
 pause
 start

 elif [ $option -eq '3' ]
 then
 read -p "what do you want the server to be called:" server
 ./createserver.sh $server
 pause
 start

 elif [ $option -eq '4' ]
 then
 screen -ls
 pause
 start

 elif [ $option -eq '5' ]
 then
 read -p "what server do you want to connect to?:" server
 screen -rd $server
 start

 fi
}

start
