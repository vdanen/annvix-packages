#
# spec file for package httpd-mod_ssl
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		httpd-%{mod_name}
%define version		%{apache_version}
%define release		%_revrel

# Module-Specific definitions
%define apache_version	2.0.55
%define mod_name	mod_ssl
%define mod_conf	40_%{mod_name}.conf
%define mod_so		%{mod_name}.so

Summary:	Strong cryptography using the SSL, TLS and distcache protocols
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://httpd.apache.org
Source1:	README.distcache
Source2: 	mod_ssl-gentestcrt.sh
Source3: 	%{mod_conf}
Source4: 	41_mod_ssl.default-vhost.conf
Source5:	certwatch.tar.bz2
Patch0:		certwatch-avx-annvix.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-devel
BuildRequires:	httpd-devel >= %{apache_version}, httpd-source >= %{apache_version}

Prereq:		rpm-helper
Prereq:		httpd = %{apache_version}, httpd-conf
Provides:	apache2-mod_ssl
Obsoletes:	apache2-mod_ssl

%description
This module provides SSL v2/v3 and TLS v1 support for the Apache
HTTP Server. It was contributed by Ralf S. Engeschall based on
his mod_ssl project and originally derived from work by Ben
Laurie.

This module relies on OpenSSL to provide the cryptography engine.


%prep
%setup -c -T

cp -p %{_prefix}/src/httpd-%{version}/modules/ssl/* .
cp -p %{_prefix}/src/httpd-%{version}/modules/loggers/* .

# fix one obstacle
perl -pi -e "s|../../modules/loggers/||g" ssl_engine_vars.c

tar xjf %{SOURCE5}

%patch0 -p0 -b .avx


%build
%{_sbindir}/apxs -I%{_includedir}/openssl -lssl -lcrypto -lpthread -DHAVE_OPENSSL -DSSL_EXPERIMENTAL_ENGINE \
    -c `cat mod_ssl.txt`

gcc %{optflags} -o certwatch/certwatch -Wall -Werror certwatch/certwatch.c -lcrypto


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/httpd-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
install -m 0755 .libs/mod_ssl.so %{buildroot}%{_libdir}/httpd-extramodules/

install -d %{buildroot}%{_libdir}/ssl/httpd-mod_ssl
cat %{SOURCE2} > %{buildroot}%{_libdir}/ssl/httpd-mod_ssl/gentestcrt.sh

# install module conf files for the "modules.d" dir loading structure
install -d %{buildroot}/%{_sysconfdir}/httpd/modules.d
cat %{SOURCE3} > %{buildroot}/%{_sysconfdir}/httpd/modules.d/%{mod_conf}
cat %{SOURCE4} > %{buildroot}/%{_sysconfdir}/httpd/modules.d/41_mod_ssl.default-vhost.conf

install -d %{buildroot}%{_sysconfdir}/ssl/httpd
cat > %{buildroot}%{_sysconfdir}/ssl/httpd/README.test-certificates <<EOF
Use the %{_libdir}/ssl/httpd-mod_ssl/gentestcrt.sh script to generate your own,
self-signed certificates to replace the localhost server name.
EOF

install -d %{buildroot}/var/cache/httpd

# fix a msec safe cache for the ssl stuff
install -d %{buildroot}/var/cache/httpd/mod_ssl
touch %{buildroot}/var/cache/httpd/mod_ssl/scache.dir
touch %{buildroot}/var/cache/httpd/mod_ssl/scache.pag
touch %{buildroot}/var/cache/httpd/mod_ssl/scache.sem

# install certwatch
mkdir -p %{buildroot}%{_sysconfdir}/cron.daily
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}%{_sbindir}
install -m 0755 certwatch/certwatch %{buildroot}%{_sbindir}/certwatch
install -m 0755 certwatch/certwatch.cron %{buildroot}%{_sysconfdir}/cron.daily/certwatch
install -m 0644 certwatch/certwatch.8 %{buildroot}%{_mandir}/man8/certwatch.8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
if [ $1 = "1" ]; then 
    # Create a self-signed server key and certificate 
    # The script checks first if they exists, if yes, it exits, 
    # otherwise, it creates them.
    if [ -d %{_sysconfdir}/ssl/httpd ];then
        pushd %{_sysconfdir}/ssl/httpd > /dev/null
            yes ""|%{_libdir}/ssl/httpd-mod_ssl/gentestcrt.sh >/dev/null 
        popd > /dev/null
    fi
    %{_datadir}/ADVX/mod_ssl-migrate-20
fi

%create_ghostfile /var/cache/httpd/mod_ssl/scache.dir  apache root 0600
%create_ghostfile /var/cache/httpd/mod_ssl/scache.pag  apache root 0600
%create_ghostfile /var/cache/httpd/mod_ssl/scache.sem  apache root 0600
%_post_srv httpd2

%postun
%_post_srv httpd2


%files
%defattr(-,root,root)
%doc README
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_ssl.conf
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/*_mod_ssl.default-vhost.conf
%dir %{_sysconfdir}/ssl/httpd
%config(noreplace) %{_sysconfdir}/ssl/httpd/README*
%config(noreplace) %{_sysconfdir}/cron.daily/certwatch
%dir %{_libdir}/ssl/httpd-mod_ssl
%attr(0755,root,root) %{_libdir}/ssl/httpd-mod_ssl/gentestcrt.sh
%attr(0755,root,root) %{_sbindir}/certwatch
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_name}.so
%attr(0700,root,root) %dir /var/cache/httpd/mod_ssl
%attr(0600,apache,root) %ghost /var/cache/httpd/mod_ssl/scache.dir
%attr(0600,apache,root) %ghost /var/cache/httpd/mod_ssl/scache.pag
%attr(0600,apache,root) %ghost /var/cache/httpd/mod_ssl/scache.sem
%{_mandir}/man8/certwatch.8*


%changelog
* Wed Mar 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55
- point ssl keys to /etc/ssl/httpd rather than /etc/ssl/apache2 to fix
  bug #22

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55
- rebuild against apr and apr-util 0.9.7 (needed to make mod_cgi.so work
  properly)

* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55
- apache 2.0.55

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54
- Clean rebuild

* Thu Oct 13 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54-3avx
- updated P0: fix the certwatch cron script to look in the right file
  (we no longer use commonhttpd.conf)

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54-2avx
- rebuild to get the fixes for CAN-2005-2700 and CAN-2005-2728

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54-1avx
- apache 2.0.54
- s/conf.d/modules.d/
- s/apache2/httpd/

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-6avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-5avx
- rebuild

* Fri Mar 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-4avx
- remove ADVX macro

* Fri Mar 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-3avx
- update P0 to make certwatch.c accept an extra argument (the email
  address to send to) and make certwatch.cron handle this as well as
  exiting 0 in all cases

* Wed Mar 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-2avx
- P0: fix certwatch script so it doesn't use an initscript to get
  the defines; and s/Mandrakelinux/Annvix
- NOTE: certwatch.c needs to be fixed so that we can pass another
  argument to it, namely the ServerAdmin email address as mailing
  root@localhost is stupid (and bounces with default exim settings
  anyways)

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53-1avx
- apache 2.0.53
- add certwatch
- remove ADVX stuff

* Fri Nov  5 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52-2avx
- rebuild against new apache2 sources to get the mod_ssl fix

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52-1avx
- 2.0.52

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.50-1avx
- first Annvix build for new-style apache2
- migrate keys and certs from /etc/ssl/apache to /etc/ssl/apache2 because
  previous packages used /etc/ssl/apache for mod_ssl and without this, httpd2
  will refuse to start
- own /etc/ssl/apache2

* Thu Sep 09 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50-4mdk
- security fixes for CAN-2004-0748 and CAN-2004-0751

* Tue Aug 10 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50-3mdk
- rebuilt

* Mon Jul 12 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50-2mdk
- remove redundant provides

* Wed Jun 30 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50-1mdk
- 2.0.50

* Wed Jun 23 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.49-12mdk
- initial mandrake package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
