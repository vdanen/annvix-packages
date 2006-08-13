#
# spec file for package squid
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		squid
%define version		2.5.STABLE14
%define release		%_revrel

## Redefine configure values.
%define         	_bindir %{_prefix}/sbin
%define         	_libexecdir %{_libdir}/squid
%define         	_sysconfdir /etc/squid
%define         	_localstatedir /var

Summary:	The Squid proxy caching server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.squid-cache.org
Source:		ftp://ftp.squid-cache.org/pub/squid-2/STABLE/%{name}-%{version}.tar.bz2
Source3:	squid.logrotate
Source4:	squid.conf.authenticate
Source5:	smb.conf
Source6:	squid.conf.transparent
Source7:	rc.firewall
Source8:	ERR_CUSTOM_ACCESS_DENIED.English
Source10:	squid-2.5-samba-2.2.7-winbindd_nss.h
Source11:	squid.run
Source12:	squid-log.run
Source13:	squid.stop
Source14:	squid.sysconfig
Patch0:		squid-2.5.STABLE7-avx-make.patch
Patch1:		squid-2.5-config.patch
Patch2:		squid-2.5.STABLE7-avx-user_group.patch
Patch3:		squid-2.5.STABLE2-ssl.patch
Patch4:		squid-2.5.STABLE5-pipe.patch
# Upstream bugfix patches
Patch100:	http://www.squid-cache.org/Versions/v2/2.5/bugs/squid-2.5.STABLE14-httpReplyDestroy.patch


BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openldap-devel
BuildRequires:	libsasl-devel
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	pam-devel

Requires(pre):	rpm-helper
Requires(preun): rpm-helper
Requires(post):	rpm-helper
Requires(postun): rpm-helper

%description
Squid is a high-performance proxy caching server for Web clients,
supporting FTP, gopher, and HTTP data objects. Unlike traditional
caching software, Squid handles all requests in a single,
non-blocking, I/O-driven process. Squid keeps meta data and especially
hot objects cached in RAM, caches DNS lookups, supports non-blocking
DNS lookups, and implements negative caching of failed requests.

Squid consists of a main server program squid, a Domain Name System
lookup program (dnsserver), a program for retrieving FTP data
(ftpget), and some management and client tools.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q

%patch1 -p1
%patch2 -p1
%patch0 -p1
%patch3 -p1 -b .ssl
%patch4 -p1 -b .pipe
%patch100 -p1

cp %{_sourcedir}/squid-2.5-samba-2.2.7-winbindd_nss.h helpers/basic_auth/winbind/winbindd_nss.h
cp %{_sourcedir}/squid-2.5-samba-2.2.7-winbindd_nss.h helpers/ntlm_auth/winbind/winbindd_nss.h
cp %{_sourcedir}/squid-2.5-samba-2.2.7-winbindd_nss.h helpers/external_acl/winbind_group/winbindd_nss.h


%build
%serverbuild
perl -p -i -e "s|^SAMBAPREFIX.*|SAMBAPREFIX = /usr|" helpers/basic_auth/SMB/Makefile.in
perl -p -i -e "s|^icondir.*|icondir = \\$\(libexecdir\)/icons|" icons/Makefile.am icons/Makefile.in

grep -r "local/bin/perl" %{_builddir}/%{name}-%{version} |sed -e "s/:.*$//g" | xargs perl -p -i -e "s@local/bin/perl@bin/perl@g"

%configure \
    --enable-poll \
    --enable-snmp \
    --enable-removal-policies="heap,lru" \
    --enable-storeio="aufs,coss,diskd,ufs,null" \
    --enable-useragent-log \
    --enable-referer-log \
    --enable-cachemgr-hostname=localhost \
    --enable-truncate \
    --enable-underscores \
    --enable-carp \
    --enable-async-io \
    --enable-htcp \
    --enable-delay-pools \
    --enable-linux-netfilter \
    --enable-ssl \
    --enable-arp-acl \
    --enable-auth="basic,digest,ntlm" \
    --enable-basic-auth-helpers="winbind,multi-domain-NTLM,getpwnam,YP,SMB,PAM,NCSA,MSNT,LDAP" \
    --enable-ntlm-auth-helpers="SMB,fakeauth,no_check,winbind" \
    --enable-digest-auth-helpers="password" \
    --enable-external-acl-helpers="ip_user,ldap_group,unix_group,wbinfo_group,winbind_group" \
    --with-pthreads \
    --with-winbind-auth-challenge \
    --disable-dependency-tracking \
    --disable-ident-lookups \
    --with-maxfd=1024

# Some versions of autoconf fail to detect sys/resource.h correctly;
# apparently because it generates a compiler warning.

if [ -e /usr/include/sys/resource.h ]; then
cat >>include/autoconf.h <<EOF
#ifndef HAVE_SYS_RESOURCE_H
#define HAVE_SYS_RESOURCE_H 1
#define HAVE_STRUCT_RUSAGE 1
#endif
EOF
fi

# move the errors files
grep -r errors * |grep share | sed -e "s/:.*$//g" | xargs perl -p -i -e "s|usr/share/errors|usr/lib/squid/errors|g" 
grep -r iconsdir * |grep share | sed -e "s/:.*$//g" | xargs perl -p -i -e "s|usr/share/errors|usr/lib/squid/errors|g" 

%make

grep -r errors * |grep share | sed -e "s/:.*$//g" | xargs perl -p -i -e "s|usr/share/errors|usr/lib/squid/errors|g" 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall 

pushd errors
    rm -rf %{buildroot}%{_sysconfdir}/errors
    mkdir -p %{buildroot}%{_libexecdir}/errors
    mkdir -p %{buildroot}/%{_libexecdir}/icons
    for i in *; do
        if [ -d $i ]; then
            mkdir -p %{buildroot}%{_libexecdir}/errors/$i
            install -m 644 $i/* %{buildroot}%{_libexecdir}/errors/$i
        fi
    done
popd
ln -fs %{_libexecdir}/errors/English %{buildroot}%{_sysconfdir}/errors

mkdir -p %{buildroot}%{_srvdir}/squid/log
mkdir -p %{buildroot}%{_sysconfdir}/
mkdir -p %{buildroot}/etc/{logrotate.d,pam.d,sysconfig}

install -m 0740 %{_sourcedir}/squid.run %{buildroot}%{_srvdir}/squid/run
install -m 0740 %{_sourcedir}/squid-log.run %{buildroot}%{_srvdir}/squid/log/run
cp %{_sourcedir}/squid.logrotate %{buildroot}/etc/logrotate.d/squid
cp %{_sourcedir}/squid.sysconfig %{buildroot}/etc/sysconfig/squid

cp helpers/basic_auth/SMB/smb_auth.sh %{buildroot}/%{_libexecdir}
cp helpers/basic_auth/SASL/squid_sasl_auth %{buildroot}/%{_libexecdir}
cp helpers/basic_auth/MSNT/msntauth.conf.default %{buildroot}%{_sysconfdir}

cp helpers/basic_auth/LDAP/README README.auth_ldap
cp helpers/ntlm_auth/no_check/README.no_check_ntlm_auth .
cp helpers/basic_auth/SMB/README README.auth_smb
cp helpers/basic_auth/SASL/README README.auth_sasl
cp helpers/basic_auth/MSNT/README.html README.auth_msnt.html
cp helpers/basic_auth/SASL/squid_sasl_auth.conf .

mkdir -p %{buildroot}/%{_mandir}/man8
cp helpers/basic_auth/LDAP/*.8 %{buildroot}/%{_mandir}/man8

cp %{_sourcedir}/squid.conf.authenticate squid.conf.authenticate
cp %{_sourcedir}/smb.conf smb.conf
cp %{_sourcedir}/squid.conf.transparent squid.conf.transparent
cp %{_sourcedir}/rc.firewall rc.firewall
mkdir -p %{buildroot}/%{_libexecdir}/errors/English
cp %{_sourcedir}/ERR_CUSTOM_ACCESS_DENIED.English %{buildroot}/%{_libexecdir}/errors/English/ERR_CUSTOM_ACCESS_DENIED

strip %{buildroot}/%{_libexecdir}/{msnt_auth,pam_auth,unlinkd,diskd}
strip %{buildroot}/%{_libexecdir}/{ncsa_auth,smb_auth,squid_ldap_auth,yp_auth}

cat >> %{buildroot}/etc/pam.d/squid <<EOF
#%PAM-1.0
auth		include		system-auth
auth		required	pam_nologin.so
account		include		system-auth
password	include		system-auth
session		include		system-auth
session		required	pam_limits.so
EOF

mkdir -p %{buildroot}/var/log/squid
mkdir -p %{buildroot}/var/spool/squid

# some cleaning
rm -rf %{buildroot}/%{_libdir}/%{name}/no_check.pl
mv %{buildroot}/%{_datadir}/mib.txt .
rm -rf %{buildroot}/%{_datadir}/errors


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
%_pre_useradd squid /var/spool/squid /bin/false 86

for i in /var/log/squid /var/spool/squid ; do
    if [ -d $i ] ; then
        for adir in `find $i -maxdepth 0 \! -user squid`; do
            chown -R squid:squid $adir
        done
    fi
done


%post
%_post_srv squid


%preun
%_preun_srv squid
if [ $1 = 0 ] ; then
    rm -f /var/log/squid/*
fi


%postun
%_postun_userdel squid


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/*.conf
%config(noreplace) %{_sysconfdir}/*.default
%config(noreplace) /etc/pam.d/squid
%config(noreplace) /etc/sysconfig/squid
%config(noreplace) /etc/logrotate.d/squid
%{_sysconfdir}/errors
%{_libexecdir}/errors
%{_libexecdir}/icons
%{_libexecdir}/diskd
%{_libexecdir}/unlinkd
%{_libexecdir}/cachemgr.cgi
%attr(0755,root,squid) %{_libexecdir}/ncsa_auth
%attr(0755,root,squid) %{_libexecdir}/getpwname_auth
%attr(7755,root,squid) %{_libexecdir}/pam_auth
%attr(0755,root,squid) %{_libexecdir}/msnt_auth
%attr(0755,root,squid) %{_libexecdir}/smb_auth*
%attr(0755,root,squid) %{_libexecdir}/ntlm_auth
%attr(0755,root,squid) %{_libexecdir}/squid_sasl_auth
%attr(0755,root,squid) %{_libexecdir}/squid_ldap_auth
%attr(0755,root,squid) %{_libexecdir}/yp_auth
%attr(0755,root,squid) %{_libexecdir}/wb_auth
%attr(0755,root,squid) %{_libexecdir}/fakeauth_auth
%attr(0755,root,squid) %{_libexecdir}/digest_pw_auth
%attr(0755,root,squid) %{_libexecdir}/wb_ntlmauth
%attr(0755,root,squid) %{_libexecdir}/wb_group
%attr(0755,root,squid) %{_libexecdir}/ip_user_check
%attr(0755,root,squid) %{_libexecdir}/squid_unix_group
%attr(0755,root,squid) %{_libexecdir}/squid_ldap_group
%attr(0755,root,squid) %{_libexecdir}/wbinfo_group.pl
%{_sbindir}/*
%{_mandir}/man8/*
%attr(755,squid,squid) %dir /var/log/squid
%attr(755,squid,squid) %dir /var/spool/squid
%dir %attr(0750,root,admin) %{_srvdir}/squid
%dir %attr(0750,root,admin) %{_srvdir}/squid/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/squid/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/squid/log/run

%files doc
%defattr(-,root,root)
%doc C* S* R* Q* squid.conf.* rc.firewall smb.conf doc/*


%changelog
* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE14
- rebuild against new openssl
- spec cleanups
- drop the french custom error file (S9)

* Sat Jun 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE14
- rebuild against new pam and update pam config

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE14
- 2.5.STABLE14
- drop old upstream P100, add a new one
- default to 1024 for --with-maxfd
- get rid of the %%{their_version} crap
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE12
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE12
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq
- some spec cleanups

* Wed Oct 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE12-1avx
- 2.5.STABLE12 - includes fix for CAN-2005-3258

* Thu Oct 13 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE11-1avx
- 2.5.STABLE11 - includes fix for CAN-2005-2917
- resync upstream patches

* Wed Sep 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE10-5avx
- P110-P132: more upstream bugfixes including fixes for CAN-2005-2794
  and CAN-2005-2796

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE10-4avx
- use execlineb for run scripts
- move logdir to /var/log/service/sshd
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE10-3avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE10-2avx
- bootstrap build (new gcc, new glibc)

* Wed Jun 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE10-1avx
- 2.5.STABLE10
- P100-P109 updated for all current bugfix patches
- this release also fixes the following vulnerabilities: CAN-2005-0194,
  CAN-2005-0626, CAN-2005-0718, CAN-2005-1345, CAN-2005-1519, CVE-1999-0710
- spec tidying

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE8-3avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE8-2avx
- use logger for logging

* Fri Feb 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE8-1avx
- 2.5.STABLE8
- sync with current bugfix patches
- fix P0 so that the store.log location is correct
- don't grep the entire builddir, just *our* builddir

* Tue Feb 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE7-4avx
- P123: fix for CAN-2005-0211
- P124: security fix for oversized reply headers (no CVE name yet)
- previous fixes have CVE names assigned now: CAN-2005-0173 (P117),
  CAN-2005-0174 (P118), and CAN-2005-0175 (P122)

* Mon Jan 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE7-3avx
- P102-P122: upstream patch fixes including fixes for CAN-2005-0094 and
  CAN-2005-0095

* Wed Jan 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE7-2avx
- rebuild against new openssl

* Tue Oct 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE7-1avx
- 2.5.STABLE7 (fixes CAN-2004-0918)
- regen P0, P2
- drop P5, P6, P100-P1112 (merged upstream)
- add new P100, P101 (STABLE7 fixes)

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE5-6avx
- update run scripts

* Thu Sep  9 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE5-5avx
- P6: security fix for CAN-2004-0832

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE5-4avx
- rebuild against new openssl

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.STABLE5-3avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.5.STABLE5-2sls
- use some rh work (sysconfig, two patches (P4, P5)) (florin)
- P100 through P112: upstream fixes
- S14: sysconfig file
- remove S2: don't need the initscript
- change squid's uid/gid to 86 (83 taken by nscd)

* Mon Mar 29 2004 Vincent Danen <vdanen@opensls.org> 2.5.STABLE5-1sls
- 2.5.STABLE5 (security fixes; specifically CAN-2004-0189)

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.5.STABLE3-7sls
- rebuild

* Fri Feb 06 2004 Vincent Danen <vdanen@opensls.org> 2.5.STABLE3-6sls
- squid has static uid/gid 83
- srv macros
- change run script so we shouldn't have to use the stop script

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 2.5.STABLE3-5sls
- fix the run and stop scripts (re: tmb)

* Mon Jan 12 2004 Vincent Danen <vdanen@opensls.org> 2.5.STABLE3-4sls
- OpenSLS build
- tidy spec
- remove paths from pam.d file
- don't BuildRequires: sgml-tools
- remove S1 (FAQ.sgml)
- remove initscript, add supervise scripts
