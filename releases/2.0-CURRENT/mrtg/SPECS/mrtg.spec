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
%define version		2.14.4
%define release		%_revrel

%define _provides_exceptions perl(MRTG_lib)\\|perl(locales_mrtg)\\|perl(stat.pl)\\|perl(find.pl)\\|perl(MRP::BaseClass)\\|%{_bindir}/ksh\\|%{_bindir}/expect
%define _requires_exceptions perl(MRTG_lib)\\|perl(locales_mrtg)\\|perl(stat.pl)\\|perl(find.pl)\\|perl(MRP::BaseClass)\\|%{_bindir}/ksh\\|%{_bindir}/expect\\|pear(.*.inc.php)\\|perl(Net::SNMP)

Summary:	Multi Router Traffic Grapher
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Other
URL:		http://www.mrtg.org/
Source0:	http://oss.oetiker.ch/mrtg/pub/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gd-devel
BuildRequires:	zlib-devel
BuildRequires:	png-devel
BuildRequires:	chrpath

Requires:	perl
Requires:	net-snmp

%description
The Multi Router Traffic Grapher (MRTG) is a tool to monitor the
traffic load on network-links. MRTG generates HTML pages containing
PNG images which provide a LIVE visual representation of this traffic.


%package contribs
Summary:	Multi Router Traffic Grapher contribs
Group:		Networking/Other
Requires:	%{name} = %{version}
Requires(pre):	expect
Requires(pre):	pdksh

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
find -type f | xargs perl -pi -e "s|/store/bin/perl|%{_bindir}/perl|g; \
    s|/usr/local/bin/perl|%{_bindir}/perl|g; \
    s|/usr/sepp/bin/perl|%{_bindir}/perl|g; \
    s|/usr/tardis/local/gnu/bin/perl5|%{_bindir}/perl|g; \
    s|/usr/local/gnu/bin/perl5|%{_bindir}/perl|g; \
    s|/usr/drwho/local/bin/perl|%{_bindir}/perl|g; \
    s|c\:\\\perl\\\bin|%{_bindir}/perl|g; \
    s|/opt/gnu/bin/perl|%{_bindir}/perl|g; \
    s|/pkg/gnu/bin/perl|%{_bindir}/perl|g"


%build
export LIBS="$LIBS -L%{_prefix}/X11R6/%{_lib} -lXpm -lX11"

%configure \
    --with-gd=%{_prefix} \
    --with-gd-lib=%{_libdir} \
    --with-gd-inc=%{_includedir} \
    --with-z=%{_prefix} \
    --with-z-lib=%{_libdir} \
    --with-z-inc=%{_includedir} \
    --with-png=%{_prefix} \
    --with-png-lib=%{_libdir} \
    --with-png-inc=%{_includedir}

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

mkdir -p %{buildroot}%{_datadir}
mkdir -p %{buildroot}/var/www/html/mrtg
mkdir -p %{buildroot}%{perl_vendorarch}

find contrib | cpio -dpm %{buildroot}%{_datadir}/mrtg2

install -m 0644 images/*.png %{buildroot}/var/www/html/mrtg
install -m 0644 -c lib/mrtg2/{Pod/*pm,*pm} %{buildroot}%{perl_vendorarch}/

# clean up
rm -rf %{buildroot}/%{_libdir}/mrtg2/{*gif,*png,Pod/*pm,*pm}
rm -rf %{buildroot}/%{_libdir}/mrtg2/contrib/mrtgmk/src/

pushd %{buildroot}/%{_datadir}/mrtg2
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


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(755,root,root) %dir /var/www/html/mrtg
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
%attr(644,root,root) /var/www/html/mrtg/*

%files contribs
%defattr(-,root,root)
%{_mandir}/man1/mrtg-contrib.1*
%{_datadir}/mrtg2/contrib/*

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
