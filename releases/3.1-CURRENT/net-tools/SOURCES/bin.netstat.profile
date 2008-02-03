# Last Modified: Tue Jun 19 14:51:09 2007
#include <tunables/global>
/bin/netstat {
  #include <abstractions/base>
  #include <abstractions/nameservice>

  capability sys_ptrace,

  /bin/netstat rmix,

  /usr/share/locale/** rm,
  /etc/networks r,
  @{PROC} r,
  @{PROC}/[0-9]*/cmdline r,
  @{PROC}/[0-9]*/fd/ r,
  @{PROC}/[0-9]*/fd/* r,
  @{PROC}/net/ r,
  @{PROC}/net/* r,

}
