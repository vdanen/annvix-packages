# NOTE: This doesn't seem to compile with gcc 3.3.1 so no binary package
# yet, just the src.rpm until someone can fix it

%define name	tcp_wrappers
%define version	7.6
%define release	24sls

Summary: 	A security tool which acts as a wrapper for TCP daemons.
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Group: 		System/Servers	
License: 	BSD
URL:		http://ftp.porcupine.org/pub/security/
Source:	        http://ftp.porcupine.org/pub/security/tcp_wrappers_7.6.tar.bz2
Patch0:         http://www.imasy.or.jp/~ume/ipv6/tcp_wrappers_7.6-ipv6-1.14.diff.bz2
Patch1: 	tcp_wrappers_7.6-config.patch.2.bz2
Patch2:		tcp_wrappers-7.16-ia64-compile-fix.patch.bz2

BuildRoot: 	%{_tmppath}/%{name}-%{version}-buildroot


%description
The tcp_wrappers package provides small daemon programs which can
monitor and filter incoming requests for systat, finger, ftp, telnet,
rlogin, rsh, exec, tftp, talk and other network services.

Install the tcp_wrappers program if you need a security tool for
filtering incoming network services requests.

%package devel
Summary:	A security library which acts as a wrapper for TCP daemons.
Group:		Development/C

%description devel
Library and header files for the tcp_wrappers program

%prep
%setup -q -n tcp_wrappers_7.6
%patch0 -p2 
%patch1 -p1 
%patch2 -p1

%build
%make  REAL_DAEMON_DIR=%{_sbindir} linux

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_includedir},%{_libdir},%{_sbindir},%{_mandir}/man3,%{_mandir}/man5,%{_mandir}/man8}

install -m 644 hosts_access.3 $RPM_BUILD_ROOT/%{_mandir}/man3
install -m 644 hosts_access.5 hosts_options.5 $RPM_BUILD_ROOT/%{_mandir}/man5
( cd $RPM_BUILD_ROOT/%{_mandir}/man5 && {
	ln hosts_access.5 hosts.allow.5
	ln hosts_access.5 hosts.deny.5
  }
)
install -m 644 tcpd.8 tcpdchk.8 tcpdmatch.8 $RPM_BUILD_ROOT/%{_mandir}/man8
install -m 644 libwrap.a $RPM_BUILD_ROOT/%{_libdir}
install -m 644 tcpd.h $RPM_BUILD_ROOT/%{_includedir}
install -m 755 safe_finger $RPM_BUILD_ROOT/%{_sbindir}
install -m 755 tcpd $RPM_BUILD_ROOT/%{_sbindir}
install -m 755 tcpdchk $RPM_BUILD_ROOT/%{_sbindir}
install -m 755 tcpdmatch $RPM_BUILD_ROOT/%{_sbindir}
install -m 755 try-from $RPM_BUILD_ROOT/%{_sbindir}

# (fg) 20000905 FIXME FIXME FIXME: setenv in libwrap.a is rather strange for
# one, so I remove it here - but will it break anything else?

ar d $RPM_BUILD_ROOT/%{_libdir}/libwrap.a setenv.o

%clean
rm -Rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,755)
%doc BLURB CHANGES README* DISCLAIMER Banners.Makefile
%{_mandir}/man*/*
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%doc DISCLAIMER
%{_includedir}/tcpd.h
%{_libdir}/libwrap.a

%changelog
* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 7.6-24sls
- OpenSLS build
- tidy spec

* Mon Jul 21 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 7.6-23mdk
- rebuild
- rm -rf $RPM_BUILD at the beginning of %%install

* Wed Aug 28 2002 Warly <warly@mandrakesoft.com> 7.6-22mdk
- new ipv6 patch version

* Sun Jul  7 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 7.6-21mdk
- Apply Patch2 on all arches to build with PIC code

* Wed Feb 13 2002 Warly <warly@mandrakesoft.com> 7.6-20mdk
- update specfile

* Sat Mar 17 2001 Francis Galiegue <fg@mandrakesoft.com> 7.6-19mdk

- /me sucks, resubmit

* Sat Mar 17 2001 Francis Galiegue <fg@mandrakesoft.com> 7.6-18mdk

- Add -fPIC to CFLAGS for ia64

* Tue Jan 09 2001 Francis Galiegue <fg@mandrakesoft.com> 7.6-17mdk

- No -b for %%patch directives
- Fixed group for -devel package

* Tue Sep 05 2000 Francis Galiegue <fg@mandrakesoft.com> 7.6-16mdk

- Removed setenv.o from libwrap.a

* Fri Jul 28 2000 Francis Galiegue <fg@mandrakesoft.com> 7.6-15mdk

- Spec file fixes
- %files list fixes
- permission fixes
- use links, not symlinks
- include doc in only one package, not both

* Mon Jul 17 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 7.6-14mdk
- fix %%clean
- Christian Zoffoli <czoffoli@linux-mandrake.com> :
	* fixed permission
	* removed %group
	* removed _sysconfdir 
	* macroszifications
	* new IPv6 patch v1.9

* Fri Jun 23 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 7.6-13mdk
- compiled with IPv6 patch

* Sat Apr 08 2000 John Buswell <johnb@mandrakesoft.com> 7.6-12mdk
- split devel elements into devel package
- removed version number from spec file
- added docs to devel package

* Thu Mar 30 2000 John Buswell <johnb@mandrakesoft.com> 7.6-11mdk
- Fixed groups
- spec-helper

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- add netgroup support (r).

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 7)

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Sat Aug 22 1998 Jeff Johnson <jbj@redhat.com>
- close setenv bug (problem #690)
- spec file cleanup

* Thu Jun 25 1998 Alan Cox <alan@redhat.com>
- Erp where did the Dec 05 patch escape to

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Dec 05 1997 Erik Troan <ewt@redhat.com>
- don't build setenv.o module -- it just breaks things

* Wed Oct 29 1997 Marc Ewing <marc@redhat.com>
- upgrade to 7.6

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Mon Mar 03 1997 Erik Troan <ewt@redhat.com>
- Upgraded to version 7.5
- Uses a build root
