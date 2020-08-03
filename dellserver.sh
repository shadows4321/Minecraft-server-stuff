#!/bin/bash
if [[ $1 == "" ]]
then
read -p "what server do you want to delete:" dell
else
dell=$1
fi
read -p "are you sure you want to delete $dell?:" answer
if [ $answer = yes ] || [ $answer = y ]
then
 rm -rf /var/opt/minecraft/crafty/servers/$dell
 echo delleted $dell

else
 echo canceled
fi
