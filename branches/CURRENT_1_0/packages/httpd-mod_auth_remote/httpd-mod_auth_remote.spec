%define name	%{ap_name}-%{mod_name}
%define version %{ap_version}_%{mod_version}
%define release 1avx

# Module-Specific definitions
%define mod_version	0.1
%define mod_name	mod_auth_remote
%define mod_conf	82_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

# New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}
%{expand:%%global ap_version %(%{apxs} -q ap_version)}

Summary:	Mod_auth_remote is a DSO module for the %{ap_name} Web server.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		1
License:	GPL
Group:		System/Servers
URL:		http://puggy.symonds.net/~srp/stuff/mod_auth_remote/
Source0:	%{sourcename}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		%{sourcename}-register.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
# Standard ADVX requires
BuildRequires:  ADVX-build >= 9.2
BuildRequires:  %{ap_name}-devel

# Standard ADVX requires
Prereq:		%{ap_name} = %{ap_version}
Prereq:		%{ap_name}-conf
Provides: 	ADVXpackage
Provides:	AP20package


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
%{apxs} -c %{mod_name}.c

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%ADVXinstlib
%ADVXinstconf %{SOURCE1} %{mod_conf}
%ADVXinstdoc %{name}-%{version}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%ADVXpost

%postun
%ADVXpost

%files
%defattr(-,root,root)
%config(noreplace) %{ap_confd}/%{mod_conf}
%{ap_extralibs}/%{mod_so}
%{ap_webdoc}/*
%doc readme.txt

%changelog
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
