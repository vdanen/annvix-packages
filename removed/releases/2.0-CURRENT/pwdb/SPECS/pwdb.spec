#
# spec file for package pwdb
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		pwdb
%define version		0.62
%define release		%_revrel

%define majver		0
%define libname_orig	%mklibname pwdb
%define libname		%{libname_orig}%{majver}

Summary:	The password database library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
Source:		pwdb-%{version}.tar.bz2
Patch0:		pwdb-0.62-includes.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gcc

%description
The pwdb package contains libpwdb, the password database library.
Libpwdb is a library which implements a generic user information
database.  Libpwdb was specifically designed to work with Linux's PAM
(Pluggable Authentication Modules).  Libpwdb allows configurable
access to and management of security tools like /etc/passwd,
/etc/shadow and network authentication systems including NIS and
Radius.


%package conf
Summary:	The password database library config
Group:		System/Libraries

%description conf
Configuration package for the libpwdb, the password database library.


%package -n %{libname}
Summary:	The password database library
Group:		System/Libraries
Requires:	%{name}-conf
Provides:	pwdb = %{version}-%{release}
Obsoletes:	pwdb

%description -n %{libname}
The pwdb package contains libpwdb, the password database library.
Libpwdb is a library which implements a generic user information
database.  Libpwdb was specifically designed to work with Linux's PAM
(Pluggable Authentication Modules).  Libpwdb allows configurable
access to and management of security tools like /etc/passwd,
/etc/shadow and network authentication systems including NIS and
Radius.


%package -n %{libname}-devel
Summary:	The pwdb include files and link library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	pwdb-devel = %{version}-%{release}
Conflicts:	pwdb-devel <= 0.61

%description -n %{libname}-devel
The development header / link library for pwdb.


%package -n %{libname}-static-devel
Summary:	The pwdb static library
Group:		Development/C
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	pwdb-static-devel = %{version}-%{release}

%description -n %{libname}-static-devel
The static development library for pwdb.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .includes

rm default.defs
ln -s defs/redhat.defs default.defs
# checking out of the CVS sometimes preserves the setgid bit on
# directories...
chmod -R g-s .


%build
RPM_OPT_FLAGS="%{optflags}" %make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{/%{_lib},%{_sysconfdir},%{_includedir}/pwdb}

make INCLUDED=%{buildroot}%{_includedir}/pwdb \
    LIBDIR=%{buildroot}/%{_lib} \
    LDCONFIG=":" \
    install

install -m 0644 conf/pwdb.conf %{buildroot}%{_sysconfdir}/pwdb.conf

ln -sf lib%{name}.so.%{version} %{buildroot}/%{_lib}/lib%{name}.so.%{majver}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files conf
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pwdb.conf

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/libpwdb.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
/%{_lib}/libpwdb.so
%{_includedir}/pwdb

%files -n %{libname}-static-devel
%defattr(-,root,root)
/%{_lib}/libpwdb.a

%files doc
%defattr(-,root,root)
%doc Copyright doc/pwdb.txt doc/html


%changelog
* Thu Jun 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.62
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.62
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.62
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.62-4avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.62-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.62-2avx
- bootstrap build
- re-enable stack protection

* Fri Sep 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.62-1avx
- 0.62

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.61.2-6avx
- Annvix build
- remove %%build_propolice macro; pass -fno-stack-protector by default

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 0.61.2-5sls
- minor spec cleanups
- change %%build_opensls to %%build_propolice

* Mon Dec 22 2003 Vincent Danen <vdanen@opensls.org> 0.61.2-4sls
- OpenSLS build
- tidy spec
- build without stack protection due to some symbol problems

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
