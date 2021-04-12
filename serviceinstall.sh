#!/bin/bash

echo 'Server Monitor set-up script V1.0'
echo 'This script will install the PRTG Environmental sensor as a system service.'

while:
do
    read 'Continue with setup? (Yes/No)' $CONTCHOICE

    case $CONTCHOICE in
    yes)
        continue
    no)
        exit
    *)
        'Invalid response!'
done


if [ $(whoami) != "root" ];
then
    echo "Please run with sudo!"
    exit 3

fi

# Installs Python3
apt-get install python3 && wait

# Sets up the script as a system service
while:
do

    read 'Do you want to set this up as a system service? (Yes/No) ' SERVICECHOICE

    case $SERVICECHOICE in
        yes)
            echo 'Starting service install.'
            SERVICETEMPLATE="
            [Unit]
            Description=PRTG Environmental Sensor Service
            After=syslog.target

            [Service]
            Type=simple
            User=root
            Group=root
            WorkingDirectory=$(PWD)
            ExecStart=$(PWD)/sensor.py
            StandardOutput=syslog
            StandardError=syslog

            [Install]
            WantedBy=multi-user.target"
            
            touch "EnviroSensor.service"
            echo -e "$SERVICETEMPLATE" > EnviroSensor.service
            mv EnviroSensor.service /etc/systemd/system/EnviroSensor.service
            systemctl daemon-reload
            systemctl daemon-reexec
            systemctl status EnviroSensor.service
            echo 'Service Installed.'

        no)
            echo 'Skipping service install.'
            continue
        *)
            echo 'Invalid response!'
    esac
done