#!/bin/bash

# The first time before running this script, connect once manually to 
# accept the ssh key:

# sftp sftp://changelog.qgis.org:2222 

#First the database backups on the remote server
SOURCE=ftp/db
DEST=backups/db
OBJECTIVE=$2
REMOVE_FILE=$3
shopt -s nocasematch
if [ -z "$OBJECTIVE" ]
then
	OBJECTIVE='DOWNLOAD'
elif [[ $OBJECTIVE == 'upload' ]]; then
	#statements
	OBJECTIVE='UPLOAD'
	TEMP=$SOURCE
	SOURCE=$DEST
	DEST=$TEMP
else
	OBJECTIVE='DOWNLOAD'
fi
if [[ $REMOVE_FILE == 'True' ]]; then
	REMOVE_FILE='-e'
else
	REMOVE_FILE=''
fi
shopt -u nocasematch
echo 'Source :' $SOURCE
echo 'Destination :' $DEST
echo 'Objective :' $OBJECTIVE
lftp -u kartoza, sftp://changelog.qgis.org:2222 -e "mirror $REMOVE_FILE $SOURCE $DEST; bye"
#Next the media backups on the remote server
SOURCE=ftp/media
DEST=backups/media
OBJECTIVE=$2
REMOVE_FILE=$3
shopt -s nocasematch
if [ -z "$OBJECTIVE" ]
then
	OBJECTIVE='DOWNLOAD'
elif [[ $OBJECTIVE == 'upload' ]]; then
	#statements
	OBJECTIVE='UPLOAD'
	TEMP=$SOURCE
	SOURCE=$DEST
	DEST=$TEMP
else
	OBJECTIVE='DOWNLOAD'
fi
if [[ $REMOVE_FILE == 'True' ]]; then
	REMOVE_FILE='-e'
else
	REMOVE_FILE=''
fi
shopt -u nocasematch
echo 'Source :' $SOURCE
echo 'Destination :' $DEST
echo 'Objective :' $OBJECTIVE
lftp -u kartoza, sftp://changelog.qgis.org:2222 -e "mirror $REMOVE_FILE $SOURCE $DEST; bye"
