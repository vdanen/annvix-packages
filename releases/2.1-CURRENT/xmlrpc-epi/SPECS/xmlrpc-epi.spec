#
# spec file for package xmlrpc-epi
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		xmlrpc-epi
%define version		0.51
%define release		%_revrel

%define major		0
%define libname		%mklibname xmlrpc %{major}
%define devname		%mklibname xmlrpc -d

Summary:	Library providing XMLPC support in C
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group: 		System/Libraries
URL:		http://xmlrpc-epi.sourceforge.net/
Source0:	xmlrpc-epi-%{version}.tar.bz2
Patch0:		xmlrpc-epi-0.51-64bit-fixes.patch
Patch1:		xmlrpc-epi-0.51-avx-gcc4.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an 
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.


%package -n %{libname}
Summary:	Library providing XMLRPC support in C
Group:		System/Libraries
Provides:	libxmlrpc = %{version}-%{release}
Obsoletes:	libxmlrpc0 < %{version}-%{release}

%description -n %{libname}
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an 
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.
 

%package -n %{devname}
Summary:	Libraries, includes, etc. to develop XML and HTML applications
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{libname}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	libxmlrpc0-devel < %{version}-%{release}

%description -n %{devname}
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .64bit-fixes
%patch1 -p1 -b .gcc4

# Make it lib64 aware
find . -name Makefile.in | xargs perl -pi -e "s,-L\@prefix\@/lib,,g"
perl -pi -e "s,-L/usr/local/lib\b,," configure


%build
%configure2_5x

#cp %{_datadir}/automake-1.6/depcomp .

#don't use parallel compilation, it is broken 
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

# remove unpackaged files
rm -f %{buildroot}%{_bindir}/{client,hello_{client,server},memtest,sample,server{,_compliance_test}}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-, root, root)
%{_libdir}/lib*.so.*

%files -n %{devname}
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*.a

%files doc
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README INSTALL


%changelog
* Fri Sep 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.51
- fix obsoletes so x86_64 upgrades properly

* Fri Sep 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.51
- fix this (seriously screwed up) package
- implement devel naming policy
- implement library provides policy

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.51
- add -doc subpackage
- rebuild with gcc4
- P1: make it compile with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.51
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.51
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51-11avx
- rebuild (I don't see libxml2 in the buildreq, but better to be safe than sorry)

* Tue Aug 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51-10avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51-9avx
- bootstrap build

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.51-8avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 0.51-7sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 0.51-6sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
