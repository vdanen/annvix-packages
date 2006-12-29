#
# spec file for package libuser
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libuser
%define version		0.54.5
%define release		%_revrel

%define major		1
%define libname		%mklibname user %{major}

Summary:	A user and group account administration library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Configuration
URL:		http://qa.mandriva.com
Source:		libuser-%{version}.tar.bz2
Patch1:		libuser-0.54.5-nosgml.patch	

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext
BuildRequires:	glib2-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	popt-devel
BuildRequires:	python-devel

%description
The libuser library implements a standardized interface for manipulating
and administering user and group accounts.  The library uses pluggable
back-ends to interface to its data sources.

Sample applications modeled after those included with the shadow password
suite are included.


%package -n %{name}-python
Summary:	Library bindings for python
Group:		Development/Python

%description -n %{name}-python
this package contains the python library for python applications that 
use libuser


%package -n %{name}-ldap
Summary:	Libuser ldap library 
Group:		System/Libraries

%description -n %{name}-ldap
this package contains the libuser ldap library


%package -n %{libname}
Summary:	The actual libraries for libuser
Group:		System/Libraries

%description -n %{libname}
This is the actual library for the libuser library.


%package -n %{libname}-devel
Summary:	Files needed for developing applications which use libuser
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
The libuser-devel package contains header files, static libraries, and other
files useful for developing applications with libuser.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.



%prep
%setup -q
%patch1 -p0 -b .nosgml


%build
export CFLAGS="%{optflags} -DG_DISABLE_ASSERT -I/usr/include/sasl -DLDAP_DEPRECATED"
%configure2_5x \
    --with-ldap \
    --with-python-version=%{pyver} \
    --with-python-path=%{_includedir}/python%{pyver} \
    --enable-gtk-doc=no
%make 

# since P1 doesn't "make doc" anymore, make the manpage manually
pushd docs
    make libuser.conf.5
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

LD_LIBRARY_PATH=%{buildroot}%{_libdir}:${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH

# Verify that all python modules load, just in case.
pushd %{buildroot}%{_libdir}/python%{pyver}/site-packages/
    python -c "import libuser"
popd

# since P1 doesn't "make doc" anymore, install the manpage manually
mkdir -p %{buildroot}%{_mandir}/man5
install -m 0644 docs/libuser.conf.5 %{buildroot}%{_mandir}/man5/

%kill_lang %{name}
%find_lang %{name}

# Remove unpackaged files
rm -rf %{buildroot}/usr/share/man/man3/userquota.3
rm -rf %{buildroot}%{_libdir}/python%{pyver}/site-packages/*a


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/libuser.conf
%attr(0755,root,root) %{_bindir}/*
%attr(0755,root,root) %{_sbindir}/*
%attr(0755,root,root) %{_libdir}/%{name}/libuser_files.so
%attr(0755,root,root) %{_libdir}/%{name}/libuser_shadow.so
%{_mandir}/man1/*
%{_mandir}/man5/*

%files -n %{libname}
%attr(0755,root,root) %{_libdir}/*.so.*

%files -n %{name}-python
%attr(0755,root,root) %{_libdir}/python%{pyver}/site-packages/*.so

%files -n %{name}-ldap
%attr(0755,root,root) %{_libdir}/%{name}/libuser_ldap.so

%files -n %{libname}-devel
%defattr(-,root,root)
%attr(0755,root,root) %dir %{_includedir}/libuser
%attr(0644,root,root) %{_includedir}/libuser/*
%attr(0644,root,root) %{_libdir}/*.la
%attr(0755,root,root) %{_libdir}/*.so
%attr(0755,root,root) %{_libdir}/libuser
#%attr(0644,root,root) %{_mandir}/man3/*
%attr(0644,root,root) %{_libdir}/pkgconfig/*

%files doc
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README TODO docs/*.txt python/modules.txt


%changelog
* Fri Dec 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.54.5
- rebuild against new pam

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.54.5
- rebuild against new openldap

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.54.5
- remove locales

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.54.5
- rebuild against new glib2.0

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.54.5
- rebuild against new openldap 
- spec cleanups

* Sun Jun 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.54.5
- rebuild against new pam

* Tue May 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.54.5
- 0.54.5
- rediff P1
- make libuser.conf.5 manually since P1 patches out make doc
- remove invalid locale directories/files
- add -doc subpackage
- rebuild with gcc4
- rebuild against new python

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.53.2
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.53.2
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.53.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.53.2-6avx
- rebuild against new glib2.0

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.53.2-5avx
- pass -DLDAP_DEPRECATED to CFLAGS (oden)
- BuildRequires: openldap-devel, not libldap-devel
- libuser_ldap module is in it's own package now

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.53.2-4avx
- bootstrap build (new gcc, new glibc)

* Fri Jul 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.53.2-3avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.53.2-2avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.53.2-1avx
- 0.53.2
- remove redundant BuildRequires (stefan)
- move non-versioned-file from library package to main package (stefan)
- remove useless files from -devel package (gotz)
- drop unneeded patches
- use pyver macro
- spec cosmetics
- mklibname (gbeauchesne)

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.51.7-13avx
- rebuild against latest openssl

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.51.7-12avx
- rebuild against latest openssl

* Wed Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.51.7-11avx
- Annvix build

* Mon May 17 2004 Vincent Danen <vdanen@opensls.org> 0.51.7-10sls
- security fixes from Steve Grubb

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 0.51.7-9sls
- remove %%build_opensls macro
- minor spec cleanups

* Mon Dec 22 2003 Vincent Danen <vdanen@opensls.org> 0.51.7-8sls
- OpenSLS build
- tidy spec
- use %%build_opensls to apply P3; don't build sgml junk

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
