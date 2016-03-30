#!/bin/bash

#killall postgres

dir="/usr/local/var/postgres"
owner=whoami
rm -rf $dir && mkdir $dir && chmod 775 $dir && chown $owner $dir
initdb -D $dir
./scripts/db/stop.sh && sleep 1s
./scripts/db/start.sh && sleep 1s

createdb bapa-local
