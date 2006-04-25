#
# spec file for package net-snmp
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		net-snmp
%define version		5.3.0.1
%define release		%_revrel

%define major		10
%define libname		%mklibname net-snmp %{major}

Summary:	A collection of SNMP protocol tools and libraries
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License:	BSDish
Group:		System/Servers
URL:		http://www.net-snmp.org/
Source0:	http://prdownloads.sourceforge.net/net-snmp/net-snmp-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/net-snmp/net-snmp-%{version}.tar.gz.asc
Source2:	snmpd.run
Source3:	snmpd-log.run
Source4:	snmptrapd.run
Source5:	snmptrapd-log.run
Source6:	snmpd.conf
Source8:	snmptrapd.conf
Source10:	ucd5820stat
Source11:	snmp.local.conf
Source12:	NOTIFICATION-TEST-MIB.txt
Source13:	TRAP-TEST-MIB.txt
Patch0:		net-snmp-5.1-nodb.patch
# OE: stolen from fedora
Patch20:	net-snmp-5.0.6-syslog.patch
Patch21:	net-snmp-5.0.8-ipv6-sock-close.patch
Patch22:	net-snmp-5.0.8-readonly.patch
Patch23:	net-snmp-5.1-async-getnext.patch
Patch24:	net-snmp-5.1.1-pie.patch
Patch25:	net-snmp-5.2-64bit.diff
Patch26:	net-snmp-5.1.2-dir-fix.patch
Patch27:	net-snmp-5.2.1-file_offset.patch
Patch28:	ucd-snmp-4.2.4.pre3-mnttab.patch
Patch29:	net-snmp-5.3.0.1-maxsensors.patch
Patch30:	net-snmp-5.3-agent-registry-unregister-free.patch
Patch31:	net-snmp-5.3-proc_if_inet6.patch
Patch32:	net-snmp-5.3-size_t.patch
# Extra MDK patches
Patch50:	net-snmp-5.2.2-64bit-fixes.diff
Patch51:	net-snmp-5.2.1-no_rpath.diff
# (gb) remove built-in libtool 1.4 and use the system one instead, be
# on the safe side and don't touch to the rest
Patch52:	net-snmp-5.2.1.2-libtool.patch
Patch53:	net-snmp-5.3.0.1-no_perlinstall.diff
Patch54:	net-snmp-5.3.0.1-avx-disable_test_T160.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5 >= 2.59, chrpath
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	openssl-devel, perl-devel, tcp_wrappers-devel

Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	%{libname} = %{version}
Requires(postun): %{libname} = %{version}
Requires:	openssl, net-snmp-mibs, net-snmp-utils, tcp_wrappers

%description
SNMP (Simple Network Management Protocol) is a protocol used for
network management. The NET-SNMP project includes various SNMP
tools: an extensible agent, an SNMP library, tools for requesting
or setting information from SNMP agents, tools for generating and
handling SNMP traps, a version of the netstat command which uses
SNMP, and a Tk/Perl mib browser. This package contains the snmpd
and snmptrapd daemons, documentation, etc.

You will probably also want to install the net-snmp-utils package,
which contains NET-SNMP utilities.


%package -n %{libname}
Summary:	Libraries for Network management (SNMP), from the NET-SNMP project
Group:		System/Libraries
Requires:	openssl

%description -n	%{libname}
The %{libname} package contains the libraries for use with
the NET-SNMP project's network management tools.


%package -n %{libname}-devel
Summary:	The development environment for the NET-SNMP project
Group:		Development/C
Provides:	%{name}-devel
Provides:	libnet-snmp-devel
Requires:	%{libname} = %{version}
Requires:	tcp_wrappers-devel

%description -n	%{libname}-devel
The %{libname}-devel package contains the development
libraries and header files for use with the NET-SNMP project's
network management tools.


%package -n %{libname}-static-devel
Summary:	The static development libraries for the NET-SNMP project
Group:		Development/C
Provides:	%{name}-static-devel
Requires:	%{libname}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{libname}-static-devel
The %{libname}-static-devel package contains the static
development libraries and header files for use with the NET-SNMP
project's network management tools.


%package utils
Summary:	Network management utilities using SNMP, from the NET-SNMP project
Group:		Networking/Other
Requires:	%{libname} = %{version}
Requires:	openssl
Requires:	net-snmp-mibs

%description utils
The net-snmp package contains various utilities for use with the
NET-SNMP network management project.


%package mibs
Summary:	MIBs for the NET-SNMP project
Group:		Networking/Other

%description mibs
The net-snmp-mibs package contains various MIBs for use with the
NET-SNMP network management project.

%package trapd
Summary:	The trap collecting daemon for %{name}
Group:		System/Servers
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}
Requires:	openssl, net-snmp-mibs, net-snmp-utils, tcp_wrappers

%description trapd
The net-snmp-trapd package contains the trap collecting daemon for
use with the NET-SNMP network management project.


%package -n perl-NetSNMP
Summary:	Perl utilities using SNMP, from the NET-SNMP project
Group: 		Development/Perl
Requires:	%{name} = %{version}
Requires:	%{libname} = %{version}
Requires:	net-snmp-mibs
Requires:	net-snmp-utils

%description -n	perl-NetSNMP
NET SNMP (Simple Network Management Protocol) Perl5 Support
The Simple Network Management Protocol (SNMP) provides a framework
for the exchange of management information between agents (servers)
and clients.  The NET SNMP perl5 support files provide the perl
functions for integration of SNMP into applications, written in perl.


%prep
%setup -q
%patch0 -p0 -b .nodb

# OE: added from fedora
%patch20 -p1 -b .syslog
%patch21 -p1 -b .ipv6-sock-close
%patch22 -p1 -b .readonly
%patch23 -p1 -b .async-getnext
%ifnarch ia64
%patch24 -p1 -b .pie
%endif
%patch25 -p0 -b .64bit
%patch26 -p1 -b .dir-fix
%patch27 -p1 -b .file_offset
%patch28 -p1 -b .mnttab
%patch29 -p1 -b .maxsensors
%patch30 -p0
%patch31 -p1 -b .proc_if
%patch32 -p1 -b .size_t

# Extra MDK patches
%patch50 -p1 -b .64bit-fixes
%patch51 -p0 -b .no_rpath
%patch52 -p1 -b .libtool
%patch53 -p0 -b .no_perlinstall
%patch54 -p1

cat %{_datadir}/aclocal/libtool.m4 >> aclocal.m4

# run tests in dir that is cleaned
install -d -m 0777 test_tmp_dir
HERE="$RPM_BUILD_DIR/%{name}-%{version}"
perl -pi -e "s|/tmp/snmp-test|$HERE/test_tmp_dir/snmp-test|g" testing/*

# Do this patch with a perl hack...
perl -pi -e "s|'\\\$install_libdir'|'%{_libdir}'|" ltmain.sh

# regenerate configure script
autoconf


%build
%serverbuild

%ifarch ia64 x86_64 s390x ppc64
export LDFLAGS="-L%{_libdir}"
%endif

%configure2_5x \
    --without-rpm \
    --enable-static \
    --enable-shared \
    --with-perl-modules="INSTALLDIRS=vendor" \
    --with-cflags="%{optflags} -D_REENTRANT " \
    --with-sys-location="Unknown" \
    --with-logfile="/var/log/snmpd.log" \
    --with-persistent-directory="/var/lib/net-snmp" \
    --with-mib-modules="host agentx smux" \
    --with-libwrap \
    --sysconfdir=%{_sysconfdir} \
    --enable-ipv6 \
    --enable-ucd-snmp-compatibility \
    --with-sys-contact="root@localhost" \
    --with-default-snmp-version="3"


make

# more verbose tests
perl -pi -e "s|\./RUNTESTS|\./RUNTESTS -V|g" testing/Makefile
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall \
    includedir=%{buildroot}%{_includedir}/net-snmp \
    ucdincludedir=%{buildroot}%{_includedir}/net-snmp/ucd-snmp

# the perl code needs special treatment
%makeinstall_std -C perl

mkdir -p %{buildroot}%{_sysconfdir}/{snmp,logrotate.d}

mkdir -p %{buildroot}%{_srvdir}/snmpd/{log,env}
install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/snmpd/run
install -m 0740 %{SOURCE3} %{buildroot}%{_srvdir}/snmpd/log/run
echo "-Lo -p /var/run/snmpd.pid -a" >%{buildroot}%{_srvdir}/snmpd/env/OPTIONS
install -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/snmp/snmpd.conf

mkdir -p %{buildroot}%{_srvdir}/snmptrapd/{log,env}
install -m 0740 %{SOURCE4} %{buildroot}%{_srvdir}/snmptrapd/run
install -m 0740 %{SOURCE5} %{buildroot}%{_srvdir}/snmptrapd/log/run
echo "-Lo -p /var/run/snmptrapd.pid" >%{buildroot}%{_srvdir}/snmptrapd/env/OPTIONS
install -m 0644 %{SOURCE8} %{buildroot}%{_sysconfdir}/snmp/snmptrapd.conf


install -m 0755 %{SOURCE10} %{buildroot}%{_bindir}/ucd5820stat

install -m 0644 %{SOURCE11} %{buildroot}%{_sysconfdir}/snmp/snmp.local.conf

rm -f %{buildroot}%{_bindir}/snmpinform
rm -f %{buildroot}%{_bindir}/snmpcheck
rm -f %{buildroot}%{_bindir}/tkmib
ln -s snmptrap %{buildroot}%{_bindir}/snmpinform

# install some extra stuff...
install -m 0644 mibs/DISMAN-EVENT-MIB.txt %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 mibs/LM-SENSORS-MIB.txt %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 mibs/MTA-MIB.txt %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 mibs/NET-SNMP-MONITOR-MIB.txt %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 mibs/NET-SNMP-SYSTEM-MIB.txt %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 mibs/NET-SNMP-TC.txt %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 mibs/NETWORK-SERVICES-MIB.txt %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 mibs/TUNNEL-MIB.txt %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 mibs/UCD-IPFILTER-MIB.txt %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 mibs/UCD-SNMP-MIB-OLD.txt %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 mibs/ianalist %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 mibs/rfclist %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 mibs/rfcmibs.diff %{buildroot}%{_datadir}/snmp/mibs/
install -m 0755 mibs/mibfetch %{buildroot}%{_datadir}/snmp/mibs/
install -m 0755 mibs/smistrip %{buildroot}%{_datadir}/snmp/mibs/
install -m 0755 mibs/Makefile.mib %{buildroot}%{_datadir}/snmp/mibs/
install -m 0644 man/mib2c.1 %{buildroot}%{_mandir}/man1/mib2c.1
install -m 0644 %{SOURCE12} %{buildroot}%{_datadir}/snmp/mibs/NOTIFICATION-TEST-MIB.txt
install -m 0644 %{SOURCE13} %{buildroot}%{_datadir}/snmp/mibs/TRAP-TEST-MIB.txt

# fix strange permissions
find %{buildroot}%{_datadir}/snmp/ -type f | xargs chmod 0644

# fix one bug
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_libdir}/*.la

# nuke rpath
find %{buildroot}%{perl_vendorarch} -name "*.so" | xargs chrpath -d || :

# strip these manually because otherwise they won't get stripped for some reason...
file %{buildroot}%{_bindir}/* | grep ELF | cut -d':' -f1 | xargs strip || :
file %{buildroot}%{_sbindir}/* | grep ELF | cut -d':' -f1 | xargs strip || :

%multiarch_binaries %{buildroot}%{_bindir}/net-snmp-config
%multiarch_includes %{buildroot}%{_includedir}/net-snmp/net-snmp-config.h


%post
%_post_srv snmpd


%preun
%_preun_srv snmpd


%post trapd
%_post_srv snmptrapd


%preun trapd
%_preun_srv snmptrapd


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AGENT.txt ChangeLog EXAMPLE.conf FAQ INSTALL NEWS README* TODO
%doc local/passtest local/README.mib2c local/ipf-mod.pl
%dir %attr(0750,root,admin) %{_srvdir}/snmpd
%dir %attr(0750,root,admin) %{_srvdir}/snmpd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/snmpd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/snmpd/log/run
%attr(0640,root,admin) %{_srvdir}/snmpd/env/OPTIONS
%attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/snmp/snmpd.conf
%attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/snmp/snmp.local.conf
%{_bindir}/ucd5820stat
%{_sbindir}/snmpd
%attr(0644,root,root) %{_mandir}/man5/snmpd.conf.5*
%attr(0644,root,root) %{_mandir}/man5/snmp_config.5*
%attr(0644,root,root) %{_mandir}/man5/snmp.conf.5*
%attr(0644,root,root) %{_mandir}/man5/variables.5*
%attr(0644,root,root) %{_mandir}/man5/snmpd.examples.5*
%attr(0644,root,root) %{_mandir}/man5/snmpd.internal.5*
%attr(0644,root,root) %{_mandir}/man8/snmpd.8*

%files trapd
%defattr(-,root,root,-)
%dir %attr(0750,root,admin) %{_srvdir}/snmptrapd
%dir %attr(0750,root,admin) %{_srvdir}/snmptrapd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/snmptrapd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/snmptrapd/log/run
%attr(0640,root,admin) %{_srvdir}/snmptrapd/env/OPTIONS
%attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/snmp/snmptrapd.conf
%{_sbindir}/snmptrapd
%attr(0644,root,root) %{_mandir}/man5/snmptrapd.conf.5*
%attr(0644,root,root) %{_mandir}/man8/snmptrapd.8*

%files utils
%defattr(-,root,root,-)
%{_bindir}/encode_keychange
%{_bindir}/fixproc
%{_bindir}/ipf-mod.pl
%{_bindir}/mib2c
%{_bindir}/mib2c-update
%{_bindir}/snmpbulkget
%{_bindir}/snmpbulkwalk
%{_bindir}/snmpconf
%{_bindir}/snmpdelta
%{_bindir}/snmpdf
%{_bindir}/snmpget
%{_bindir}/snmpgetnext
%{_bindir}/snmpinform
%{_bindir}/snmpnetstat
%{_bindir}/snmpset
%{_bindir}/snmpstatus
%{_bindir}/snmptable
%{_bindir}/snmptest
%{_bindir}/snmptranslate
%{_bindir}/snmptrap
%{_bindir}/snmpusm
%{_bindir}/snmpvacm
%{_bindir}/snmpwalk
%{_bindir}/traptoemail
%{_datadir}/snmp/snmpconf-data
%{_datadir}/snmp/mib2c-data
%{_datadir}/snmp/snmp_perl_trapd.pl
%{_datadir}/snmp/*.conf
%attr(0644,root,root) %{_mandir}/man1/mib2c.1*
%attr(0644,root,root) %{_mandir}/man1/snmpbulkget.1*
%attr(0644,root,root) %{_mandir}/man1/snmpbulkwalk.1*
%attr(0644,root,root) %{_mandir}/man1/snmpcmd.1*
%attr(0644,root,root) %{_mandir}/man1/snmpconf.1*
%attr(0644,root,root) %{_mandir}/man1/snmpdelta.1*
%attr(0644,root,root) %{_mandir}/man1/snmpdf.1*
%attr(0644,root,root) %{_mandir}/man1/snmpget.1*
%attr(0644,root,root) %{_mandir}/man1/snmpgetnext.1*
%attr(0644,root,root) %{_mandir}/man1/snmpinform.1*
%attr(0644,root,root) %{_mandir}/man1/snmpnetstat.1*
%attr(0644,root,root) %{_mandir}/man1/snmpset.1*
%attr(0644,root,root) %{_mandir}/man1/snmpstatus.1*
%attr(0644,root,root) %{_mandir}/man1/snmptable.1*
%attr(0644,root,root) %{_mandir}/man1/snmptest.1*
%attr(0644,root,root) %{_mandir}/man1/snmptranslate.1*
%attr(0644,root,root) %{_mandir}/man1/snmptrap.1*
%attr(0644,root,root) %{_mandir}/man1/snmpusm.1*
%attr(0644,root,root) %{_mandir}/man1/snmpwalk.1*
%attr(0644,root,root) %{_mandir}/man1/snmpvacm.1*
%attr(0644,root,root) %{_mandir}/man5/mib2c.conf.5*

%files mibs
%defattr(-,root,root,-)
%doc mibs/README.mibs
%{_datadir}/snmp/mibs

%files -n %{libname}
%defattr(-,root,root,-)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(0644,root,root,755)
%defattr(-,root,root,-)
%multiarch %{multiarch_bindir}/net-snmp-config
%multiarch %{multiarch_includedir}/net-snmp/net-snmp-config.h
%{_bindir}/net-snmp-config
%{_libdir}/*.so
%{_libdir}/*.la
#%{_includedir}/ucd-snmp
%{_includedir}/net-snmp
%{_includedir}/net-snmp/net-snmp-config.h
%{_mandir}/man3/*

%files -n %{libname}-static-devel
%defattr(0644,root,root,755)
%defattr(-,root,root,-)
%{_libdir}/*.a

%files -n perl-NetSNMP
%defattr(0644,root,root,755)
%{perl_vendorarch}/auto/NetSNMP
%{perl_vendorarch}/auto/SNMP
%{perl_vendorarch}/SNMP.pm
%{perl_vendorarch}/NetSNMP
%{perl_vendorarch}/Bundle/Makefile.subs.pl
%{_mandir}/man3/NetSNMP*
%{_mandir}/man3/SNMP.3*


%changelog
* Tue Apr 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.3.0.1
- drop all lmsensors stuff since a) we don't ship it and b) apparently
  it doesn't work too well anyways

* Fri Apr 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.3.0.1
- first Annvix build
- comment out lm_sensors stuff
- P54: disable test T160 for now so we can finish building the spec (this
  still needs to be fixed, however)
- add run scripts
- remove initscripts
- remove sysconfig files (use ./env/OPTIONS instead)
- don't log to syslog, but log to STDOUT/STDERR instead
- remove logrotate file

* Thu Apr 06 2006 Oden Eriksson <oeriksson@mandriva.com> 5.3.0.1-6mdk
- deactivate the lm_sensors mibs per default (S13) (#19388)

* Wed Mar 15 2006 Oden Eriksson <oeriksson@mandriva.com> 5.3.0.1-5mdk
- disable rpm support because it eats file descriptors like crazy and 
  makes the snmp daemon easy to kill
- drop the apache hooks as it is poorly written and unmaintained

* Wed Mar 08 2006 Oden Eriksson <oeriksson@mandriva.com> 5.3.0.1-4mdk
- fix deps

* Sun Feb 05 2006 Oden Eriksson <oeriksson@mandriva.com> 5.3.0.1-3mdk
- fix crash on s390x and ppc64 (from fedora 5.3-4)

* Wed Feb 01 2006 Oden Eriksson <oeriksson@mandriva.com> 5.3.0.1-2mdk
- added P29,P30,P31 from fedora (5.3-3)

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 5.3.0.1-1mdk
- 5.3.0.1 (security fix)

* Fri Jan 06 2006 Oden Eriksson <oeriksson@mandriva.com> 5.3-2mdk
- drop selinux support

* Wed Jan 04 2006 Oden Eriksson <oeriksson@mandriva.com> 5.3-1mdk
- 5.3
- drop obsolete/upstream patches (P29-P32)

* Sat Dec 31 2005 Stefan van der Eijk <stefan@eijk.nu> 5.2.2-3mdk
- re-enable rpm support

* Wed Dec 21 2005 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-2mdk
- bump major to 9 (!)
- fix deps

* Tue Dec 20 2005 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-1mdk
- 5.2.2
- drop obsolete/upstream patches, reorder patches
- sync with fedora (5.2.2-4.1)
- rediffed P50
- added a work around for #20256 (S13)

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 5.2.1.2-6mdk
- rebuilt against openssl-0.9.8a

* Tue Oct 25 2005 Oden Eriksson <oeriksson@mandriva.com> 5.2.1.2-5mdk
- rebuilt against new shared tcp_wrappers lib (libwrap)
- fix deps
- fix #16460

* Fri Sep  9 2005 Olivier Blin <oblin@mandriva.com> 5.2.1.2-4mdk
- fix typo in summary

* Tue Aug 23 2005 Oden Eriksson <oeriksson@mandriva.com> 5.2.1.2-3mdk
- mod_ap2_snmp_1.03 (Minor bugfixes)
- fix deps

* Thu Aug 18 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 5.2.1.2-2mdk
- add back some of previous 64-bit fixes
- libtool fixes for the testsuite to work with just-built libraries

* Fri Aug 12 2005 Olivier Blin <oblin@mandriva.com> 5.2.1.2-1mdk
- 5.2.1.2

* Wed Jul 20 2005 Olivier Blin <oblin@mandriva.com> 5.2.1-6mdk
- conflict with libsnmp-devel (#16460)

* Thu Jun 09 2005 Oden Eriksson <oeriksson@mandriva.com> 5.2.1-5mdk
- added P52 to fix a mem leak (Loic Vaillant)
- added two mibs on request by Loic Vaillant
- use the %%mkrel macro
- reactivate the make test test suite

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.2.1-4mdk
- sync with fedora (5.2.1-13)
- rediffed our 64bit fixes patch (now P50)
- use new rpm-4.4.x pre,post magic
- nuke rpath, spec file hack + P51
- rpmlint fixes

* Fri Mar 11 2005 Luca Berra <bluca@vodka.it> 5.2.1-3mdk 
- devel pacjage requires lm_sensors-devel when building with lm_sensors support

* Mon Feb 14 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.2.1-2mdk
- mod_ap2_snmp_1.02
- drop P28, it's implemented upstream

* Tue Feb 01 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.2.1-1mdk
- 5.2.1
- added P27 (fedora)

* Mon Jan 31 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.2-3mdk
- fix deps and conditional %%multiarch

* Sat Jan 15 2005 Luca Berra <bluca@vodka.it> 5.2-2mdk 
- rebuild to catch libwrap requiring libnsl

* Fri Dec 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.2-1mdk
- 5.2
- sync with fedora
- drop P4,P6,P22,P27,P31, redundant/merged upstream
- rpmlint fixes

* Tue Nov 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.1.2-7mdk
- rebuilt for unthreaded perl

* Mon Oct  4 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.1.2-6mdk
- 64-bit fixes + little endian fix for AgentX (SF #996462)

* Thu Aug 26 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.1.2-5mdk
- fix a problem with showing numerical OID's (S9), reported by "tbsky"

* Thu Aug 26 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.1.2-4mdk
- perl-Net-SNMP does not obsolete the older perl-Net-SNMP that 
  provides perl(Net::SNMP), these are unrelated(!) rename _this_ 
  perl package to perl-NetSNMP.

* Thu Aug 26 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.1.2-3mdk
- added the perl-Net-SNMP sub package

* Mon Aug 23 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.1.2-2mdk
- added P28 to make S10 compile

* Sat Aug 21 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.1.2-1mdk
- 5.1.2
- added S10, but it won't compile just yet...
- drop P1 & P5, it's included

* Sun Jun 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 5.1.1-1mdk
- 5.1.1
- stole P20 - P27 from fedora
- fixed the initscripts
- use the %%configure2_5x macro
- remove deprecated stuff from S6
- run tests in dir that is cleaned
- misc spec file fixes

* Wed Mar 17 2004 Florin <florin@mandrakesoft.com> 5.1-7mdk
- add the bsd-compat patch to fix the error:
"process `snmptrapd' is using obsolete setsockopt SO_BSDCOMPAT"

* Mon Jan 19 2004 Jean-Michel Dault <jmdault@mandrakesoft.com> 5.1-6mdk
- build without rpm support. This was the old behavior, until 9.2 it really 
  just depended on whether the build host had rpm-devel installed.
- All versions except 9.2 were compiled without rpm support and noone 
  complained, whereas many people complained about the extra dependency
  in 9.2. 
- It also creates problems in postxif/cyrus-imapd under user-mode linux.
  Linking with both db4 and librpmdb, which have the same symbols, causes
  confusion, weird behavior, and potential segfaults.
- According to rfc 1514 (Host Resources MIB), paragraph 4.7, this feature is
  optional.
- It can also create security risks, by making all versions of packages
  installed remotely.
- I guess if someone needs snmp rpm support badly, they're mostly
  experienced sysadmins and can recompile the package.

* Sun Jan 18 2004 Luca Berra <bluca@vodka.it> 5.1-5mdk 
- make net-snmp-config tell about libwrap
- devel package Requires rpm-devel and tcp_wrappers-devel

* Sun Dec 14 2003 Stefan van der Eijk <stefan@eijk.nu> 5.1-4mdk
- BuildRequires

* Mon Dec 01 2003 Florin <florin@mandrakesoft.com> 5.1-3mdk
- fix libname

* Mon Dec 01 2003 Florin <florin@mandrakesoft.com> 5.1-2mdk
- obsoletes libnet-snmp50

* Thu Nov 27 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.1-1mdk
- 5.1
- rediff P3
- honour %%{_sysconfdir}/sysconfig/snmpd if present in S2 (fix by Andre Nathan)
- drop P5 in favour to INSTALL_PREFIX
- misc spec file fixes

* Sun Nov 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.0.9-1mdk
- 5.0.9 (security release)
- added P5

* Thu Sep 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.0.8-8mdk
- fix deps

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 5.0.8-7mdk
- Rebuild to fix bad signature

* Fri Jul 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.0.8-6mdk
- rebuild

* Sat Jun 28 2003 Stefan van der Eijk <stefan@eijk.nu> 5.0.8-5mdk
- fixed provides on -static-devel package, should not Provide -devel

* Fri Jun 06 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 5.0.8-4mdk
- use double %'s in changelog

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.0.8-3mdk
- rebuilt against rpm v4.2

* Tue Apr 22 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.0.8-2mdk
- many spec file fixes
- fix buildrequires and requires
- try to make it work out of the box... (less secure...)
- revert "enable snmp v3 as default"
- run "make test"

* Tue Apr 01 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.0.8-1mdk
- 5.0.8
- fix P3
- misc spec file fixes

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.0.7-2mdk
- really build against openssl-0.9.7 this time
- enable snmp v3 as default
- added S9
- fixed S6
- misc spec file fixes

* Wed Jan 15 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.0.7-1mdk
- 5.0.7
- ship with pgp sig file
- built against openssl-0.9.7
- fix P3, removed P5 (it's included)

* Wed Jan 01 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.0.6-1mdk
- stolen from RH Rawhide and adapted for ML
- added the static-devel sub package
- misc spec file fixes
- fixed the sysv scripts
- used rpm logic from the xerces-c.spec file
- break out the mibs into a sub package so that for example a 
  future php-snmp package would only require %{libname} and
  net-snmp-mibs (correct?)
- added the %%changelog from the ucd-snmp.spec file

* Fri Jul 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2.3-4mdk
- rpmlint fixes: configure-without-libdir-spec, hardcoded-library-path

* Mon Jun 10 2002 Stefan van der Eijk <stefan@eijk.nu> 4.2.3-3mdk
- BuildRequires
- fix %%configure

* Thu Feb 14 2002 Vincent Danen <vdanen@mandrakesoft.com> 4.2.3-2mdk
- fix initscript (restart was acting like restop)
- bzip2 all patches
- re-include perlpath patch

* Wed Feb 13 2002 Vincent Danen <vdanen@mandrakesoft.com> 4.2.3-1mdk
- 4.2.3
- merge patches from RedHat

* Tue Nov  6 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 4.2.2-2mdk
- pass --build/--host/--target when not using %%configure
- add URL (rpmlint)
- Add Provides for what is Obsolete (rpmlint)

* Wed Oct 10 2001 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.2-1mdk
- new version
- removed P3, it's merged upstream
- made rpmlint happy.

* Mon Sep 24 2001 Vincent Saugey <vince@mandrakesoft.com> 4.2.1-5mdk
- Change release

* Sat Sep 22 2001 Vincent Saugey <vince@mandrakesoft.com> 4.2.1-4mdk
- Change require on openssl.

* Sun Sep 16 2001 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.2.1-3mdk
- added patch 2 and 3
- build with OpenSSL support

* Mon Aug 25 2001 Vincent Saugey <vince@mandrakesoft.com> 4.2.1-2mdk
- Add obsolete

* Thu Apr  5 2001 Vincent Saugey <vince@mandrakesoft.com> 4.2.1-1mdk
- Up to 4.2.1
- Libification
- Merging rh patch

* Fri Jun  9 2000 Vincent Saugey <vince@mandrakesoft.com> 4.1.2-1mdk
- Up to 4.1.2
- Clean in %file

* Tue Jun  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.1.1-6mdk
- Remove crappy perl-PDL dependences.

* Thu May 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.1.1-5mdk
- libtoolizifications.

* Wed Apr 12 2000 Vincent Saugey <vince@mandrakesoft.com> 4.1.1-4mdk
- Correct ldconfig in postun

* Sat Mar 25 2000 Vincent Saugey <vince@mandrakesoft.com> 4.1.1-3mdk
- many change in config snmpd file

* Thu Mar 23 2000 Vincent Saugey <vince@mandrakesoft.com> 4.1.1-2mdk
- Remove tkmib
- Patch for broken link in man page

* Thu Mar 21 2000 Vincent Saugey <vince@mandrakesoft.com> 4.1.1-1mdk
- Update to 4.1.1
- Modification in spec file
- corrected group

* Mon Jan 24 2000 Francis Galiegue <francis@mandrakesoft.com>
- Fixed spec file (%%install tried to mkdir /var/ucd-snmp)

* Tue Nov 30 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- --with-libwrap, not --with-libwrap="-lwrap -lnsl" (rh on crack)
- bump spec to 3mdk to get above Chmouel

* Sun Oct 31 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- SMP check/build
- 4.0.1 + redhat patches

* Sat Jul 17 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 3.6.2

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Thu Apr  8 1999 Wes Hardaker <wjhardaker@ucdavis.edu>
- fix Source0 location.
- fix the snmpd.conf file to use real community names.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Fri Mar 19 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 3.6.1, fix configuration file stuff.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Tue Feb  2 1999 Jeff Johnson <jbj@redhat.com>
- restore host resources mib
- simplified config file
- rebuild for 6.0.

* Tue Dec 22 1998 Bill Nottingham <notting@redhat.com>
- remove backup file to fix perl dependencies

* Tue Dec  8 1998 Jeff Johnson <jbj@redhat.com>
- add all relevant rpm scalars to host resources mib.

* Sun Dec  6 1998 Jeff Johnson <jbj@redhat.com>
- enable libwrap (#253)
- enable host module (rpm queries over SNMP!).

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries

* Fri Oct  2 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.5.3.
- don't include snmpcheck until perl-SNMP is packaged.

* Thu Aug 13 1998 Jeff Johnson <jbj@redhat.com>
- ucd-snmpd.init: start daemon w/o -f.

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- don't start snmpd unless requested
- start snmpd after pcmcia.

* Sun Jun 21 1998 Jeff Johnson <jbj@redhat.com>
- all but config (especially SNMPv2p) ready for prime time

* Sat Jun 20 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.5.

* Tue Dec 30 1997 Otto Hammersmith <otto@redhat.com>
- created the package... possibly replace cmu-snmp with this.
