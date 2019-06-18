#!/bin/bash

if [ $(id -un) != youruser ]; then
    exec sudo -u youruser "$0" "$@"
fi

PATH=/home/youruser/bin:/home/youruser/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
USER=youruser
HOME=/home/youruser

eval $1
