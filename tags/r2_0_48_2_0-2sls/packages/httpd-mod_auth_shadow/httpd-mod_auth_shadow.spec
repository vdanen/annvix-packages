%define name	%{ap_name}-%{mod_name}
%define version %{ap_version}_%{mod_version}
%define release 2sls

# Module-Specific definitions
%define mod_version	2.0
%define mod_name	mod_auth_shadow
%define mod_conf	83_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

# New ADVX macros
%define ADVXdir %{_datadir}/ADVX
%{expand:%(cat %{ADVXdir}/ADVX-build)}
%{expand:%%global ap_version %(%{apxs} -q ap_version)}

Summary:	Shadow password authentication for the %{ap_name} web server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Servers
URL:		http://mod-auth-shadow.sourceforge.net/
Source0:	%{sourcename}.tar.bz2
Source1:	%{mod_conf}.bz2
Patch0:		%{sourcename}-register.patch.bz2
Patch1:		%{sourcename}-makefile.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
# Standard ADVX requires
BuildRequires:  ADVX-build >= 9.2
BuildRequires:  %{ap_name}-devel >= 2.0.44-6mdk

# Standard ADVX requires
Prereq:		%{ap_name} = %{ap_version}
Prereq:		%{ap_name}-conf
Provides: 	ADVXpackage
Provides:	AP20package

%description
%{mod_name} is an %{ap_name} module which authenticates against
the /etc/shadow file. You may use this module with a mode 400 
root:root /etc/shadow file, while your web daemons are running
under a non-privileged user.

%prep

%setup -q -n %{sourcename}
%patch0 -p0
%patch1 -p0

%build

export PATH="$PATH:/usr/sbin"
%make CFLAGS="%{optflags}" -f makefile

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%ADVXinstlib
%ADVXinstconf %{SOURCE1} %{mod_conf}
%ADVXinstdoc %{name}-%{version}

install -d %{buildroot}%{_sbindir}
install -m4755 validate %{buildroot}%{_sbindir}/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post
%ADVXpost

%postun
%ADVXpost

%files
%defattr(-,root,root)
%doc CHANGES INSTALL README
%{ap_extralibs}/%{mod_so}
%config(noreplace) %{ap_confd}/%{mod_conf}
%{ap_webdoc}/*
%attr(4755,root,root) %{_sbindir}/validate

%changelog
* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.0.48_2.0-2sls
- OpenSLS build
- tidy spec

* Wed Nov 05 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.48_2.0-1mdk
- built for apache 2.0.48

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 2.0.47_2.0-2mdk
- Rebuild to fix bad signature

* Thu Jul 10 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.47_2.0-1mdk
- rebuilt against latest apache2, requires and buildrequires

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.46_2.0-1mdk
- rebuilt for apache v2.0.46
- buildrequires ADVX-build >= 9.2

* Fri Apr 11 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.45_2.0-3mdk
- cosmetic rebuild for apache v2.0.45

* Sat Feb 22 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44_2.0-3mdk
- fix another typo in config file (damn templates ;-)

* Sat Feb 22 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.0.44_2.0-2mdk
- fix typo in config file

* Tue Jan 21 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.44_2.0-1mdk
- initial cooker contrib
