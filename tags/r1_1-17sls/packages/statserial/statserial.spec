%define name	statserial
%define version	1.1
%define release	17sls

Summary:	A tool which displays the status of serial port modem lines
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Communications
URL:		ftp://sunsite.unc.edu/pub/Linux/system/serial/
Source:		ftp://sunsite.unc.edu/pub/Linux/system/serial/%{name}-%{version}.tar.bz2
Patch:		%{name}-1.1-config.patch.bz2
Patch1: 	%name-1.1-dev.patch.bz2

BuildRoot:	%_tmppath/%name-%version-%release-root
BuildRequires:	ncurses-devel
BuildRequires:	glibc-static-devel 

%description
The statserial utility displays a table of the signals on a standard
9-pin or 25-pin serial port and indicates the status of the
handshaking lines.  Statserial is useful for debugging serial port
and/or modem problems.

Install the statserial package if you need a tool to help debug serial
port or modem problems.

%prep

%setup -q
%patch -p1 -b .config
%patch1 -p1 -b .dev

%build
%{make} CFLAGS="$RPM_OPT_FLAGS -O3"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_bindir},%{_mandir}/man1}

install -m 755 -s statserial $RPM_BUILD_ROOT%{_bindir}/statserial
install -m 444 statserial.1 $RPM_BUILD_ROOT%{_mandir}/man1/statserial.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/statserial
%{_mandir}/man1/statserial.1.bz2

%changelog
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
- Use %%_tmppath for BuildRoot

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
