#
# spec file for package audit
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name 		audit
%define version 	1.6.1
%define release 	%_revrel

%define major		0
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary:	User-space tools for Linux 2.6 kernel auditing
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License:	GPL
Group:		Monitoring
URL: 		http://people.redhat.com/sgrubb/audit/
Source0:	http://people.redhat.com/sgrubb/audit/%{name}-%{version}.tar.gz
Source1:	auditd.run
Source2:	auditd.finish
Source3:	auditd-log.run
Patch1:		audit-1.6.1-avx-config.patch
Patch2:		audit-1.6.1-mdv-sendmail.patch
Patch3:		audit-1.6.1-mdv-offt.patch
Patch4:		audit-1.6.1-avx-no-system-config-audit.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	libtool
BuildRequires:	swig
BuildRequires:	automake1.9
BuildRequires:	autoconf2.5
BuildRequires:	glibc-devel
BuildRequires:	gettext-devel
BuildRequires:	python-devel

Requires:	%{libname} = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description
The audit package contains the user space utilities for storing and
searching the audit records generate by the audit subsystem in the
Linux 2.6 kernel.


%package -n %{libname}
Summary:        Dynamic library for libaudit
Group:          System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the dynamic libraries needed for applications to
use the audit framework.


%package -n %{devname}
Summary:	Libraries and header files for libaudit
Group:		Development/Libraries
Requires:	%{libname} = %{version}
Requires:	glibc-devel
Provides:	audit-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 0 -d

%description -n %{devname}
This package contains the static libraries and header files needed
for developing applications that need to use the audit framework
libraries.


%package -n python-audit
Summary:	Python bindings for audit
Group:		Development/Python
Requires:	%{libname} = %{version}
Obsoletes:	%{libname}-python

%description -n python-audit
This package contains the bindings so that libaudit can be used by
python.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1 -b .config
%patch2 -p1 -b .sendmail
%patch3 -p1 -b .offt
%patch4 -p1 -b .no-system-config-audit


%build
%serverbuild

aclocal && autoconf && autoheader && automake

%configure2_5x \
    --sbindir=/sbin \
    --libdir=/%{_lib} \
    --libexecdir=%{_sbindir} \
    --with-apparmor
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

mkdir -p %{buildroot}%{_srvdir}/auditd/log
install -m 0740 %{_sourcedir}/auditd.run %{buildroot}%{_srvdir}/auditd/run
install -m 0740 %{_sourcedir}/auditd-log.run %{buildroot}%{_srvdir}/auditd/log/run
install -m 0740 %{_sourcedir}/auditd.finish %{buildroot}%{_srvdir}/auditd/finish

# remove unwanted files
rm -f %{buildroot}%{py_siteplatdir}/*.{a,la}
rm -rf %{buildroot}%{_sysconfdir}/rc.d
rm -f %{buildroot}%{_sysconfdir}/sysconfig/auditd



%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%post
%_post_srv auditd


%preun
%_preun_srv auditd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/*
%dir %{_sysconfdir}/audit
%dir %{_sysconfdir}/audisp
%dir %{_sysconfdir}/audisp/plugins.d
%config(noreplace) %{_sysconfdir}/audisp/audispd.conf
%config(noreplace) %{_sysconfdir}/audisp/plugins.d/af_unix.conf
%config(noreplace) %{_sysconfdir}/audisp/plugins.d/syslog.conf
%config(noreplace) %{_sysconfdir}/audit/auditd.conf
%config(noreplace) %{_sysconfdir}/audit/audit.rules
%dir %attr(0750,root,admin) %{_srvdir}/auditd
%dir %attr(0750,root,admin) %{_srvdir}/auditd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/auditd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/auditd/log/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/auditd/finish
%{_mandir}/man5/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/lib*.so.*
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/libaudit.conf

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/*.h
/%{_lib}/*.a
/%{_lib}/*.la
/%{_lib}/*.so
%{_mandir}/man3/*

%files -n python-audit
%defattr(-,root,root)
%{py_platsitedir}/*
%{py_purelibdir}/*

%files doc
%defattr(-,root,root)
%doc README COPYING ChangeLog sample.rules contrib/capp.rules contrib/lspp.rules contrib/skeleton.c


%changelog
* Tue Dec 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.6.1
- 1.6.1
- updated buildrequires
- rename %%libname-python to python-audit
- use %%configure2_5x and %%makeinstall_std to ease the build
- dropped P0
- rediffed P1
- P2: fix the sendmail check
- P3: fix "config file too large" on x86_64
- P4: don't build or try to build system-config-audit
- don't delete the development files we want

* Thu Sep 13 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.9
- implement devel naming policy
- implement library provides policy
- fix the build with python 2.5

* Sat Dec 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.9
- rebuild against new swig

* Fri Nov 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.9
- 1.2.9
- P1: fix the auditd.conf file

* Tue Aug 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.5
- first Annvix package
- P0: fix the makefile's install of the libaudit.conf file

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
