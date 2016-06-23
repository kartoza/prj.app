#!/bin/bash
MYDATE=`date +%d-%B-%Y`
MONTH=$(date +%B)
YEAR=$(date +%Y)
cd /home/data/changelog.inasafe.org/deployment
MYBASEDIR=`pwd`/backups
MYBACKUPDIR=${MYBASEDIR}/${YEAR}/${MONTH}
mkdir -p ${MYBACKUPDIR}

cd ${MYBACKUPDIR}
docker exec -ti projecta-db /bin/bash -c "PGPASSWORD=docker pg_dump -Fc -f /tmp/latest.dmp -h localhost -U docker gis"
docker cp projecta-db:/tmp/latest.dmp PG_projecta-${MYDATE}.dmp

cd -
rm backups/latest.dmp

cd backups
ln -s ${MYBACKUPDIR}/PG_projecta-${MYDATE}.dmp latest.dmp

cd ..
