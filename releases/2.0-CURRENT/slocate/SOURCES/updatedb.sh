#!/bin/sh
# (c) MandrakeSoft.
# Chmouel Boudjnah <chmouel@mandraksoft.com>
#
# Modified 20010109 by Francis Galiegue <fg@mandrakesoft.com>
#
# Fixes by mlord@pobox.com

# No need to source /etc/updatedb.conf. Use the -c option, that's what it's
# for...

source /etc/updatedb.conf
/usr/bin/slocate -c -u -l"$SECURITY"

