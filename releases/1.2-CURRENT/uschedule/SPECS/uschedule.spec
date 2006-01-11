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

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	dietlibc-devel >= 0.20

Requires:	srv

%description
uschedule is not cron and uschedule is not at - it does offer
similar functionality, but is not intended to be a drop-in 
replacement. It works differently. It's designed to be different.


%prep
%setup -q -n admin


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
%doc %{name}-%{version}/src/ChangeLog
%doc %{name}-%{version}/src/INSTALL
%doc %{name}-%{version}/src/NEWS
%doc %{name}-%{version}/src/SECURITY-BUG
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


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
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
