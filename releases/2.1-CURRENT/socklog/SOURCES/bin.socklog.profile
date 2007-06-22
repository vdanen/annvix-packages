# vim:syntax=apparmor
# Last Modified: Mon Jun 18 16:59:58 2007
#
# $Id: usr.sbin.ntpd.profile 7395 2007-06-18 23:40:50Z vdanen $

#include <tunables/global>

/bin/socklog {
  #include <abstractions/base>

  # this is only needed when socklog listens to UDP ports (i.e. to receive
  # remote syslog messages)
  capability net_bind_service,
  
  capability setgid,
  capability setuid,
  capability sys_admin,

  /bin/socklog mr,
}
