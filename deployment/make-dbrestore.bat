docker exec -t -i projecta-db su - postgres -c "dropdb gis"
docker exec -t -i projecta-db su - postgres -c "createdb -O docker -T template_postgis gis"
docker exec -t -i projecta-db su - postgres -c "pg_restore /backups/latest.dmp -d gis"
