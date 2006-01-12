#
# spec file for package libxmlrpc0
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		%{libnamemajor}
%define version		0.51
%define release		%_revrel

%define realname	xmlrpc
%define libname		lib%{realname}
%define major		0
%define libnamemajor	%{libname}%{major}

Summary:	Library providing XMLPC support in C
Name:		%{libnamemajor}
Version:	%{version}
Release:	%{release}
License:	BSD
Group: 		System/Libraries
URL:		http://xmlrpc-epi.sourceforge.net/
Source0:	xmlrpc-epi-%{version}.tar.bz2
Patch0:		xmlrpc-epi-0.51-64bit-fixes.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Provides:	%{libname} = %{version}

%description
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an 
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.
 

%package devel
Summary:	Libraries, includes, etc. to develop XML and HTML applications
Group:		Development/C
Requires:	%{libnamemajor} = %{version}
Provides:	%{libname}-devel = %{version}

%description devel
xmlrpc-epi is an implementation of the xmlrpc protocol in C. It provides an
easy to use API for developers to serialize RPC requests to and from XML.
It does *not* include a transport layer, such as HTTP. The API is primarily
based upon proprietary code written for internal usage at Epinions.com, and
was later modified to incorporate concepts from the xmlrpc protocol.


%prep
%setup -q -n xmlrpc-epi-%{version}
%patch0 -p1 -b .64bit-fixes

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


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog README
%{_libdir}/lib*.so.*

%files devel
%defattr(-, root, root)
%doc INSTALL
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/lib*.a


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org>
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

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.51-5mdk
- rebuild

* Sun Dec  8 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.51-4mdk
- Usual and famous JC-lib64
- Patch0: assorted fixes, mostly for 64-bit architectures

* Mon Oct 28 2002 Pixel <pixel@mandrakesoft.com> 0.51-3mdk
- remove the sample binaries from libxmlrpc0-devel, also remove the conflict
with memtester (not needed anymore)
- remove BuildRequires on automake1.6 (not needed, we don't need to call
automake since we don't apply any patches), remove copying "depcomp"
- rename spec file name to %%{name}.spec

* Wed Aug 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.51-2mdk
- fix conflict with memtester.

* Tue Jun 25 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.51-1mdk
- new version 0.51.

* Wed May 22 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.50-2mdk
- BuildRequires on automake1.6

* Tue May 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.50-1mdk
- initial mandrake release.

