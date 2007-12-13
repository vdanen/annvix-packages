#
# spec file for package php-ini
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		php-ini
%define version		5.2.5
%define release		%_revrel

Summary:	INI files for PHP
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	PHP License
Group:		Development/PHP
URL:		http://www.php.net
Source0:	php.ini.annvix

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The php-ini package contains the ini files required for PHP.


%prep
%setup -c -T -q


%build


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/php.d
mkdir -p %{buildroot}%{_libdir}/php/extensions
mkdir -p %{buildroot}/var/tmp/php_sessions
install -m 0644 %{_sourcedir}/php.ini.annvix %{buildroot}%{_sysconfdir}/php.ini

perl -pi -e 's|/usr/lib|%{_libdir}|' %{buildroot}%{_sysconfdir}/php.ini
perl -pi -e 's|EXTENSIONDIR|%{_libdir}/php/extensions|g' %{buildroot}%{_sysconfdir}/php.ini


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/php.ini
%dir %{_sysconfdir}/php.d
%dir %{_libdir}/php
%dir %{_libdir}/php/extensions
%attr(1777,root,root) %dir /var/tmp/php_sessions


%changelog
* Wed Dec 12 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.5
- php 5.2.5

* Mon Jun 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.3
- add [Session] to the main php.ini since it's now built-in

* Sun Jun 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.3
- php 5.2.3

* Fri May 04 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.2
- php 5.2.2
- increased upload_max_filesize from 2MB to 8MB
- add missing [Pcre] section

* Wed Feb 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.2.1
- php 5.2.1

* Sun Dec 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.2.0
- php 5.2.0

* Fri Oct 20 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.6
- php 5.1.6
- update the default ini to remove the hardened php stuff

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.4
- php 5.1.4
- update config to add realpath_cache_ttl and realpath_cache_size

* Mon Apr 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- remove some extension options that are duplicated by modules (such
  as mysql*, exif, postgresql, etc.) and are available in their own
  ini files

* Thu Mar 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.1.2
- 5.1.2
- made the following changes to php.ini (aside from making it based on PHP5):
  - output_buffering = 4096
  - register_argc_argv = Off
  - magic_quotes_gpc = Off
  - register_long_arrays = Off

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- 4.4.2
- use /var/tmp/php_sessions for the session.save_path and make it sticky
  (fixes bug #16)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Nov 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.1-1avx
- php 4.4.1

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-3avx
- reverse the perl call in %%install so we don't end up with
  /usr/lib6464 for the extension_dir

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-2avx
- lib64 fix in php.ini

* Wed Sep 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.0-1avx
- php 4.4.0
- put back hardened php settings

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-2avx
- rebuild

* Sat May 14 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.3.11-1avx
- php 4.3.11

* Fri Dec 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-1avx
- spec cleanups
- remove %%post migratory stuff
- remove hardened-php changes to php.ini

* Fri Dec 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.10-1avx
- php 4.3.10
- update php.ini to accomodate hardened-php directives

* Thu Sep 30 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.9-1avx
- php 4.3.9

* Wed Jul 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.8-1avx
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

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.3.7-2avx
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
