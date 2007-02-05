#
# spec file for package httpd-mod_security
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		httpd-%{mod_name}
%define version		%{apache_version}_%{mod_version}
%define release 	%_revrel

# Module-Specific definitions
%define apache_version	2.2.4
%define mod_version	1.9.4
%define mod_name	mod_security
%define mod_conf	82_%{mod_name}.conf
%define mod_so		%{mod_name}.so

Summary:	Mod_security is a DSO module for the Apache Web server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.modsecurity.org/
Source0:	http://www.modsecurity.org/download/modsecurity-apache_%{mod_version}.tar.gz
Source1:	http://www.modsecurity.org/download/modsecurity-apache_%{mod_version}.tar.gz.asc
Source2:	http://www.modsecurity.org/download/modsecurity-rules-current.tar.gz
Source3:	snortrules-2.3.3.tar.bz2
Source4:	%{mod_conf}
Patch0:		modsecurity-apache-1.9.1-web-attacks.rules.diff
Patch1:		modsecurity-apache-1.9.1-web-php.rules.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	httpd-devel >= %{apache_version}

Requires(pre):	httpd >= %{apache_version}
Requires(pre):	httpd-conf >= 2.2.0
Provides:	apache2-mod_security
Obsoletes:	apache2-mod_security

%description
ModSecurity is an open source intrustion detection and prevention
engine for web applications. It operates embedded into the web
server, acting as a powerful umbrella - shielding applications
from attacks.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n modsecurity-apache_%{mod_version} -a 2 -a 3
pushd rules
%patch0 -p0 -b .web-attacks
%patch1 -p0 -b .web-php
popd

cat > mod_security-snortrules.conf << EOF
# This file was generated using the %{_sbindir}/snort2modsec.pl perl script.

EOF

perl util/snort2modsec.pl rules/web*.rules >> mod_security-snortrules.conf

# fix attribs
find doc -type f -exec chmod 0644 {} \;


%build
cp apache2/%{mod_name}.c .
%{_sbindir}/apxs -c %{mod_name}.c


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/httpd-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
install -m 0755 .libs/*.so %{buildroot}%{_libdir}/httpd-extramodules/
cat %{_sourcedir}/%{mod_conf} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

mkdir -p %{buildroot}{%{_sbindir},%{_sysconfdir}/httpd/conf}

install -m 0755 util/snort2modsec.pl %{buildroot}%{_sbindir}/
install -m 0644 mod_security-snortrules.conf %{buildroot}%{_sysconfdir}/httpd/conf
install -m 0644 modsecurity-experimental.conf %{buildroot}%{_sysconfdir}/httpd/conf/
install -m 0644 modsecurity-general.conf %{buildroot}%{_sysconfdir}/httpd/conf/
install -m 0644 modsecurity-hardening.conf %{buildroot}%{_sysconfdir}/httpd/conf/
install -m 0644 modsecurity-output.conf %{buildroot}%{_sysconfdir}/httpd/conf/
install -m 0644 modsecurity-php.conf %{buildroot}%{_sysconfdir}/httpd/conf/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/mod_security-snortrules.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/modsecurity-experimental.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/modsecurity-general.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/modsecurity-hardening.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/modsecurity-output.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/modsecurity-php.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_so}
%attr(0755,root,root) %{_sbindir}/snort2modsec.pl

%files doc
%defattr(-,root,root)
%doc INSTALL CHANGES README httpd.conf* doc/*


%changelog
* Fri Jan 19 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.2.4_1.9.4
- apache 2.2.4 (we're keeping this for now for backwards compatibility, for
  2.1 it'll be removed to favour mod_security2)

* Sun Jul 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_1.9.4
- apache 2.2.3
- spec cleanups

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.2_1.9.4
- apache 2.2.2
- modsecurity 1.9.4
- update patches and sources from mandriva
- refresh snort rules from snort 2.3.3
- add -doc subpackage
- rebuild with gcc4

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_1.8.7
- rebuild against apr and apr-util 0.9.7 (needed to make mod_cgi.so work
  properly)

* Thu Jan 19 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.55_1.8.7
- apache 2.0.55

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_1.8.7
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_1.8.7
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_1.8.7
- Clean rebuild

* Wed Sep 07 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.54_1.8.7-1avx
- apache 2.0.54
- mod_security 1.8.7
- s/conf.d/modules.d/
- s/apache2/httpd/

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_1.8.6-3avx
- bootstrap build (new gcc, new glibc)
- don't include the symlinks to docs in /var/www/html/addon-modules

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_1.8.6-2avx
- rebuild

* Sat Feb 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.53_1.8.6-1avx
- 1.8.6
- apache 2.0.53
- remove ADVX stuff
- remove pdf docs

* Thu Oct 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.52_1.7.5-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.49_1.7.5-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_1.7.5-1sls
- apache 2.0.49

* Tue Feb 24 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_1.7.5-1sls
- 1.7.5 (potential security fix)
- use the tar.gz and include the detached pgp sig
- snortrules-snapshot-CURRENT (20040225)

* Wed Jan 21 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_1.7.4-2sls
- OpenSLS build
- tidy spec
- don't require an active internet connection to build
- snortrules-current (20040121)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
