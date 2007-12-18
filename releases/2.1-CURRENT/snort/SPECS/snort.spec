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
%define version		2.7.0.1
%define release		%_revrel

Summary:	An intrusion detection system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Other
URL:		http://www.snort.org
Source0:	http://www.snort.org/dl/current/%{name}-%{version}.tar.gz
Source1:	http://www.snort.org/dl/current/%{name}-%{version}.tar.gz.sig
Source2:	snortd.run
Source3:	snortd-log.run
Source4:	snort.logrotate
Source5:	snort.sysconfig
Source6:	snortdb-extra
# snort rules are now bundled separately; these "community" rules are under the GPL
Source7:	http://www.snort.org/pub-bin/downloads.cgi/Download/comm_rules/Community-Rules-2.4.tar.gz

Patch0:		snort-2.7.0.1-mdv-lib64.patch
# (oe): make -L work as stated in the man page.
Patch1:		snort-2.6.1.5-mdv-no_timestamp.patch
Patch2:		snort-2.6.1-mdv-plugins_fix.patch
Patch3:		snort-2.7.0.1-avx-config.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libpcap-devel >= 0.6
BuildRequires:	mysql-devel
BuildRequires:	openssl-devel
BuildRequires:	postgresql-devel
BuildRequires:	texinfo
BuildRequires:	zlib-devel
BuildRequires:	pcre-devel
BuildRequires:	net1.0-devel
BuildRequires:	chrpath
BuildRequires:	iptables-devel
#BuildRequires:	net-snmp-devel
#BuildRequires:	libdnet-devel >= 1.10

Requires(pre):	rpm-helper
Requires(preun): rpm-helper
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Requires:	pcre
Requires:	libpcap >= 0.6

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
Summary:	Snort with Flexible Response support
Group:		Networking/Other
Requires:	snort = %{version}

%description plain+flexresp
Snort compiled with flexresp support.


%package mysql
Summary:	Snort with MySQL database support
Group:		Networking/Other
Requires:	snort = %{version}

%description mysql
Snort compiled with mysql support.


%package mysql+flexresp
Summary:	Snort with MySQL database and Flexible Response support
Group:		Networking/Other
Requires:	snort = %{version}

%description mysql+flexresp
Snort compiled with mysql+flexresp support.


%package postgresql
Summary:	Snort with PostgreSQL database support
Group:		Networking/Other
Requires:	snort = %{version}

%description postgresql
Snort compiled with postgresql support. 


%package postgresql+flexresp
Summary:	Snort with PostgreSQL database and Flexible Response support
Group:		Networking/Other
Requires:	snort = %{version}

%description postgresql+flexresp
Snort compiled with postgresql+flexresp support.


%package bloat
Summary:	Snort with Flexible Response, PostgreSQL, and MySQL database support
Group:		Networking/Other
Requires:	snort = %{version}

%description bloat
Snort compiled with flexresp+mysql+postgresql support.


%package inline
Summary:	Snort with Inline support
Group:		Networking/Other
Requires:	snort = %{version}
Requires:	iptables

%description inline
Snort compiled with inline support. 


%package inline+flexresp
Summary:	Snort with Inline and Flexible Response support
Group:		Networking/Other
Requires:	snort = %{version}
Requires:	iptables

%description inline+flexresp
Snort compiled with inline+flexresp support.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 7
%patch0 -p1 -b .lib64
%patch1 -p1 -b .no_timestamp
%patch2 -p1 -b .plugins_fix
%patch3 -p1 -b .config

# fix some docs
mv docs rule-docs
rm -f doc/README.WIN32
chmod 0644 rule-docs/*.txt

# fix pid file path
echo "#define _PATH_VARRUN \"/var/run/%{name}\"" >> acconfig.h

cp %{_sourcedir}/snortdb-extra .


%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal-1.7 -I m4; automake-1.7 --foreign --add-missing --copy; autoconf

# build snort
rm -rf building && mkdir -p building && cd building
SNORT_BASE_CONFIG="--prefix=%{_prefix} \
    --build=%{_build} \
    --host=%{_host} \
    --target=%{_target_platform} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libdir}/%{name} \
    --mandir=%{_mandir} \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --enable-shared \
    --enable-pthread \
    --enable-rulestate \
    --enable-dynamicplugin \
    --enable-timestats \
    --enable-perfprofiling \
    --enable-linux-smp-stats \
    --cache-file=../../config.cache"

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
    --disable-inline
make
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
    --disable-inline
make
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
    --disable-inline
make
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
    --disable-inline
make
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
    --disable-inline
make
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
    --disable-inline
make
mv src/%{name} ../%{name}-postgresql
#make distclean
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
    --with-libipq-includes=%{_includedir} \
    --with-libipq-libraries=%{_libdir}
make
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
    --with-libipq-includes=%{_includedir} \
    --with-libipq-libraries=%{_libdir}
make
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
    --with-libipq-includes=%{_includedir} \
    --with-libipq-libraries=%{_libdir}
make
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

%makeinstall_std -C building/plain

# cleanup                                                                                                                                                                          
rm -f %{buildroot}%{_bindir}/%{name}                                                                                                                                               
rm -rf %{buildroot}%{_prefix}/src                                                                                                                                                  
rm -f %{buildroot}%{_libdir}/%{name}/dynamicengine/*.{a,la}                                                                                                                        
rm -f %{buildroot}%{_libdir}/%{name}/dynamicpreprocessor/*.{a,la}

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

install %{name}.8* %{buildroot}%{_mandir}/man8

install -m 0644 etc/*.conf %{buildroot}/%{_sysconfdir}/%{name}/
install -m 0644 etc/*.config %{buildroot}/%{_sysconfdir}/%{name}/
install -m 0644 etc/*.map %{buildroot}/%{_sysconfdir}/%{name}/
install -m 0644 etc/generators %{buildroot}/%{_sysconfdir}/%{name}/
install -m 0644 rules/*.rules %{buildroot}%{_sysconfdir}/%{name}/rules/

install -m 0644 %{_sourcedir}/snort.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m 0644 %{_sourcedir}/snort.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}

mkdir -p %{buildroot}%{_srvdir}/snortd/log
install -m 0740 %{_sourcedir}/snortd.run %{buildroot}%{_srvdir}/snortd/run
install -m 0740 %{_sourcedir}/snortd-log.run %{buildroot}%{_srvdir}/snortd/log/run

cp contrib/README doc/README.contrib

# prevent having to type every blood doc in %%files
mkdir doc2
mv doc/README.INLINE doc2/

# strip rpath
chrpath -d %{buildroot}%{_sbindir}/%{name}-*
strip %{buildroot}%{_sbindir}/%{name}-*

# where does this zero file come from? from outer space?
rm -f doc/README.SNMP.SNMP

# fix libexecdir                                                                                                                                                                   
perl -pi -e "s|/usr/local/lib/snort_|%{_libdir}/%{name}/|g" %{buildroot}%{_sysconfdir}/%{name}/snort.conf


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
%_pre_useradd snort /var/log/snort /bin/false 77


%post
update-alternatives --install %{_sbindir}/%{name} %{name} %{_sbindir}/%{name}-plain 10
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
%attr(0755,root,root) %{_sbindir}/%{name}-plain
%attr(0755,root,root) %{_mandir}/man8/%{name}.8*
%attr(0755,snort,snort) %dir /var/log/%{name}
%attr(0755,snort,snort) %dir /var/log/%{name}/empty
%attr(0755,snort,snort) %dir /var/run/%{name}
%attr(0755,snort,snort) %dir %{_sysconfdir}/%{name}
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*.config
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/generators
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/threshold.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*.map
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/rules/*.rules
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%attr(0644,root,root) %config(noreplace) /etc/sysconfig/%{name}
%attr(0755,root,root) %dir %{_libdir}/%{name}                                                                                                                                      
%attr(0755,root,root) %dir %{_libdir}/%{name}/dynamicengine                                                                                                                        
%attr(0755,root,root) %dir %{_libdir}/%{name}/dynamicpreprocessor                                                                                                                  
%attr(0755,root,root) %{_libdir}/%{name}/dynamicengine/libsf_engine.so        
%attr(0755,root,root) %{_libdir}/%{name}/dynamicpreprocessor/libsf_dcerpc_preproc.so                                                                                                     
%attr(0755,root,root) %{_libdir}/%{name}/dynamicpreprocessor/libsf_dns_preproc.so
%attr(0755,root,root) %{_libdir}/%{name}/dynamicpreprocessor/libsf_ftptelnet_preproc.so                                                                                            
%attr(0755,root,root) %{_libdir}/%{name}/dynamicpreprocessor/libsf_smtp_preproc.so
%attr(0755,root,root) %{_libdir}/%{name}/dynamicpreprocessor/libsf_ssh_preproc.so
%dir %attr(0750,root,admin) %{_srvdir}/snortd
%dir %attr(0750,root,admin) %{_srvdir}/snortd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/snortd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/snortd/log/run

%files plain+flexresp
%defattr(-,root,root)
%attr(755,root,root) %{_sbindir}/%{name}-plain+flexresp

%files mysql
%defattr(-,root,root)
%attr(755,root,root) %{_sbindir}/%{name}-mysql

%files mysql+flexresp
%defattr(-,root,root)
%attr(755,root,root) %{_sbindir}/%{name}-mysql+flexresp

%files postgresql
%defattr(-,root,root)
%attr(755,root,root) %{_sbindir}/%{name}-postgresql

%files postgresql+flexresp
%defattr(-,root,root)
%attr(755,root,root) %{_sbindir}/%{name}-postgresql+flexresp

%files inline
%defattr(-,root,root)
%attr(0755,root,root) %{_sbindir}/%{name}-inline

%files inline+flexresp
%defattr(-,root,root)
%attr(0755,root,root) %{_sbindir}/%{name}-inline+flexresp

%files bloat
%defattr(-,root,root)
%attr(755,root,root) %{_sbindir}/%{name}-bloat

%files doc
%defattr(-,root,root)
%doc doc/AUTHORS doc/BUGS doc/CREDITS doc/NEWS doc/USAGE doc/README*
%doc COPYING ChangeLog snortdb-extra RELEASE.NOTES
%doc schemas/create_mysql
%doc schemas/create_postgresql
%doc doc2/README.INLINE
%doc rule-docs


%changelog
* Mon Dec 17 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.7.0.1
- P3: comment non-existant rules and include community rules in config
- fix the perl rewrite of the config file for lib paths
- refresh the Community Rules (2007-04-27)

* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.7.0.1
- rebuild against new mysql, openssl

* Tue Jul 24 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.7.0.1
- 2.7.0.1
- updated P0 from Mandriva due to mysqlclient check changes
- don't bzip2 the manpages manually
- rebuild against new libpcap, pcre, postgresql

* Tue Jul 24 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.7.0
- 2.7.0
- rediffed P0
- update P1 from Mandriva
- rebuild against new mysql

* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.6.1.2
- 2.6.1.2
- make the snort logrotate script better (check if it's running and use
  srv rather than sv)
- drop P5; no longer required
- build against new postgresql

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.1.1
- P4: drop as it no longer applies and we weren't using it
- re-enable disabled patches (were disabled for debugging)

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.1.1
- 2.6.1.1
- fix summaries and changelog
- don't build with clamav support, as a result drop P2
- updated patches from Mandriva: 
- P4: nuke bundled libtool and fix the dynamic plugin directory
- disbable parallel build
- refresh the community rules (2.4; dated 10/23/2006)
- fix the build

* Sun Sep 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.4
- change runsvctrl calls to /sbin/sv calls

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.4
- rebuild against new mysql
- rebuild against new openssl
- spec cleanups

* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.4
- change requires: s/libpcap0/libpcap/ so it will install on x86_64 properly

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.4
- 2.4.4
- updated P2 from Mandriva
- took updated P1 from Mandriva and dropped the SNMP-related bits
- add -doc subpackage
- drop the pdf docs
- S7: new community rules (GPL-licensed so ok to include) for 2.4 dated 2006-06-05
- cleanup some assumptions about contrib files
- rebuild with gcc4

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
