#
# spec file for package iputils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		iputils
%define version		20070202
%define release		%_revrel

%define bondingver	1.1.0

Summary:	Network monitoring tools including ping
Name:		%{name}
Version: 	%{version}
Release:	%{release}
License:	BSD
Group:		System/Base
URL:		http://linux-net.osdl.org/index.php/Iputils
Source0:	http://www.skbuff.net/iputils/iputils-s%{version}.tar.bz2
Source1:	bonding-%{bondingver}.tar.bz2
Source2:	iputils-s20070202-manpages.tar.bz2
Source3:	bin.ping.profile
Patch0:		iputils-s20070202-s_addr.patch
Patch2:		iputils-s20070202-ping_sparcfix.patch
Patch3:		iputils-s20070202-rdisc-server.patch
Patch4:		iputils-20020124-countermeasures.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The iputils package contains ping, a basic networking tool.  The ping
command sends a series of ICMP protocol ECHO_REQUEST packets to a
specified network host and can tell you if that machine is alive and
receiving network traffic.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-s%{version} -a 1 -a 2
%patch0 -p1 -b .s_addr
%patch2 -p1 -b .ping_sparcfix
%patch3 -p1 -b .rdisc-server
%patch4 -p1 -b .counter

%build
%serverbuild
perl -pi -e 's!\$\(MAKE\) -C doc html!!g' Makefile
%make CCOPT="%{optflags}"
%make ifenslave CFLAGS="%{optflags}" -C bonding-%{bondingver}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_sbindir},%{_bindir},%{_mandir}/man8,/bin,/sbin}

install -c arping %{buildroot}/sbin/
ln -s ../../sbin/arping %{buildroot}%{_sbindir}/arping

install -c clockdiff %{buildroot}%{_sbindir}/
install -c ping %{buildroot}/bin/
install -c bonding-%{bondingver}/ifenslave %{buildroot}/sbin/
install -c ping6 %{buildroot}%{_bindir}/
install -c rdisc %{buildroot}%{_sbindir}/
install -c tracepath %{buildroot}%{_sbindir}/
install -c tracepath6 %{buildroot}%{_sbindir}/
install -c traceroute6 %{buildroot}%{_sbindir}/

install -c man/*.8 %{buildroot}%{_mandir}/man8/

mkdir -p %{buildroot}%{_profiledir} 
install -m 0640 %{_sourcedir}/bin.ping.profile %{buildroot}%{_profiledir}/bin.ping


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%posttrans
%_aa_reload


%files
%defattr(-,root,root)
%{_sbindir}/clockdiff
%attr(0700,root,root) /bin/ping
/sbin/arping
%{_sbindir}/arping
/sbin/ifenslave
%attr(0700,root,root) %{_bindir}/ping6
%{_sbindir}/tracepath6
%{_sbindir}/tracepath
%attr(0700,root,root) %{_sbindir}/traceroute6
%{_sbindir}/rdisc
%{_mandir}/man8/*
%config(noreplace) %attr(0640,root,root) %{_profiledir}/bin.ping

%files doc
%defattr(-,root,root)
%doc RELNOTES bonding-%{bondingver}/bonding.txt


%changelog
* Sat Dec 29 2007 Vincent Danen <vdanen-at-build.annvix.org> 20070202
- rebuild with new %%_aa_reload macro definition

* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 20070202
- 20070202
- bonding 1.1.0
- S2: bundle the manpages since we don't have docbook and friends
- S3: include apparmor profile for ping
- use %%serverbuild
- dropped all unneeded patches and sync with Mandriva 

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 20020927
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 20020927
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 20020927
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 20020927-11avx
- strip suid bits from ping, ping6, and traceroute6

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 20020927-10avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 20020927-9avx
- bootstrap build

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 20020927-8avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 20020927-7sls
- remove %%build_opensls macro
- minor spec cleanups

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 20020927-6sls
- remove ipv6calc as it is it's own package now
- rearrange patches

* Mon Dec 22 2003 Vincent Danen <vdanen@opensls.org> 20020927-5sls
- OpenSLS build
- tidy spec
- use %%build_opensls to prevent building doc files

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
