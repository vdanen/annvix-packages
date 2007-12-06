#!/bin/sh

zonedir="/usr/share/zoneinfo"
localtime_file="/etc/localtime"
clock_file="/etc/sysconfig/env/clock/ZONE"

unset ZONE
[[ -f ${clock_file} ]] && ZONE=$(head -1 ${clock_file})

if [ -z "${ZONE}" ]; then
    ZONE="Canada/Mountain"
fi

if [ -f ${zonedir}/${ZONE} ] && [ ! -L ${localtime_file} ]; then
    cp -f ${zonedir}/${ZONE} ${localtime_file}
fi
