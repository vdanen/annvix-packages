%define name	uschedule
%define version	0.7.0
%define release	1mdk

Summary:	Scheduling service
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Servers
URL:		http://www.ohse.de/uwe/uschedule.html
Source0:	%{name}-%{version}.tar.gz
Requires:	daemontools
BuildRequires:	dietlibc-devel >= 0.20
Buildroot:	%{_tmppath}/%{name}-%{version}
Packager:	Oden Eriksson <oden.eriksson@deserve-it.com>

%description
uschedule is not cron and uschedule is not at - it does offer
similar functionality, but is not intended to be a drop-in 
replacement. It works differently. It's designed to be different.

%prep

%setup -q -n admin

%build
pushd %{name}-%{version}/src
    make CFLAGS="-Os -pipe" \
    GCC="diet gcc -Os -static -s" \
    CC="diet gcc -Os -static -s" \
    LDFLAGS=""
popd

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_mandir}/man7
install -d %{buildroot}%{_mandir}/man8


pushd %{name}-%{version}/src
for i in uscheduled uschedulerm uschedulelist uschedulecmd \
    uschedulecp uscheduleedit uschedule uscheduleconf; do
    install -m0755 $i %{buildroot}%{_bindir}/
done

install -m0644 *.1 %{buildroot}%{_mandir}/man1/
install -m0644 *.7 %{buildroot}%{_mandir}/man7/
install -m0644 *.8 %{buildroot}%{_mandir}/man8/

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
* Wed Dec 31 2003 Oden Eriksson <oden.eriksson@deserve-it.com> 0.7.0-1mdk
- initial package
