#
# spec file for package cups
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		cups
%define version		1.2.7
%define release		%_revrel

%define major		2
%define libname		%mklibname %{name} %{major}

Summary:	Common Unix Printing System
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.cups.org/
Source0:	ftp://ftp.easysw.com/pub/cups/%{version}/%{name}-%{version}-source.tar.bz2
Source1:	cupsd.run
Source2:	cupsd-log.run
Source3:	cups.pam
Patch0:		cups-CVE-2007-3387.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	openldap-devel
BuildRequires:	zlib-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libjpeg-devel

Requires:	%{libname} >= %{version}-%{release}
Requires:	openssl
Requires:	net-tools
Requires(post):	rpm-helper
Requires(preun): rpm-helper



%description
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. It contains the command line utilities for
printing and administration (lpr, lpq, lprm, lpadmin, lpc, ...), man
pages, locales, and a sample configuration file for daemon-less CUPS
clients (/etc/cups/client.conf).


%package -n %{libname}
Summary:	Common Unix Printing System - CUPS library
License:	LGPL
Group:		System/Servers
Requires:	openssl
Requires:	net-tools

%description -n %{libname}
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This package contains the CUPS API library
which contains common functions used by both the CUPS daemon and all
CUPS frontends (lpr-cups, xpp, qtcups, kups, ...).


%package -n %{libname}-devel
Summary:	Common Unix Printing System - Development environment "libcups"
License:	LGPL
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Requires:	cups-common = %{version}-%{release}
Requires:	openssl
Requires:	openssl-devel
Provides:	libcups-devel = %{version}-%{release}
Provides:	cups-devel

%description -n %{libname}-devel
The Common Unix Printing System provides a portable printing layer for
UNIX(TM) operating systems. This is the development package for
creating additional printer drivers, printing software, and other CUPS
services using the main CUPS library "libcups".


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .cve-2007-3387

# fix the makefiles so they don't set file ownerships
perl -p -i -e "s/ -o \\$.CUPS_USER.//" scheduler/Makefile
perl -p -i -e "s/ -g \\$.CUPS_GROUP.//" scheduler/Makefile
perl -p -i -e "s/ -o \\$.CUPS_USER.//" systemv/Makefile
perl -p -i -e "s/ -g \\$.CUPS_GROUP.//" systemv/Makefile

perl -p -i -e 's:(libdir=")\$exec_prefix/lib64("):$1%{_libdir}$2:' config-scripts/cups-directories.m4


%build
%serverbuild
export CFLAGS="%{optflags} -fPIC"
export CXXFLAGS="%{optflags} -fPIC"
export STRIP="/usr/bin/strip"

./configure \
    --libdir=%{_libdir} \
    --enable-ssl \
    --enable-static \
    --enable-install_static \
    --with-cups-user=lp \
    --with-cups-group=sys \
    --with-system-groups="admin root" \
    --without-php \
    --with-docdir=%{_datadir}/cups/doc

# Remove hardcoded "chgrp" from Makefiles
perl -p -i -e 's/chgrp/:/' Makefile */Makefile

make CHOWN=":" STRIP="$STRIP" OPTIM="$CFLAGS" \
    REQUESTS=%{buildroot}%{_var}/spool/cups \
    LOGDIR=%{buildroot}%{_var}/log/cups \
    STATEDIR=%{buildroot}%{_var}/run/cups

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make install BUILDROOT=%{buildroot} \
    DOCDIR=%{buildroot}%{_datadir}/cups/doc \
    CHOWN=":" CHGRP=":" STRIP="$STRIP" \
    LOGDIR=%{buildroot}%{_var}/log/cups \
    REQUESTS=%{buildroot}%{_var}/spool/cups \
    STATEDIR=%{buildroot}%{_var}/run/cups

mkdir -p %{buildroot}%{_sysconfdir}/cups/ssl
mkdir -p %{buildroot}%{_prefix}/lib/cups/driver
mkdir -p %{buildroot}/var/run/cups/certs

# install PPDs
mkdir -p %{buildroot}%{_datadir}/cups/model
install -m 0755 ppd/*.ppd %{buildroot}%{_datadir}/cups/model/

mkdir -p %{buildroot}%{_srvdir}/cupsd/log
install -m 0740 %{_sourcedir}/cupsd.run %{buildroot}%{_srvdir}/cupsd/run
install -m 0740 %{_sourcedir}/cupsd-log.run %{buildroot}%{_srvdir}/cupsd/log/run

%ifarch x86_64
ln -s %{_prefix}/lib/cups %{buildroot}%{_libdir}/cups
%endif

# cleanup
rm -rf %{buildroot}%{_sysconfdir}/rc*
rm -rf %{buildroot}%{_sysconfdir}/init.d
rm -rf %{buildroot}%{_mandir}/cat*
rm -rf %{buildroot}%{_mandir}/*/cat*
rm -rf %{buildroot}%{_datadir}/locale

# install missing devel files
mkdir -p %{buildroot}%{_includedir}/cups
install -m 0644 cups/debug.h  %{buildroot}%{_includedir}/cups/
install -m 0644 cups/string.h %{buildroot}%{_includedir}/cups/
install -m 0644 config.h %{buildroot}%{_includedir}/cups/
#install -m 0755 cups/libcups.a %{buildroot}%{_libdir}/
#install -m 0755 filter/libcupsimage.a %{buildroot}%{_libdir}/

%multiarch_includes %{buildroot}%{_includedir}/cups/config.h

# Create dummy config files /etc/cups/printers.conf,
# /etc/cups/classes.conf, and /etc/cups/client.conf
touch %{buildroot}%{_sysconfdir}/cups/printers.conf
touch %{buildroot}%{_sysconfdir}/cups/classes.conf
touch %{buildroot}%{_sysconfdir}/cups/client.conf

# pam
cp -f %{_sourcedir}/cups.pam %{buildroot}%{_sysconfdir}/pam.d/cups
chmod 0644 %{buildroot}%{_sysconfdir}/pam.d/cups


%post
/sbin/ldconfig
chgrp -R sys /etc/cups /var/*/cups
%_post_srv cupsd


%post -n %{libname} -p /sbin/ldconfig


%preun
%_preun_srv cupsd


%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{_sysconfdir}/cups
%config(noreplace) %{_sysconfdir}/cups/cupsd.conf
%ghost %config(noreplace) %attr(-,lp,sys) %{_sysconfdir}/cups/client.conf
%ghost %config(noreplace) %{_sysconfdir}/cups/printers.conf
%ghost %config(noreplace) %{_sysconfdir}/cups/classes.conf
%attr(-,root,sys) %{_sysconfdir}/cups/cupsd.conf.default
%config(noreplace) %attr(-,root,sys) %{_sysconfdir}/cups/interfaces
%config(noreplace) %attr(0644,root,sys) %{_sysconfdir}/cups/mime.convs
%config(noreplace) %attr(0644,root,sys) %{_sysconfdir}/cups/mime.types
%config(noreplace) %attr(-,root,sys) %{_sysconfdir}/cups/ppd
%config(noreplace) %attr(-,root,sys) %{_sysconfdir}/cups/ssl
%config(noreplace) %{_sysconfdir}/pam.d/cups
%{_bindir}/*
%attr(6755,root,sys) %{_bindir}/lppasswd
%exclude %{_bindir}/cups-config
%{_sbindir}/*
%dir %{_prefix}/lib/cups
%{_prefix}/lib/cups/*
%ifarch x86_64
%{_libdir}/cups
%endif
%{_datadir}/cups
#%{_datadir}/locale/*/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_var}/log/cups
%dir %attr(0710,lp,sys) %{_var}/spool/cups
%dir %attr(1700,lp,sys) %{_var}/spool/cups/tmp
%dir %attr(0775,lp,sys) %{_var}/cache/cups
%attr(0511,lp,sys) /var/run/cups/certs
%dir %attr(0750,root,admin) %{_srvdir}/cupsd
%dir %attr(0750,root,admin) %{_srvdir}/cupsd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/cupsd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/cupsd/log/run

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libcups.so.*
%{_libdir}/libcupsimage.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/cups/*
%multiarch %{multiarch_includedir}/cups/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_bindir}/cups-config

%files doc
%defattr(-,root,root)
%doc *.txt


%changelog
* Sun Sep 2 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- P0: security fix for CVE-2007-3387

* Fri Dec 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- 1.2.7
- rebuild against new pam

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.2
- rebuild against new openldap 

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.2
- rebuild against new mysql
- rebuild against new openssl
- rebuild against new openldap 
- spec cleanups

* Fri Jun 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.2
- 1.2.2
- rebuild against new libtiff

* Fri Jun 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.1
- rebuild against new pam
- S3: pam config

* Sat May 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.1
- 1.2.1
- rebuild with gcc4
- requires(post|preun): rpmhelper

* Wed May 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.0
- 1.2.0

* Mon May 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2
- first Annvix build (this is actually 1.2rc3 but i'm tagging it 1.2
  to avoid epoch issues or stupid version names)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
