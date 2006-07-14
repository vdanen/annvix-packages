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

* Mon Jul 28 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 20020927-4mdk
- remove ppc exception

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 20020927-3mdk
- rebuild

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 20020927-2mdk
- really uses 20020927 snapshot
- rediff patches 1 and 2
- patch 3 : enable the rdisc server
- patcg 4 : only display the countermeasures warnings in verbose mode
- patch 125 : fix traceroute6 that did a useless "x==y;" statement instead
  of setting a variable

* Thu Oct 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 20020927-1mdk
- 20020927 snapshot (well, there's no differences with 20020124 one...)

* Thu Jul 11 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 20020124-4mdk
- Move ping6 from %%{_sbindir} to %%{_bindir}.
- Way to get help in ipv6calc is -h now, -? still works without a hitch of
  course.
- Fix potential build problem: file not found README.

* Thu May  2 2002 Stew Benedict <sbenedict@mandrakesoft.com> 20020124-3mdk
- drop PPC no ping6 patch

* Wed Mar 27 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 20020124-2mdk
- add docbook-dtd31-sgml in BuildRequires (this fix the man build,
  thanks to camille)

* Tue Mar 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 20020124-1mdk
- 20020124 snapshot
- resync with rh
- remove merged patches
- shift mdk patches numbers by 100
- add BuildRequires: openjade perl-SGMLSpm for man pages

* Sat Jan 19 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 20001110-9mdk
- Patch103: Use official SIOCBONDxxx ioctls for bonding
  (fixes build on all platforms)
- Pass COPTS not RPM_OPT_FLAGS to ipv6calc build, to build w/ MDK cflags
- s/Copyright/License/
- add URL tag

* Fri Sep 28 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 20001110-8mdk
- Fixed buffer overflow problem in traceroute6.c (rh)

* Thu Aug 23 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 20001110-7mdk
- Merge RH patch.
- Move arping to /sbin/ (and make link compat).

* Fri Jun  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 20001110-6mdk
- install in.rdisc.8c as rdisc.8 (rh).
- clean spec.

* Sun Apr  8 2001 Warly <warly@mandrakesoft.com> 20001110-5mdk
- add ipv6calc

* Thu Mar 8 2001 Stew Benedict <sbenedict@mandrakesoft.com> 20001110-4mdk
- no ping6 on PPC for now ;^(

* Mon Feb 26 2001 Warly <warly@mandrakesoft.com> 20001110-3mdk
- Change conflicts to xinetd < 2.1.8.9pre14-2mdk

* Wed Feb 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 20001110-2mdk
- Make conflicts with xinetd <= 2.1.8.9pre14-2mdk
- Adjust group.

* Wed Feb 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 20001110-1mdk
- First mandrake version from Red Hat version.

