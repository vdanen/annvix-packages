%define name	apache2-%{mod_name}
%define version	%{apache_version}
%define release	2avx

# Module-Specific definitions
%define apache_version	2.0.53
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
Source1:	README.distcache.bz2
Source2: 	mod_ssl-gentestcrt.sh.bz2
Source3: 	%{mod_conf}.bz2
Source4: 	41_mod_ssl.default-vhost.conf.bz2
Source5:	certwatch.tar.bz2
Patch0:		certwatch-avx-annvix.patch

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	openssl-devel
BuildRequires:	apache2-devel >= %{apache_version}, apache2-source >= %{apache_version}

Prereq:		rpm-helper
Prereq:		apache2 = %{apache_version}, apache2-conf

%description
This module provides SSL v2/v3 and TLS v1 support for the Apache
HTTP Server. It was contributed by Ralf S. Engeschall based on
his mod_ssl project and originally derived from work by Ben
Laurie.

This module relies on OpenSSL to provide the cryptography engine.

%prep
%setup -c -T

cp -p %{_prefix}/src/apache2-%{version}/modules/ssl/* .
cp -p %{_prefix}/src/apache2-%{version}/modules/loggers/* .

# fix one obstacle
perl -pi -e "s|../../modules/loggers/||g" ssl_engine_vars.c

tar xjf %{SOURCE5}

%patch0 -p0 -b .avx

%build

%{_sbindir}/apxs2 -I%{_includedir}/openssl -lssl -lcrypto -lpthread -DHAVE_OPENSSL -DSSL_EXPERIMENTAL_ENGINE \
    -c `cat mod_ssl.txt`

gcc %{optflags} -o certwatch/certwatch -Wall -Werror certwatch/certwatch.c -lcrypto

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/apache2-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -m 0755 .libs/mod_ssl.so %{buildroot}%{_libdir}/apache2-extramodules/

install -d %{buildroot}%{_libdir}/ssl/apache2-mod_ssl
bzcat %{SOURCE2} > %{buildroot}%{_libdir}/ssl/apache2-mod_ssl/gentestcrt.sh

# install module conf files for the "conf.d" dir loading structure
install -d %{buildroot}/%{_sysconfdir}/httpd/conf.d
bzcat %{SOURCE3} > %{buildroot}/%{_sysconfdir}/httpd/conf.d/%{mod_conf}
bzcat %{SOURCE4} > %{buildroot}/%{_sysconfdir}/httpd/conf.d/41_mod_ssl.default-vhost.conf

install -d %{buildroot}%{_sysconfdir}/ssl/apache2
cat > %{buildroot}%{_sysconfdir}/ssl/apache2/README.test-certificates <<EOF
Use the %{_libdir}/ssl/apache2-mod_ssl/gentestcrt.sh script to generate your own,
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
    if [ -d %{_sysconfdir}/ssl/apache2 ];then
        pushd %{_sysconfdir}/ssl/apache2 > /dev/null
            yes ""|%{_libdir}/ssl/apache2-mod_ssl/gentestcrt.sh >/dev/null 
        popd > /dev/null
    fi
    %{ADVXdir}/mod_ssl-migrate-20
fi

if [ $1 = "2" ]; then
    # we need this to move keys; this can be removed at a later date, but is required
    # due to keys moving from apache/ to apache2/
    if [ -f %{_sysconfdir}/ssl/apache/server.crt ]; then
	echo "Moving %{_sysconfdir}/ssl/apache/server.crt to %{_sysconfdir}/ssl/apache2..."
        mv %{_sysconfdir}/ssl/apache/server.crt %{_sysconfdir}/ssl/apache2/
    fi
    if [ -f %{_sysconfdir}/ssl/apache/server.key ]; then
	echo "Moving %{_sysconfdir}/ssl/apache/server.key to %{_sysconfdir}/ssl/apache2..."
        mv %{_sysconfdir}/ssl/apache/server.key %{_sysconfdir}/ssl/apache2/
    fi
    # if the directory only contained our files, it should be removed; if someone has put
    # something in there, it should be retained
    rmdir %{_sysconfdir}/ssl/apache >/dev/null 2>&1
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
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/*_mod_ssl.conf
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/*_mod_ssl.default-vhost.conf
%dir %{_sysconfdir}/ssl/apache2
%config(noreplace) %{_sysconfdir}/ssl/apache2/README*
%config(noreplace) %{_sysconfdir}/cron.daily/certwatch
%dir %{_libdir}/ssl/apache2-mod_ssl
%attr(0755,root,root) %{_libdir}/ssl/apache2-mod_ssl/gentestcrt.sh
%attr(0755,root,root) %{_sbindir}/certwatch
%attr(0755,root,root) %{_libdir}/apache2-extramodules/%{mod_name}.so
%attr(0700,root,root) %dir /var/cache/httpd/mod_ssl
%attr(0600,apache,root) %ghost /var/cache/httpd/mod_ssl/scache.dir
%attr(0600,apache,root) %ghost /var/cache/httpd/mod_ssl/scache.pag
%attr(0600,apache,root) %ghost /var/cache/httpd/mod_ssl/scache.sem
%{_mandir}/man8/certwatch.8*

%changelog
* Wed Mar 16 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-2avx
- P0: fix certwatch script so it doesn't use an initscript to get
  the defines; and s/Mandrakelinux/Annvix
- NOTE: certwatch.c needs to be fixed so that we can pass another
  argument to it, namely the ServerAdmin email address as mailing
  root@localhost is stupid (and bounces with default exim settings
  anyways)

* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 2.0.53-1avx
- apache 2.0.53
- add certwatch
- remove ADVX stuff

* Fri Nov  5 2004 Vincent Danen <vdanen@annvix.org> 2.0.52-2avx
- rebuild against new apache2 sources to get the mod_ssl fix

* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.52-1avx
- 2.0.52

* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.50-1avx
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
