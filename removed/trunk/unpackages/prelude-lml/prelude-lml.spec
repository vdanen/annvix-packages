%define name	prelude-lml
%define version	0.8.1
%define release	3sls

%define prefix	/usr

Summary:	Prelude Hybrid Intrusion Detection System - Log Analyzer Sensor
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Other
URL:		http://www.prelude-ids.org/
Source:		http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	libprelude-devel
BuildRequires:	pcre-devel

Requires:	libprelude >= 0.8.4

%description
The Prelude Log Monitoring Lackey (LML) is the host-based sensor program part
of the Prelude Hybrid IDS suite. It can act as a centralized log collector for
local or remote systems, or as a simple log analyzer (such as swatch). It can
run as a network server listening on a syslog port or analyze log files. It
supports logfiles in the BSD syslog format and is able to analyze any logfile
by using the PCRE library. It can apply logfile-specific analysis through
plugins such as PAX. It can send an alert to the Prelude Manager when a
suspicious log entry is detected. 

%package devel
Summary:	Libraries, includes, etc. to develop Prelude Log Analyzer Sensor
Group:		Development/C
Requires:	%{name} = %{version}
BuildRequires:	libprelude-devel
Requires:	libprelude

%description devel
The Prelude Log Monitoring Lackey (LML) is the host-based sensor program part
of the Prelude Hybrid IDS suite. It can act as a centralized log collector for
local or remote systems, or as a simple log analyzer (such as swatch). It can
run as a network server listening on a syslog port or analyze log files. It
supports logfiles in the BSD syslog format and is able to analyze any logfile
by using the PCRE library. It can apply logfile-specific analysis through
plugins such as PAX. It can send an alert to the Prelude Manager when a
suspicious log entry is detected. 
The devel headers.

%prep
%setup -q -n %{name}-%{version}

%build
export WANT_AUTOCONF_2_5=1

%configure2_5x --localstatedir=/var
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README INSTALL
%{_bindir}/prelude-lml
%{_libdir}/prelude-lml/*
%config(noreplace) %{_sysconfdir}/prelude-lml/*

%files devel
%defattr(-,root,root)
%doc AUTHORS ChangeLog README INSTALL
%{_includedir}/prelude-lml/*.h

%changelog
* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 0.8.1-3sls
- BuildRequires: pcre-devel, not libpcre-devel (for amd64)
- use %%configure2_5x to get libs where we want them
- clean buildroot before install

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 0.8.1-2sls
- OpenSLS build
- tidy spec

* Tue Sep 09 2003 Florin Grad <florin@mandrakesoft.com> 0.8.1-1mdk
- first mandrake release

* Wed Sep 03 2002 Sylvain GIL <prelude-packaging@tootella.org> 0.8.1-1
-  Initial Packaging.

