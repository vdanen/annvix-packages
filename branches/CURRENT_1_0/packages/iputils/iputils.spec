%define name	iputils
%define version	20%{ver}
%define release	6sls
%define ver	020927

%{!?build_opensls:%global build_opensls 0}

Summary:	Network monitoring tools including ping.
Name:		%{name}
Version: 	%{version}
Release:	%{release}
License:	BSD
Group:		System/Base
URL:		ftp://ftp.inr.ac.ru/ip-routing/
Source0:	http://ftp.sunet.se/pub/os/Linux/ip-routing/iputils-ss%ver.tar.bz2
Source1:	bonding-0.2.tar.bz2
Patch0:		iputils-20001007-rh7.patch.bz2
Patch1:		iputils-20020927-datalen.patch.bz2
Patch2:		iputils-20020927-ping_sparcfix.patch.bz2
Patch3:		iputils-20020124-rdisc-server.patch.bz2 
Patch4:		iputils-20020124-countermeasures.patch.bz2 
Patch5:		iputils-20001110-bonding-sockios.patch.bz2
Patch6:		iputils-20020927-fix-traceroute.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
%if !%{build_opensls}
BuildRequires:	openjade perl-SGMLSpm docbook-dtd31-sgml
%endif

Conflicts:	xinetd < 2.1.8.9pre14-2mdk

%description
The iputils package contains ping, a basic networking tool.  The ping
command sends a series of ICMP protocol ECHO_REQUEST packets to a
specified network host and can tell you if that machine is alive and
receiving network traffic.

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
%make CCOPT="%optflags"
%make ifenslave -C bonding-0.2

make ifenslave -C bonding-0.2
%if !%{build_opensls}
make -C doc man
%endif

%install
rm -rf ${RPM_BUILD_ROOT}

# (TV): this is broken and uneeded
#make install DESTDIR=${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%_bindir
mkdir -p ${RPM_BUILD_ROOT}/{bin,sbin}
install -c clockdiff		${RPM_BUILD_ROOT}%{_sbindir}/
%ifos linux
install -c arping		${RPM_BUILD_ROOT}/sbin/
ln -s ../../sbin/arping ${RPM_BUILD_ROOT}%{_sbindir}/arping
install -c ping			${RPM_BUILD_ROOT}/bin/
install -c bonding-0.2/ifenslave ${RPM_BUILD_ROOT}/sbin/
%else
install -c arping      ${RPM_BUILD_ROOT}%{_sbindir}/
install -c ping            ${RPM_BUILD_ROOT}%{_sbindir}/
install -c bonding-0.2/ifenslave ${RPM_BUILD_ROOT}%{_sbindir}/
%endif
#%ifnarch ppc
install -c ping6		${RPM_BUILD_ROOT}%{_bindir}
#%endif
install -c rdisc		${RPM_BUILD_ROOT}%{_sbindir}/
install -c tracepath		${RPM_BUILD_ROOT}%{_sbindir}/
install -c tracepath6		${RPM_BUILD_ROOT}%{_sbindir}/
install -c traceroute6		${RPM_BUILD_ROOT}%{_sbindir}/

mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
#install -c in.rdisc.8c		${RPM_BUILD_ROOT}%{_mandir}/man8/rdisc.8
install -c doc/arping.8        ${RPM_BUILD_ROOT}%{_mandir}/man8/
install -c doc/clockdiff.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/
install -c doc/rdisc.8     ${RPM_BUILD_ROOT}%{_mandir}/man8/rdisc.8
install -c doc/ping.8      ${RPM_BUILD_ROOT}%{_mandir}/man8/
install -c doc/tracepath.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/


%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc RELNOTES bonding*/README.ifenslave
%{_sbindir}/clockdiff
%attr(4755,root,root)	/bin/ping
/sbin/arping
%{_sbindir}/arping
/sbin/ifenslave
#%ifnarch ppc
%attr(4755,root,root) %{_bindir}/ping6
%{_sbindir}/tracepath6
#%endif
%{_sbindir}/tracepath
%attr(4755,root,root) %{_sbindir}/traceroute6
%{_sbindir}/rdisc
%{_mandir}/man8/*

%changelog
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
- Move ping6 from %%_sbindir to %%_bindir.
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

