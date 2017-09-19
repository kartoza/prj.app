#!/bin/bash

echo "Use this to deploy a tagged version to production"
echo "Be sure to first use tag_and_deploy_to_staging.sh"
echo "to deploy to staging and test there before running this script."
echo "Note that migrations are not automatically run in this script"
echo "you should log in to the server and do that manually if needed."
echo "e.g."
echo "$0 1.2.3"

read -p "Are you sure you want to continue? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
	VERSION=$1
	make dbbackup
	make mediasync
	ssh changelog.qgis.org "cd /home/projecta/deployment && git fetch --tags && git checkout $VERSION && make collectstatic && make reload"
else
	echo "Deploy to production aborted."
fi
