%define name	vixie-cron
%define version	3.0.1
%define release 56mdk

Summary:	The Vixie cron daemon for executing specified programs at set times.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	distributable
Group:		System/Servers
Source0:	ftp://ftp.vix.com/pub/vixie/vixie-cron-3.0.1.tar.bz2
Source1:	vixie-cron.init.bz2
Source2:	cron.log.bz2
Patch0:		vixie-cron-3.0.1-redhat-mdk.patch.bz2
Patch1:		vixie-cron-3.0.1-security.patch.bz2
Patch2:		vixie-cron-3.0.1-security2.patch.bz2
Patch3:		vixie-cron-3.0.1-badsig.patch.bz2
Patch4:		vixie-cron-3.0.1-crontab.patch.bz2
Patch5:		vixie-cron-3.0.1-sigchld.patch.bz2
Patch6:		vixie-cron-3.0.1-sprintf.patch.bz2
Patch7:		vixie-cron-3.0.1-sigchld2.patch.bz2
Patch8:		vixie-cron-3.0.1-crond.patch.bz2
Patch9:		vixie-cron-3.0.1-dst.patch.bz2
Patch10:	vixie-cron-3.0.1-0days.patch.bz2
#Patch11:	vixie-cron-3.0.1-nodot.patch.bz2
Patch12:	vixie-cron-3.0.1-syslog.patch.bz2
Patch13:	vixie-cron-3.0.1-crontabloc.patch.bz2
Patch14:	vixie-cron-3.0.1-name.patch.bz2
Patch15:	vixie-cron-3.0.1-time.patch.bz2
Patch16:	vixie-cron-3.0.1-newtime.patch.bz2
Patch17:	vixie-cron-3.0.1-buffer.patch.bz2
Patch18:	vixie-cron-3.0.1-timeaftertime.patch.bz2
Patch19:	vixie-cron-3.0.1-noroot.patch.bz2
Patch150:	vixie-cron-3.0.1-linux.patch.bz2
Buildroot:	%{_tmppath}/%{name}-root
Requires:	sysklogd >= 1.3.33-6, bash >= 2.0
Prereq:		/sbin/chkconfig /sbin/service rpm-helper

%description
The vixie-cron package contains the Vixie version of cron.  Cron is a
standard UNIX daemon that runs specified programs at scheduled times.
Vixie cron adds better security and more powerful configuration
options to the standard version of cron.

%prep
%setup
%patch0 -p1 -b .norh
%patch1 -p1 -b .nomisc
%patch2 -p1 -b .security2
%patch3 -p1 -b .badsig
%patch4 -p1 -b .crontabhole
%patch5 -p1 -b .sigchld
%patch6 -p1 -b .sprintf
%patch7 -p1 -b .sigchld
%patch8 -p1 -b .crond
%patch9 -p1 -b .dst
%patch10 -p1 -b .0days
%patch12 -p1 -b .syslog
%patch13 -p1 -b .crontabloc
%patch14 -p1 -b .name
%patch15 -p1 -b .time
%patch16 -p1 -b .newtime
%patch17 -p1 -b .buffer
%patch18 -p1 -b .buffer
%patch19 -p1 -b .noroot

%ifarch ppc
%patch150 -p1 -b .linux
%endif

%build
%serverbuild
%make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{1,5,8}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
%makeinstall \
	DESTDIR=$RPM_BUILD_ROOT \
	DESTMAN=$RPM_BUILD_ROOT/%{_mandir}
mkdir -p $RPM_BUILD_ROOT/var/spool/cron
chmod 0700 $RPM_BUILD_ROOT/var/spool/cron
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
chmod 0755 $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
chmod 0755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d

bzcat %{SOURCE1} > $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/crond
chmod 0755 $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/crond

bzcat %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/cron
chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/cron


%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service crond

%preun
%_preun_service crond

%files
%defattr(-,root,root)
%doc CHANGES CONVERSION FEATURES INSTALL MAIL
%doc README THANKS MANIFEST FEATURES.crond
%{_sbindir}/crond
%{_bindir}/crontab
%{_mandir}/man*/*

%dir /var/spool/cron
%dir %{_sysconfdir}/cron.d

%config(noreplace) %{_sysconfdir}/rc.d/init.d/crond
%config(noreplace) %{_sysconfdir}/logrotate.d/cron

%changelog
* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.0.1-56mdk
- rebuild
- drop unapplied P11

* Thu Feb 13 2003 Warly <warly@mandrakesoft.com> 3.0.1-55mdk
- do not open /dev/console when launching crond (thanks to ekj@vestdata.no) [bug 1489]
- do not remove log file after uninstall

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.0.1-54mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Fri Aug  2 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 3.0.1-53mdk
- rebuild
- s/Copyright/License/

* Sat Jul  7 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 3.0.1-52mdk
- add %%doc section to %%files section
- clean up spec a bit

* Fri May 11 2001 Vincent Danen <vdanen@mandrakesoft.com> 3.0.1-51mdk
- security fix for local root compromise (patch #19)

* Wed Apr  4 2001 Frederic Lepied <flepied@mandrakesoft.com> 3.0.1-50mdk
- use server macros

* Tue Apr  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.1-49mdk
- Don't require /etc/init.d/ (rpm bugs ?).

* Thu Mar 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.1-48mdk
- Prereq: /etc/init.d /sbin/service.
- Rework the init files.
- add patch from Alan Eldridge <alane@geeksrus.net> to fix double
  execution of jobs (rh).

* Wed Mar  7 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 3.0.1-47mdk
- stop crond in preun stage.
- condrestart crond in postun stage.
- Use better glob for man pages.
- Remove pre-chkconfig stuff.
- Compress crond init script.

* Tue Feb 20 2001 Vincent Danen <vdanen@mandrakesoft.com> 3.0.1-46mdk
- merge patches from redhat, fixes buffer overflow

* Tue Sep 12 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.1-45mdk
- force crond to use syslog.

* Mon Aug 21 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 3.0.1-44mdk
- Macro's
- BM
- /etc/rc.d/init.d --> /etc/init.d
- Geoff <snailtalk@mandrakesoft.com> no we actually use _initrddir ..

* Mon Jul 17 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0.1-43mdk
- remove useless man-pages compression and let spec-helper work

* Sat Jul 15 2000 Stefan van der Eijk <s.vandereijk@chello.nl>
- changed way manpages are compressed, use find instead of for

* Mon Apr 10 2000 Christopher Molnar <molnarc@mandrakesoft.com> 3.0.1-42mdk
- Fixed group

* Sun Mar 19 2000 John Buswell <johnb@mandrakesoft.com> 3.0.1-41mdk
- Added PPC patches

* Tue Jan 11 2000 Pixel <pixel@linux-mandrake.com>
- non root build

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Move some to from %postun to %preun.
- Merge with redhat patchs.

* Thu Apr 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Mandrake adaptations.

* Wed Apr 14 1999 Michael K. Johnson <johnsonm@redhat.com>
- add note to man page about DST conversion causing strangeness
- documented cron.d patch

* Tue Apr 13 1999 Michael K. Johnson <johnsonm@redhat.com>
- improved cron.d patch

* Mon Apr 12 1999 Erik Troan <ewt@redhat.com>
- added cron.d patch

* Tue Mar 23 1999 Bill Nottingham <notting@redhat.com>
- logrotate changes

* Tue Mar 23 1999 Preston Brown <pbrown@redhat.com>
- clean up log files on deinstallation

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 28)

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Wed Jun 10 1998 Jeff Johnson <jbj@redhat.com>
- reset SIGCHLD before grandchild execle (problem #732)

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- enhanced initscript

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Dec 11 1997 Cristian Gafton <gafton@redhat.com>
- added a patch to get rid of the dangerous sprintf() calls
- added BuildRoot and Prereq: /sbin/chkconfig

* Sun Nov 09 1997 Michael K. Johnson <johnsonm@redhat.com>
- fixed cron/crond dichotomy in init file.

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- fixed bad init symlinks

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- force it to use SIGCHLD instead of defunct SIGCLD

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- updated for chkconfig
- added status, restart options to init script

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Wed Feb 19 1997 Erik Troan <ewt@redhat.com>
- Switch conditional from "axp" to "alpha" 

