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
%define version 	1.2.9
%define release 	%_revrel

%define major		0
%define libname		%mklibname audit %{major}

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
Patch0:		audit-1.2.5-avx-makefile.patch
Patch1:		audit-1.2.9-avx-config.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	libtool
BuildRequires:	swig
BuildRequires:	automake1.9
BuildRequires:	autoconf2.5
BuildRequires:	glibc-devel

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
Provides:	libaudit

%description -n %{libname}
This package contains the dynamic libraries needed for applications to
use the audit framework.


%package -n %{libname}-devel
Summary:	Libraries and header files for libaudit
Group:		Development/Libraries
Requires:	%{libname} = %{version}-%{release}
Requires:	glibc-devel
Provides:	audit-devel
Provides:	libaudit-devel

%description -n %{libname}-devel
This package contains the static libraries and header files needed
for developing applications that need to use the audit framework
libraries.


%package -n %{libname}-python
Summary:	Python bindings for libaudit
Group:		Development/Libraries
Requires:	%{libname} = %{version}-%{release}
Requires:	glibc-devel

%description -n %{libname}-python
This package contains the bindings so that libaudit can be used by
python.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .avx
%patch1 -p1 -b .config


%build
%serverbuild
autoreconf -fv --install
CFLAGS="%{optflags}" \
    %configure \
        --sbindir=/sbin \
        --libdir=/%{_lib} \
        --with-apparmor
make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/{sbin,%{_mandir}/man8,%{_lib}}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}{%{_includedir},%{_libdir}}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_srvdir}/auditd/log
install -m 0740 %{_sourcedir}/auditd.run %{buildroot}%{_srvdir}/auditd/run
install -m 0740 %{_sourcedir}/auditd-log.run %{buildroot}%{_srvdir}/auditd/log/run
install -m 0740 %{_sourcedir}/auditd.finish %{buildroot}%{_srvdir}/auditd/finish

# the Makefile doesn't handle much of this gracefully
install -m 0644 lib/libaudit.h %{buildroot}%{_includedir}/
mv %{buildroot}/%{_lib}/libaudit.a %{buildroot}%{_libdir}/

pushd %{buildroot}%{_libdir}
    LIBNAME="`basename \`ls %{buildroot}/%{_lib}/libaudit.so.*.*.*\``"
    ln -s ../../%{_lib}/${LIBNAME} libaudit.so
popd

# this gets installed in the wrong place
%ifarch x86_64
mv %{buildroot}/usr/lib/python%{pyver}/site-packages/AuditMsg.py* %{buildroot}%{_libdir}/python%{pyver}/site-packages/
%endif

# remove unwanted files
rm -f %{buildroot}/%{_lib}/libaudit.{so,la}
rm -f %{buildroot}%{_libdir}/python2.4/site-packages/_audit.{a,la}
rm -rf %{buildroot}%{_sysconfdir}/rc.d
rm -f %{buildroot}%{_sysconfdir}/sysconfig/auditd

# rpm isn't stripping /sbin/auditd
strip %{buildroot}/sbin/auditd


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
%attr(0750,root,root) /sbin/auditctl
%attr(0750,root,root) /sbin/auditd
%attr(0750,root,root) /sbin/ausearch
%attr(0750,root,root) /sbin/aureport
%attr(0750,root,root) /sbin/autrace
%attr(0750,root,root) /sbin/audispd
%attr(0770,root,root) %dir %{_sysconfdir}/audit
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/audit/auditd.conf
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/audit/audit.rules
%{_libdir}/python%{pyver}/site-packages/AuditMsg.py*
%dir %attr(0750,root,admin) %{_srvdir}/auditd
%dir %attr(0750,root,admin) %{_srvdir}/auditd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/auditd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/auditd/log/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/auditd/finish
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/libaudit.so.*
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/libaudit.conf

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/libaudit.h
%{_libdir}/libaudit.a
%{_libdir}/libaudit.so
%{_mandir}/man3/*

%files -n %{libname}-python
%defattr(-,root,root)
%{_libdir}/python%{pyver}/site-packages/_audit.so
%{_libdir}/python%{pyver}/site-packages/audit.py*

%files doc
%defattr(-,root,root)
%doc README COPYING ChangeLog sample.rules contrib/capp.rules contrib/lspp.rules contrib/skeleton.c


%changelog
* Fri Nov 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.9
- 1.2.9
- P1: fix the auditd.conf file

* Tue Aug 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.5
- first Annvix package
- P0: fix the makefile's install of the libaudit.conf file

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
