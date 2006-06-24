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
Source9:	ERR_CUSTOM_ACCESS_DENIED.French
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
BuildRequires:	openldap-devel libsasl-devel openssl-devel >= 0.9.7 pam-devel

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

cat %{SOURCE10} > helpers/basic_auth/winbind/winbindd_nss.h
cat %{SOURCE10} > helpers/ntlm_auth/winbind/winbindd_nss.h
cat %{SOURCE10} > helpers/external_acl/winbind_group/winbindd_nss.h


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

install -m 0740 %{SOURCE11} %{buildroot}%{_srvdir}/squid/run
install -m 0740 %{SOURCE12} %{buildroot}%{_srvdir}/squid/log/run
cat %{SOURCE3} > %{buildroot}/etc/logrotate.d/squid
cat %{SOURCE14} > %{buildroot}/etc/sysconfig/squid

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

cat %{SOURCE4} > squid.conf.authenticate
cat %{SOURCE5} > smb.conf
cat %{SOURCE6} > squid.conf.transparent
cat %{SOURCE7} > rc.firewall
mkdir -p %{buildroot}/%{_libexecdir}/errors/{English,French}
cat %{SOURCE8} > %{buildroot}/%{_libexecdir}/errors/English/ERR_CUSTOM_ACCESS_DENIED
cat %{SOURCE9} > %{buildroot}/%{_libexecdir}/errors/French/ERR_CUSTOM_ACCESS_DENIED

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
if [ -d /var/log/supervise/squid -a ! -d /var/log/service/squid ]; then
    mv /var/log/supervise/squid /var/log/service/
fi
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

* Mon Oct 20 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.5.STABLE3-3mdk
- rebuild for rewriting /etc/pam.d file

* Fri Aug 08 2003 Florin <florin@mandrakesoft.com> 2.5.STABLE3-2mdk
- remove the SASL module (depends on the obsolete cyrus-salsl 1.5.8)

* Wed Jul 16 2003 Florin <florin@mandrakesoft.com> 2.5.STABLE3-1mdk
- 2.5.STABLE3
- add the "winbind_group" option (Norman Zhang's suggestion)
- add the wb_group binary

* Thu Apr 10 2003 Florin <florin@mandrakesoft.com> 2.5.STABLE2-2mdk
- change the icondir => update the make patch (thx to M. Ducea)

* Thu Apr 03 2003 Florin <florin@mandrakesoft.com> 2.5.STABLE2-1mdk
- 2.5.STABLE2

* Fri Feb 07 2003 Florin <florin@mandrakesoft.com> 2.5.STABLE1-7mdk
- add BuildRequires:Openssl-devel >= 0.9.7 (thx to David MacKenzie)

* Mon Feb 03 2003 Florin <florin@mandrakesoft.com> 2.5.STABLE1-6mdk
- thx to Buchan Milne's Idea
- Update winbind headers from samba-2.2.7 (Source 10)
- Add wb_ntlmauth (allow NTLM auth with winbind with
samba-winbind-2.2.7-5mdk)

* Wed Jan 22 2003 Florin <florin@mandrakesoft.com> 2.5.STABLE1-5mdk
- fix the make patch (thx to Viestiss Tiistai 21. Tammikuuta)

* Tue Jan 21 2003 Florin <florin@mandrakesoft.com> 2.5.STABLE1-4mdk
- 2.5.STABLE1-20030121
- update the make patch
- add the ssl patch
- fix spec file

* Tue Oct 29 2002 Florin <florin@mandrakesoft.com> 2.5.STABLE1-3mdk
- add the forgotten icons (thx to M. Ducea)
- update the authenticate example

* Tue Oct 29 2002 Stefan van der Eijk <stefan@eijk.nu> 2.5.STABLE1-2mdk
- BuildRequires: libsasl-devel openssl-devel

* Fri Oct 18 2002 Florin <florin@mandrakesoft.com> 2.5.STABLE1-1mdk
- 2.5STABLE1
- update the make, config and the user_group patches
- remove the obsoleted perlpath patch
- update the paths for the SMB substitutions
- misc adaptions

* Tue Aug 06 2002 Florin <florin@mandrakesoft.com> 2.4.STABLE7-2mdk
- add user squid

* Fri Jul 05 2002 Florin <florin@mandrakesoft.com> 2.4.STABLE7-1mdk
- 2.4STABLE7 - security fixes

* Thu Jun 20 2002 Florin <florin@mandrakesoft.com> 2.4.STABLE6-2mdk
- add the ncsa compiled authentication module
- remove the FQ html from the docs qs the sgm2html is obsolete now
- qns db2html doesn't work

* Thu Apr 18 2002 Florin <florin@mandrakesoft.com> 2.4.STABLE6-1mdk
- rebuild for cooker

* Wed Mar 27 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.4.STABLE6-1.1mdk
- security fix for 8.1/8.2

* Wed Mar 27 2002 Vincent Danen <vdanen@mandrakesoft.com> 2.4.STABLE6-1mdk
- 2.4STABLE6

* Mon Feb 25 2002 Florin <florin@mandrakesoft.com> 2.4.STABLE4-2mdk
- make sure SAMBAPREFIX is replaced in the Makefile (thx to L.F.L. Mejia)
- use some sugestions for lrus, post link (thx to M.Ducea)
- remove some useless checking for a null cache (thx to A.Borsenkow)

* Thu Feb 21 2002 Florin <florin@mandrakesoft.com> 2.4.STABLE4-1mdk
- 2.4.STABLE4

* Wed Feb 13 2002 Florin <florin@mandrakesoft.com> 2.4.STABLE3-2mdk
- add the possibility of a null cache config

* Mon Jan 14 2002 Florin <florin@mandrakesoft.com> 2.4.STABLE3-1mdk
- 2.4.STABLE3
- better name for patch3

* Tue Nov 06 2001 Florin <florin@mandrakesoft.com> 2.4.STABLE2-4mdk
- bring back the pre and postun and modify the preun section for 7.2
- users

* Fri Oct 19 2001 Florin <florin@mandrakesoft.com> 2.4.STABLE2-3mdk
- rebuild for db3

* Thu Oct 11 2001 Florin <florin@mandrakesoft.com> 2.4.STABLE2-2mdk
- rebuild for db3

* Fri Oct 05 2001 Florin <florin@mandrakesoft.com> 2.4.STABLE2-1mdk
- 2.4.STABLE2
- add the ldap_auth man page
- new squid.conf.authenticate file
- add the squid.ldap.transparent, ERR_CUSTOM*, rc.firewall files
- run again as squid.squid user.group like in good old days
- replace the nogroup patch with squid.squid.patch

* Wed Oct 03 2001 Florin <florin@mandrakesoft.com> 2.4.STABLE1-11mdk
- better explanation for the samba auth in the sample conf file

* Wed Oct 03 2001 Florin <florin@mandrakesoft.com> 2.4.STABLE1-10mdk
- modify a bit the ldap authentication -> squid*ldap*patch 
- add the authenticate README files
- add a sample squid.conf.authenticate file, including diskd
- NIS, samba, ldap, pam authentication have been tested
- modify the SAMBAPREFIX var for samba authentication
- add a smb.conf sample file in docs
- s/use Authen::Smb/use Authen::Smb::Smb in smb_auth.pl
- remove the ncsa_auth module as it doesn't seem to work (use pam anyway)

* Fri Sep 28 2001 Stefan van der Eijk <stefan@eijk.nu> 2.4.STABLE1-9mdk
- BuildRequires:        openldap-devel pam-devel
- Removed BuildRequires:        jade

* Thu Aug 09 2001 Florin Grad <florin@mandrakesoft.com> 2.4.STABLE1-8mdk
- fix the authentication  
- add two authentication scripts (.sh & .pl)

* Fri Aug 03 2001 Florin <florin@mandrakesoft.com> 2.4.STABLE1-7mdk
- add the forgotten diskd. Thanks to Ian C. Sison for letting me now.

* Wed Jul 18 2001 Stefan van der Eijk <stefan@eijk.nu> 2.4.STABLE1-6mdk
- BuildRequires:        openldap-devel pam-devel
- Removed BuildRequires:        jade

* Tue Jul 17 2001 Florin <florin@mandrakesoft.com> 2.4.STABLE1-5mdk
- add the nogroup patch - the default group is now nobody instead of nogroup
- comment out the pre section - the squid user is added and deleted by the system
- add the auth_modules and their README files
- some spec file cleanings

* Sun Jun 03 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.4.STABLE1-4mdk
- Applied a patch for the config file

* Mon May 28 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.4.STABLE1-3mdk
- The init script now handle the /var/run/squid.pid file

* Tue May 22 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.4.STABLE1-2mdk
- Applied some necessary patches
- Changed log & spool file permission to nobody

* Tue May 15 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.4.STABLE1-1mdk
- Added the swap directory in /var/cache
- Changed log files permission
- Removed dnsserver's related things, it's now internal.
- Fixed the configure parameters for 2.4 
- updated to version 2.4.STABLE1

* Sun Apr 08 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.3.STABLE4-5mdk
- conformed to server policy
  
* Tue Mar 13 2001 Geoffrey Lee  <snailtalk@mandrakesoft.com> 2.3.STABLE4-4mdk
- Fix the paths where the initscript gets installed (Christian Zoffoli).

* Tue Mar 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.3.STABLE4-3mdk
- Include fixes for Squid as asked by Alexander Skwar.
- Remove stripping of binary.
- Use %configure and %makeinstall.
- Enable async io, enable carp support and enable useragent logging.

* Tue Jan 16 2001 Vincent Danen <vdanen@mandrakesoft.com> 2.3.STABLE4-2mdk
- security fix for tmpfile problems (patch#20)
- cleanup spec; macros

* Sun Nov 12 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.3.STABLE4-1mdk
- shiny version.
- comment out already applied patches.

* Tue Sep  5 2000 Etienne Faure  <etienne@mandraksoft.com> 2.3.STABLE2-3mdk
- rebuilt with %%doc macro
- added noreplace tag for config files

* Tue May  2 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.3.STABLE2-2mdk
- fixed %post script
- three more bugfix patches from the squid people
- buildprereq jade, sgmltools

* Fri Apr  7 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.3.STABLE2-1mdk
- merged with redhat again

* Sun Mar 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- make %pre more portable

* Thu Mar 16 2000 Bill Nottingham <notting@redhat.com>
- bugfix patches
- fix dependency on /usr/local/bin/perl

* Sat Mar  4 2000 Bill Nottingham <notting@redhat.com>
- 2.3.STABLE2

* Mon Feb 14 2000 Bill Nottingham <notting@redhat.com>
- Yet More Bugfix Patches

* Tue Feb  8 2000 Bill Nottingham <notting@redhat.com>
- add more bugfix patches
- --enable-heap-replacement

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- grab some bugfix patches

* Mon Jan 10 2000 Bill Nottingham <notting@redhat.com>
- 2.3.STABLE1 (whee, another serial number)

* Tue Dec 21 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix compliance with ftp RFCs
  (http://www.wu-ftpd.org/broken-clients.html)
- Work around a bug in some versions of autoconf
- BuildPrereq sgml-tools - we're using sgml2html

* Mon Oct 18 1999 Bill Nottingham <notting@redhat.com>
- add a couple of bugfix patches

* Wed Oct 13 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.STABLE5.
- update FAQ, fix URLs.

* Sat Sep 11 1999 Cristian Gafton <gafton@redhat.com>
- transform restart in reload and add restart to the init script

* Tue Aug 31 1999 Bill Nottingham <notting@redhat.com>
- add squid user as user 23.

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging
- fix conflict between logrotate & squid -k (#4562)

* Wed Jul 28 1999 Bill Nottingham <notting@redhat.com>
- put cachemgr.cgi back in /usr/lib/squid

* Wed Jul 14 1999 Bill Nottingham <notting@redhat.com>
- add webdav bugfix patch (#4027)

* Mon Jul 12 1999 Bill Nottingham <notting@redhat.com>
- fix path to config in squid.init (confuses linuxconf)

* Wed Jul  7 1999 Bill Nottingham <notting@redhat.com>
- 2.2.STABLE4

* Wed Jun 9 1999 Dale Lovelace <dale@redhat.com>
- logrotate changes
- errors from find when /var/spool/squid or
- /var/log/squid didn't exist

* Thu May 20 1999 Bill Nottingham <notting@redhat.com>
- 2.2.STABLE3

* Thu Apr 22 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.STABLE.2

* Sun Apr 18 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.STABLE1

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- don't need to run groupdel on remove
- fix useradd

* Mon Apr 12 1999 Bill Nottingham <notting@redhat.com>
- fix effective_user (bug #2124)

* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- strip binaries

* Thu Apr  1 1999 Bill Nottingham <notting@redhat.com>
- duh. adduser does require a user name.
- add a serial number

* Tue Mar 30 1999 Bill Nottingham <notting@redhat.com>
- add an adduser in %pre, too

* Thu Mar 25 1999 Bill Nottingham <notting@redhat.com>
- oog. chkconfig must be in %preun, not %postun

* Wed Mar 24 1999 Bill Nottingham <notting@redhat.com>
- switch to using group squid
- turn off icmp (insecure)
- update to 2.2.DEVEL3
- build FAQ docs from source

* Tue Mar 23 1999 Bill Nottingham <notting@redhat.com>
- logrotate changes

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Wed Feb 10 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.PRE2

* Wed Dec 30 1998 Bill Nottingham <notting@redhat.com>
- cache & log dirs shouldn't be world readable
- remove preun script (leave logs & cache @ uninstall)

* Tue Dec 29 1998 Bill Nottingham <notting@redhat.com>
- fix initscript to get cache_dir correct

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- update to 2.1.PATCH2
- merge in some changes from RHCN version

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries
- version 1.1.22

* Sun May 10 1998 Cristian Gafton <gafton@redhat.com>
- don't make packages conflict with each other...

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- added a proxy auth patch from Alex deVries <adevries@engsoc.carleton.ca>
- fixed initscripts

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- rebuilt for Manhattan

* Fri Mar 20 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.1.21/1.NOVM.21

* Mon Mar 02 1998 Cristian Gafton <gafton@redhat.com>
- updated the init script to use reconfigure option to restart squid instead
  of shutdown/restart (both safer and quicker)

* Sat Feb 07 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.1.20
- added the NOVM package and tryied to reduce the mess in the spec file

* Wed Jan 7 1998 Cristian Gafton <gafton@redhat.com>
- first build against glibc
- patched out the use of setresuid(), which is available only on kernels
  2.1.44 and later

