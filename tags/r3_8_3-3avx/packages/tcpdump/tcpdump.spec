%define name	tcpdump
%define version	3.8.3
%define release	3avx
%define epoch	2

Summary:	A network traffic monitoring tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	BSD
Group:	 	Monitoring
URL:		http://www.tcpdump.org
Source:		http://www.tcpdump.org/release/%{name}-%{version}.tar.bz2
Patch0:		tcpdump-3.8.2-bgp-dos.patch.bz2
Patch1:		tcpdump-3.8.2-isis-dos.patch.bz2
Patch2:		tcpdump-3.8.2-ldp-dos.patch.bz2
Patch3:		tcpdump-3.8.2-rsvp-dos.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	libpcap-devel

%description
tcpdump is a command-line tool for monitoring network traffic.  tcpdump
can capture and display the packet headers on a particular network
interface or on all interfaces.  tcpdump can display all of the packet
headers, or just the ones that match particular criteria.

Install tcpdump if you need a program to monitor network traffic.

%prep
%setup -q
%patch0 -p1 -b .bgp-dos
%patch1 -p1 -b .isis-dos
%patch2 -p1 -b .ldp-dos
%patch3 -p1 -b .rsvp-dos

%build
libtoolize --copy --force
%define	optflags $RPM_OPT_FLAGS -DIP_MAX_MEMBERSHIPS=20
%configure --enable-ipv6
%undefine optflags

%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
#mkdir -p $RPM_BUILD_ROOT{%{_mandir}/man1,%{_sbindir}}

make install DESTDIR=$RPM_BUILD_ROOT

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README CHANGES CREDITS FILES LICENSE TODO VERSION PLATFORMS
%{_sbindir}/tcpdump
%{_mandir}/man1/tcpdump.1*

%changelog
* Thu May 12 2005 Vincent Danen <vdanen@annvix.org> 3.8.3-3avx
- P0-P3: security fixes for CAN-2005-1278, CAN-2005-1279, CAN-2005-1280

* Mon Jun 21 2004 Vincent Danen <vdanen@annvix.org> 3.8.3-2avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 3.8.3-1sls
- OpenSLS build
- tidy spec

* Thu Apr 15 2004 Michael Scherer <mscherer@mandrakesoft.com> 3.8.3-1mdk
- New release 3.8.3

* Tue Jan 27 2004 Warly <warly@mandrakesoft.com> 2:3.8.1-1mdk
- new version

* Mon Apr 28 2003 Warly <warly@mandrakesoft.com> 3.7.2-2mdk
- fix rebuild (move in.h inclusion)

* Sat Mar 01 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.7.2-1mdk
- 3.7.2 (security fixes)

* Thu Mar 28 2002 Warly <warly@mandrakesoft.com> 3.7.1-1mdk
- new version

* Tue Dec  4 2001 Warly <warly@mandrakesoft.com> 3.6.2-2mdk
- rpmlint fixes

* Tue May  8 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 3.6.2-1mdk
- version 3.6.2
- make use of this jewel of technology, the `BuildRequires', which is
  mostly unknown to packagers; on a side note, with dynamic linkage
  against libpcap, we save around 25% of binary size

* Tue Jan 09 2001 Geoff <snailtalk@mandrakesoft.com> 3.6.1-1mdk
- new and shiny source.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.4-10mdk
- automatically added BuildRequires


* Fri Jul 21 2000 Francis Galiegue <fg@mandrakesoft.com> 3.4-9mdk

- s,tmpdir,tmppath, :/


* Wed Jul 19 2000 Francis Galiegue <fg@mandrakesoft.com> 3.4-8mdk

- tcpdump is now in its own src rpm
- %files list fixes
- 3.5


