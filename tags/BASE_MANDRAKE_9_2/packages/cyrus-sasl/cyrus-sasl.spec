%define major 2
%define libname %mklibname sasl %{major}
%define up_name cyrus-sasl

Summary: SASL is the Simple Authentication and Security Layer.
Name: %{up_name}
Version: 2.1.15
Release: 4mdk
Source0: ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/%{up_name}-%{version}.tar.gz
Source1: ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/%{up_name}-%{version}.tar.gz.sig
Source2:        saslauthd.init
Source3:        saslauthd.sysconfig
Patch0:  cyrus-sasl-doc-patch.bz2
Patch1:	 cyrus-sasl-2.1.12-rpath.patch.bz2
Patch2: cyrus-sasl-2.1.15-lib64.patch.bz2

License: OSI Approved
Group: System/Libraries
URL: http://asg.web.cmu.edu/cyrus/download/
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Prefix: %{_prefix}
Requires: %{libname}
Obsoletes: cyrus-sasl >= 2.1.0
PreReq: rpm-helper
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  db4-devel
BuildRequires:  pam-devel
BuildRequires:  openssl-devel >= 0.9.6a
BuildRequires:  libtool >= 1.4
BuildRequires:  krb5-devel
%{?!bootstrap:BuildRequires: openldap-devel}

%description
SASL is the Simple Authentication and Security Layer, 
a method for adding authentication support to connection-based protocols. 
To use SASL, a protocol includes a command for identifying and authenticating 
a user to a server and for optionally negotiating protection of subsequent 
protocol interactions. If its use is negotiated, a security layer is inserted 
between the protocol and the connection. 

%package -n %{libname}
Summary: Libraries for SASL a the Simple Authentication and Security Layer.
Group: System/Libraries


%description -n %{libname}
SASL is the Simple Authentication and Security Layer, 
a method for adding authentication support to connection-based protocols. 
To use SASL, a protocol includes a command for identifying and authenticating 
a user to a server and for optionally negotiating protection of subsequent 
protocol interactions. If its use is negotiated, a security layer is inserted 
between the protocol and the connection. 

%package -n %{libname}-devel
Summary: Librairies for SASL a the Simple Authentication and Security Layer.
Group: Development/C
Provides: libsasl-devel
Requires: %{libname} = %{version}

%description -n %{libname}-devel
SASL is the Simple Authentication and Security Layer, 
a method for adding authentication support to connection-based protocols. 
To use SASL, a protocol includes a command for identifying and authenticating 
a user to a server and for optionally negotiating protection of subsequent 
protocol interactions. If its use is negotiated, a security layer is inserted 
between the protocol and the connection. 

%package -n %{libname}-plug-anonymous
Summary: SASL ANONYMOUS mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}

%description -n %{libname}-plug-anonymous
This plugin implements the SASL ANONYMOUS mechanism,
used for anonymous authentication.

%package -n %{libname}-plug-crammd5
Summary: SASL CRAM-MD5 mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}

%description -n %{libname}-plug-crammd5
This plugin implements the SASL CRAM-MD5 mechanism.
CRAM-MD5 is the mandatory-to-implement authentication mechanism for a
number of protocols; it uses MD5 with a challenge/response system to
authenticate the user.

%package -n %{libname}-plug-digestmd5
Summary: SASL DIGEST-MD5 mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}

%description -n %{libname}-plug-digestmd5
This plugin implements the latest draft of the SASL DIGEST-MD5
mechanism.  Although not yet finalized, this is likely to become the
new mandatory-to-implement authentication system in all new protocols.
It's based on the digest md5 authentication system designed for HTTP.

#%package plug-kerberos4
#Summary: SASL KERBEROS_V4 mechanism plugin

#%description plug-kerberos4
#This plugin implements the SASL KERBEROS_V4 mechanism, allowing
#authentication via kerberos version four.

%package -n %{libname}-plug-plain
Summary: SASL PLAIN mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}

%description -n %{libname}-plug-plain
This plugin implements the SASL PLAIN mechanism.  Although insecure,
PLAIN is useful for transitioning to new security mechanisms, as this
is the only mechanism which gives the server a copy of the user's
password.

%package -n %{libname}-plug-scrammd5
Summary: SASL SCRAM-MD5 mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}

%description -n %{libname}-plug-scrammd5
This plugin implements the SASL SCRAM-MD5 mechanism.  Although
deprecated (this will be replaced by DIGEST-MD5 at some point), it may
be useful for the time being.

%package -n %{libname}-plug-login
Summary: SASL LOGIN mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}

%description -n %{libname}-plug-login
This plugin implements the SASL LOGIN mechanism.
THIS PLUGIN IS DEPRECATED, is maintained only for compatibility reasons 
and will be dropped soon.
Please use the plain plugin instead.

%package -n %{libname}-plug-gssapi
Summary: SASL GSSAPI mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}
Requires: krb5-libs
 
%description -n %{libname}-plug-gssapi
This plugin implements the SASL GSSAPI (kerberos 5)mechanism.

%package -n %{libname}-plug-otp
Summary: SASL OTP mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}

%description -n %{libname}-plug-otp
This plugin implements the SASL OTP mechanism.


%package -n %{libname}-plug-sasldb
Summary: SASL sasldb mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}

%description -n %{libname}-plug-sasldb
This plugin implements the SASL sasldb mechanism.

%package -n %{libname}-plug-srp
Summary: SASL srp mechanism plugin
Group: System/Libraries
Requires: %{libname} = %{version}

%description -n %{libname}-plug-srp
This plugin implements the srp  mechanism.


%package -n %{libname}-plug-ntlm
Summary: SASL ntlm authentication plugin
Group: System/Libraries
Requires: %{libname} = %{version}

%description -n %{libname}-plug-ntlm
This plugin implements the (unsupported) ntlm authentication.
%prep
%setup -q -n %{up_name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .lib64

%build

%serverbuild

export LDFLAGS="-L%{_libdir}"

%{?__cputoolize: %{__cputoolize} -c saslauthd}
%configure 	--enable-static --enable-shared \
		--with-plugindir=%{_libdir}/sasl2 \
		--disable-krb4 \
		--enable-login \
		--enable-srp \
		--enable-srp-setpass \
		--enable-ntlm \
		--enable-db4 \
		--without-mysql \
%{?!bootstrap:--with-ldap=/usr} \
		--with-dbpath=/var/lib/sasl2/sasl.db \
		--with-configdir=%{_libdir}/sasl2 \
		--with-saslauthd=/var/lib/sasl2 

%make

install saslauthd/LDAP_SASLAUTHD README.ldap

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/var/lib/sasl2
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d/
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig


%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/saslauthd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/saslauthd
# Install man pages in the expected location, even if they are
# pre-formatted.
install -m755 -d $RPM_BUILD_ROOT%{_mandir}/man8/
install -m644 */*.8 $RPM_BUILD_ROOT%{_mandir}/man8/

%makeinstall_std

# dbconverter-2 isn't installed by make install

cd utils
/bin/sh ../libtool --mode=install /usr/bin/install -c dbconverter-2 \
  $RPM_BUILD_ROOT/%{_sbindir}/dbconverter-2

%clean
rm -rf $RPM_BUILD_ROOT

%post
#convert old sasldb
if [ -f /var/lib/sasl/sasl.db -a ! -f /var/lib/sasl2/sasl.db ]; then
   echo "" | /usr/sbin/dbconverter-2 /var/lib/sasl/sasl.db /var/lib/sasl2/sasl.db
fi
if [ -f /var/lib/sasl/sasl.db.rpmsave -a ! -f /var/lib/sasl2/sasl.db ]; then
   echo "" | /usr/sbin/dbconverter-2 /var/lib/sasl/sasl.db.rpmsave /var/lib/sasl2/sasl.db
fi

%_post_service saslauthd
%preun
%_preun_service saslauthd

%post -n %{libname}
/sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc COPYING AUTHORS INSTALL NEWS README* ChangeLog sample/{client,server}
%doc doc/{TODO,ONEWS,*.txt,*.html}
%dir /var/lib/sasl2
%attr (755,root,root) %config(noreplace) /etc/rc.d/init.d/saslauthd
%attr (644,root,root) %config(noreplace) /etc/sysconfig/saslauthd

%{_sbindir}/*
%{_mandir}/man8/*
%{_mandir}/cat8/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libsasl*.so.*

%files -n %{libname}-plug-anonymous
%defattr(-,root,root)
%{_libdir}/*/libanonymous*.so*
%{_libdir}/*/libanonymous*.la

%files -n %{libname}-plug-otp
%defattr(-,root,root)
%{_libdir}/*/libotp*.so.*
%{_libdir}/*/libotp*.la

%files -n %{libname}-plug-sasldb
%defattr(-,root,root)
%{_libdir}/*/libsasldb*.so.*
%{_libdir}/*/libsasldb*.la

%files -n %{libname}-plug-gssapi
%defattr(-,root,root)
%{_libdir}/*/libgssapi*.so.*
%{_libdir}/*/libgssapi*.la

%files -n %{libname}-plug-crammd5
%defattr(-,root,root)
%{_libdir}/*/libcrammd5*.so*
%{_libdir}/*/libcrammd5*.la

%files -n %{libname}-plug-digestmd5
%defattr(-,root,root)
%{_libdir}/*/libdigestmd5*.so*
%{_libdir}/*/libdigestmd5*.la

%files -n %{libname}-plug-plain
%defattr(-,root,root)
%{_libdir}/*/libplain*.so*
%{_libdir}/*/libplain*.la

#%files -n %{libname}-plug-kerberos4
#%defattr(-,root,root)
#%{_libdir}/*/libkerberos4*.so*

%files -n %{libname}-plug-login
%defattr(-,root,root)
%{_libdir}/*/liblogin*.so*
%{_libdir}/*/liblogin*.la

%files -n %{libname}-plug-srp
%defattr(-,root,root)
%{_libdir}/*/libsrp*.so*
%{_libdir}/*/libsrp*.la


%files -n %{libname}-plug-ntlm
%defattr(-,root,root)
%{_libdir}/*/libntlm*.so*
%{_libdir}/*/libntlm*.la

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.*so
%{_libdir}/*.*a
%{_libdir}/*/*.a
%{_mandir}/man3/*
 
%changelog
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
