#!/bin/bash
clear
if [[ $1 == "" ]]
then
 read -p "server name:" name
else
 name=$1
fi
path="/var/opt/minecraft/server/"
output=$(ls $path | grep $name)
fullpathname="$path"$name
MCVER="1.16.1"
export MCVER
VERSION_LIST="https://papermc.io/api/v1/paper/${MCVER}/latest"
JARFILE="paper-${MCVER}.jar"
UPDATE_FILE="current_version.txt"
DOWNLOAD_URL="https://papermc.io/api/v1/paper/${MCVER}/latest/download"
. ./setport.sh
essentials_url=https://www.dropbox.com/s/8bka1lz3948w6m0/EssentialsX-2.18.0.0.zip?dl=1
waterfall=$(echo waterfall.txt)
nametagedit="https://www.spigotmc.org/resources/nametagedit.3836/download?version=339235"
function update_check() {
    oldpath=$(pwd)
    cd $fullpathname

    current_version="-1" # Default version

    if [ ! -f ${UPDATE_FILE} ]; then
        echo ${current_version} > ${UPDATE_FILE}
    else
        current_version=$(<${UPDATE_FILE})
    fi

    latest_version=`curl -JLs ${VERSION_LIST} | jq -r .build` # Gets the build key of the JSON result


    if [ ! ${current_version} -eq ${latest_version} ] ; then

        echo "UPDATING TO NEW VERSION"
        curl -JLo ${JARFILE} ${DOWNLOAD_URL}

        if [ ! "$?" -eq 0 ]; then
            echo "FAILED TO DOWNLOAD LATEST VERSION OF MINECRAFT SERVER"
        fi

        echo ${latest_version} > ${UPDATE_FILE}
		cd $oldpath
    fi
}
if [[ $output = $name ]] && [[ ! $output =  "" ]]
then
 echo "server allready exists"
 read -p "do you want do delete $name?:" dell
  if [ $dell = yes ] || [ $dell = y ]
  then
  ./dellserver.sh $name
  exit 0
  fi
else
 mkdir "$path"$name
 #ls | grep $name
 echo "server located at /var/opt/minecraft/crafty/servers/"$name
 echo ~~~~~~~~~~~~~~~
 echo "[0] cancel"
 echo "[1] paper"
 echo "[2] fabric"
 echo "[3] spigot"
 echo ~~~~~~~~~~~~~~~
 read -p "select server type number:" server_type
 if [ $server_type -eq "0" ]
 then
  rm -rf /var/opt/minecraft/crafty/servers/$name
  echo canceled
  exit
  elif [ $server_type -eq "1" ]
 then
  echo "server type paper selected"
  update_check
  cp -r serverfiles/* "$path"$name/
  mkdir temp
  cd temp
  curl -JLo EssentialsX.zip $essentials_url
  curl -JLo NametagEdit.jar $nametagedit_url
  chmod -R 0777 EssentialsX.zip
  unzip -o EssentialsX.zip; rm EssentialsX.zip
  #mkdir $path$name/plugins
  cp EssentialsX-*.jar "$path"$name/plugins; cp EssentialsXChat-*.jar "$path"$name/plugins
  cd ~/; rm -rf temp

  elif [ $server_type -eq "2" ]
 then
  echo "server type fabric selected"
  curl -JLo "$path"$name/fabric-installer.jar https://maven.fabricmc.net/net/fabricmc/fabric-installer/0.6.1.45/fabric-installer-0.6.1.45.jar
  cd "$path"$name/
  java -jar fabric-installer.jar server; rm fabric-installer.jar
  cd ~
  cp ~/fabricserverfiles/* "$path"$name/
  elif [ $server_type -eq "3" ]
 then
  echo "server type spigot selected"
  curl -JLo spigot-$MCVER.jar https://cdn.getbukkit.org/spigot/spigot-$MCVER.jar
fi
read -p "do you want the port to be set to $newport:" portans
 if [ $portans = yes ] || [ $portans = y ]
 then
 sed -i -e "s/25565/$newport/g" $path$name/server.properties
 echo port has been set to $newport
 port=$newport
 else
 read -p "what do you want the port to be?(current port is $newport):" port
 sed -i -e "s/25565/$port/g" $path$name/server.properties
 echo port has been set to $port
 sed -i -e "s/$newport/$oldport/g" port.txt
 fi
sed -i -e "s/export MC_PORT=\"25565\"/export MC_PORT=\"$port\"/g" $path$name/settings.sh
touch $path$nane/port.txt
echo "$port" >> $path$name/port.txt
read -p "do you want to push the port to the waterfall config?:" YN
if [[ $YN = yes ]] || [[ $YN = y ]]
then
 echo "  $name:" >> "$path"waterfall/config.yml
 echo "    address: localhost:$port" >> "$path"waterfall/config.yml
fi
read -p "do you want to edit server.properties?:" propans
function anythingelse(){
read -p "is there any thing else?:" anyelse
if [ $anyelse = yes ] || [ $anyelse = y ]
then
 echo ""
 read -p "what setting do you want to change(include true or false):" var1
 read -p "what do you want to change $var1 to?:" var2
 sed -i -e "s/$var1/$var2/g" $path$name/server.properties
 anythingelse
 fi
}
if [ $propans = yes ] || [ $propans = y ]
then
  clear
  cat "$path"$name/server.properties
  read -p "what setting do you want to change(include true or false):" var1
  read -p "what do you want to change $var1 to?:" var2
  sed -i -e "s/$var1/$var2/g" $path$name/server.properties
  anythingelse
fi
./startserver.sh $name
screen -dmS config
screen -S config -X stuff './configure.sh '$name''$(echo -ne '\015')

fi
