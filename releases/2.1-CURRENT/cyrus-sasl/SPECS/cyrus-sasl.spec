#
# spec file for package cyrus-sasl
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		cyrus-sasl
%define version		2.1.22
%define release		%_revrel

%define major		2
%define libname		%mklibname sasl %{major}
%define devname		%mklibname sasl -d
%define sasl2_db_fname	/var/lib/sasl2/sasl.db

Summary:	SASL is the Simple Authentication and Security Layer
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD style
Group:		System/Libraries
URL:		http://asg.web.cmu.edu/cyrus/download/
Source0:	ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/%{name}-%{version}.tar.gz.sig
Source2:        saslauthd.init
Source4:	saslauthd.run
Source5:	saslauthd-log.run
Source6:	saslauthd.8
Source7:	service.conf.example
Source8:	SASLAUTHD_OPTS.env
Source9:	SASL_AUTHMECH.env
Source10:	SASL_MECH_OPTIONS.env
Patch0:		cyrus-sasl-2.1.22-avx-doc.patch
Patch1:		cyrus-sasl-2.1.19-mdk-no_rpath.patch
Patch2:		cyrus-sasl-2.1.15-mdk-lib64.patch
Patch3:		cyrus-sasl-2.1.20-fdr-gssapi-dynamic.patch
Patch4:		cyrus-sasl-2.1.19-mdk-pic.patch
Patch6:		cyrus-sasl-2.1.22-mdk-sed_syntax.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  autoconf
BuildRequires:	automake1.7
BuildRequires:	db4-devel
BuildRequires:	pam-devel
BuildRequires:	krb5-devel
BuildRequires:  openssl-devel >= 0.9.6a
BuildRequires:	libtool >= 1.4
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	openldap-devel

Requires:	%{libname} = %{version}
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description
SASL is the Simple Authentication and Security Layer, 
a method for adding authentication support to connection-based protocols. 
To use SASL, a protocol includes a command for identifying and authenticating 
a user to a server and for optionally negotiating protection of subsequent 
protocol interactions. If its use is negotiated, a security layer is inserted 
between the protocol and the connection. 


%package -n %{libname}
Summary:	Libraries for SASL a the Simple Authentication and Security Layer
Group:		System/Libraries
Provides:	libsasl = %{version}-%{release}

%description -n %{libname}
SASL is the Simple Authentication and Security Layer, 
a method for adding authentication support to connection-based protocols. 
To use SASL, a protocol includes a command for identifying and authenticating 
a user to a server and for optionally negotiating protection of subsequent 
protocol interactions. If its use is negotiated, a security layer is inserted 
between the protocol and the connection. 


%package -n %{devname}
Summary:	Libraries for SASL a the Simple Authentication and Security Layer
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libsasl-devel = %{version}-%{release}
Obsoletes:	%mklibname sasl 2 -d

%description -n %{devname}
SASL is the Simple Authentication and Security Layer, 
a method for adding authentication support to connection-based protocols. 
To use SASL, a protocol includes a command for identifying and authenticating 
a user to a server and for optionally negotiating protection of subsequent 
protocol interactions. If its use is negotiated, a security layer is inserted 
between the protocol and the connection. 


%package -n %{libname}-plug-anonymous
Summary:	SASL ANONYMOUS mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-anonymous = %{version}-%{release}

%description -n %{libname}-plug-anonymous
This plugin implements the SASL ANONYMOUS mechanism,
used for anonymous authentication.


%package -n %{libname}-plug-crammd5
Summary:	SASL CRAM-MD5 mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-crammd5 = %{version}-%{release}

%description -n %{libname}-plug-crammd5
This plugin implements the SASL CRAM-MD5 mechanism.
CRAM-MD5 is the mandatory-to-implement authentication mechanism for a
number of protocols; it uses MD5 with a challenge/response system to
authenticate the user.


%package -n %{libname}-plug-digestmd5
Summary:	SASL DIGEST-MD5 mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-digestmd5 = %{version}-%{release}

%description -n %{libname}-plug-digestmd5
This plugin implements the latest draft of the SASL DIGEST-MD5
mechanism.  Although not yet finalized, this is likely to become the
new mandatory-to-implement authentication system in all new protocols.
It's based on the digest md5 authentication system designed for HTTP.


%package -n %{libname}-plug-plain
Summary:	SASL PLAIN mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-plain = %{version}-%{release}

%description -n %{libname}-plug-plain
This plugin implements the SASL PLAIN mechanism.  Although insecure,
PLAIN is useful for transitioning to new security mechanisms, as this
is the only mechanism which gives the server a copy of the user's
password.


%package -n %{libname}-plug-scrammd5
Summary:	SASL SCRAM-MD5 mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-scrammd5 = %{version}-%{release}

%description -n %{libname}-plug-scrammd5
This plugin implements the SASL SCRAM-MD5 mechanism.  Although
deprecated (this will be replaced by DIGEST-MD5 at some point), it may
be useful for the time being.


%package -n %{libname}-plug-login
Summary:	SASL LOGIN mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-login = %{version}-%{release}

%description -n %{libname}-plug-login
This plugin implements the SASL LOGIN mechanism.
THIS PLUGIN IS DEPRECATED, is maintained only for compatibility reasons 
and will be dropped soon.
Please use the plain plugin instead.


%package -n %{libname}-plug-gssapi
Summary:	SASL GSSAPI mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Requires:	krb5-libs
Provides:	sasl-plug-gssapi = %{version}-%{release}
 
%description -n %{libname}-plug-gssapi
This plugin implements the SASL GSSAPI (kerberos 5)mechanism.


%package -n %{libname}-plug-otp
Summary:	SASL OTP mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-otp = %{version}-%{release}

%description -n %{libname}-plug-otp
This plugin implements the SASL OTP mechanism.


%package -n %{libname}-plug-sasldb
Summary:	SASL sasldb mechanism plugin
Group:		System/Libraries
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires:	%{libname} = %{version}
Requires:	%{name} = %{version}
Provides:	sasl-plug-sasldb = %{version}-%{release}

%description -n %{libname}-plug-sasldb
This plugin implements the SASL sasldb mechanism.


%package -n %{libname}-plug-ntlm
Summary:	SASL ntlm authentication plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-ntlm = %{version}-%{release}

%description -n %{libname}-plug-ntlm
This plugin implements the (unsupported) ntlm authentication.


%package -n %{libname}-plug-sql
Summary:	SASL sql auxprop plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-sql = %{version}-%{release}

%description -n %{libname}-plug-sql
This plugin implements the SQL auxprop authentication method
supporting MySQL and PostgreSQL.


%package -n %{libname}-plug-ldapdb
Summary:	SASL ldapdb auxprop plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-ldapdb = %{version}-%{release}

%description -n %{libname}-plug-ldapdb
This plugin implements the LDAP auxprop authentication method.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .sasldoc
%patch1 -p1 -b .rpath
%patch2 -p1 -b .lib64
#%patch3 -p1 -b .gssapi
%patch4 -p1 -b .pic
%patch6 -p0 -b .sed_syntax

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure.in

rm -f config/ltconfig config/libtool.m4
libtoolize -f -c
aclocal-1.7 -I config -I cmulocal
automake-1.7 -a -c -f
autoheader
autoconf -f
pushd saslauthd
    rm -f config/ltconfig
    libtoolize -f -c
    aclocal-1.7 -I ../config -I ../cmulocal
    automake-1.7 -a -c -f
    autoheader
    autoconf -f
popd


%build
%serverbuild
# (bluca) trim spaces into CFLAGS or configure will whine
%ifarch x86_64
CFLAGS="$CFLAGS -fPIC"
%endif
export CFLAGS=`echo ${CFLAGS} | sed -e 's/  */ /'`

export LDFLAGS="-L%{_libdir}"

%{?__cputoolize: %{__cputoolize} -c saslauthd}
%configure \
    --enable-static \
    --enable-shared \
    --with-plugindir=%{_libdir}/sasl2 \
    --with-configdir=%{_sysconfdir}/sasl2:%{_libdir}/sasl2 \
    --disable-krb4 \
    --enable-login \
    --enable-db4 \
    --enable-sql \
    --with-mysql=%{_prefix} \
    --with-pgsql=%{_prefix} \
    --with-gssapi \
    --disable-gss_mutexes \
    --without-sqlite \
    --without-srp --without-srp-setpass \
    --enable-ntlm \
    --with-ldap=%{_prefix} \
    --enable-ldapdb \
    --with-dbpath=%{sasl2_db_fname} \
    --with-saslauthd=/var/lib/sasl2 \
    --with-authdaemond=/var/run/authdaemon.courier-imap/socket

# ugly hack: there is an ordering problem introduced in 2.1.21 
# when --enable-static is given to ./configure which calling 
# make twice "solves"
%make || :
make -C saslauthd testsaslauthd
make -C sample

install saslauthd/LDAP_SASLAUTHD README.ldap


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/var/lib/sasl2
mkdir -p %{buildroot}%{_sysconfdir}/sasl2

make install DESTDIR=%{buildroot}

install -m 0644 %{_sourcedir}/service.conf.example %{buildroot}%{_sysconfdir}/sasl2/
# Install man pages in the expected location, even if they are
# pre-formatted.
install -m 0755 -d %{buildroot}%{_mandir}/man8/
install -m 0644 */*.8 %{buildroot}%{_mandir}/man8/

%makeinstall_std

# we don't need these
rm -f %{buildroot}%{_libdir}/sasl2/*.a

# dbconverter-2 isn't installed by make install

pushd utils
    /bin/sh ../libtool --mode=install /usr/bin/install -c dbconverter-2 \
        %{buildroot}/%{_sbindir}/dbconverter-2
popd
cp saslauthd/testsaslauthd %{buildroot}%{_sbindir}

mkdir -p %{buildroot}%{_srvdir}/saslauthd/{env,log}
install -m 0740 %{_sourcedir}/saslauthd.run %{buildroot}%{_srvdir}/saslauthd/run
install -m 0740 %{_sourcedir}/saslauthd-log.run %{buildroot}%{_srvdir}/saslauthd/log/run
install -m 0640 %{_sourcedir}/SASLAUTHD_OPTS.env %{buildroot}%{_srvdir}/saslauthd/env/SASLAUTHD_OPTS
install -m 0640 %{_sourcedir}/SASL_AUTHMECH.env %{buildroot}%{_srvdir}/saslauthd/env/SASL_AUTHMECH
install -m 0640 %{_sourcedir}/SASL_MECH_OPTIONS.env %{buildroot}%{_srvdir}/saslauthd/env/SASL_MECH_OPTIONS

# fix the horribly broken manpage
cp %{_sourcedir}/saslauthd.8 %{buildroot}%{_mandir}/man8/saslauthd.8

pushd sample
    /bin/sh ../libtool --mode=install /usr/bin/install -c client \
        %{buildroot}%{_sbindir}/sasl-sample-client
    /bin/sh ../libtool --mode=install /usr/bin/install -c server \
        %{buildroot}%{_sbindir}/sasl-sample-server
popd

# multiarch policy
%multiarch_includes %{buildroot}%{_includedir}/sasl/md5global.h

# quick README about the sasl.db file permissions
cat > README.Annvix.sasldb <<EOF
Starting with %{libname}-plug-sasldb-2.1.22-1avx, Annvix by default 
creates a system group called "sasl" and installs an empty 
%{sasl2_db_filename} file with the following permissions:
mode 0640, ownership root:sasl.

If the %{sasl2_db_filename} file already exists, it is not changed
in any way.

It is recommended that administrators keep these permissions and add
application users to the "sasl" group if access to this database is needed.

For example, to permit the Postfix SMTP to authenticate users via the sasldb
auxprop plugin, add the "postfix" user to the "sasl" group and read the
"SMTP Authentication" section of the README.AVX documentation file for 
details regarding Postfix's chroot setup.

For other applications in general, just add their user to the "sasl" group.
EOF

rm -rf %{buildroot}%{_mandir}/cat8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre -n %{libname}-plug-sasldb
%_pre_groupadd sasl 90


%post -n %{libname}-plug-sasldb
#convert old sasldb
# XXX - what about berkeley db versions? - andreas
if [ -f /var/lib/sasl/sasl.db -a ! -f %{sasl2_db_fname} ]; then
    echo "" | /usr/sbin/dbconverter-2 /var/lib/sasl/sasl.db %{sasl2_db_fname}
    if [ -f %{sasl2_db_fname} ]; then
        # conversion was successfull
        chmod 0640 %{sasl2_db_fname}
        chown root:sasl %{sasl2_db_fname}
    fi
fi
if [ -f /var/lib/sasl/sasl.db.rpmsave -a ! -f %{sasl2_db_fname} ]; then
    echo "" | /usr/sbin/dbconverter-2 /var/lib/sasl/sasl.db.rpmsave %{sasl2_db_fname}
    if [ -f %{sasl2_db_fname} ]; then
        # conversion was successfull
        chmod 0640 %{sasl2_db_fname}
        chown root:sasl %{sasl2_db_fname}
    fi
fi
if [ ! -f %{sasl2_db_fname} ]; then
    # the file was never created before nor converted from sasl1
    touch %{sasl2_db_fname}
    chmod 0640 %{sasl2_db_fname}
    chown root:sasl %{sasl2_db_fname}
fi


%post
%_post_srv saslauthd


%preun
%_preun_srv saslauthd


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%dir %{_sysconfdir}/sasl2
%{_sysconfdir}/sasl2/service.conf.example
%dir /var/lib/sasl2
%dir %attr(0750,root,admin) %{_srvdir}/saslauthd
%dir %attr(0750,root,admin) %{_srvdir}/saslauthd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/saslauthd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/saslauthd/log/run
%config(noreplace) %attr(0640,root,admin)%{_srvdir}/saslauthd/env/SASLAUTHD_OPTS
%config(noreplace) %attr(0640,root,admin)%{_srvdir}/saslauthd/env/SASL_AUTHMECH
%config(noreplace) %attr(0640,root,admin)%{_srvdir}/saslauthd/env/SASL_MECH_OPTIONS
%{_sbindir}/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
%dir %{_libdir}/sasl2
%{_libdir}/libsasl*.so.*

%files -n %{libname}-plug-anonymous
%defattr(-,root,root)
%{_libdir}/sasl2/libanonymous*.so*
%{_libdir}/sasl2/libanonymous*.la

%files -n %{libname}-plug-otp
%defattr(-,root,root)
%{_libdir}/sasl2/libotp*.so*
%{_libdir}/sasl2/libotp*.la

%files -n %{libname}-plug-sasldb
%defattr(-,root,root)
%{_libdir}/sasl2/libsasldb*.so*
%{_libdir}/sasl2/libsasldb*.la

%files -n %{libname}-plug-gssapi
%defattr(-,root,root)
%{_libdir}/sasl2/libgssapi*.so*
%{_libdir}/sasl2/libgssapi*.la

%files -n %{libname}-plug-crammd5
%defattr(-,root,root)
%{_libdir}/sasl2/libcrammd5*.so*
%{_libdir}/sasl2/libcrammd5*.la

%files -n %{libname}-plug-digestmd5
%defattr(-,root,root)
%{_libdir}/sasl2/libdigestmd5*.so*
%{_libdir}/sasl2/libdigestmd5*.la

%files -n %{libname}-plug-plain
%defattr(-,root,root)
%{_libdir}/sasl2/libplain*.so*
%{_libdir}/sasl2/libplain*.la

%files -n %{libname}-plug-login
%defattr(-,root,root)
%{_libdir}/sasl2/liblogin*.so*
%{_libdir}/sasl2/liblogin*.la

%files -n %{libname}-plug-ntlm
%defattr(-,root,root)
%{_libdir}/sasl2/libntlm*.so*
%{_libdir}/sasl2/libntlm*.la

%files -n %{libname}-plug-sql
%defattr(-,root,root)
%{_libdir}/sasl2/libsql*.so*
%{_libdir}/sasl2/libsql*.la

%files -n %{libname}-plug-ldapdb
%defattr(-,root,root)
%{_libdir}/sasl2/libldap*.so*
%{_libdir}/sasl2/libldap*.la

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.*so
%{_libdir}/*.*a
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc COPYING AUTHORS INSTALL NEWS README* ChangeLog
%doc doc/{TODO,ONEWS,*.txt,*.html}

 
%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- rebuild against new mysql
- enable GSSAPI support
- go back to automake1.7, as it doesn't build properly with automake1.8

* Sat Sep 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- rebuild against new postgresql, pam, openldap
- /etc/sasl2 should be in the main package, not the libs
- environment files shouldn't be executable

* Tue Jul 24 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- rebuild against new mysql
- implement devel naming policy
- implement library provides policy
- verioned provides

* Fri Jan 29 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- rebuild against new postgresql

* Fri Dec 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- rebuild against new pam

* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- rebuild against new krb5

* Sat Dec 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- rebuild against new openldap, mysql, postgresql
- get rid of static plugin files
- add sample file for service configuration
- use environment directory instead of sysconfig file

* Sun Aug 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- rebuild against new mysql
- rebuild against new openssl
- rebuild against new openldap 
- spec cleanups

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- really add -doc subpackage

* Fri Jun 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- rebuild against new db4

* Wed Jun 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- the real 2.1.22 (which I don't get, but ok...)
- remove SRP support due to patent tainting (re:
  http://www.ietf.org/ietf/IPR/PHOENIX-SRP-RFC2945.txt )
- drop P5; no longer needed
- use /etc/sasl2 for the configuration dir with a fallback to /usr/lib/sasl2
- re-enable the ntlm plugin; it compiles now
- rebuild against new pam
- add -doc subpackage
- rebuild with gcc4

* Wed Feb  1 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- build against new postgresql

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22-4avx
- fix typeo in summary

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22-3avx
- use execlineb for run scripts
- move logdir to /var/log/service/saslauthd
- run scripts are now considered config files and are not replaceable
- P5: make it acknowledge openldap 2.3.6 (oden)
- P6: fix the sed syntax (andreas)

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22-2avx
- fix perms on run scripts

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.22-1avx
- 2.1.22
- add ldapdb plugin
- BuildReq always on openldap-devel now
- create sasl system group and empty sasl.db (mode 0640; root:sasl)
  and a README.Annvix.sasldb explaining it (andreas)
- moved sasldb conversion to the sasldb plugin package (andreas)
- add provides for plugins (andreas)
- disable the srp plugin; for some reason it doesn't play too nice
  with openssl 0.9.8

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.20-2avx
- bootstrap build

* Tue Mar 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.20-1avx
- 2.1.20
- rediff P0, P3
- drop P4; merged upstream

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.19-4avx
- multiarch
- use automake1.8 (bluca)
- added the sql plugin and build for mysql/postgres by default
- added courier authdaemon support (bluca)
- own %%{_libdir}/sasl2
- provide libsasl2-devel and lib64sasl2-devel on biarches (bluca)
- use logger for logging

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.19-3avx
- rebuild against new openssl

* Thu Oct 07 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.19-2avx
- P4: fixes CAN-2004-0884

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.19-1avx
- 2.1.19
- drop %%{_prefix}
- patch policy
- sync with Mandrake 2.1.19-3mdk:
  - add testsaslauthd (jmdault)
  - add missing plugin files (jmdault)
  - reworked P1 and added P3 from fedora (bluca)
  - recreate autoconf stuff in prep (bluca)
  - really install sample client and server (bluca)
  - remove obsoletes on myself and fix library require (bluca)

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.15-10avx
- update run scripts

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.15-9avx
- rebuild against latest openssl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.1.15-8avx
- Annvix build

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 2.1.15-7sls
- minor spec cleanups

* Tue Feb 03 2004 Vincent Danen <vdanen@opensls.org> 2.1.15-6sls
- supervise scripts
- remove initscript
- fix the saslauthd.8 manpage (a patch would be bigger than the file so
  include it as S6)

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 2.1.15-5sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
