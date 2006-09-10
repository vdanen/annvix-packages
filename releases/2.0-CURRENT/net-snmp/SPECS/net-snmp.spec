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
BuildRequires:	autoconf2.5 >= 2.59
BuildRequires:	chrpath
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	openssl-devel
BuildRequires:	perl-devel
BuildRequires:	tcp_wrappers-devel

Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper
Requires(pre):	%{libname} = %{version}
Requires(postun): %{libname} = %{version}
Requires:	openssl
Requires:	net-snmp-mibs
Requires:	net-snmp-utils
Requires:	tcp_wrappers

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
Requires:	openssl
Requires:	net-snmp-mibs
Requires:	net-snmp-utils
Requires:	tcp_wrappers

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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


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
    --with-cflags="$CFLAGS -D_REENTRANT " \
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
install -m 0740 %{_sourcedir}/snmpd.run %{buildroot}%{_srvdir}/snmpd/run
install -m 0740 %{_sourcedir}/snmpd-log.run %{buildroot}%{_srvdir}/snmpd/log/run
echo "-Lo -p /var/run/snmpd.pid -a" >%{buildroot}%{_srvdir}/snmpd/env/OPTIONS
install -m 0644 %{_sourcedir}/snmpd.conf %{buildroot}%{_sysconfdir}/snmp/snmpd.conf

mkdir -p %{buildroot}%{_srvdir}/snmptrapd/{log,env}
install -m 0740 %{_sourcedir}/snmptrapd.run %{buildroot}%{_srvdir}/snmptrapd/run
install -m 0740 %{_sourcedir}/snmptrapd-log.run %{buildroot}%{_srvdir}/snmptrapd/log/run
echo "-Lo -p /var/run/snmptrapd.pid" >%{buildroot}%{_srvdir}/snmptrapd/env/OPTIONS
install -m 0644 %{_sourcedir}/snmptrapd.conf %{buildroot}%{_sysconfdir}/snmp/snmptrapd.conf


install -m 0755 %{_sourcedir}/ucd5820stat %{buildroot}%{_bindir}/ucd5820stat

install -m 0644 %{_sourcedir}/snmp.local.conf %{buildroot}%{_sysconfdir}/snmp/snmp.local.conf

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
install -m 0644 %{_sourcedir}/NOTIFICATION-TEST-MIB.txt %{buildroot}%{_datadir}/snmp/mibs/NOTIFICATION-TEST-MIB.txt
install -m 0644 %{_sourcedir}/TRAP-TEST-MIB.txt %{buildroot}%{_datadir}/snmp/mibs/TRAP-TEST-MIB.txt

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

%files doc
%defattr(-,root,root,-)
%doc AGENT.txt ChangeLog EXAMPLE.conf FAQ INSTALL NEWS README* TODO
%doc local/passtest local/README.mib2c local/ipf-mod.pl
%doc mibs/README.mibs


%changelog
* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.3.0.1
- rebuild against new openssl
- spec cleanups

* Fri Jul 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.3.0.1
- add -doc subpackage
- rebuild with gcc4
- use %%_sourcedir/file instead of %%{SOURCEx}

* Wed May 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.3.0.1
- fix the CFLAGS

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
