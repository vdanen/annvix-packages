#
# spec file for package libpcap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libpcap
%define version		0.9.8
%define release		%_revrel

%define	major		0
%define minor		9
%define libname 	%mklibname pcap %{major}
%define devname		%mklibname pcap -d

Summary:        A system-independent interface for user-level packet capture
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
URL:		http://www.tcpdump.org
Source0:	http://www.tcpdump.org/release/libpcap-%{version}.tar.gz
Source1:	http://www.tcpdump.org/release/libpcap-%{version}.tar.gz.sig

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	bison
BuildRequires:	flex

%description
Libpcap provides a portable framework for low-level network monitoring.
Libpcap can provide network statistics collection, security monitoring
and network debugging.  Since almost every system vendor provides a
different interface for packet capture, the libpcap authors created this
system-independent API to ease in porting and to alleviate the need for
several system-dependent packet capture modules in each application.


%package -n %{libname}
Summary:	A system-independent interface for user-level packet capture
Group:          System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n %{libname}
Libpcap provides a portable framework for low-level network monitoring.
Libpcap can provide network statistics collection, security monitoring
and network debugging.  Since almost every system vendor provides a
different interface for packet capture, the libpcap authors created this
system-independent API to ease in porting and to alleviate the need for
several system-dependent packet capture modules in each application.


%package -n %{devname}
Summary:	Static library and header files for the pcap library
Group:		Development/C
License: 	BSD
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname pcap 0 -d

%description -n %{devname}
Libpcap provides a portable framework for low-level network monitoring.
Libpcap can provide network statistics collection, security monitoring
and network debugging.  Since almost every system vendor provides a
different interface for packet capture, the libpcap authors created this
system-independent API to ease in porting and to alleviate the need for
several system-dependent packet capture modules in each application.

This package contains the static pcap library and its header files needed to
compile applications such as tcpdump, etc.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
rm -rf doc/CVS


%build
%serverbuild
%configure2_5x --enable-ipv6

%make "CCOPT=%{optflags} -fPIC"

#
# (fg) FIXME - UGLY - HACK - but libpcap's Makefile doesn't allow to build a
# shared lib...
#

gcc -Wl,-soname,libpcap.so.%{major} -shared -fPIC -o libpcap.so.%{major}.%{minor} *.o


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

install -m 0755 libpcap.so.%{major}.%{minor} %{buildroot}/%{_libdir}

pushd %{buildroot}%{_libdir}
    ln -s libpcap.so.%{major}.%{minor} libpcap.so.0
    ln -s libpcap.so.%{major}.%{minor} libpcap.so
popd

# install additional headers
install -m 0644 pcap-int.h %{buildroot}%{_includedir}/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libpcap.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libpcap.so
%{_libdir}/libpcap.a
%{_mandir}/man3/pcap.3*

%files doc
%defattr(-,root,root)
%doc README* CHANGES CREDITS FILES INSTALL.txt LICENSE VERSION doc TODO


%changelog
* Thu Dec 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8
- 0.9.8

* Sat Sep 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9.7
- 0.9.7
- use %%serverbuild
- implement devel naming policy
- implement library provides policy

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1
- 0.9.1
- bump minor to 9
- install additional headers
- add signature
- fix redundant provides

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.8.3-5avx
- bootstrap build (new gcc, new glibc)

* Sat Jul 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.8.3-4avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.8.3-3avx
- bootstrap build

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.8.3-2avx
- Annvix build

* Fri Apr 30 2004 Vincent Danen <vdanen@opensls.org> 0.8.3-1sls
- 0.8.3
- mklibname
- BuildRequires: autoconf >= 2.5, automake >= 1.7
- drop redundant Provides

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 0.7.2-4sls
- minor spec cleanups

* Tue Dec 09 2003 Vincent Danen <vdanen@opensls.org> 0.7.2-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
