%define name	%{ap_name}-%{mod_name}
%define version	%{ap_version}_%{mod_version}
%define release 1avx

# Module-Specific definitions
%define mod_version	1.7.5
%define mod_name	mod_security
%define mod_conf	82_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

# New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}
%{expand:%%global ap_version %(%{apxs} -q ap_version)}

Summary:	Mod_security is a DSO module for the %{ap_name} Web server.
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

# Standard ADVX requires
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildPreReq:	ADVX-build >= 9.2
BuildRequires:	%{ap_name}-devel >= 2.0.44-6mdk

Prereq:		%{ap_name} = %{ap_version}
Prereq:		%{ap_name}-conf
Prereq:		rpm-helper
Provides: 	ADVXpackage
Provides:	AP20package

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
%{apxs} -c %{mod_name}.c

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%ADVXinstlib
%ADVXinstconf %{SOURCE1} %{mod_conf}
%ADVXinstdoc %{name}-%{version}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{ap_sysconfdir}

install -m0755 util/snort2modsec.pl %{buildroot}%{_sbindir}/
install -m0644 mod_security-snortrules.conf %{buildroot}%{ap_sysconfdir}/

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post
%ADVXpost

%postun
%ADVXpost

%files
%defattr(-,root,root)
%doc tests CHANGES README httpd.conf* mod_security-manual-*.pdf
%config(noreplace) %{ap_sysconfdir}/mod_security-snortrules.conf
%config(noreplace) %{ap_confd}/%{mod_conf}
%{ap_extralibs}/%{mod_so}
%{ap_webdoc}/*
%{_sbindir}/snort2modsec.pl

%changelog
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
