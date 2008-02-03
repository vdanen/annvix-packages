#
# spec file for package tcpdump
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		tcpdump
%define version		3.9.8
%define release		%_revrel
%define epoch		2

Summary:	A network traffic monitoring tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	BSD
Group:	 	Monitoring
URL:		http://www.tcpdump.org
Source0:	http://www.tcpdump.org/release/%{name}-%{version}.tar.gz
Source1:	http://www.tcpdump.org/release/%{name}-%{version}.tar.gz.sig

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libpcap-devel

%description
tcpdump is a command-line tool for monitoring network traffic.  tcpdump
can capture and display the packet headers on a particular network
interface or on all interfaces.  tcpdump can display all of the packet
headers, or just the ones that match particular criteria.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.



%prep
%setup -q


%build
libtoolize --copy --force
%define	optflags $RPM_OPT_FLAGS -DIP_MAX_MEMBERSHIPS=20
%configure --enable-ipv6
%undefine optflags

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_sbindir}/tcpdump
%{_mandir}/man1/tcpdump.1*

%files doc
%defattr(-,root,root)
%doc README CHANGES CREDITS FILES LICENSE TODO VERSION PLATFORMS


%changelog
* Thu Dec 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.9.8
- 3.9.8

* Mon Sep 17 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.9.7
- 3.9.7; fixes CVE-2007-3798
- drop P0; fixed upstream
- rebuild against new libpcap

* Thu Mar 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.9.4
- P0: security fix for CVE-2007-1218

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.9.4
- really remove docs from main package

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.9.4
- 3.9.4
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.9.3
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.9.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.9.3-2avx
- rebuild against new libpcap

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.9.3-1avx
- 3.9.3
- drop P0-P3

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.8.3-4avx
- rebuild

* Thu May 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.8.3-3avx
- P0-P3: security fixes for CAN-2005-1278, CAN-2005-1279, CAN-2005-1280

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.8.3-2avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 3.8.3-1sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
