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
%{_mandir}/man1/statserial.1*


%changelog
* Fri Dec 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1
- rebuild against new ncurses

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.1
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
