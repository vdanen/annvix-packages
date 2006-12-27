#
# spec file for package nc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision        $Rev$
%define name            nc
%define version         1.10
%define release         %_revrel

Summary: 	Reads and writes data across network connections using TCP or UDP
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Networking/Other
URL:		http://www.vulnwatch.org/netcat/
Source0:	http://www.vulnwatch.org/netcat/nc110.tar.bz2
Source1: 	nc.1
Patch0: 	nc-1.10-arm.patch
Patch1: 	nc-1.10-resolv.patch
Patch2:		nc-1.10-posix_setjmp.patch
Patch3:		nc-1.10-nopunt.patch
Patch4:		nc-1.10-nosleep.patch
Patch5:		nc-1.10-single_verbose.patch
Patch6:		nc-1.10-use_getservbyport.patch
Patch7:		nc-1.10-read_overflow.patch
Patch8:		nc-1.10-inet_aton.patch
Patch9:		nc-1.10-udp_broadcast.patch
Patch10:	nc-1.10-quit.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}

Provides:	netcat = %{version}

%description
The nc package contains Netcat (the program is now netcat), a simple
utility for reading and writing data across network connections, using
the TCP or UDP protocols. Netcat is intended to be a reliable back-end
tool which can be used directly or easily driven by other programs and
scripts.  Netcat is also a feature-rich network debugging and exploration
tool, since it can create many different connections and has many
built-in capabilities.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -c -n nc -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1


%build
# Make linux is supported, but it makes a static binary. 
# don't build with -DGAPING_SECURITY_HOLE
%make CFLAGS="%{optflags}" \
      DFLAGS='-DLINUX' generic


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man1}

install -m 0755 nc %{buildroot}%{_bindir}
(cd %{buildroot}%{_bindir}; ln -s nc netcat)

install -m 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/nc
%{_bindir}/netcat
%{_mandir}/man1/nc.1*

%files doc
%defattr(-,root,root)
%doc README Changelog
%doc scripts


%changelog
* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.10
- add -doc subpackage
- rebuild with gcc4

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.10
- first Annvix build
- major spec cleanups
- use the correct URL

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
