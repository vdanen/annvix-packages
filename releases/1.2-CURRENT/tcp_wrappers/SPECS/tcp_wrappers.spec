#
# spec file for package tcp_wrappers
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		tcp_wrappers
%define version		7.6
%define release		%_revrel

Summary: 	A security tool which acts as a wrapper for TCP daemons
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Group: 		System/Servers	
License: 	BSD
URL:		http://ftp.porcupine.org/pub/security/
Source:	        http://ftp.porcupine.org/pub/security/%{name}_%{version}.tar.bz2
Patch0:		tcpw7.2-config.patch
Patch1:		tcpw7.2-setenv.patch
Patch2:		tcpw7.6-netgroup.patch
Patch3:		tcp_wrappers-7.6-bug11881.patch
Patch4:		tcp_wrappers-7.6-bug17795.patch
Patch5:		tcp_wrappers-7.6-bug17847.patch
Patch6:		tcp_wrappers-7.6-fixgethostbyname.patch
Patch7:		tcp_wrappers-7.6-docu.patch
Patch9:		tcp_wrappers.usagi-ipv6.patch
Patch10:	tcp_wrappers.ume-ipv6.patch
Patch11:	tcp_wrappers-7.6-shared.patch
Patch12:	tcp_wrappers-7.6-sig.patch
Patch13:	tcp_wrappers-7.6-strerror.patch
Patch14:	tcp_wrappers-7.6-ldflags.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}


%description
The tcp_wrappers package provides small daemon programs which can
monitor and filter incoming requests for systat, finger, ftp, telnet,
rlogin, rsh, exec, tftp, talk and other network services.

Install the tcp_wrappers program if you need a security tool for
filtering incoming network services requests.


%package devel
Summary:	A security library which acts as a wrapper for TCP daemons
Group:		Development/C

%description devel
Library and header files for the tcp_wrappers program


%prep
%setup -q -n %{name}_%{version}
%patch0 -p1 -b .config
%patch1 -p1 -b .setenv
%patch2 -p1 -b .netgroup
%patch3 -p1 -b .bug11881
%patch4 -p1 -b .bug17795
%patch5 -p1 -b .bug17847
%patch6 -p1 -b .fixgethostbyname
%patch7 -p1 -b .docu
%patch9 -p0 -b .usagi-ipv6
%patch10 -p1 -b .ume-ipv6
%patch11 -p1 -b .shared
%patch12 -p1 -b .sig
%patch13 -p1 -b .strerror
%patch14 -p1 -b .cflags


%build
%make OPTFLAGS="%{optflags} -fPIC -DPIC -D_REENTRANT -DHAVE_STRERROR" LDFLAGS="-pie" REAL_DAEMON_DIR=%{_sbindir} linux


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_includedir},%{_libdir},%{_sbindir},%{_mandir}/{man3,man5,man8}}

install -m 0644 hosts_access.3 %{buildroot}%{_mandir}/man3
install -m 0644 hosts_access.5 hosts_options.5 %{buildroot}%{_mandir}/man5
pushd %{buildroot}%{_mandir}/man5
    ln hosts_access.5 hosts.allow.5
    ln hosts_access.5 hosts.deny.5
popd

install -m 0644 tcpd.8 tcpdchk.8 tcpdmatch.8 %{buildroot}%{_mandir}/man8
install -m 0644 libwrap.a %{buildroot}%{_libdir}
install -m 0644 tcpd.h %{buildroot}%{_includedir}
install -m 0755 safe_finger %{buildroot}%{_sbindir}
install -m 0755 tcpd %{buildroot}%{_sbindir}
install -m 0755 tcpdchk %{buildroot}%{_sbindir}
install -m 0755 tcpdmatch %{buildroot}%{_sbindir}
install -m 0755 try-from %{buildroot}%{_sbindir}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


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
* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.6-29avx
- sync patches with Mandriva (who synced with Fedora)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.6-28avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.6-27avx
- bootstrap build

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.6-26avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 7.6-25sls
- minor spec cleanups

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
