%define name	%{ap_name}-%{mod_name}
%define version	%{ap_version}
%define release	1avx

# New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}
%{expand:%%global ap_version %(%{apxs} -q ap_version)}

# Module-Specific definitions
%define mod_name	mod_ssl
%define mod_conf	40_%{mod_name}.conf
%define mod_so		%{mod_name}.so

Summary:	Strong cryptography using the SSL, TLS and distcache protocols
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.advx.org
Source1:	README.distcache.bz2
Source2: 	gentestcrt.sh.bz2
Source3: 	%{mod_conf}.bz2
Source4: 	41_mod_ssl.default-vhost.conf.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	openssl-devel
# Standard ADVX requires
BuildRequires:	ADVX-build >= 10
BuildRequires:	%{ap_name}-devel >= 2.0.50-1avx
BuildRequires:	%{ap_name}-source >= 2.0.50-1avx

Prereq:		rpm-helper
# Standard ADVX requires
Prereq:		%{ap_name} = %{ap_version}
Prereq:		%{ap_name}-conf

%description
This module provides SSL v2/v3 and TLS v1 support for the Apache
HTTP Server. It was contributed by Ralf S. Engeschall based on
his mod_ssl project and originally derived from work by Ben
Laurie.

This module relies on OpenSSL to provide the cryptography engine.

%prep

%build

# Use the source Luke
[ "./%{mod_name}-%{mod_version}" != "/" ] && rm -rf ./%{mod_name}-%{mod_version}
mkdir -p %{mod_name}-%{mod_version}
cp -p %{ap_abs_srcdir}/modules/ssl/* %{mod_name}-%{mod_version}/
cp -p %{ap_abs_srcdir}/modules/loggers/* %{mod_name}-%{mod_version}/

# fix one obsticle
perl -pi -e "s|../../modules/loggers/||g" %{mod_name}-%{mod_version}/ssl_engine_vars.c

pushd %{mod_name}-%{mod_version}
%{apxs} -I%{_includedir}/openssl -lssl -lcrypto -lpthread -DHAVE_OPENSSL -DSSL_EXPERIMENTAL_ENGINE \
    -c `cat mod_ssl.txt`
popd

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

pushd %{mod_name}-%{mod_version}
    install -d %{buildroot}%{ap_extralibs}
    install -m0755 .libs/mod_ssl.so %{buildroot}%{ap_extralibs}/

    install -d %{buildroot}%{ap_ssldir}
    bzcat %{SOURCE2} > %{buildroot}%{ap_ssldir}/gentestcrt.sh

    # install module conf files for the "conf.d" dir loading structure
    install -d %{buildroot}/%{ap_confd}
    bzcat %{SOURCE3} > %{buildroot}/%{ap_confd}/%{mod_conf}
    bzcat %{SOURCE4} > %{buildroot}/%{ap_confd}/41_mod_ssl.default-vhost.conf

    install -d %{buildroot}%{ap_sslconf}
    cat > %{buildroot}%{ap_sslconf}/README.test-certificates <<EOF
    Use the %{ap_ssldir}/gentestcrt.sh script to generate your own,
    self-signed certificates to replace the localhost server name.
EOF

    install -d %{buildroot}%{ap_proxycachedir}

    # fix a msec safe cache for the ssl stuff
    install -d %{buildroot}%{ap_proxycachedir}/mod_ssl
    touch %{buildroot}%{ap_proxycachedir}/mod_ssl/scache.dir
    touch %{buildroot}%{ap_proxycachedir}/mod_ssl/scache.pag
    touch %{buildroot}%{ap_proxycachedir}/mod_ssl/scache.sem
popd

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
[ "./%{mod_name}-%{mod_version}" != "/" ] && rm -rf ./%{mod_name}-%{mod_version}


%post
if [ $1 = "1" ]; then 
    # Create a self-signed server key and certificate 
    # The script checks first if they exists, if yes, it exits, 
    # otherwise, it creates them.
    if [ -d %{ap_sslconf} ];then
        pushd %{ap_sslconf} > /dev/null
            yes ""|%{ap_ssldir}/gentestcrt.sh >/dev/null 
        popd > /dev/null
    fi
    %{ADVXdir}/mod_ssl-migrate-20
fi

if [ $1 = "2" ]; then
    # we need this to move keys; this can be removed at a later date, but is required
    # due to keys moving from apache/ to apache2/
    if [ -f %{_sysconfdir}/ssl/apache/server.crt ]; then
	echo "Moving %{_sysconfdir}/ssl/apache/server.crt to %{ap_sslconf}..."
        mv %{_sysconfdir}/ssl/apache/server.crt %{ap_sslconf}/
    fi
    if [ -f %{_sysconfdir}/ssl/apache/server.key ]; then
	echo "Moving %{_sysconfdir}/ssl/apache/server.key to %{ap_sslconf}..."
        mv %{_sysconfdir}/ssl/apache/server.key %{ap_sslconf}/
    fi
    # if the directory only contained our files, it should be removed; if someone has put
    # something in there, it should be retained
    rmdir %{_sysconfdir}/ssl/apache >/dev/null 2>&1
fi

%create_ghostfile %{ap_proxycachedir}/mod_ssl/scache.dir  apache root 0600
%create_ghostfile %{ap_proxycachedir}/mod_ssl/scache.pag  apache root 0600
%create_ghostfile %{ap_proxycachedir}/mod_ssl/scache.sem  apache root 0600
%_post_srv httpd2

%postun
%_post_srv httpd2

%files
%defattr(-,root,root)
%doc %{mod_name}-%{mod_version}/README
%{ap_extralibs}/mod_ssl.so
%attr(0640,root,root) %config(noreplace) %{ap_confd}/*_mod_ssl.conf
%attr(0640,root,root) %config(noreplace) %{ap_confd}/*_mod_ssl.default-vhost.conf
%dir %{ap_sslconf}
%config(noreplace) %{ap_sslconf}/README*
%dir %{ap_ssldir}
%attr(0755,root,root) %{ap_ssldir}/gentestcrt.sh
%attr(0700,root,root) %dir %{ap_proxycachedir}/mod_ssl
%attr(0600,apache,root) %ghost %{ap_proxycachedir}/mod_ssl/scache.dir
%attr(0600,apache,root) %ghost %{ap_proxycachedir}/mod_ssl/scache.pag
%attr(0600,apache,root) %ghost %{ap_proxycachedir}/mod_ssl/scache.sem

%changelog
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
