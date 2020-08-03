#!/bin/bash
if [ ! -f port.txt ]
then
touch port.txt
echo "25565" >> port.txt
fi
oldport=$(cat port.txt)
if [[ $1 = set ]]
then
  sed -i -e "s/$oldport/$2/g" port.txt
  oldport=$(cat port.txt)
  newport=$oldport
elif [[ $1 = reset ]]
then
 sed -i -e "s/$oldport/25565/g" port.txt
 oldport=$(cat port.txt)
 newport=$oldport
else
newport=$(expr $oldport + 1)
sed -i -e "s/$oldport/$newport/g" port.txt
fi
export newport="$newport"
export oldport="$oldport"
#echo $newport
