#
# spec file for package httpd-mod_apparmor
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
%define apache_version	2.2.3
%define mod_version	2.0
%define mod_name	mod_apparmor
%define mod_conf	01_%{mod_name}.conf
%define mod_so		%{mod_name}.so
%define sourcename	%{mod_name}-%{mod_version}

Summary:	AppArmor module for Apache
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Servers
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	apache2-mod-apparmor-%{mod_version}-6354.tar.gz
Source1:	%{mod_conf}

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  httpd-devel >= %{apache_version}
BuildRequires:	libapparmor-devel

Requires(pre):	httpd >= %{apache_version}
Requires(pre):	libapparmor
Requires(pre):	httpd-conf >= 2.2.2

%description
httpd-mod-apparmor adds support to Apache to provide AppArmor
confinement to individual cgi scripts handled by apache modules like
mod_php and mod_perl.

This package is part of a suite of tools that used to be named SubDomain.


%prep
%setup -q -n apache2-mod-apparmor-%{mod_version}


%build
make %{mod_name}.so APXS=%{_sbindir}/apxs


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p %{buildroot}%{_libdir}/httpd-extramodules
mkdir -p %{buildroot}%{_sysconfdir}/httpd/modules.d
install -m 0755 *.so %{buildroot}%{_libdir}/httpd-extramodules/
cat %{_sourcedir}/%{mod_conf} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}


%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/httpd-extramodules/%{mod_so}


%changelog
* Wed Aug 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.2.3_2.0
- first Annvix build
