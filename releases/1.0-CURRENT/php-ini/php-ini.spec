%define name	php-ini
%define version	4.3.10
%define release	1avx

Summary:	INI files for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/Other
URL:		http://www.php.net
Source0:	php.ini.annvix.bz2

BuildRoot:	%{_tmppath}/%{name}-root

%description
The php-ini package contains the ini files required for PHP.

%prep
%setup -c -T

%build

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/php.d
mkdir -p %{buildroot}%{_libdir}/php/extensions
bzcat %{SOURCE0} > %{buildroot}%{_sysconfdir}/php.ini

perl -pi -e 's|EXTENSIONDIR|%{_libdir}/php/extensions|g' %{buildroot}%{_sysconfdir}/php.ini


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/extensions

%changelog
* Fri Dec 17 2004 Vincent Danen <vdanen@annvix.org> 4.3.10-1avx
- spec cleanups
- remove %%post migratory stuff
- remove hardened-php changes to php.ini

* Fri Dec 17 2004 Vincent Danen <vdanen@annvix.org> 4.3.10-1avx
- php 4.3.10
- update php.ini to accomodate hardened-php directives

* Thu Sep 30 2004 Vincent Danen <vdanen@annvix.org> 4.3.9-1avx
- php 4.3.9

* Wed Jul 14 2004 Vincent Danen <vdanen@annvix.org> 4.3.8-1avx
- 4.3.8
- remove ADVXpackage provides
- by default, allow_url_fopen is off, as is register_globals
- move scandir to /etc/php.d
- update php.ini from 4.3.8 with the following changes (based on
  php.ini-recommended):
  - output_buffering = Off
  - expose_php = Off
  - error_log = /var/log/httpd/php-error.log
  - variables_order = "EGPCS"
  - register_argc_argv = On
  - magic_quotes_gpc = On
  - include_path = ".:/usr/lib/php/:/usr/share/pear/"
  - allow_url_fopen = Off
  - session.gc_divisor = 100

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 4.3.7-2avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.3.7-1sls
- 4.3.7

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.3.6-1sls
- 4.3.6

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-5sls
- minor spec cleanups

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-4sls
- no longer noarch due to amd64 vs. x86 libdir changes

* Fri Jan 09 2004 Vincent Danen <vdanen@opensls.org> 4.3.4-3sls
- replace /usr/lib/php/extensions in php.ini with EXTENSIONDIR so that
  we can dynamically create the extension dir (amd64)

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 4.3.4-2sls
- OpenSLS build
- tidy spec

* Tue Nov 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.4-1mdk
- built for 4.3.4

* Mon Aug 25 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.3-1mdk
- built for 4.3.3
- updated S0

* Mon Jul 21 2003 David BAUDENS <baudens@mandrakesoft.com> 4.3.2-2mdk
- Rebuild to fix bad signature

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-1mdk
- built for 4.3.2

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.2-0.1mdk
- built for 4.3.2RC4
- updated the php.ini file

* Mon May 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 4.3.1-1mdk
- the obvious rebuild

* Sat Jan  4 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 4.3.0-1mdk
- New package
