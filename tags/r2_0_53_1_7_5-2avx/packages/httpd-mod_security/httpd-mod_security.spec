%define name	apache2-%{mod_name}
%define version	%{apache_version}_%{mod_version}
%define release 2avx

# Module-Specific definitions
%define apache_version	2.0.53
%define mod_version	1.7.5
%define mod_name	mod_security
%define mod_conf	82_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

Summary:	Mod_security is a DSO module for the apache2 Web server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://www.modsecurity.org/
Source0:	%{sourcename}.tar.gz
Source1:	%{mod_conf}.bz2
Source2:	snortrules-snapshot-CURRENT.tar.gz
Source3:	%{sourcename}.tar.gz.asc

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	apache2-devel >= %{apache_version}

Prereq:		apache2 >= %{apache_version}, apache2-conf
Prereq:		rpm-helper

%description
ModSecurity is an open source intrustion detection and prevention
engine for web applications. It operates embedded into the web
server, acting as a powerful umbrella - shielding applications
from attacks.

%prep

%setup -q -n %{mod_name}-%{mod_version}

tar -zxf %{SOURCE2}
cat > mod_security-snortrules.conf << EOF
# This file was generated using the %{_sbindir}/snort2modsec.pl perl script.

EOF
perl util/snort2modsec.pl rules/web*.rules >> mod_security-snortrules.conf

%build
cp apache2/%{mod_name}.c .
%{_sbindir}/apxs2 -c %{mod_name}.c

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/apache2-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -m 0755 .libs/*.so %{buildroot}%{_libdir}/apache2-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/conf.d/%{mod_conf}

mkdir -p %{buildroot}/var/www/html/addon-modules
ln -s ../../../../%{_docdir}/%{name}-%{version} %{buildroot}/var/www/html/addon-modules/%{name}-%{version}

mkdir -p %{buildroot}{%{_sbindir},%{_sysconfdir}/httpd/2.0/conf}

install -m 0755 util/snort2modsec.pl %{buildroot}%{_sbindir}/
install -m 0644 mod_security-snortrules.conf %{buildroot}%{_sysconfdir}/httpd/2.0/conf

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc tests CHANGES README httpd.conf*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/2.0/conf/mod_security-snortrules.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache2-extramodules/%{mod_so}
%attr(0755,root,root) %{_sbindir}/snort2modsec.pl
/var/www/html/addon-modules/*

%changelog
* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 2.0.53_1.8.6-2avx
- rebuild

* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 2.0.53_1.8.6-1avx
- 1.8.6
- apache 2.0.53
- remove ADVX stuff
- remove pdf docs

* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.52_1.7.5-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 2.0.49_1.7.5-2avx
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

* Sun Dec 07 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_1.7.4-1mdk
- 1.7.4

* Wed Nov 12 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.7.3-1mdk
- 1.7.3

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_1.7.2-1mdk
- built for apache 2.0.48

* Sun Nov 02 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.7.2-1mdk
- 1.7.2

* Tue Oct 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.7.1-1mdk
- 1.7.1
- drop S2, it's included

* Sun Oct 19 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.7-1mdk
- 1.7
- added S2 and some spec file magic

* Sun Sep 28 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.6-1mdk
- 1.6

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.5.1-1mdk
- 1.5.1
- rebuilt against latest apache2, requires and buildrequires
- misc spec file fixes
- updated S1

* Fri Jun 06 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_1.5-1mdk
- initial cooker contrib
