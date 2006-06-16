#
# spec file for package clamav
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		clamav
%define version		0.88.2
%define release		%_revrel

%define	major		1
%define libname		%mklibname %{name} %{major}

Summary:	An anti-virus utility for Unix
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File Tools
URL:		http://clamav.sourceforge.net/
Source0:	http://www.clamav.net/%{name}-%{version}.tar.gz
Source1:	http://www.clamav.net/%{name}-%{version}.tar.gz.sig
Source4:	clamd.run
Source5:	clamd-log.run
Source6:	freshclam.run
Source7:	freshclam-log.run
Patch0:		clamav-0.87-avx-config.patch
Patch1:		clamav-0.88.1-avx-stderr.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5, automake1.7
BuildRequires:	zlib-devel, gmp-devel, bzip2-devel

Requires(post):	clamav-db
Requires(preun): clamav-db
Requires(post):	%{libname} = %{version}
Requires(preun): %{libname} = %{version}
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper

%description 
Clam AntiVirus is an anti-virus toolkit for Unix. The main purpose
of this software is the integration with mail seversions (attachment
scanning). The package provides a flexible and scalable
multi-threaded daemon, a commandline scanner, and a tool for
automatic updating via Internet. The programs are based on a
shared library distributed with the Clam AntiVirus package, which
you can use in your own software. 


%package -n clamd
Summary:	The Clam AntiVirus Daemon
Group:		System/Servers
Requires:	%{name} = %{version}
Requires(post):	clamav-db
Requires(preun): clamav-db
Requires(post):	%{libname} = %{version}
Requires(preun): %{libname} = %{version}
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper

%description -n	clamd
The Clam AntiVirus Daemon


%package -n %{name}-db
Summary:	Virus database for %{name}
Group:		Databases
Requires:	%{name} = %{version}
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper


%description -n	%{name}-db
The actual virus database for %{name}


%package -n %{libname}
Summary:	Shared libraries for %{name}
Group:          System/Libraries

%description -n	%{libname}
Shared libraries for %{name}


%package -n %{libname}-devel
Summary:	Development library and header files for the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel lib%{name}-devel
Obsoletes:	%{name}-devel lib%{name}-devel

%description -n	%{libname}-devel
This package contains the static %{libname} library and its header
files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}

# clean up
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done
	
%patch0 -p1 -b .avx
%patch1 -p1 -b .stderr


%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force && aclocal-1.7 && autoconf && automake-1.7

#export SENDMAIL="%{_libdir}/sendmail"

%serverbuild

%configure2_5x \
    --disable-%{name} \
    --with-user=%{name} \
    --with-group=%{name} \
    --with-dbdir=%{_localstatedir}/%{name} \
    --enable-id-check \
    --enable-clamuko \
    --enable-bigstack \
    --without-libcurl \
    --with-zlib=%{_prefix} \
    --disable-zlib-vcheck \
    --disable-milter \
    --without-tcpwrappers
#   --enable-debug

%make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

install -m 0644 etc/clamd.conf %{buildroot}%{_sysconfdir}/clamd.conf
install -m 0644 etc/freshclam.conf %{buildroot}%{_sysconfdir}/freshclam.conf

mkdir -p %{buildroot}%{_srvdir}/{clamd,freshclam}/log
install -m 0740 %{SOURCE4} %{buildroot}%{_srvdir}/clamd/run
install -m 0740 %{SOURCE5} %{buildroot}%{_srvdir}/clamd/log/run
install -m 0740 %{SOURCE6} %{buildroot}%{_srvdir}/freshclam/run
install -m 0740 %{SOURCE7} %{buildroot}%{_srvdir}/freshclam/log/run

# pid file dir
mkdir -p %{buildroot}/var/run/%{name}

# fix TMPDIR
mkdir -p %{buildroot}%{_localstatedir}/%{name}/tmp


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
if [ -d /var/log/supervise/freshclam -a ! -d /var/log/service/freshclam ]; then
    mv /var/log/supervise/freshclam /var/log/service/
fi
%_post_srv freshclam


%preun
%_preun_srv freshclam


%post -n clamd
if [ -d /var/log/supervise/clamd -a ! -d /var/log/service/clamd ]; then
    mv /var/log/supervise/clamd /var/log/service/
fi
%_post_srv clamd


%preun -n clamd
%_preun_srv clamd


%pre -n %{name}-db
%_pre_useradd clamav %{_localstatedir}/%{name} /bin/sh 91


%post -n %{name}-db
# try to keep most uptodate database
for i in main daily; do
    if [ -f /var/lib/clamav/$i.cvd.rpmnew ]; then
        if [ /var/lib/clamav/$i.cvd.rpmnew -nt /var/lib/clamav/$i.cvd ]; then
            mv -f /var/lib/clamav/$i.cvd.rpmnew /var/lib/clamav/$i.cvd
        else
            rm -f /var/lib/clamav/$i.cvd.rpmnew
        fi
    fi
done


%postun -n %{name}-db
%_postun_userdel clamav


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/clamd.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/freshclam.conf
%{_bindir}/clamscan
%{_bindir}/clamdscan
%{_bindir}/freshclam
%{_bindir}/sigtool
%{_mandir}/man1/sigtool.1*
%{_mandir}/man1/clamdscan.1*
%{_mandir}/man1/clamscan.1*
%{_mandir}/man1/freshclam.1*
%{_mandir}/man5/clamd.conf.5*
%{_mandir}/man5/freshclam.conf.5*
%exclude %{_mandir}/man8/%{name}-milter.8*
%dir %attr(0755,clamav,clamav) /var/run/%{name}
%dir %attr(0755,clamav,clamav) %{_localstatedir}/%{name}
%dir %attr(0750,root,admin) %{_srvdir}/freshclam
%dir %attr(0750,root,admin) %{_srvdir}/freshclam/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/freshclam/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/freshclam/log/run

%files -n clamd
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/clamd.conf
%{_sbindir}/clamd
%{_mandir}/man8/clamd.8*
%dir %attr(0750,root,admin) %{_srvdir}/clamd
%dir %attr(0750,root,admin) %{_srvdir}/clamd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/clamd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/clamd/log/run

%files -n %{name}-db
%defattr(-,root,root)
%dir %attr(0755,clamav,clamav) %{_localstatedir}/%{name}
%attr(0644,clamav,clamav) %config(noreplace) %{_localstatedir}/%{name}/daily.cvd
%attr(0644,clamav,clamav) %config(noreplace) %{_localstatedir}/%{name}/main.cvd
%dir %attr(0755,clamav,clamav) %{_localstatedir}/%{name}/tmp

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_bindir}/clamav-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/libclamav.pc

%files doc
%defattr(-,root,root)
%doc AUTHORS BUGS ChangeLog FAQ NEWS README test UPGRADE COPYING
%doc contrib/clamdwatch contrib/clamavmon contrib/clamdmon

      
%changelog
* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.88.2
- add -doc subpackage
- rebuild with gcc4
- fixed group

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.88.2
- 0.88.2: fixes CVE-2006-1989

* Tue Apr 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.88.1
- 0.88.1: fixes CVE-2006-1614, CVE-2006-1615, CVE-2006-1630
- rediff P1

* Fri Feb 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.88
- 0.88 (fixes CVE-2006-0162)

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.87.1
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.87.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Mon Nov 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.87.1-1avx
- 0.87.1; security fixes for CVE-2005-3239, CVE-2005-3303, CVE-2005-3500,
  CVE-2005-3501

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.87-2avx
- clamav is static uid/gid 91, not 89 (clashes with dhcpd)
- useradd only in clamav-db, not in clamav or clamd
- execline the runscripts and make both freshclam and clamd run
  as user clamav rather than root
- P1: allow clamav/freshclam to log to stderr (from http://www.gluelogic.com/code/)
- P0: adjust the configs to log to stderr by default
- drop the logrotate files and logfiles

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.87-1avx
- 0.87

* Sat Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.2-4avx
- don't build against libcurl as apparently that would be in violation
  of the GPL since we build it against OpenSSL; see:
    http://curl.haxx.se/legal/distro-dilemma.html

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.2-3avx
- s/supervise/service/ in log/run

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.2-2avx
- spec tidys

* Fri Sep 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.2-1avx
- 0.86.2
- use execlineb for run scripts
- move logdir to /var/log/service/{freshclam,clamd}
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.1-3avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.1-2avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.86.1-1avx
- 0.86.1 (fixes a possible crash in libmspack's Quantum decompressor)
- make the freshclam and clamd logfiles mode 0640 rather than 0644

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.83-3avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.83-2avx
- use logger for logging

* Wed Feb 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.83-1avx
- 0.83
- first Annvix build
- big spec cleanups; get rid of milter support
- remove BuildRequires: bc
- clamav is static uid/gid 89
- supervise scripts

* Mon Feb 07 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.82-1mdk
- 0.82
- drop cvs fixes patch, it's implemented upstream

* Wed Feb 02 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.81-4mdk
- exclude the %{name}-milter.8 man page if built without milter 

* Wed Feb 02 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.81-3mdk
- new P1
- mention the conditional build switch in the description

* Mon Jan 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.81-2mdk
- added P1 in an attempt to fix #13355, P1 also fixes various
  other issues

* Wed Jan 26 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.81-1mdk
- 0.81
- we were allready shipping the clamav source, so.. there's little
  point of nuking the M$ *.exe binary...
- please mrlint in the requires-on-release quest
- misc spec file fixes

* Thu Jan 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.81-0.rc1.1mdk
- fix release string (duh!)

* Thu Jan 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.81-0.rc1.1mdk
- 0.81rc1
- drop the libtool patch by Gwenole Beauchesne, it's merged upstream
- fix deps
- fix P0 and TMPDIR

* Wed Dec 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.80-8mdk
- revert latest "lib64 fixes"

* Tue Dec 28 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.80-7mdk
- applied fixes by Bill Randle
- handle log file creation in the sysv scripts too, cleanup these
  scripts some
- misc spec file fixes

* Thu Nov 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.80-6mdk
- rebuilt due to missing clamd package

* Thu Nov 18 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.80-5mdk
- libtool fixes

* Thu Nov 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.80-4mdk
- use "export EGREP=egrep" as suggested by Luca Berra in an 
  attempt to fix build on x86_64

* Tue Nov 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.80-3mdk
- since the libs won't provide, we need to require them

* Wed Nov 10 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.80-2mdk
- fix a silly groups typo

* Mon Oct 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.80-1mdk
- 0.80
- rediffed P0
- add the freshclam init script (S3)
- reorder and rename S1 - S6
- fix S6
- change so that client parts belongs to the main clamav package
- fix deps
- misc spec file fixes

* Sat Jul 31 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.75.1-1mdk
- use "-1mdk" ;) (catched by Bill Randle)

* Fri Jul 30 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.75.1-1mdk
- 0.75.1 (bugfix release)

* Thu Jul 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.75-2mdk
- 0.75-1 (bugfix release)

* Fri Jul 23 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.75-1mdk
- 0.75

* Wed Jun 30 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.74-1mdk
- 0.74

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.73-1mdk
- 0.73
- drop P2, it's in there

* Thu Jun 03 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.72-1mdk
- 0.72

* Thu Jun 03 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.72-0.1mdk
- 0.72 (from cvs)

* Tue May 25 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.71-3mdk
- added P2 from PLD

* Sun May 23 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.71-2mdk
- added fixes by Bill Randle <billr@neocat.org>:
  | drop S9 (not needed as default mdk install does not run amavisd chroot)
  | add German docs
  | add --with/--without freshclamhourly option for hourly+random offset
  | freshclam runs
  | add P1
  | add clamav user to amavis group
  | drop unneeded mdk92/mdk100 defines
- fixed a more convenient README.qmail+qmail-scanner file ;)
- don't ship the *.exe file, put contrib sources in the devel sub package

* Fri May 21 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.71-1mdk
- 0.71
- rediffed P0
- drop clamdmail, eventually it will be a stand alone package, if 
  it's better maintained

* Sun May 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.70-2mdk
- remove stuff that always enable build of clamdmail (thanks 
  Luca Berra <bluca@comedia.it>)

* Sun Apr 18 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.70-1mdk
- 0.70
- clamdmail-0.15a
- merge static devel into devel
- added fixes by Bill Randle <billr@neocat.org>:
  - rediff Patch0
  - additonal doc files
  - create Patch1 for clamdmail
  - clamav.clamav+amavisd-new-fixup.sh script
  - change start priority for clamd so it starts before clamav-milter
    (reported by and suggested fix by jbolin@users.sourceforge.net)

* Fri Apr 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.68-1mdk
- 0.68-1
- drop P1
- fix P0

* Tue Feb 17 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.67-4mdk
- added fixes from 0.67-1 (P2)
- fixed a stupid spec file thang (thanks Luca Berra and Daniel J McDonald)
- added a note about qmail+qmail-scanner
- for now i will only correct things i find too strange or too stupid,
  don't expect me to work this fulltime as the previous 2-3 years... the
  previous changelog entry explains why i jumped in here.

* Tue Feb 17 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.67-3mdk
- fix freshclam cron policy: do not ship clamav with a db update frequency 
  of one hour. once a day is ok for joe user. thousands or maybe millions 
  of mdk10+ boxes could bring the clamav antivirus database mirrors to its 
  knees, or even worse in about six months turn it into a pre-paid 
  subscription service. any serious admin can change this update frequency,
  at will post install...
- fix conditional build for the sendmail milter
- turn on debug code, disable clamuko (who uses it?)
- make clamd use its own config file
- misc spec file fixes

* Sun Feb 15 2004 Bill Randle <billr@neocat.org> 0.67-2mdk
- update spec file to match Luca's version in contrib
- put freshclam cron file in cron.hourly

* Sun Feb 15 2004 Bill Randle <billr@neocat.org> 0.67-1mdk
- sync with new 0.67 release (fixes memory management problem)

* Sun Feb 15 2004 Luca Berra <bluca@vodka.it> 0.66-3mdk
- really fix freshclam cron script

* Wed Feb 11 2004 Luca Berra <bluca@vodka.it> 0.66-2mdk 
- fix clamdmail version

* Wed Feb 11 2004 Luca Berra <bluca@vodka.it> 0.66-1mdk 
- 0.66
- fix freshclam return code in cron script
- use freshclam.conf
- allow building without clamdmail for 9.2 (no libripmime-devel)
- removed P1 (included upstream)
- rediffed P0
- massage rpm for easy snapshot/release build

* Sun Dec 07 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.66-0.20031204.1mdk
- fix weird #6486 (S2)
- use a recent CVS snapshot (there's simply too much going on here...)
- clamdmail-0.15
- buildrequires ripmime-devel (for clamdmail)
- drop P1 & P2
- rediffed P0
- added new P1

* Wed Nov 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.65-4mdk
- added P2 (CVS fixes)

* Wed Nov 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.65-3mdk
- clamdmail-0.14
- drop P2, it's included

* Fri Nov 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.65-2mdk
- fixed P0

* Thu Nov 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.65-1mdk
- 0.65
- removed one patch, added P1 & P2
- gmp is needed now
- misc spec file fixes

* Sat Sep 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.61-0.20030829.1mdk
- use the 20030829 snapshot
- remove patches that's included in the upstream source
- changed P3 to P1
- fix S7 and log stuff in the spec file
- fetch virus databases as these are not included
- clamdmail-0.13
- fix buildrequires

* Mon Aug 25 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.61-0.20030806.2mdk
- use the correct 20030806 snapshot
- added P1 to fix stale sockets if unclean shutdown.
- added P2 to fix cli_malloc build error
- update url
- update url in mirrors.txt file (P3)

* Tue Aug 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.61-0.20030806.1mdk
- use the 20030806 snapshot
- added 2 files from contrib into docdir

* Tue Aug 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.61-0.20030705.5mdk
- spec file work around for rpm stupidity...

* Tue Aug 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.61-0.20030705.4mdk
- added the clamdmail subpckage

* Tue Jul 29 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.61-0.20030705.3mdk
- use some more spec file voodoo magic to please distlint (a bit?)

* Sat Jul 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.61-0.20030705.2mdk
- change description on request by the author

* Wed Jul 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.61-0.20030705.1mdk
- use the 20030705 snapshot
- added some more docs

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.60-2mdk
- rebuild
- misc spec file fixes

* Sun Jun 22 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.60-1mdk
- misc fixes by mutt@free.fr:
  - upgrade to 0.60 (clamav-0.54-buffer_overflow_fix included)
  - doc changes (Spanish, Japanese), new file mirrors.txt
- added the clamav-milter sub package (S3 & S4)
- added cron script to auto update the virus database, plus a logrotate
  configuration file (S5 & S6)
- use the %%configure2_5x macro
- fix buildrequires
- rediff P0
- move logs to /var/log/clamav/ (msec fix)
- misc spec file fixes

* Sat May 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.54-8mdk
- rebuilt to have rpm v4.2 pick up provides

* Thu Mar 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.54-7mdk
- fix potential security hole (P1) as in:
  http://archive.elektrapro.com/clamav.elektrapro.com/users/2003/3/msg00016.html

* Thu Mar 06 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.54-6mdk
- use the %%mklibname macro
- misc spec file fixes
- fix pid file location
- got rpmlint a little happier...

* Thu Jan 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.54-5mdk
- build release

* Fri Nov 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.54-4mdk
- argh!!! viruscanner should spell virusscanner, right?

* Fri Nov 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.54-3mdk
- added virtual provides (pointed out by Buchan Milne)
  clamav Provides: viruscanner AV-Scanner
  clamd Provides: viruscanner-daemon AV-Scanner-Daemon

* Fri Nov 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.54-2mdk
- fix %%_pre_useradd (pointed out by Buchan Milne)
- also fix ldconfig in %%post %%postun (wierd...)

* Thu Nov 21 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.54-1mdk
- new version
- updated P0
- %{_bindir}/clamdscan was added to the clamd package
- misc spec file fixes

* Fri Nov 01 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.53-1mdk
- new version

* Tue Oct 29 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.52-1mdk
- new version
- misc spec file fixes

* Sat Oct 19 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.51-3mdk
- attrib 711 on %{_localstatedir}/clamav was too restrictive for
  qmail-scanner, changed that to 755

* Mon Oct 14 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.51-2mdk
- fixed Group=File tools for main package (correct?)

* Wed Oct 09 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.51-1mdk
- new version
- libifictions and daemonification
- major spec file fixes

* Thu Aug 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.24-1mdk
- new version
- added GnuPG signature
- misc spec file fixes

* Sat Aug  3 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.23-1mdk
- new version

* Wed Jul 24 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.22-1mdk
- new version

* Thu Jul 18 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.21-1mdk
- new version

* Tue Jul 16 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.20-1mdk
- new version, new url
- misc spec file fixes

* Wed Jun 12 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.15-1mdk
- new version

* Sat Jun  1 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.14-1mdk
- new version
- remove P0

* Sat May 11 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.11-1mdk
- initial cooker contrib
