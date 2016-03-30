#!/bin/bash

dir="/usr/local/var/postgres"
pg_ctl -D $dir -l logs/postgres stop
