%define name	apache2-%{mod_name}
%define version %{apache_version}_%{mod_version}
%define release 1avx

# Module-Specific definitions
%define apache_version	2.0.53
%define mod_version	1.7PR1
%define mod_name	mod_auth_radius
%define mod_conf	14_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}

Summary:	Mod_radius is a DSO module for the apache2 Web server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		https://www.gnarst.net/authradius/
Source0:	%{mod_name}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		%{mod_name}-register.patch.bz2
Patch1:		%{mod_name}-invalid-hostname.patch.bz2
Patch2:		%{mod_name}-wierd_fix.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:  apache2-devel >= %{apache_version}

Prereq:		apache2 >= %{apache_version}, apache2-conf

%description
Make apache2 a RADIUS client for authentication and
accounting requests.

%prep

%setup -q -c -n mod_auth_radius
mv mod_auth_radius_apache2.c mod_auth_radius.c
%patch0
%patch1
%patch2

%build
%{_sbindir}/apxs2 -c mod_auth_radius.c -Wl,-lresolv

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/apache2-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -m 0755 .libs/*.so %{buildroot}%{_libdir}/apache2-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/conf.d/%{mod_conf}

mkdir -p %{buildroot}/var/www/html/addon-modules
ln -s ../../../../%{_docdir}/%{name}-%{version} %{buildroot}/var/www/html/addon-modules/%{name}-%{version}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc mod_auth_radius.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache2-extramodules/%{mod_so}
/var/www/html/addon-modules/*

%changelog
* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 2.0.53_1.7PR1-1avx
- apache 2.0.53
- remove ADVX stuff

* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.52_1.7PR1-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 2.0.49_1.7PR1-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_1.7PR1-1sls
- apache 2.0.49

* Wed Feb 18 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_1.7PR1-3sls
- small cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_1.7PR1-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_1.7PR1-1mdk
- built for apache 2.0.48

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 2.0.47_1.7PR1-2mdk
- Rebuild to fix bad signature

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.7PR1-1mdk
- rebuilt against latest apache2, requires and buildrequires
- added P2 to make it compile

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_1.7PR1-1mdk
- rebuilt for apache v2.0.46
- buildrequires ADVX-build >= 9.2

* Fri Apr 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45_1.7PR1-1mdk
- cosmetic rebuild for apache v2.0.45

* Fri Feb 28 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44_1.7PR1-2mdk
- Fix segfault when hostname is invalid

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44_1.7PR1-1mdk
- rebuilt for apache v2.0.44

* Mon Jan 20 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.7PR1-6mdk
- fix buildrequires apache2-devel >= 2.0.43-5mdk, as 
  pointed out by Olivier Thauvin

* Sat Jan 18 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.7PR1-5mdk
- rebuilt against rebuilt buildrequires

* Mon Jan 13 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.7PR1-4mdk
- Rebuilt with the new apache-devel that uses /usr/sbin/apxs2 and
  /usr/include/apache2

* Sat Nov 02 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.7PR1-3mdk
- rebuilt for/against apache2 where dependencies has changed in apr

* Tue Oct 22 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.7PR1-2mdk
- extra modules needs to be loaded _before_ mod_ssl, mod_php and mod_perl
  in order to show up in the server string...

* Fri Oct 04 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.43_1.7PR1-1mdk
- rebuilt for/against new apache2 version 2.0.43 (even though 2.0.42 and 
  2.0.43 are binary compatible, we have to consider rpm dependencies)
- sanitize rpm package versioning

* Thu Sep 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42_1.7PR1-5mdk
- P0 was not applied, i wonder why not?, it is now

* Thu Sep 26 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.42_1.7PR1-4mdk
- rebuilt against new apache v2.0.42

* Wed Sep  3 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.40ADVX_1.7PR1-3mdk
- Comply with ADVX policy at http://advx.org/devel/policy.php
- Add Register patch

* Mon Aug 19 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.7PR1-2mdk
- add %%description ;)

* Mon Aug 19 2002 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.7PR1-1mdk
- initial cooker contrib


