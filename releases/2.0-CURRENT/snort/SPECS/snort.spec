#
# spec file for package snort
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		snort
%define version		2.3.3
%define release		%_revrel

Summary:	An intrusion detection system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Other
URL:		http://www.snort.org
Source0:	http://www.snort.org/dl/%{name}-%{version}.tar.gz
Source1:	snortd.run
Source2:	snortd-log.run
Source3:	http://www.snort.org/dl/%{name}-%{version}.tar.gz.asc
Source4:	snort.logrotate
Source5:	snort.sysconfig
Source6:	snortdb-extra

Patch1:		snort-2.3.0RC2-lib64.patch
Patch2:		snort-2.3.0RC2-clamav.diff
# (oe): make -L work as stated in the man page.
Patch3:		snort-2.3.0-no_timestamp.diff
# (oe) disable some code to make it build
Patch4:		snort-2.3.0-net-snmp_fix.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5, automake1.7
BuildRequires:	libpcap-devel >= 0.6
BuildRequires:	MySQL-devel
BuildRequires:	openssl-devel
BuildRequires:	postgresql-devel
BuildRequires:	texinfo
BuildRequires:	zlib-devel
BuildRequires:	pcre-devel
BuildRequires:	net1.0-devel
BuildRequires:	chrpath
BuildRequires:	iptables-devel, clamav-devel
#BuildRequires:	net-snmp-devel

Requires(pre):	rpm-helper
Requires(preun): rpm-helper
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Requires:	pcre
Requires:	libpcap0 >= 0.6

%description
Snort is a libpcap-based packet sniffer/logger which 
can be used as a lightweight network intrusion detection system. 
It features rules based logging and can perform protocol analysis, 
content searching/matching and can be used to detect a variety of 
attacks and probes, such as buffer overflows, stealth port scans, 
CGI attacks, SMB probes, OS fingerprinting attempts, and much more. 
Snort has a real-time alerting capabilty, with alerts being sent to syslog, 
a separate "alert" file, or as a WinPopup message via Samba's smbclient

This version is compiled without database support. Edit the spec file
and rebuild the rpm to enable it.

Edit %{_sysconfdir}/%{name}/snort.conf to configure snort and use snort.d to start snort

This rpm is different from previous rpms and while it will not clobber
your current snortd file, you will need to modify it.

There are 9 different packages available

All of them require the base snort rpm.  Additionally, you will need
to chose a binary to install.

%{_sbindir}/snort should end up being a symlink to a binary in one of
the following configurations. We use update-alternatives for this.
Here are the different packages along with their priorities.

plain(10)		plain+flexresp(11)
mysql(12)		mysql+flexresp(13)
postgresql(14)		postgresql+flexresp(15)
bloat(16)
inline(17)		inline+flexresp(18)

Please see the documentation in %{_docdir}/%{name}-%{version}


%package plain+flexresp
Summary:	Snort with Flexible Response
Group:		Networking/Other
Requires:	snort = %{version}

%description plain+flexresp
Snort compiled with flexresp support.


%package mysql
Summary:	Snort with Flexible Response
Group:		Networking/Other
Requires:	snort = %{version}

%description mysql
Snort compiled with mysql support.


%package mysql+flexresp
Summary:	Snort with Flexible Response
Group:		Networking/Other
Requires:	snort = %{version}

%description mysql+flexresp
Snort compiled with mysql+flexresp support.


%package postgresql
Summary:	Snort with Flexible Response
Group:		Networking/Other
Requires:	snort = %{version}

%description postgresql
Snort compiled with postgresql support. 


%package postgresql+flexresp
Summary:	Snort with Flexible Response
Group:		Networking/Other
Requires:	snort = %{version}

%description postgresql+flexresp
Snort compiled with postgresql+flexresp support.


%package bloat
Summary:	Snort with Flexible Response
Group:		Networking/Other
Requires:	snort = %{version}

%description bloat
Snort compiled with flexresp+mysql+postgresql support.


%package inline
Summary:	Snort with Flexible Response
Group:		Networking/Other
Requires:	snort = %{version}
Requires:	iptables, clamav, clamav-db

%description inline
Snort compiled with inline support. 


%package inline+flexresp
Summary:	Snort with Flexible Response
Group:		Networking/Other
Requires:	snort = %{version}
Requires:	iptables, clamav, clamav-db

%description inline+flexresp
Snort compiled with inline+flexresp support.


%prep
%setup -q
%patch1 -p0 -b .lib64
%patch2 -p1 -b .clamav
%patch3 -p0 -b .no_timestamp
#%patch4 -p0 -b .net-snmp_fix

# fix pid file path
echo "#define _PATH_VARRUN \"/var/run/%{name}\"" >> acconfig.h

cp %{SOURCE6} .


%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force && aclocal-1.7 && autoheader && automake-1.7 --add-missing && autoconf --force


# build snort
rm -rf building && mkdir -p building && cd building
export AM_CFLAGS="-g -O2"
SNORT_BASE_CONFIG="--prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --cache-file=../../config.cache "

# there are some strange configure errors
# when not doing a distclean between major builds.
# plain 
{
mkdir plain; cd plain
../../configure $SNORT_BASE_CONFIG \
    --without-mysql \
    --disable-mysql \
    --without-postgresql \
    --disable-postgresql \
    --without-oracle \
    --disable-oracle \
    --without-odbc \
    --disable-odbc \
    --without-snmp \
    --disable-snmp \
    --without-inline \
    --disable-inline \
    --without-clamav \
    --disable-clamav
%make
mv src/%{name} ../%{name}-plain
#make distclean 
cd ..
}

# plain+flexresp
{
mkdir plain+flexresp; cd plain+flexresp
../../configure $SNORT_BASE_CONFIG \
    --without-mysql \
    --disable-mysql \
    --without-postgresql \
    --disable-postgresql \
    --without-oracle \
    --disable-oracle \
    --without-odbc \
    --disable-odbc \
    --without-snmp \
    --disable-snmp \
    --enable-flexresp \
    --with-libnet-includes=%{_includedir} \
    --with-libnet-libraries=%{_libdir} \
    --without-inline \
    --disable-inline \
    --without-clamav \
    --disable-clamav
%make
mv src/%{name} ../%{name}-plain+flexresp
# make distclean 

cd ..
}

# mysql+flexresp
{
mkdir mysql+flexresp; cd mysql+flexresp
../../configure $SNORT_BASE_CONFIG \
    --with-mysql=%{_prefix} \
    --without-postgresql \
    --disable-postgresql \
    --without-oracle \
    --disable-oracle \
    --without-odbc \
    --disable-odbc \
    --without-snmp \
    --disable-snmp \
    --enable-flexresp \
    --with-libnet-includes=%{_includedir} \
    --with-libnet-libraries=%{_libdir} \
    --without-inline \
    --disable-inline \
    --without-clamav \
    --disable-clamav
%make
mv src/%{name} ../%{name}-mysql+flexresp
# make distclean 
cd ..
}

# mysql
{
mkdir mysql; cd mysql
../../configure $SNORT_BASE_CONFIG \
    --with-mysql=%{_prefix} \
    --without-postgresql \
    --disable-postgresql \
    --without-oracle \
    --disable-oracle \
    --without-odbc \
    --disable-odbc \
    --without-snmp \
    --disable-snmp \
    --without-inline \
    --disable-inline \
    --without-clamav \
    --disable-clamav
%make
mv src/%{name} ../%{name}-mysql
# make distclean 
cd ..
}

# postgresql+flexresp
{
mkdir postgresql+flexresp; cd postgresql+flexresp
../../configure $SNORT_BASE_CONFIG \
    --without-mysql --disable-mysql \
    --with-postgresql=%{_prefix} \
    --without-oracle \
    --disable-oracle \
    --without-odbc \
    --disable-odbc \
    --without-snmp \
    --disable-snmp \
    --enable-flexresp \
    --with-libnet-includes=%{_includedir} \
    --with-libnet-libraries=%{_libdir} \
    --without-inline \
    --disable-inline \
    --without-clamav \
    --disable-clamav
%make
mv src/%{name} ../%{name}-postgresql+flexresp
# make distclean 
cd ..
}

# postgresql
{
mkdir postgresql; cd postgresql
../../configure $SNORT_BASE_CONFIG \
    --without-mysql \
    --disable-mysql \
    --with-postgresql=%{_prefix} \
    --without-oracle \
    --disable-oracle \
    --without-odbc \
    --disable-odbc \
    --without-snmp \
    --disable-snmp \
    --without-inline \
    --disable-inline \
    --without-clamav \
    --disable-clamav
%make
mv src/%{name} ../%{name}-postgresql
# make distclean 
cd ..
}

# bloat
{
mkdir bloat; cd bloat
../../configure $SNORT_BASE_CONFIG \
    --with-mysql=%{_prefix} \
    --with-postgresql=%{_prefix} \
    --without-oracle \
    --disable-oracle \
    --without-odbc \
    --disable-odbc \
    --without-snmp \
    --disable-snmp \
    --with-openssl=%{_prefix} \
    --enable-flexresp \
    --with-libnet-includes=%{_includedir} \
    --with-libnet-libraries=%{_libdir} \
    --with-inline \
    --enable-inline \
    --with-clamav \
    --enable-clamav \
    --with-libipq-includes=%{_includedir} \
    --with-libipq-libraries=%{_libdir} \
    --with-clamav-includes=%{_includedir} \
    --with-clamav-defdir=%{_localstatedir}/clamav
%make
mv src/%{name} ../%{name}-bloat
# make distclean
cd ..
}

# inline
{
mkdir inline; cd inline
../../configure $SNORT_BASE_CONFIG \
    --without-mysql \
    --disable-mysql \
    --without-postgresql \
    --disable-postgresql \
    --without-oracle \
    --disable-oracle \
    --without-odbc \
    --disable-odbc \
    --without-snmp \
    --disable-snmp \
    --with-inline \
    --enable-inline \
    --with-clamav \
    --enable-clamav \
    --with-libipq-includes=%{_includedir} \
    --with-libipq-libraries=%{_libdir} \
    --with-clamav-includes=%{_includedir} \
    --with-clamav-defdir=%{_localstatedir}/clamav
%make
mv src/%{name} ../%{name}-inline
# make distclean 
cd ..
}

# inline+flexresp
{
mkdir inline+flexresp; cd inline+flexresp
../../configure $SNORT_BASE_CONFIG \
    --without-mysql \
    --disable-mysql \
    --without-postgresql \
    --disable-postgresql \
    --without-oracle \
    --disable-oracle \
    --without-odbc \
    --disable-odbc \
    --without-snmp \
    --disable-snmp \
    --enable-flexresp \
    --with-inline \
    --enable-inline \
    --with-clamav \
    --enable-clamav \
    --with-libipq-includes=%{_includedir} \
    --with-libipq-libraries=%{_libdir} \
    --with-clamav-includes=%{_includedir} \
    --with-clamav-defdir=%{_localstatedir}/clamav
%make
mv src/%{name} ../%{name}-inline+flexresp
# make distclean 
cd ..
}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/%{name}/rules
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}/var/log/%{name}/empty
install -d %{buildroot}/var/run/%{name}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_mandir}/man8

{
pushd building
    install %{name}-plain %{buildroot}%{_sbindir}/%{name}-plain
    install %{name}-plain+flexresp %{buildroot}%{_sbindir}/%{name}-plain+flexresp
    install %{name}-mysql %{buildroot}%{_sbindir}/%{name}-mysql
    install %{name}-mysql+flexresp %{buildroot}%{_sbindir}/%{name}-mysql+flexresp
    install %{name}-postgresql %{buildroot}%{_sbindir}/%{name}-postgresql
    install %{name}-postgresql+flexresp %{buildroot}%{_sbindir}/%{name}-postgresql+flexresp
    install %{name}-inline %{buildroot}%{_sbindir}/%{name}-inline
    install %{name}-inline+flexresp %{buildroot}%{_sbindir}/%{name}-inline+flexresp
    install %{name}-bloat %{buildroot}%{_sbindir}/%{name}-bloat
popd
}

[[ -f "%{name}.8.bz2" ]] || bzip2 %{name}.8
install %{name}.8* %{buildroot}%{_mandir}/man8
perl -pi -e "s|var RULE_PATH ../rules|var RULE_PATH rules|" etc/%{name}.conf

install -m 0644 etc/*.conf %{buildroot}/%{_sysconfdir}/%{name}/
install -m 0644 etc/*.config %{buildroot}/%{_sysconfdir}/%{name}/
install -m 0644 etc/*.map %{buildroot}/%{_sysconfdir}/%{name}/
install -m 0644 rules/*.rules %{buildroot}%{_sysconfdir}/%{name}/rules/

install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

mkdir -p %{buildroot}%{_srvdir}/snortd/log
install -m 0740 %{SOURCE1} %{buildroot}%{_srvdir}/snortd/run
install -m 0740 %{SOURCE2} %{buildroot}%{_srvdir}/snortd/log/run

#remove the contrib archive files
# remove some of the contrib archive files
bzme contrib/snortdb-extra.gz
bzme contrib/Spade-092200.1.tar.gz
bzme contrib/passiveOS.tar.gz
bzme contrib/snortnet.tar.gz
bzme contrib/snortwatch-0.7.tar.gz

rm -rf contrib/*.gz
cp contrib/README doc/README.contrib

# don't ship this
rm -rf contrib/rpm

# prevent having to type every blood doc in %%files
mkdir doc2
mv doc/README.INLINE doc2/

# strip rpath
chrpath -d %{buildroot}%{_sbindir}/%{name}-*

# where does this zero file come from? from outer space?
rm -f doc/README.{SNMP.SNMP,clamav.clamav}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
%_pre_useradd snort /var/log/snort /bin/false 77

%post
update-alternatives --install %{_sbindir}/%{name} %{name} %{_sbindir}/%{name}-plain 10
if [ -d /var/log/supervise/snortd -a ! -d /var/log/service/snortd ]; then
    mv /var/log/supervise/snortd /var/log/service/
fi
%_post_srv snortd

%preun
%_preun_srv snortd

%postun
%_postun_userdel snort
# remove the link if not upgrade
if [ $1 = 0 ]; then
    update-alternatives --remove %{name} %{_sbindir}/%{name}-plain
fi

%post plain+flexresp
update-alternatives --install %{_sbindir}/%{name} %{name} %{_sbindir}/%{name}-plain+flexresp 11

%postun plain+flexresp
update-alternatives --remove %{name} %{_sbindir}/%{name}-plain+flexresp

%post mysql
update-alternatives --install %{_sbindir}/%{name} %{name} %{_sbindir}/%{name}-mysql 12

%postun mysql
update-alternatives --remove %{name} %{_sbindir}/%{name}-mysql

%post mysql+flexresp
update-alternatives --install %{_sbindir}/%{name} %{name} %{_sbindir}/%{name}-mysql+flexresp 13

%postun mysql+flexresp
update-alternatives --remove %{name} %{_sbindir}/%{name}-mysql+flexresp

%post postgresql
update-alternatives --install %{_sbindir}/%{name} %{name} %{_sbindir}/%{name}-postgresql 14

%postun postgresql
update-alternatives --remove %{name} %{_sbindir}/%{name}-postgresql

%post postgresql+flexresp
update-alternatives --install %{_sbindir}/%{name} %{name} %{_sbindir}/%{name}-postgresql+flexresp 15

%postun postgresql+flexresp
update-alternatives --remove %{name} %{_sbindir}/%{name}-postgresql+flexresp

%post bloat
update-alternatives --install %{_sbindir}/%{name} %{name} %{_sbindir}/%{name}-bloat 16

%postun bloat
update-alternatives --remove %{name} %{_sbindir}/%{name}-bloat

%post inline
update-alternatives --install %{_sbindir}/%{name} %{name} %{_sbindir}/%{name}-inline 17

%postun inline
update-alternatives --remove %{name} %{_sbindir}/%{name}-inline

%post inline+flexresp
update-alternatives --install %{_sbindir}/%{name} %{name} %{_sbindir}/%{name}-inline+flexresp 18

%postun inline+flexresp
update-alternatives --remove %{name} %{_sbindir}/%{name}-inline+flexresp


%files
%defattr(-,root,root)
%doc doc/snort_manual.pdf
%doc doc/AUTHORS doc/BUGS doc/CREDITS doc/NEWS doc/USAGE doc/README*
%doc COPYING ChangeLog contrib/* snortdb-extra.bz2 RELEASE.NOTES
%attr(0755,root,root) %{_sbindir}/%{name}-plain
%attr(0755,root,root) %{_mandir}/man8/%{name}.8*
%attr(0755,snort,snort) %dir /var/log/%{name}
%attr(0755,snort,snort) %dir /var/log/%{name}/empty
%attr(0755,snort,snort) %dir /var/run/%{name}
%attr(0755,snort,snort) %dir %{_sysconfdir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*.config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/threshold.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*.map
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/rules/*.rules
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0644,root,root) %config(noreplace) /etc/sysconfig/%{name}
%dir %attr(0750,root,admin) %{_srvdir}/snortd
%dir %attr(0750,root,admin) %{_srvdir}/snortd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/snortd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/snortd/log/run

%files plain+flexresp
%defattr(-,root,root)
%attr(755,root,root) %{_sbindir}/%{name}-plain+flexresp

%files mysql
%defattr(-,root,root)
%doc schemas/create_mysql
%attr(755,root,root) %{_sbindir}/%{name}-mysql

%files mysql+flexresp
%defattr(-,root,root)
%doc schemas/create_mysql
%attr(755,root,root) %{_sbindir}/%{name}-mysql+flexresp

%files postgresql
%defattr(-,root,root)
%doc schemas/create_postgresql
%attr(755,root,root) %{_sbindir}/%{name}-postgresql

%files postgresql+flexresp
%defattr(-,root,root)
%doc schemas/create_postgresql
%attr(755,root,root) %{_sbindir}/%{name}-postgresql+flexresp

%files inline
%defattr(-,root,root)
%doc doc2/README.INLINE
%attr(0755,root,root) %{_sbindir}/%{name}-inline

%files inline+flexresp
%defattr(-,root,root)
%doc doc2/README.INLINE
%attr(0755,root,root) %{_sbindir}/%{name}-inline+flexresp

%files bloat
%defattr(-,root,root)
%attr(755,root,root) %{_sbindir}/%{name}-bloat


%changelog
* Wed Feb  1 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.3
- build against new postgresql

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.3
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.3
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.3.3
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.3-3avx
- rebuild against new pcre

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.3-2avx
- s/supervise/service/ in log/run

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.3-1avx
- 2.3.3
- use execlineb for run scripts
- move logdir to /var/log/service/snortd
- run scripts are now considered config files and are not replaceable
- P3: make -L work as stated in the manpage (oden)
- own %%{_sysconfdir}/%%{name}
- P4: make the snmp-enabled snort binary build (currently unapplied due
  to the fact we don't ship net-snmp)

* Sat Aug 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.0-4avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.0-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.0-2avx
- rebuild

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.3.0-1avx
- 2.3.0
- use logger for logging
- strip the binaries (florin)
- speed up configure by using --cache-file (oden)
- drop previous P2; no longer needed
- P2: add inline support (thanks to William Metcalf)
- bundle the logrotate and sysconfig files

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.0-9avx
- rebuild against latest openssl

* Fri Sep 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.0-8avx
- update run scripts
- update logrotate patch

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.0-7avx
- rebuild against new openssl

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.0-6avx
- Annvix build

* Fri Apr 30 2004 Vincent Danen <vdanen@opensls.org> 2.1.0-5sls
- rebuild against new libpcap 0.8.3

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 2.1.0-4sls
- minor spec cleanups
- fix logrotation (P2)

* Tue Feb 03 2004 Vincent Danen <vdanen@opensls.org> 2.1.0-3sls
- supervise scripts
- remove initscript
- snort has static uid/gid of 77

* Sun Jan 11 2004 Vincent Danen <vdanen@opensls.org> 2.1.0-2sls
- OpenSLS build
- tidy spec
- remove all snmp support
- lib64net1.0-devel if amd64

* Sat Dec 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.1.0-1mdk
- 2.1.0
- fix build[requires]
- updated P0 (also removed hardcoded lib stuff, like in P1)
- updated P1
- build against libnet1.0-devel-1.0.2a
- remove rpath in binaries
- fix pid file path
- misc spec file fixes

* Tue Dec 02 2003 Florin <florin@mandrakesoft.com> 2.0.5-2mdk
- new initscript and sysconf files
- add the logrotate file
- use update-alternatives

* Fri Nov 28 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.5-1mdk
- 2.0.5
- _really_ enable snmp, it was removed in 2.0.0 (P0)
- built against new net-snmp libs
- misc spec file fixes

* Mon Sep 22 2003 Florin <florin@mandrakesoft.com> 2.0.2-1mdk
- 2.0.2
- fix the service snort stop in some cases (thx to S. Toothman)

* Fri Sep 05 2003 Florin <florin@mandrakesoft.com> 2.0.1-3mdk
- requires libnet-snmp instead of ucd-snmp

* Thu Sep 04 2003 Florin <florin@mandrakesoft.com> 2.0.1-2mdk
- buildrequires libpcap-devel instead of libpcap0-devel

* Thu Aug 28 2003 Florin <florin@mandrakesoft.com> 2.0.1-1mdk
- 2.0.1
- requires ucd-snmp-devel instead net-snmp-devel

* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.0.0-3mdk
- rebuild
- prereq on rpm-helper

* Tue Apr 22 2003 Florin <florin@mandrakesoft.com> 2.0.0-2mdk
- acid is already in contribs 

* Tue Apr 22 2003 Florin <florin@mandrakesoft.com> 2.0.0-1mdk
- 2.0.0 security fix
- remove the configure patch0
- update the lib64 patch
- add some more contribs

* Mon Mar 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.9.1-1mdk
- 1.9.1 (security fix)

* Sat Feb 01 2003 en Eriksson <oden.eriksson@kvikkjokk.net> 1.9.0-5mdk
- repack some of the contrib/*.gz stuff as it's crucial and needed for 
applications like acid, etc. (why cripple snort???)
- BuildRequires net-snmp-devel

* Tue Nov 26 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.9.0-4mdk
- Patch1: Make it lib64-aware, do regenerate configure script
- Fix %%doc, try to make it a little more -bi --short-circuit'able

* Wed Oct 16 2002 Florin <florin@mandrakesoft.com> 1.9.0-3mdk
- use rules instead of ../rules in PATH

* Wed Oct 16 2002 Florin <florin@mandrakesoft.com> 1.9.0-2mdk
- add the missing reference.config file

* Tue Oct 15 2002 Florin <florin@mandrakesoft.com> 1.9.0-1mdk
- 1.9.0

* Fri Aug 30 2002 Florin <florin@mandrakesoft.com> 1.8.7-3mdk
- forgot the Requires on libsnmp-devel

* Thu Aug 29 2002 Florin <florin@mandrakesoft.com> 1.8.7-2mdk
- bring back the snmp packages (configure patch)

* Fri Aug 02 2002 Florin <florin@mandrakesoft.com> 1.8.7-1mdk
- 1.8.7
- comment out the snmp package as it doesn not compile for the moment
- add the snort user

* Fri May 03 2002 Florin <florin@mandrakesoft.com> 1.8.6-1mdk
- 1.8.6
- update the libpcap0 require

* Fri Apr 05 2002 Florin <florin@mandrakesoft.com> 1.8.5-1mdk
- 1.8.5
- remove the integrated icmp patch

* Wed Feb 20 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.8.3-4mdk
- patch to fix ICMP ascii printing bug (affects 1.8.3 only)

* Wed Feb 20 2002 Florin <florin@mandrakesoft.com> 1.8.3-3mdk
- modify the init script according to the new sysconfig file
- add the contrib files (not the archives)

* Tue Feb 19 2002 Florin <florin@mandrakesoft.com> 1.8.3-2mdk
- use force while creating the links in post
- use noreplace for the initscript
- remove the add/del of the snort user/group as they come with setup
- remove the link only in uninstall cases
- add the sysconfig file 
- use -s as default in the initscript (log to syslog)

* Fri Feb 15 2002 Florin <florin@mandrakesoft.com> 1.8.3-1mdk
- 1.8.3

* Thu Jan 10 2002 Stefan van der Eijk <stefan@eijk.nu> 1.8.2-3mdk
- BuildRequires
- replace make -j with %%make

* Wed Dec 12 2001 Florin <florin@mandrakesoft.com> 1.8.2-2mdk
- update the BuildRequires

* Wed Nov 14 2001 Florin <florin@mandrakesoft.com> 1.8.2-1mdk
- 1.8.2
- merge with the original spec file
- use macros when possible
- fix some typos in post section
- create the link in all cases for snort-plain
- fix a spelling error in description
- bzip2 the man page
- strip the binaries
- create the snort/snort user/group in post
- /var/log/snort files belong to snort.snort
- add _{preun|post}_service macros

* Mon Sep 24 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.8.1-2mdk
- add manpage

* Tue Sep 04 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.8.1-1mdk
- 1.8.1

* Fri Aug 10 2001 Florin Grad <florin@mandrakesoft.com> 1.8p1-1mdk
- 1.8p1

* Tue Feb 20 2001 Florin Grad <florin@mandrakesoft.com> 1.7-1mdk
- mandrake adaptions

* Mon Nov 27 2000 Chris Green <cmg@uab.edu>
- removed strip
- upgrade to cvs version
- moved /var/snort/dev/null creation to install time

* Tue Nov 21 2000 Chris Green <cmg@uab.edu>
- changed to %{SnortPrefix}
- upgrade to patch2

* Mon Jul 31 2000 Wim Vandersmissen <wim@bofh.st>
- Integrated the -t (chroot) option and build a /home/snort chroot jail
- Installs a statically linked/stripped snort
- Updated %{_initrddir}/snortd to work with the chroot option

* Tue Jul 25 2000 Wim Vandersmissen <wim@bofh.st>
- Added some checks to find out if we're upgrading or removing the package

* Sat Jul 22 2000 Wim Vandersmissen <wim@bofh.st>
- Updated to version 1.6.3
- Fixed the user/group stuff (moved to %post)
- Added userdel/groupdel to %postun
- Automagically adds the right IP, nameservers to %{_sysconfdir}/rules.base

* Sat Jul 08 2000 Dave Wreski <dave@linuxsecurity.com>
- Updated to version 1.6.2
- Removed references to xntpd
- Fixed minor problems with snortd init script

* Fri Jul 07 2000 Dave Wreski <dave@linuxsecurity.com>
- Updated to version 1.6.1
- Added user/group snort

* Sat Jun 10 2000 Dave Wreski <dave@linuxsecurity.com>
- Added snort init.d script (snortd)
- Added Dave Dittrich's snort rules header file (ruiles.base)
- Added Dave Dittrich's wget rules fetch script (check-snort)
- Fixed permissions on /var/log/snort
- Created /var/log/snort/archive for archival of snort logs
- Added post/preun to add/remove snortd to/from rc?.d directories
- Defined configuration files as %config

* Tue Mar 28 2000 William Stearns <wstearns@pobox.com>
- Quick update to 1.6.
- Sanity checks before doing rm-rf in install and clean

* Fri Dec 10 1999 Henri Gomez <gomez@slib.fr>
- 1.5-0 Initial RPM release

