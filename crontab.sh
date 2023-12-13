#!/bin/bash

# create folder for logs
mkdir /usr/src/app/logs/
# create log file
touch /usr/src/app/logs/crontab.log
# script permission
chmod +x /usr/src/app/trigger.sh
# add to crontab
echo "0 * * * * /usr/src/app/trigger.sh >> /usr/src/app/logs/crontab.log 2>&1" > /etc/crontab
# start crontab
crontab /etc/crontab
# start cron service
/usr/sbin/service cron start
# continuously read logs to display in Docker
tail -f /usr/src/app/logs/crontab.log
