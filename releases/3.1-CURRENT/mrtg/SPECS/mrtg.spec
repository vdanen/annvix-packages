#
# spec file for package mrtg
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define	name		mrtg
%define version		2.16.1
%define release		%_revrel

%define _provides_exceptions perl(.*)
%define _requires_exceptions \\(perl(\\(MRTG_lib\\|MRP::BaseClass\\|Net::SNMP)\\)\\|pear(.*)\\)

Summary:	Multi Router Traffic Grapher
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Other
URL:		http://oss.oetiker.ch/mrtg/
Source0:	http://oss.oetiker.ch/mrtg/pub/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gd-devel
BuildRequires:	zlib-devel
BuildRequires:	png-devel
BuildRequires:	chrpath

Requires:	perl

%description
The Multi Router Traffic Grapher (MRTG) is a tool to monitor the
traffic load on network-links. MRTG generates HTML pages containing
PNG images which provide a LIVE visual representation of this traffic.


%package contribs
Summary:	Multi Router Traffic Grapher contribs
Group:		Networking/Other
Requires:	%{name} = %{version}
Requires:	expect

%description contribs
Contributed softwares for The Multi Router Traffic Grapher (MRTG)


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

# cleanups
perl -pi -e "s|^sleep .*||g" configure*

# fix perl path
find -type f | xargs perl -pi \
    -e 's|(?:/\w+)+/perl|%{_bindir}/perl|g;' \
    -e 's|c:\\perl\\bin|%{_bindir}/perl|g;'
# make the sole ksh script use sh instead (should work)
perl -pi -e 's|^#!/usr/bin/ksh|#!/bin/sh|' contrib/adm-mrtg/adm-mrtg


%build
%configure2_5x LIBS="-lXpm -lX11"
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/mrtg/contrib
mkdir -p %{buildroot}/var/www/html/mrtg
mkdir -p %{buildroot}%{perl_vendorarch}

# contribs
for contrib in \
    14all accesslistmon adm-mrtg apc_ups ascendget atmmaker \
    cfgmaker_ATM cfgmaker_cisco cfgmaker_dlci cisco_BPX_MGX ciscoindex \
    cisco_ipaccounting cisco_tftp cpuinfo cpumon \
    diskmon get-active get-equi get-multiserial GetSNMPLinesUP \
    ipchainacc ipchains ipfilter iptables_acc iptables-accounting \
    iptables_acc_snmp ircstats ircstats2 IxDisk jm linux_stat \
    meminfo monitor mrtg-archiver mrtg-archiver-script mrtg-dynip \
    mrtgidx mrtgindex.cgi mrtg-ipacc mrtg-ipget mrtg-mail \
    mrtg.php mrtg_php_portal mrtgrq \
    net-hosts NSI nt_n_cisco nt-services \
    ovmrtg ping-probe PMLines portmasters procmem \
    routers rumb-stat snmpping stat stfc switchmaker \
    TCH TotalControlModem TTrafic whodo xlsummary; do
        cp -pr contrib/${contrib} %{buildroot}/%{_datadir}/mrtg/contrib/
done

install -m 0644 images/*.png %{buildroot}/var/www/html/mrtg
install -m 0644 -c lib/mrtg2/{Pod/*pm,*pm} %{buildroot}%{perl_vendorarch}/

# clean up
rm -rf %{buildroot}/%{_libdir}/mrtg2/{*gif,*png,Pod/*pm,*pm}
rm -rf %{buildroot}/%{_libdir}/mrtg2/contrib/mrtgmk/src/

pushd %{buildroot}/%{_datadir}/mrtg
    for i in `find -name "*.h"` `find -name "*.c"`; do
	rm -f $i
    done
popd

rm -f %{buildroot}/var/www/html/mrtg/*-nt*
rm -f %{buildroot}%{_mandir}/man1/*-nt*

rm -rf %{buildroot}/usr/doc/mrtg2
rm -rf %{buildroot}/usr/share/mrtg2/icons

# fix the stupid rpatch stuff...
chrpath -d %{buildroot}%{_bindir}/rateup

# clean up
mv %{buildroot}%{_datadir}/doc/mrtg2 .

# drop private versions of perl modules
rm -f %{buildroot}%{_datadir}/%{name}/lib/SNMP_Session.pm
rm -f %{buildroot}%{_datadir}/%{name}/lib/SNMP_util.pm
rm -f %{buildroot}%{_datadir}/%{name}/lib/BER.pm
rm -rf %{buildroot}%{_datadir}/%{name}/pod
rm -rf %{buildroot}%{_datadir}/%{name}/contrib/whodo/GIFgraph


%clean
#[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %{perl_vendorarch}/*
%{_mandir}/man1/cfgmaker.1*
%{_mandir}/man1/mrtg-faq.1*
%{_mandir}/man1/mrtg-forum.1*
%{_mandir}/man1/indexmaker.1*
%{_mandir}/man1/mrtg-logfile.1*
%{_mandir}/man1/mrtg-mibhelp.1*
%{_mandir}/man1/mrtg-rrd.1*
%{_mandir}/man1/mrtg.1*
%{_mandir}/man1/mrtglib.1*
%{_mandir}/man1/mrtg-reference.1*
%{_mandir}/man1/mrtg-squid.1*
%{_mandir}/man1/mrtg-unix-guide.1*
%{_mandir}/man1/mrtg-webserver.1*
%{_mandir}/man1/mrtg-ipv6.1*
%{_mandir}/man1/mrtg-nw-guide.1*
%attr(755,root,root) %dir /var/www/html/mrtg
%attr(644,root,root) /var/www/html/mrtg/*

%files contribs
%defattr(-,root,root)
%{_mandir}/man1/mrtg-contrib.1*
%{_datadir}/mrtg/contrib/*

%files doc
%defattr(-,root,root)
%doc CHANGES MANIFEST README THANKS
%doc doc/cfgmaker.txt
%doc doc/mrtg-faq.txt
%doc doc/mrtg-forum.txt
%doc doc/indexmaker.txt
%doc doc/mrtg-logfile.txt
%doc doc/mrtg-mibhelp.txt
%doc doc/mrtg-rrd.txt
%doc doc/mrtg.txt
%doc doc/mrtglib.txt
%doc doc/mrtg-reference.txt
%doc doc/mrtg-squid.txt
%doc doc/mrtg-unix-guide.txt
%doc doc/mrtg-webserver.txt
%doc doc/mrtg-contrib.txt


%changelog
* Fri Feb 22 2008 Vincent Danen <vdanen-at-build.annvix.org> 2.16.1
- rebuild against new libpng

* Sun Feb 17 2008 Vincent Danen <vdanen-at-build.annvix.org> 2.16.1
- 2.16.1
- fix url
- don't install all contrib modules
- cleanup private copies of perl modules
- cleanup require exceptions
- drop requires on pdksh and make the one script that uses ksh use sh
  instead
- keep the requires exclusion on Net::SNMP for now as it will require a
  whole host of perl crypto modules

* Sun Sep 23 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.15.2
- 2.15.2
- build against new gd
- cleanup the configure call
- cleanup the perl path regexp
- doesn't require net-snmp
- exclude more private perl modules

* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.14.4
- 2.14.4
- fix source url

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.13.2
- add -doc subpackage
- rebuild with gcc4

* Tue Apr 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.13.2
- exclude requires on Net::SNMP until we can bundle it and the dozen or so
  modules it requires (only really required for SNMP v3 support)

* Fri Apr 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.13.2
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
