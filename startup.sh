#!/usr/bin/env bash
echo " ----   starting background worker processes ----- "

# TODO
# check if supervisord is running else kill it and restart the process
LOG_PATH="/var/log/bns-service"

# create log path

if [ ! -d "$LOG_PATH" ]; then
    echo "---- creating log directories ------"
    sudo mkdir -p /var/log/bns-service
    chmod -R 777 /var/log/bns-service
else
    echo "--- log directory exists ------"
fi

export DEPLOY_PATH=/home/samparsky/app/bns
export BNS_LOGPATH=/var/log/bns-service

#supervisor_process_id=$(pidof supervisord)

supervisord -c scripts/bns-service.conf
