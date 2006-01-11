#
# spec file for package statserial
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		statserial
%define version		1.1
%define release		%_revrel

Summary:	A tool which displays the status of serial port modem lines
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Communications
URL:		ftp://sunsite.unc.edu/pub/Linux/system/serial/
Source:		ftp://sunsite.unc.edu/pub/Linux/system/serial/%{name}-%{version}.tar.bz2
Patch:		statserial-1.1-config.patch
Patch1: 	statserial-1.1-dev.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel
BuildRequires:	glibc-static-devel 

%description
The statserial utility displays a table of the signals on a standard
9-pin or 25-pin serial port and indicates the status of the
handshaking lines.  Statserial is useful for debugging serial port
and/or modem problems.


%prep
%setup -q
%patch -p1 -b .config
%patch1 -p1 -b .dev


%build
%{make} CFLAGS="%{optflags} -O3"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man1}

install -m 0755 -s statserial %{buildroot}%{_bindir}/statserial
install -m 0444 statserial.1 %{buildroot}%{_mandir}/man1/statserial.1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/statserial
%{_mandir}/man1/statserial.1.bz2


%changelog
* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-21avx
- bootstrap build (new gcc, new glibc)
- update P0 from mdk

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.1-20avx
- rebuild

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.1-19avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.1-18sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 1.1-17sls
- OpenSLS build
- tidy spec

* Thu Jul 24 2003 Götz Waschk <waschk@linux-mandrake.com> 1.1-16mdk
- fix buildrequires

* Mon Jul 14 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.1-15mdk
- compile with $RPM_OPT_FLAGS

* Fri Jan 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1-14mdk
- add url (yura gusev)

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1-13mdk
- build release
- fix permissions

* Sat Aug 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.1-12mdk
- Add RH patch to make ttyS1 the standard device.
- Sanity build for 8.1.

* Thu Jul 12 2001 Stefan van der Eijk <stefan@eijk.nu> 1.1-11mdk
- BuildRequires:	ncurses-devel

* Tue May 01 2001 David BAUDENS <baudens@mandrakesoft.com> 1.1-10mdk
- Use %%{_buildroot} for BuildRoot

* Tue Mar 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.1-9mdk
- Do nothing but rebuild.

* Thu Jul 20 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1-8mdk
- BM, spec-helper and macros

* Wed Mar 22 2000 Daouda Lo <daouda@mandrakesoft.com> 1.1-7mdk
- added define sections
- fix group 

* Sun Oct 31 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- SMP check/build

* Sun Jul  4 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- bzip manpages

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 13)

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root
- include arch sparc

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc
