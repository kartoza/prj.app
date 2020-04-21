#!/bin/sh

# To run : ./sftp_copy.sh {folder_name} -> ./sftp_copy.sh postgis_history
# First argument is the name of the folder of sftp that we want to copy
LOCALPATH=./$1
REMOTEPATH=/ftp/$1

if [ ! -d "$LOCALPATH" ]; then
	echo "Folder does not exist, create one"
	mkdir -p -- "$LOCALPATH"
fi

# Open and copy files from sftp
echo "get -r $REMOTEPATH/* $LOCALPATH" | sftp -P 2222 kartoza@78.46.204.5
