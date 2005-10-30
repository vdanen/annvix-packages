Summary: Job spooling tools.
Name: at
Version: 3.1.8
Release: 7mdk
License: GPL
Group: System/Servers
Source: ftp://tsx-11.mit.edu/pub/linux/sources/usr.bin/at-3.1.8.tar.bz2
Source2: atd.init.bz2
Patch0: at-3.1.7-lockfile.patch.bz2
#Patch1: at-3.1.7-noon.patch.bz2
Patch2: at-3.1.7-paths.patch.bz2
Patch3: at-3.1.7-sigchld.patch.bz2
Patch4: at-3.1.8-noroot.patch.bz2
Patch5: at-3.1.8-typo.patch.bz2
Patch6: at-3.1.8-debian.patch.bz2
Patch7: at-3.1.8-buflen.patch.bz2
Patch8: at-3.1.8-UTC.patch.bz2
Patch9: at-3.1.8-shell.patch.bz2
Patch10: at-3.1.8-o_excl.patch.bz2
Patch11: at-3.1.8-heapcorruption.patch.bz2
Prereq: fileutils chkconfig /etc/init.d rpm-helper
Conflicts: crontabs <= 1.5
Buildroot: %{_tmppath}/%{name}-root
Requires: common-licenses mailx
BuildRequires: autoconf automake flex gcc python smtpdaemon

%description
At and batch read commands from standard input or from a specified file.
At allows you to specify that a command will be run at a particular time
(now or a specified time in the future).  Batch will execute commands
when the system load levels drop to a particular level.  Both commands
use /bin/sh to run the commands.

You should install the at package if you need a utility that will do
time-oriented job control.  Note: you should use crontab instead, if it is
a recurring job that will need to be repeated at the same time every
day/week/etc.

%prep
%setup -q
%patch0 -p1 -b .lockfile
# The next path is a brute-force fix that will have to be updated
# when new versions of at are released.
%patch2 -p1 -b .paths

%patch3 -p1 -b .sigchld
%patch6 -p0 -b .debian
%patch4 -p1 -b .noroot
%patch5 -p1 -b .tyop
%patch7 -p1 -b .buflen
%patch8 -p1
%patch9 -p1 -b .shell
%patch10 -p1 -b .o_excl
%patch11 -p1 -b .heapcorruption

cat /usr/share/aclocal/libtool.m4 >> aclocal.m4
libtoolize --force
aclocal
autoconf


%build
%serverbuild
%configure --with-atspool=/var/spool/at/spool --with-jobdir=/var/spool/at

make

%install
rm -rf $RPM_BUILD_ROOT 
mkdir -p $RPM_BUILD_ROOT/{%{_initrddir},%{_bindir},%{_sbindir},%{_mandir}/man{1,5,8}}

make install IROOT=$RPM_BUILD_ROOT DAEMON_USERNAME=`id -nu` \
	DAEMON_GROUPNAME=`id -ng`
	# \
	#etcdir=$RPM_BUILD_ROOT/etc \
	#ATJOB_DIR=$RPM_BUILD_ROOT/var/spool/at \
	#ATSPOOL_DIR=$RPM_BUILD_ROOT/var/spool/at/spool 
echo > $RPM_BUILD_ROOT/%{_sysconfdir}/at.deny
bzcat %{SOURCE2} > $RPM_BUILD_ROOT%{_initrddir}/atd
#install -m 755 $RPM_SOURCE_DIR/atd.init 
chmod 755 $RPM_BUILD_ROOT%{_initrddir}/atd

#(peroyvind) remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_mandir}/man5/at_allow.5

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch /var/spool/at/.SEQ
chmod 600 /var/spool/at/.SEQ
chown daemon.daemon /var/spool/at/.SEQ

%_post_service atd

%preun
%_preun_service atd

%files
%defattr(-,root,root)
%doc ChangeLog Problems README Copyright timespec
%config(noreplace) %{_sysconfdir}/at.deny
%config(noreplace) %{_initrddir}/atd
%attr(0700,daemon,daemon)	%dir /var/spool/at
%attr(0600,daemon,daemon)	%verify(not md5 size mtime) %ghost /var/spool/at/.SEQ
%attr(0700,daemon,daemon)	%dir /var/spool/at/spool
%{_sbindir}/atrun
%{_sbindir}/atd
%{_mandir}/*/atrun.8.bz2
%{_mandir}/*/atd.8.bz2
%{_mandir}/*/at.1.bz2
%{_bindir}/batch
%{_bindir}/atrm
%{_bindir}/atq
%attr(4755,root,root)   %{_bindir}/at


%changelog
* Thu Jun 05 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.1.8-7mdk
- fix unpackaged files
- fix E: at no-prereq-on rpm-helper
- drop unapplied Patch1

* Thu Mar 28 2002 Warly <warly@mandrakesoft.com> 3.1.8-6mdk
- change group

* Thu Feb 14 2002 Stefan van der Eijk <stefan@eijk.nu> 3.1.8-5mdk
- BuildRequires

* Thu Jan 17 2002 Vincent Danen <vdanen@mandrakesoft.com> 3.1.8-4mdk
- security fix (possible local root)
- use newer debian patch instead of the old one
- regenerate buflen, typo, UTC, and noroot patches
- fixes segfault when using improper time commands

* Fri Sep 28 2001 Stefan van der Eijk <stefan@eijk.nu> 3.1.8-3mdk
- BuildRequires:        flex
- Copyright --> License


* Wed Sep 12 2001 Pixel <pixel@mandrakesoft.com> 3.1.8-2mdk
- change the "BuildRequires: mailx" in "Requires: mailx"
- /var/spool/at/.SEQ must be 600 says the %%post, 
  have the same rights in the rpm db (aka quiet rpm -V)

* Tue Apr 10 2001 Gregory Letoquart <gletoquart@mandrakesoft.com> 3.1.8-1mdk
- Up to 3.1.8 and add new patch to correct prb of compilation and man page

* Fri Mar 30 2001 Gregory Letoquart <gletoquart@mandrakesoft.com> 3.1.7-20mdk
- fno-ommit-frame-pointer Fred compliant
 
* Wed Mar 28 2001 Francis Galiegue <fg@mandrakesoft.com> 3.1.7-19mdk
- BuildRequires: mailx
 
* Fri Mar  2 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 3.1.7-18mdk
- spec cleanup
 
* Mon Sep 11 2000 Enzo Maggi <enzo@mandrakesoft.com> 3.1.7-17mdk
- added (noreplace) to config files. 

* Wed Aug 30 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.1.7-16mdk
- rebuild for the user of the _initrddir macro.
 
* Tue Jul 25 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.1.7-15mdk
- rebulid for BM
- macroszifications
 
* Sun Apr 23 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 3.1.7-14mdk
- fixed man page compression --> is handled by spechelper
 
* Wed Mar 22 2000 Daouda Lo <daouda@mandrakesoft.com> 3.1.7-13mdk
- now under system/Servers group
 
* Tue Oct 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
 
- Build Release.
 
* Tue Jun 22 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
 
- Merging with the RedHat changes :
        -* correct perms for /var/spool/at after defattr.
        -* reset SIGCHLD before exec (#3016).
        -* fix handling the 12:00 time
 
* Wed May 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
 
- Prereq update (we need setup package before) 

* Fri Apr  9 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man pages
- handle RPM_OPT_FLAGS
- add de locale
 
* Wed Jan 13 1999 Bill Nottingham <notting@redhat.com>
- configure fix for arm
 
* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1
 
* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr
 
* Wed Apr 22 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced initscript
 
* Sun Nov 09 1997 Michael K. Johnson <johnsonm@redhat.com>
- learned to spell
 
* Wed Oct 22 1997 Michael K. Johnson <johnsonm@redhat.com>
- updated to at version 3.1.7
- updated lock and sequence file handling with %ghost
- Use chkconfig and atd, now conflicts with old crontabs packages
 
* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc 
