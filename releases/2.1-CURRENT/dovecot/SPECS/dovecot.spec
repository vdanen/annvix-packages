#
# spec file for package dovecot
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		dovecot
%define version		1.0.1
%define release		%_revrel
	

Summary:	Secure IMAP and POP3 server
Name: 		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://dovecot.org
Source0:	http://dovecot.org/releases/%{name}-%{version}.tar.gz
Source1:	dovecot-pamd
Source2:	dovecot.run
Source3:	dovecot-log.run
Source4:	http://dovecot.org/tools/migration_wuimp_to_dovecot.pl
Source5:	http://dovecot.org/tools/mboxcrypt.pl
Patch0:		dovecot-1.0.1-avx-config.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	pam-devel
BuildRequires:	openssl-devel
BuildRequires:	openldap-devel
BuildRequires:	libsasl-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel

Provides:	imap-server
Provides:	pop3-server
Provides:	imaps-server
Provides:	pop3s-server
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun): rpm-helper
Requires(postun): rpm-helper


%description 
Dovecot is an IMAP and POP3 server for Linux/UNIX-like systems,
written with security primarily in mind. Although it's written with C,
it uses several coding techniques to avoid most of the common
pitfalls.

Dovecot can work with standard mbox and maildir formats and it's fully
compatible with UW-IMAP and Courier IMAP servers as well as mail
clients accessing the mailboxes directly.


%package devel
Summary:	Devel files for Dovecot IMAP and POP3 server
Group: 		System/Servers

%description devel
Dovecot is an IMAP and POP3 server for Linux/UNIX-like systems,
written with security primarily in mind. Although it's written with C,
it uses several coding techniques to avoid most of the common
pitfalls.

Dovecot can work with standard mbox and maildir formats and it's fully
compatible with UW-IMAP and Courier IMAP servers as well as mail
clients accessing the mailboxes directly.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p0 -b .avx_config


%build
%configure \
    --with-ssl=openssl \
    --sysconfdir=%{_sysconfdir}/dovecot \
    --with-ssldir="%{_sysconfdir}/ssl/%{name}" \
    --with-moduledir="%{_datadir}/%{name}/" \
    --with-ldap \
    --with-sql \
    --with-pgsql \
    --with-mysql \
    --with-cyrus-sasl2

%make

perl -pi -e 's|/var/run/dovecot|/var/lib/dovecot|g' dovecot-example.conf


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/%{name}
%makeinstall_std

mkdir -p %{buildroot}{%{_sysconfdir}/{pam.d,dovecot},%{_var}/%{_lib}/%{name}}

cp %{_sourcedir}/dovecot-pamd  %{buildroot}%{_sysconfdir}/pam.d/dovecot
mv %{buildroot}%{_sysconfdir}/dovecot/dovecot-example.conf %{buildroot}%{_sysconfdir}/dovecot/dovecot.conf
cp doc/*.conf %{buildroot}%{_sysconfdir}/dovecot/
cp %{_sourcedir}/migration_wuimp_to_dovecot.pl .
cp %{_sourcedir}/mboxcrypt.pl . 

mkdir -p %{buildroot}%{_srvdir}/dovecot/log
install -m 0740 %{_sourcedir}/dovecot.run %{buildroot}%{_srvdir}/dovecot/run
install -m 0740 %{_sourcedir}/dovecot-log.run %{buildroot}%{_srvdir}/dovecot/log/run
# dovecot-devel files
install -m 0644 dovecot-config %{buildroot}%{_includedir}/%{name}
install -m 0644 config.h %{buildroot}%{_includedir}/%{name}
install -m 0644 stamp.h %{buildroot}%{_includedir}/%{name}
# lib include files
for folder in deliver imap lib lib-auth lib-charset lib-dict lib-imap lib-index lib-mail lib-ntlm lib-settings lib-sql lib-storage; do
    mkdir -p %{buildroot}%{_includedir}/%{name}/$folder
    install -m 0644 src/$folder/*.h %{buildroot}%{_includedir}/%{name}/$folder/
done
# lib files
for folder in lib lib-auth lib-charset lib-dict lib-imap lib-index lib-mail lib-ntlm lib-settings lib-sql lib-storage; do
    mkdir -p %{buildroot}%{_datadir}/%{name}/$folder
    install -p -m644 src/$folder/*.a %{buildroot}%{_datadir}/%{name}/$folder/
done


# generate ghost .pem file
mkdir -p %{buildroot}%{_sysconfdir}/ssl/dovecot/{certs,private}
# Clean up buildroot
rm -rf %{buildroot}%{_datadir}/doc/dovecot/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
%_pre_useradd dovecot %{_var}/%{_lib}/%{name} /bin/false 93
%_pre_groupadd dovecot dovecot


%post
%_post_srv dovecot

# TODO
# move this somewhere else, because these commands is "dangerous" as rpmlint say
#
# create a ssl cert
if [ ! -f %{_sysconfdir}/ssl/dovecot/certs/dovecot.pem ]; then
pushd %{_sysconfdir}/ssl/dovecot &>/dev/null
umask 077
cat << EOF | openssl req -new -x509 -days 365 -nodes -out certs/dovecot.pem -keyout private/dovecot.pem &>/dev/null
--
SomeState
SomeCity
SomeOrganization
SomeOrganizationalUnit
localhost.localdomain
root@localhost.localdomain
EOF
chown root:root private/dovecot.pem certs/dovecot.pem
chmod 0600 private/dovecot.pem certs/dovecot.pem
popd &>/dev/null
fi
exit 0


%preun
%_preun_srv dovecot


%postun
%_postun_userdel dovecot
%_postun_groupdel dovecot


%files
%defattr(-,root,root)
%dir %{_sysconfdir}/ssl/%{name}
%dir %{_sysconfdir}/ssl/%{name}/certs
%attr(0600,root,root) %dir %{_sysconfdir}/ssl/%{name}/private
%dir %{_sysconfdir}/dovecot
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*
%{_sbindir}/*
%attr(0700,root,root) %dir %{_var}/%{_lib}/%{name}
%config(noreplace) %{_sysconfdir}/dovecot/*.conf
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.la
%{_datadir}/%{name}/*.so
%{_datadir}/%{name}/pop3/*.so
%{_datadir}/%{name}/lda/*.so
%{_datadir}/%{name}/imap/*.so
%{_datadir}/%{name}/imap/*.la
%dir %attr(0750,root,admin) %{_srvdir}/dovecot   
%dir %attr(0750,root,admin) %{_srvdir}/dovecot/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/dovecot/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/dovecot/log/run

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/dovecot-config
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/deliver/*.h
%{_includedir}/%{name}/imap/*.h
%{_includedir}/%{name}/lib/*.h
%{_includedir}/%{name}/lib-auth/*.h
%{_includedir}/%{name}/lib-charset/*.h
%{_includedir}/%{name}/lib-dict/*.h
%{_includedir}/%{name}/lib-imap/*.h
%{_includedir}/%{name}/lib-index/*.h
%{_includedir}/%{name}/lib-mail/*.h
%{_includedir}/%{name}/lib-ntlm/*.h
%{_includedir}/%{name}/lib-settings/*.h
%{_includedir}/%{name}/lib-sql/*.h
%{_includedir}/%{name}/lib-storage/*.h
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.a
%{_datadir}/%{name}/lib/*.a
%{_datadir}/%{name}/imap/*.a
%{_datadir}/%{name}/lib-auth/*.a
%{_datadir}/%{name}/lib-charset/*.a
%{_datadir}/%{name}/lib-dict/*.a
%{_datadir}/%{name}/lib-imap/*.a
%{_datadir}/%{name}/lib-index/*.a
%{_datadir}/%{name}/lib-mail/*.a
%{_datadir}/%{name}/lib-ntlm/*.a
%{_datadir}/%{name}/lib-settings/*.a
%{_datadir}/%{name}/lib-sql/*.a
%{_datadir}/%{name}/lib-storage/*.a

%files doc
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING* NEWS README TODO
%doc doc/*.sh doc/*.txt doc/*.cnf
%doc mboxcrypt.pl migration_wuimp_to_dovecot.pl


%changelog
* Thu Jun 28 2007 Lauris Bukðis-Haberkorns <lafriks-at-gmail.com> 1.0.1
- 1.0.1
- Add include files to devel package

* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org>  1.0
- set the uid/gid to 93
- P0: patch the config to set some paths
- copy some sample configs to /etc/dovecot/
- put dovecot.conf in /etc/dovecot/

* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org>  1.0
- rebuild against new postgresql

* Sat Jan 13 2007 Vincent Danen <vdanen-at-build.annvix.org>  1.0
- 1.0-rc17

* Fri Dec 28 2006 Vincent Danen <vdanen-at-build.annvix.org>  1.0
- rebuild against new pam

* Mon Dec 25 2006 Vincent Danen <vdanen-at-build.annvix.org>  1.0
- first Annvix build (1.0-rc15)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
