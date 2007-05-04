#
# spec file for package httpd-mod_php
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		httpd-%{mod_name}
%define version 	%{apache_version}_%{phpversion}
%define release		%_revrel

# Module-Specific definitions
%define apache_version	2.2.4
%define phpversion	5.2.2
%define mod_name	mod_php
%define mod_conf	70_%{mod_name}.conf
%define mod_so		%{mod_name}5.so
%define phpsource	%{_prefix}/src/php-devel
%define extname		apache2handler
%define plibname	%mklibname php_common 5

Summary:	The PHP5 HTML-embedded scripting language for use with Apache
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		System/Servers
URL:		http://www.php.net/ 
Source1:	%{mod_conf}

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	php-devel >= %{phpversion}
BuildRequires:	httpd-devel >= %{apache_version}

Requires:	openssl
Requires:	php-ini
Requires:       php-ftp >= %{phpversion}
Requires:       php-pcre >= %{phpversion}
Requires:       php-gettext >= %{phpversion}
Requires:       php-posix >= %{phpversion}
Requires:       php-ctype >= %{phpversion}
Requires:       php-session >= %{phpversion}
Requires:       php-sysvsem >= %{phpversion}
Requires:       php-sysvshm >= %{phpversion}
Requires:       php-tokenizer >= %{phpversion}
Requires:       php-simplexml >= %{phpversion}
Requires:       php-hash >= %{phpversion}
Requires:       php-suhosin >= 0.9.10
Requires:	%{plibname} >= %{phpversion}
Requires:	php-filter >= 0.11.0
Requires:	php-json >= 1.2.1
Provides:	php = %{version}
Provides:	php5 = %{version}
Provides:	mod_php = %{version}
Provides:	apache2-mod_php = %{version}
Obsoletes:	apache2-mod_php
Requires(pre):	httpd >= %{apache_version}
Requires(pre):	httpd-conf >= %{apache_version}
Requires(pre):	rpm-helper
Requires(postun): rpm-helper

%description
PHP is an HTML-embedded scripting language.  PHP attempts to make it easy for
developers to write dynamically generated web pages.  PHP also offers built-in
database integration for several commercial and non-commercial database
management systems, so writing a database-enabled web page with PHP is fairly
simple.  The most common use of PHP coding is probably as a replacement for CGI
scripts.  The %{name} module enables the Apache web server to understand
and process the embedded PHP language in web pages.


%prep
%setup -q -c -T
cp -dpR %{phpsource}/sapi/%{extname}/* .
cp %{phpsource}/internal_functions.c .
cp %{_includedir}/php/ext/date/lib/timelib_config.h .


%build
%{_sbindir}/apxs \
    `php-config --includes` \
    `apr-1-config --link-ld --libs` \
    `xml2-config --cflags` \
    -I%{phpsource} \
    -I. -lphp5_common \
    -c mod_php5.c sapi_apache2.c apache_config.c php_functions.c \
    internal_functions.c


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/httpd-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
install -m 0755 .libs/*.so %{buildroot}%{_libdir}/httpd-extramodules/
cat %{_sourcedir}/%{mod_conf} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_srv httpd

%postun
%_post_srv httpd


%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_so}


%changelog
* Fri May 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.4_5.2.2
- php 5.2.2
- versioned provides

* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.4_5.2.0 
- apache 2.2.4

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_5.2.0 
- php 5.2.0
- fix requires
- drop the doc package

* Fri Oct 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_5.1.6
- php 5.1.6
- requires php-suhosin

* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_5.1.4
- apache 2.2.3
- spec cleanups

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2_5.1.4
- apache 2.2.2
- php 5.1.4
- add -doc subpackage
- rebuild with gcc4

* Mon Apr 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_5.1.2
- php 5.1.2
- update the config file to reflect PHP5 rather than PHP4

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_4.4.2
- rebuild against apr and apr-util 0.9.7 (needed to make mod_cgi.so work
  properly)

* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_4.4.2
- apache 2.0.55
- php 4.4.2

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_4.4.0
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_4.4.0
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_4.4.0
- Clean rebuild

* Mon Oct 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_4.4.0-2avx
- fix the configuration file to add support for php files as DirectoryIndex

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_4.4.0-1avx
- php 4.4.0

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_4.3.11-1avx
- apache 2.0.54
- s/apache2/httpd/
- move config to modules.d/

* Tue Aug 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_4.3.11-2avx
- bootstrap build (new gcc, new glibc)
- remove the addon-modules symlink

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_4.3.11-1avx
- rebuild
- php 4.3.11

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_4.3.10-1avx
- apache 2.0.53
- remove ADVX stuff

* Thu Dec 16 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52_4.3.10-1avx
- php 4.3.10

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52_4.3.9-1avx
- 2.0.52

* Thu Sep 30 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_4.3.9-1avx
- php 4.3.9

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_4.3.8-3avx
- rebuild against new openssl

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_4.3.8-2avx
- use %%_post_srv rather than %%ADVXpost

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_4.3.8-1avx
- php 4.3.8
- remove ADVXpackage provides
- don't link against aprutil and db4

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_4.3.7-1sls
- php 4.3.7

* Fri May 09 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_4.3.6-1sls
- build for php 4.3.6 and apache 2.0.49

* Tue Feb 24 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_4.3.4-4sls
- fix the wierd BuildRequires for php-devel

* Tue Jan 06 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_4.3.4-3sls
- BuildRequires: libintl, not libintl2; db4-devel not libdb4.1-devel (for
  amd64)

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_4.3.4-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
