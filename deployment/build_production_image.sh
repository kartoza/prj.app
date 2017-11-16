#!/bin/bash
echo "Use this to build a production image of the projecta-uwsgi"
echo "docker, push the image upstream with tag :latest and "
echo "a versioned tag e.g. :1.6.19."
echo "Useage:"
echo "$0 1.2.3"
echo "Where 1.2.3 is the git tag version to build the image for"
VERSION=$1
echo "Last tag on your local system is:"
git tag | grep -v version | sort --version-sort | tail -1
echo "New tag to be added to your local repo and pushed upstream:"
echo $VERSION
read -p "Are you sure you want to continue? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
	VERSION=$1
	# Archive out just the django_project folder so it is small with no history
    # and unpack that into the docker directory so build can copy it into
    # the projects_uwsgi production image
    cd ..
	git archive --format=tar.gz $VERSION django_project > deployment/docker/projecta.tar.gz
    cd -
    # Copy all but the last line of the Dockerfile so that our 
    # production image is always based off that
    cat docker/Dockerfile | sed \$d > docker/Dockerfile-prod
    # Add will extract the archive...
    echo "ADD projecta.tar.gz /home/web" >> docker/Dockerfile-prod
    echo "CMD [\"uwsgi\", \"--ini\", \"/uwsgi.conf\"]" >> docker/Dockerfile-prod
    # Now build the image and tag it
    cd docker
	docker build -t kartoza/projecta-uwsgi:latest -f Dockerfile-prod .
    docker tag kartoza/projecta-uwsgi:latest kartoza/projecta-uwsgi:$VERSION
    docker push kartoza/projecta-uwsgi:latest
    docker push kartoza/projecta-uwsgi:$VERSION
    cd -
	# Clean up
	rm -rf docker/django_project.tar.gz docker/Dockerfile-prod
    rm docker/Dockerfile-prod
else
	echo "Production image build aborted."
fi

