%define name	mdadm
%define version	1.6.0
%define release	3avx

%define use_dietlibc 0
%ifarch %{ix86}
%define use_dietlibc 1
%endif

# we want to install in /sbin, not /usr/sbin...
%define _exec_prefix %{nil}

Summary:	A tool for managing Soft RAID under Linux
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.cse.unsw.edu.au/~neilb/source/mdadm/
Source:		http://cgi.cse.unsw.edu.au/~neilb/source/mdadm/%{name}-%{version}.tar.bz2
Source1:	mdmonitor.init.bz2
Source2:	mdadm.run
Source3:	mdadm-log.run

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	man groff groff-for-man
%if %{use_dietlibc}
BuildRequires:	dietlibc-devel
%endif

Prereq:		rpm-helper

%description 
mdadm is a program that can be used to create, manage, and monitor
Linux MD (Software RAID) devices.

As such is provides similar functionality to the raidtools packages.
The particular differences to raidtools is that mdadm is a single
program, and it can perform (almost) all functions without a
configuration file (that a config file can be used to help with
some common tasks).

%prep
%setup -q
chmod 644 ChangeLog

%build
%if %{use_dietlibc}
make mdassemble CXFLAGS="%{optflags}" SYSCONFDIR="%{_sysconfdir}"
%endif
make CXFLAGS="%{optflags}" SYSCONFDIR="%{_sysconfdir}"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make DESTDIR=%{buildroot} MANDIR=%{_mandir} BINDIR=%{_sbindir} install
install -D -m 644 mdadm.conf-example %{buildroot}%{_sysconfdir}/mdadm.conf

%if %{use_dietlibc}
install mdassemble %{buildroot}%{_sbindir}/mdassemble
%endif

mkdir -p %{buildroot}%{_srvdir}/mdadm/log
mkdir -p %{buildroot}%{_srvlogdir}/mdadm
install -m 0755 %{SOURCE2} %{buildroot}%{_srvdir}/mdadm/run
install -m 0755 %{SOURCE3} %{buildroot}%{_srvdir}/mdadm/log/run

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%preun
%_preun_srv mdadm

%post
%_post_srv mdadm

%files
%defattr(-,root,root)
%doc TODO ChangeLog mdadm.conf-example ANNOUNCE-%{version}
%{_sbindir}/mdadm
%if %{use_dietlibc}
%{_sbindir}/mdassemble
%endif
%config(noreplace,missingok)/%{_sysconfdir}/mdadm.conf
%{_mandir}/man*/md*
%dir %{_srvdir}/mdadm
%dir %{_srvdir}/mdadm/log
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/mdadm
%{_srvdir}/mdadm/run
%{_srvdir}/mdadm/log/run

%changelog
* Fri Sep 17 2004 Vincent Danen <vdanen@annvix.org> 1.6.0-3avx
- update run scripts

* Mon Jun 14 2004 Thomas Backlund <tmb@annvix.org> 1.6.0-2avx
- swith to new name Annvix / avx

* Mon Jun 14 2004 Thomas Backlund <tmb@iki.fi> 1.6.0-1sls
- 1.6.0

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.5.0-2sls
- minor spec cleanups

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 1.5.0-1sls
- 1.5.0
- drop all upstream-applied patches
- supervise scripts

* Wed Jan 21 2004 Vincent Danen <vdanen@opensls.org> 1.4.0-6sls
- sync with 5mdk (Luca Berra):
  - added raid6 patches from hpa

* Sun Jan 11 2004 Vincent Danen <vdanen@opensls.org> 1.4.0-5sls
- OpenSLS build
- tidy spec
- don't use dietlibc if building for amd64

* Sun Dec 21 2003 Luca Berra <bluca@vodka.it> 1.4.0-4mdk
- service name is mdadm

* Sat Dec 20 2003 Luca Berra <bluca@vodka.it> 1.4.0-3mdk
- updated with more patches from Neil, mdassemble is going to be integrated upstream
- added mdmonitor (from rh)

* Sun Nov 02 2003 Luca Berra <bluca@vodka.it> 1.4.0-2mdk
- added mdassemble built with dietlibc

* Fri Oct 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.4.0-1mdk
- 1.4.0
- drop patches included in the upstream source

* Mon Sep 08 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 1.3.0-2mdk
- updated by Luca Berra <bluca@vodka.it>
 - added patches from upstream maintainer
- fix perms on doc file

* Tue Jul 29 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.0-1mdk
- 1.3.0

* Fri Apr 25 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.2.0-2mdk
- fix buildrequires, thanks to Stefan van der Eijks robot

* Sun Mar 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.2.0-1mdk
- 1.2.0

* Mon Mar 03 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.1.0-1mdk
- 1.1.0
- misc spec file fixes

* Thu Jan 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.0.1-3mdk
- build release

* Sun Aug  4 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.0.1-2mdk
- rebuilt with gcc-3.2

* Mon Jun 10 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.0.1-1mdk
- 1.0.1
- capitalized summary to please rpmlint

* Mon May 20 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.0.0-2mdk
- rebuilt with gcc3.1

* Sat May 11 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.0.0-1mdk
- new version

* Sat May 11 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.8.2-1mdk
- initial cooker contrib
- used provided spec file
