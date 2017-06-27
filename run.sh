#!/usr/bin/env bash

docker_cmd=`which docker`
docker_ip=`docker-machine ip`


${docker_cmd} run -d --name db -p 8091-8093:8091-8093 -p 11210:11210 couchbase

echo "Configuring couchbase..."
sleep 10

curl -v -X POST http://${docker_ip}:8091/pools/default -d memoryQuota=300 -d indexMemoryQuota=300
curl -v -X POST http://${docker_ip}:8091/pools/default/buckets -d name=weather -d ramQuotaMB=200 -d authType=none -d proxyPort=11216
curl -v -X POST http://${docker_ip}:8091/settings/web -d port=8091 -d username=Admin -d password=password

echo "Starting python web service..."
echo
sleep 10

python main.py