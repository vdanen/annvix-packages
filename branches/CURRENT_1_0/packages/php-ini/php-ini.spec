%define name	php-ini
%define version	4.3.6
%define release	1sls

Summary:	INI files for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/Other
URL:		http://www.php.net
Source0:	php.ini.bz2

BuildRoot:	%{_tmppath}/%{name}-root

Provides: 	ADVXpackage

%description
The php-ini package contains the ini files required for PHP.

%build

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_sysconfdir}/php
mkdir -p %{buildroot}%{_libdir}/php/extensions
bzcat %{SOURCE0} > %{buildroot}%{_sysconfdir}/php.ini

perl -pi -e 's|EXTENSIONDIR|%{_libdir}/php/extensions|g' %{buildroot}%{_sysconfdir}/php.ini

mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}
echo "Thanks to Oden Eriksson for the scan-dir idea!" > \
        %{buildroot}%{_docdir}/%{name}-%{version}/CREDITS

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
#Since we use noreplace, we may have an old php.ini file which is not 
#compatible with the new way of handling extensions. Remove all
#extensions if that's the case.
cd %{_sysconfdir}
if egrep "^(;)*extension(.)*\.so" php.ini >/dev/null; then
  echo "Converting php.ini to new way of handling extensions"
  cat php.ini > php-ini.bak
  egrep -v "^(;)*extension(.)*\.so" php-ini.bak > php.ini
fi

%files 
%defattr(-,root,root)
%dir %{_sysconfdir}/php
%dir %{_libdir}/php
%dir %{_libdir}/php/extensions
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/*

%changelog
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
