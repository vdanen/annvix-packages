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
Source3:        saslauthd.sysconfig
Source4:	saslauthd.run
Source5:	saslauthd-log.run
Source6:	saslauthd.8
Patch0:		cyrus-sasl-2.1.20-avx-doc.patch
Patch1:		cyrus-sasl-2.1.19-mdk-no_rpath.patch
Patch2:		cyrus-sasl-2.1.15-mdk-lib64.patch
Patch3:		cyrus-sasl-2.1.20-fdr-gssapi-dynamic.patch
Patch4:		cyrus-sasl-2.1.19-mdk-pic.patch
Patch5:		cyrus-sasl-2.1.22-mdk-openldap-2.3.0.diff
Patch6:		cyrus-sasl-2.1.22-mdk-sed_syntax.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  autoconf, automake1.8, db4-devel, pam-devel, krb5-devel
BuildRequires:  openssl-devel >= 0.9.6a, libtool >= 1.4
BuildRequires:	MySQL-devel, postgresql-devel, openldap-devel

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

%description -n %{libname}
SASL is the Simple Authentication and Security Layer, 
a method for adding authentication support to connection-based protocols. 
To use SASL, a protocol includes a command for identifying and authenticating 
a user to a server and for optionally negotiating protection of subsequent 
protocol interactions. If its use is negotiated, a security layer is inserted 
between the protocol and the connection. 


%package -n %{libname}-devel
Summary:	Libraries for SASL a the Simple Authentication and Security Layer
Group:		Development/C
%if %{_lib} != lib
Provides:	libsasl-devel = %{version}
Provides:	libsasl2-devel = %{version}
%endif
Provides:	%{mklibname -d sasl} = %{version}
Requires:	%{libname} = %{version}

%description -n %{libname}-devel
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
Provides:	sasl-plug-anonymous

%description -n %{libname}-plug-anonymous
This plugin implements the SASL ANONYMOUS mechanism,
used for anonymous authentication.


%package -n %{libname}-plug-crammd5
Summary:	SASL CRAM-MD5 mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-crammd5

%description -n %{libname}-plug-crammd5
This plugin implements the SASL CRAM-MD5 mechanism.
CRAM-MD5 is the mandatory-to-implement authentication mechanism for a
number of protocols; it uses MD5 with a challenge/response system to
authenticate the user.


%package -n %{libname}-plug-digestmd5
Summary:	SASL DIGEST-MD5 mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-digestmd5

%description -n %{libname}-plug-digestmd5
This plugin implements the latest draft of the SASL DIGEST-MD5
mechanism.  Although not yet finalized, this is likely to become the
new mandatory-to-implement authentication system in all new protocols.
It's based on the digest md5 authentication system designed for HTTP.


%package -n %{libname}-plug-plain
Summary:	SASL PLAIN mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-plain

%description -n %{libname}-plug-plain
This plugin implements the SASL PLAIN mechanism.  Although insecure,
PLAIN is useful for transitioning to new security mechanisms, as this
is the only mechanism which gives the server a copy of the user's
password.


%package -n %{libname}-plug-scrammd5
Summary:	SASL SCRAM-MD5 mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-scrammd5

%description -n %{libname}-plug-scrammd5
This plugin implements the SASL SCRAM-MD5 mechanism.  Although
deprecated (this will be replaced by DIGEST-MD5 at some point), it may
be useful for the time being.


%package -n %{libname}-plug-login
Summary:	SASL LOGIN mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-login

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
Provides:	sasl-plug-gssapi
 
%description -n %{libname}-plug-gssapi
This plugin implements the SASL GSSAPI (kerberos 5)mechanism.


%package -n %{libname}-plug-otp
Summary:	SASL OTP mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-otp

%description -n %{libname}-plug-otp
This plugin implements the SASL OTP mechanism.


%package -n %{libname}-plug-sasldb
Summary:	SASL sasldb mechanism plugin
Group:		System/Libraries
# Requirement for %%{name} is due to dbconverter-2 being potentially called in %%post
#Requires(post): %{name} = %{version}
Requires:	%{libname} = %{version}, %{name} = %{version}
Provides:	sasl-plug-sasldb

%description -n %{libname}-plug-sasldb
This plugin implements the SASL sasldb mechanism.


%package -n %{libname}-plug-srp
Summary:	SASL srp mechanism plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-srp

%description -n %{libname}-plug-srp
This plugin implements the srp mechanism.


%package -n %{libname}-plug-ntlm
Summary:	SASL ntlm authentication plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-ntlm

%description -n %{libname}-plug-ntlm
This plugin implements the (unsupported) ntlm authentication.


%package -n %{libname}-plug-sql
Summary:	SASL sql auxprop plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-sql

%description -n %{libname}-plug-sql
This plugin implements the SQL auxprop authentication method
supporting MySQL and PostgreSQL.


%package -n %{libname}-plug-ldapdb
Summary:	SASL ldapdb auxprop plugin
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	sasl-plug-ldapdb

%description -n %{libname}-plug-ldapdb
This plugin implements the LDAP auxprop authentication method.


%prep
%setup -q
%patch0 -p1 -b .sasldoc
%patch1 -p1 -b .rpath
%patch2 -p1 -b .lib64
#%patch3 -p1 -b .gssapi
%patch4 -p1 -b .pic
%patch5 -p0 -b .openldap-2.3.0
%patch6 -p0 -b .sed_syntax

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" configure.in

rm -f config/ltconfig config/libtool.m4
libtoolize -f -c
aclocal-1.8 -I config -I cmulocal
automake-1.8 -a -c -f
autoheader
autoconf -f
pushd saslauthd
    rm -f config/ltconfig
    libtoolize -f -c
    aclocal-1.8 -I ../config -I ../cmulocal
    automake-1.8 -a -c -f
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
    --disable-krb4 \
    --enable-login \
    --enable-db4 \
    --enable-sql \
    --with-mysql=%{_prefix} \
    --with-pgsql=%{_prefix} \
    --without-sqlite \
    --with-ldap=%{_prefix} \
    --enable-ldapdb \
    --with-dbpath=%{sasl2_db_fname} \
    --with-saslauthd=/var/lib/sasl2 \
    --with-authdaemond=/var/run/authdaemon.courier-imap/socket
# when we move to krb4 add --with-gssapi and --disable-gss_mutexes to configure above
# as krb5-1.4.x is threadsafe and 1.3.x is not

# these don't seem to play too well with openssl 0.9.8
#    --enable-srp \
#    --enable-srp-setpass \
#    --enable-ntlm \

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
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig


%{__make} install DESTDIR=%{buildroot}

install %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/saslauthd
# Install man pages in the expected location, even if they are
# pre-formatted.
install -m 0755 -d %{buildroot}%{_mandir}/man8/
install -m 0644 */*.8 %{buildroot}%{_mandir}/man8/

%makeinstall_std

# dbconverter-2 isn't installed by make install

pushd utils
    /bin/sh ../libtool --mode=install /usr/bin/install -c dbconverter-2 \
        %{buildroot}/%{_sbindir}/dbconverter-2
popd
cp saslauthd/testsaslauthd %{buildroot}%{_sbindir}

mkdir -p %{buildroot}%{_srvdir}/saslauthd/log
install -m 0740 %{SOURCE4} %{buildroot}%{_srvdir}/saslauthd/run
install -m 0740 %{SOURCE5} %{buildroot}%{_srvdir}/saslauthd/log/run

# fix the horribly broken manpage
cat %{SOURCE6} >%{buildroot}%{_mandir}/man8/saslauthd.8

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
if [ -d /var/log/supervise/saslauthd -a ! -d /var/log/service/saslauthd ]; then
    mv /var/log/supervise/saslauthd /var/log/service/
fi
%_post_srv saslauthd


%preun
%_preun_srv saslauthd


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc COPYING AUTHORS INSTALL NEWS README* ChangeLog
%doc doc/{TODO,ONEWS,*.txt,*.html}
%dir /var/lib/sasl2
%attr (644,root,root) %config(noreplace) /etc/sysconfig/saslauthd
%dir %attr(0750,root,admin) %{_srvdir}/saslauthd
%dir %attr(0750,root,admin) %{_srvdir}/saslauthd/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/saslauthd/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/saslauthd/log/run
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

#%files -n %{libname}-plug-srp
#%defattr(-,root,root)
#%{_libdir}/sasl2/libsrp*.so*
#%{_libdir}/sasl2/libsrp*.la

#%files -n %{libname}-plug-ntlm
#%defattr(-,root,root)
#%{_libdir}/sasl2/libntlm*.so*
#%{_libdir}/sasl2/libntlm*.la

%files -n %{libname}-plug-sql
%defattr(-,root,root)
%{_libdir}/sasl2/libsql*.so*
%{_libdir}/sasl2/libsql*.la

%files -n %{libname}-plug-ldapdb
%defattr(-,root,root)
%{_libdir}/sasl2/libldap*.so*
%{_libdir}/sasl2/libldap*.la

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.*so
%{_libdir}/*.*a
%{_libdir}/sasl2/*.a
%{_mandir}/man3/*

 
%changelog
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

* Thu Aug 07 2003 Florin <florin@mandrakesoft.com> 2.1.15-4mdk
- update the initscript and the sysconfig files (thx to L.Olivetti)

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.15-3mdk
- mklibname, cputoolize
- Enforce use of db4 libraries
- Patch2: Let sasldir be plugindir (aka lib64 fixes)

* Wed Jul 30 2003 Warly <warly@mandrakesoft.com> 2.1.15-2mdk
- recompile for the libcom_err.so.3 replaced into libcom_err.so.2

* Wed Jul 16 2003 Florin <florin@mandrakesoft.com> 2.1.15-1mdk
- 2.1.15

* Sat May 10 2003 Luca Olivetti <luca@olivetti.cjb.net> 2.1.13-1mdk
- 2.1.13
- renamed main package cyrus-sasl2 so it can coexist with sasl v1

* Tue Feb 25 2003 Luca Olivetti <luca@olivetti.cjb.net> 2.1.12-1mdk
- 2.1.12
- install the correct dbconverter-2
- convert v1 sasl.db in post

* Mon Dec 09 2002 Luca Olivetti <luca@olivetti.cjb.net> 2.1.10-1mdk
- removed gcc3.2 patch and other hacks no longer necessary
- upgrade to 2.1.10
- fixed some rpmlint warnings

* Sat Oct 26 2002 Luca Olivetti <luca@olivetti.cjb.net> 2.1.9-1mdk
- upgrade to 2.1.9

* Sat Oct 12 2002 Luca Olivetti <luca@olivetti.cjb.net> 2.1.8-1mdk
- upgrade to 2.1.8
- enabled and packaged plugin for srp
- enabled and packaged plugin for ntlm (new in 2.1.8)

* Sat Oct 05 2002 Luca Olivetti <luca@olivetti.cjb.net> 2.1.7-2mdk
- patch and hacks to compile under mandrake 9.0 (with gcc 3.2)
- corrected init script from mdk package
- added documentation for ldap authentication

* Wed Sep 11 2002 Luca Olivetti <luca@olivetti.cjb.net> 2.1.7-1mdk
- upgrade to 2.1.7

* Sun May 12 2002 Luca Olivetti <luca@olivetti.cjb.net> 2.1.2-2mdk
- man pages weren't installed (automake problem?), quick hack to fix it
- installed dbconverter-2 (not installed by make install)
- removed /etc/sasl2 directory (not used anywhere)
- removed various commented lines

* Thu Apr 18 2002 Luca Olivetti <luca@olivetti.cjb.net> 2.1.2-1mdk
- upgrade to 2.1.2

* Wed Apr 17 2002 Luca Olivetti <luca@olivetti.cjb.net> 2.1.0-1mdk
- first try to package version 2.1.0
 
* Mon Mar  4 2002 Vincent Danen <vdanen@mandrakesoft.com> 1.5.27-3mdk
- fix the incorrect fix of permissions on sasl.db (mode 600 is not good)

* Wed Oct 24 2001 Philippe Libat <philippe@mandrakesoft.com> 1.5.27-2mdk
- fix post-install script

* Tue Oct 16 2001 Philippe Libat <philippe@mandrakesoft.com> 1.5.27-1mdk
- New version
- rebuild for db3.3(patch3)
- fix permissions on /var/lib/sasl/sasl.db
- add postinstall initialisation command

* Sat Sep 22 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.5.24-7mdk
- Fix stupid error with CONFDIR.
- As a special bonus fix the build.

* Thu Jul  5 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.5.24-6mdk
- rebuild for db3.2

* Wed Jun 20 2001 Philippe Libat <philippe@mandrakesoft.com> 1.5.24-5mdk
- review rpm organization

* Wed Jun 13 2001 Philippe Libat <philippe@mandrakesoft.com> 1.5.24-4mdk
- rpath patch <flepied@mandrakesoft.com>

* Tue Jun 12 2001 Philippe Libat <philippe@mandrakesoft.com> 1.5.24-3mdk
- mysql, ldap patch
- added documentation

* Fri Mar  9 2001 Vincent Saugey <vince@mandrakesoft.com> 1.5.24-2mdk
- Adding include file in devel package

* Mon Nov 27 2000 Vincent Saugey <vince@mandrakesoft.com> 1.5.24-1mdk
- First mdk release
