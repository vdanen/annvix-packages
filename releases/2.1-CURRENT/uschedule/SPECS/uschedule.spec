#
# spec file for package uschedule
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		uschedule
%define version		0.7.1
%define release		%_revrel

Summary:	Scheduling service
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Servers
URL:		http://www.ohse.de/uwe/uschedule.html
Source0:	%{name}-%{version}.tar.gz
Patch0:		uschedule-0.7.1-avx-runit.patch
Patch1:		uschedule-0.7.1-avx-localtime.patch
Patch2:		uschedule-0.7.1-avx-fix_commandfile.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	dietlibc-devel >= 0.20

Requires:	srv

%description
uschedule is not cron and uschedule is not at - it does offer
similar functionality, but is not intended to be a drop-in 
replacement. It works differently. It's designed to be different.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n admin
%patch0 -p0 -b .runit
%patch1 -p1 -b .localtime
%patch2 -p1 -b .fix_commandfile

%build
%ifarch x86_64
COMP="diet x86_64-annvix-linux-gnu-gcc"
%else
COMP="diet gcc"
%endif

pushd %{name}-%{version}/src
    make CFLAGS="-Os -pipe" \
    GCC="$COMP -Os -static -s" \
    CC="$COMP -Os -static -s" \
    LDFLAGS=""
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man{1,7,8}}


pushd %{name}-%{version}/src
    for i in uscheduled uschedulerm uschedulelist uschedulecmd \
        uschedulecp uscheduleedit uschedule uscheduleconf; do
        install -m 0755 $i %{buildroot}%{_bindir}/
    done

    install -m 0644 *.1 %{buildroot}%{_mandir}/man1/
    install -m 0644 *.7 %{buildroot}%{_mandir}/man7/
    install -m 0644 *.8 %{buildroot}%{_mandir}/man8/
popd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr (-,root,root)
%{_bindir}/uscheduled
%{_bindir}/uschedulerm
%{_bindir}/uschedulelist
%{_bindir}/uschedulecmd
%{_bindir}/uschedulecp
%{_bindir}/uscheduleedit
%{_bindir}/uschedule
%{_bindir}/uscheduleconf
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%files doc
%defattr (-,root,root)
%doc %{name}-%{version}/src/ChangeLog
%doc %{name}-%{version}/src/INSTALL
%doc %{name}-%{version}/src/NEWS
%doc %{name}-%{version}/src/SECURITY-BUG


%changelog
* Fri Dec 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.7.1
- remove the memory restrictions set by chpst; right now they're causing
  problems and they're not really required anyways

* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.7.1
- rebuild

* Fri Dec 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.7.1
- P2: fix the uschedulecmd's creation of the environment script that
  actually runs the commands otherwise jobs created using -e (to
  preserve the environment) will never be executed

* Thu Dec 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.7.1
- P1: make uo_now() return the seconds since the epoch adjusted for
  the local time so on a MST7MDT since you don't end up with a timespec
  of +07:03:00 when you want just +03:00

* Tue Oct 31 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.7.1
- P0: make it use runit instead of daemontools

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.7.1
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.7.1
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.7.1
- Obfuscate email addresses and new tagging
- Uncompress patches
- dietlibc fixes

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.7.1-1avx
- 0.7.1

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.7.0-4avx
- rebuild
- requires: s/daemontools/srv/

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.7.0-3avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 0.7.0-2sls
- minor spec cleanups

* Wed Dec 31 2003 Oden Eriksson <oden.eriksson@deserve-it.com> 0.7.0-1mdk
- initial package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
