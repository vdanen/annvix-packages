# Last Modified: Thu Aug  2 13:33:43 2007
# $Id: usr.sbin.traceroute 933 2007-08-17 22:46:56Z DominicReynolds_ $
# ------------------------------------------------------------------
#
#    Copyright (C) 2002-2005 Novell/SUSE
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of version 2 of the GNU General Public
#    License published by the Free Software Foundation.
#
# ------------------------------------------------------------------

#include <tunables/global>
/usr/sbin/traceroute {
  #include <abstractions/base>
  #include <abstractions/consoles>
  #include <abstractions/nameservice>

  capability net_raw,
  capability setuid,
  capability setgid,
  network inet raw,

  /usr/sbin/traceroute rmix,
  @{PROC}/net/route r,
}
