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
%define version		20%{ver}
%define release		%_revrel
%define ver		020927

Summary:	Network monitoring tools including ping
Name:		%{name}
Version: 	%{version}
Release:	%{release}
License:	BSD
Group:		System/Base
URL:		ftp://ftp.inr.ac.ru/ip-routing/
Source0:	http://ftp.sunet.se/pub/os/Linux/ip-routing/iputils-ss%{ver}.tar.bz2
Source1:	bonding-0.2.tar.bz2
Patch0:		iputils-20001007-rh7.patch
Patch1:		iputils-20020927-datalen.patch
Patch2:		iputils-20020927-ping_sparcfix.patch
Patch3:		iputils-20020124-rdisc-server.patch 
Patch4:		iputils-20020124-countermeasures.patch 
Patch5:		iputils-20001110-bonding-sockios.patch
Patch6:		iputils-20020927-fix-traceroute.patch

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
%setup -q -n %{name} -a 1

rm -f bonding-0.2/ifenslave
mv -f bonding-0.2/README bonding-0.2/README.ifenslave

%patch0 -p1 -b .rh7
%patch1 -p1 -b .datalen
%patch2 -p1 -b .ping_sparcfix
%patch3 -p1 -b .rdisc
%patch4 -p1 -b .counter
%patch5 -p1 -b .sockios
%patch6 -p1 -b .fix


%build
perl -pi -e 's!\$\(MAKE\) -C doc html!!g' Makefile
%make CCOPT="%{optflags}"
%make ifenslave -C bonding-0.2

make ifenslave -C bonding-0.2


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# (TV): this is broken and uneeded
#make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}/{bin,sbin}
install -c clockdiff		%{buildroot}%{_sbindir}/
%ifos linux
install -c arping		%{buildroot}/sbin/
ln -s ../../sbin/arping %{buildroot}%{_sbindir}/arping
install -c ping			%{buildroot}/bin/
install -c bonding-0.2/ifenslave %{buildroot}/sbin/
%else
install -c arping      %{buildroot}%{_sbindir}/
install -c ping            %{buildroot}%{_sbindir}/
install -c bonding-0.2/ifenslave %{buildroot}%{_sbindir}/
%endif
#%ifnarch ppc
install -c ping6		%{buildroot}%{_bindir}
#%endif
install -c rdisc		%{buildroot}%{_sbindir}/
install -c tracepath		%{buildroot}%{_sbindir}/
install -c tracepath6		%{buildroot}%{_sbindir}/
install -c traceroute6		%{buildroot}%{_sbindir}/

mkdir -p %{buildroot}%{_mandir}/man8
#install -c in.rdisc.8c		%{buildroot}%{_mandir}/man8/rdisc.8
install -c doc/arping.8        %{buildroot}%{_mandir}/man8/
install -c doc/clockdiff.8 %{buildroot}%{_mandir}/man8/
install -c doc/rdisc.8     %{buildroot}%{_mandir}/man8/rdisc.8
install -c doc/ping.8      %{buildroot}%{_mandir}/man8/
install -c doc/tracepath.8 %{buildroot}%{_mandir}/man8/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_sbindir}/clockdiff
%attr(0700,root,root)	/bin/ping
/sbin/arping
%{_sbindir}/arping
/sbin/ifenslave
#%ifnarch ppc
%attr(0700,root,root) %{_bindir}/ping6
%{_sbindir}/tracepath6
#%endif
%{_sbindir}/tracepath
%attr(0700,root,root) %{_sbindir}/traceroute6
%{_sbindir}/rdisc
%{_mandir}/man8/*

%files doc
%defattr(-,root,root)
%doc RELNOTES bonding*/README.ifenslave


%changelog
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
