%define name	crontabs
%define version	1.10
%define release	4sls

Summary:	Root crontab files used to schedule the execution of programs.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Other
Source0:	crontab.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildArch:	noarch

Requires:	/usr/bin/run-parts

%description
The crontabs package contains root crontab files.  Crontab is the
program used to install, uninstall or list the tables used to drive the
cron daemon.  The cron daemon checks the crontab files to see when
particular commands are scheduled to be executed.  If commands are
scheduled, it executes them.

Crontabs handles a basic system function, so it should be installed on
your system.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.{hourly,daily,weekly,monthly}

bzip2 -dc  %{SOURCE0} > $RPM_BUILD_ROOT/%{_sysconfdir}/crontab
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/crontab

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/crontab
%dir %{_sysconfdir}/cron.hourly
%dir %{_sysconfdir}/cron.daily
%dir %{_sysconfdir}/cron.weekly
%dir %{_sysconfdir}/cron.monthly

%changelog
* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 1.10-4sls
- OpenSLS build
- tidy spec

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.10-3mdk
- rebuild
- cosmetics

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.10-2mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Mon Apr 08 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.10-1mdk
- Aimlessly bump version to match it with the one in RH.

* Tue Apr  2 2002 Pixel <pixel@mandrakesoft.com> 1.9-4mdk
- don't require tmpwatch

* Wed Feb 20 2002 Pixel <pixel@mandrakesoft.com> 1.9-3mdk
- make rpmlint happy
- crontab.bz2: call run-parts with low priority (nice -n 19)

* Sat Jul 07 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.9-2mdk
- Generate a politically correct patckage aka build it on the cluster.

* Sat Jun 16 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.9-1mdk
- Shut up gc's bot aka bump it up to 1.9. :)
- s/Copyright/License/;

* Thu May  3 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.7-13mdk
- Remove run-parts now in setup package.

* Wed May  2 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.7-12mdk
- Update run-part with rh version.

* Tue Mar 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.7-11mdk
- Do nothing but rebuild.

* Tue Sep 19 2000 Francis Galiegue <fg@mandrakesoft.com> 1.7-10mdk

- /etc/crontab is %%config(noreplace)

* Fri Jul 28 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.7-9mdk
- macroszifications

* Mon Apr  3 2000 Adam Lebsack <adam@mandrakesoft.com> 1.7-8mdk
- Release build.

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Release build.

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- don't run .rpm{save,new,orig} files (bug #2190)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Mon Nov 30 1998 Bill Nottingham <notting@redhat.com>
- crontab: set HOME=/

* Sat Jun 27 1998 Jeff Johnson <jbj@redhat.com>
- run-parts: skip sub-directories (e.g. CVS) found instead of complaining

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Erik Troan <ewt@redhat.com>
- moved crontab jobs up a bit to make sure they aren't confused by
  switching to and fro daylight savings time
  
* Fri Oct 24 1997 Erik Troan <ewt@redhat.com>
- removed tmpwatch and at entries

* Thu Jul 31 1997 Erik Troan <ewt@redhat.com>
- made a noarch package
