%define name	mdadm
%define version	1.4.0
%define release	5sls

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
Patch1:		http://cgi.cse.unsw.edu.au/~neilb/source/mdadm/patch/applied/001mdadm-1.3.0-diet.diff.bz2
Patch2:		http://cgi.cse.unsw.edu.au/~neilb/source/mdadm/patch/applied/002NoMdstatWarning.bz2
Patch3:		http://cgi.cse.unsw.edu.au/~neilb/source/mdadm/patch/applied/003BlkGetSize.bz2
Patch4:		http://cgi.cse.unsw.edu.au/~neilb/source/mdadm/patch/applied/004DetailRebuild.bz2
Patch5:		http://cgi.cse.unsw.edu.au/~neilb/source/mdadm/patch/applied/005SignedUnsigned.bz2
Patch6:		http://cgi.cse.unsw.edu.au/~neilb/source/mdadm/patch/applied/006TestMsg.bz2

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

%patch1 -p0 -b .001
%patch2 -p0 -b .002
%patch3 -p0 -b .003
%patch4 -p0 -b .004
%patch5 -p0 -b .005
%patch6 -p0 -b .006

%build
%if %{use_dietlibc}
make mdassemble CXFLAGS="%{optflags}" SYSCONFDIR="%{_sysconfdir}"
%endif
make CXFLAGS="%{optflags}" SYSCONFDIR="%{_sysconfdir}"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

make DESTDIR=%{buildroot} MANDIR=%{_mandir} BINDIR=%{_sbindir} install
install -D -m 644 mdadm.conf-example %{buildroot}%{_sysconfdir}/mdadm.conf
mkdir -p %{buildroot}%{_initrddir}
bzip2 -dc %{SOURCE1} > %{buildroot}%{_initrddir}/mdadm

%if %{use_dietlibc}
install mdassemble %{buildroot}%{_sbindir}/mdassemble
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%preun
%_preun_service mdadm

%post
%_post_service mdadm

%files
%defattr(-,root,root)
%doc TODO ChangeLog mdadm.conf-example ANNOUNCE-%{version}
%{_sbindir}/mdadm
%if %{use_dietlibc}
%{_sbindir}/mdassemble
%endif
%config(noreplace,missingok)/%{_sysconfdir}/mdadm.conf
%attr(755, root, root) %config(noreplace) %{_initrddir}/mdadm
%{_mandir}/man*/md*

%changelog
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
