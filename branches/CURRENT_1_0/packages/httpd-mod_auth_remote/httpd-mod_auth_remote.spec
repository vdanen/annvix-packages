%define name	apache2-%{mod_name}
%define version %{apache_version}_%{mod_version}
%define release 1avx
%define epoch	1

# Module-Specific definitions
%define apache_version	2.0.53
%define mod_version	0.1
%define mod_name	mod_auth_remote
%define mod_conf	82_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

Summary:	Mod_auth_remote is a DSO module for the apache2 Web server
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		System/Servers
URL:		http://puggy.symonds.net/~srp/stuff/mod_auth_remote/
Source0:	%{sourcename}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		%{sourcename}-register.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:  apache2-devel >= %{apache_version}

Prereq:		apache2 >= %{apache_version}, apache2-conf


%description
This module is a very simple, lightweight method of setting up a
single signon system across multiple web-applicaitions hosted on
different servers.

The actual authentication & authorization system is deployed on a
single server instead of each individual server. All other servers
are built with mod_auth_remote enabled. When a request comes in,
mod_auth_remote obtains the client username & password from the
client via basic authentication scheme.

It then builds a HTTP header with authorization header built from
the client's userid:passwd. mod_auth_remote then makes a HEAD
request to the authentication server. On reciept of a 2XX
response, the client is validated; for all other responses the
client is not validated.

%prep

%setup -q -c -n %{sourcename} -a0
%patch0 -p0

%build
%{_sbindir}/apxs2 -c %{mod_name}.c

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
%doc readme.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache2-extramodules/%{mod_so}
/var/www/html/addon-modules/*

%changelog
* Sat Feb 26 2005 Vincent Danen <vdanen@annvix.org> 2.0.53_0.1-1avx
- apache 2.0.53
- remove ADVX stuff

* Thu Oct 14 2004 Vincent Danen <vdanen@annvix.org> 2.0.52_0.1-1avx
- apache 2.0.52

* Sun Jun 27 2004 Vincent Danen <vdanen@annvix.org> 2.0.49_0.1-2avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 2.0.49_0.1-1sls
- apache 2.0.49

* Wed Feb 18 2004 Vincent Danen <vdanen@opensls.org> 2.0.48_0.1-4sls
- small tidy

* Tue Dec 23 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_0.1-3sls
- new version from author (bugfixes)
- fix url
- this is actually 0.1 so bump up the epoch and make the version right
- rename P0

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_1.0-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_1.0-1mdk
- built for apache 2.0.48

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 2.0.47_1.0-2mdk
- Rebuild to fix bad signature

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_1.0-1mdk
- rebuilt against latest apache2, requires and buildrequires

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_1.0-1mdk
- rebuilt for apache v2.0.46
- buildrequires ADVX-build >= 9.2

* Fri Apr 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45_1.0-1mdk
- cosmetic rebuild for apache v2.0.45

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.0-1mdk
- initial cooker contrib
- the "BeerWare" license was changed to GPL
