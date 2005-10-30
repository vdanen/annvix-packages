#!/bin/sh
#---------------------------------------------------------------
# Project         : Mandrake Linux
# Module          : rpm
# File            : filter.sh
# Version         : $Id$
# Author          : Frederic Lepied
# Created On      : Tue May 13 15:45:17 2003
# Purpose         : filter using grep and first argument the
# command passed as the rest of the command line
#---------------------------------------------------------------

GREP_ARG="$1"
PROG="$2"
shift 2

# use ' ' to signify no arg as rpm filter empty strings from
# command line :(
if [ "$GREP_ARG" != ' ' ] ;then
    $PROG "$@" | grep -v "$GREP_ARG"
else
    $PROG "$@"
fi

exit 0

# filter.sh ends here
