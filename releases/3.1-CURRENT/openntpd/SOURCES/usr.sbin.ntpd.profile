# vim:syntax=apparmor
# Last Modified: Mon Jun 18 16:59:58 2007
#
# $Id$

#include <tunables/global>

/usr/sbin/ntpd {
  #include <abstractions/base>
  #include <abstractions/nameservice>

  capability kill,
  capability net_bind_service,
  capability setgid,
  capability setuid,
  capability sys_chroot,
  capability sys_time,

  /etc/ntpd.conf r,
  /usr/sbin/ntpd mr,
}
