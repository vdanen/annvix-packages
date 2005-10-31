%define name	annvix-ports
%define version	1.0
%define release	3avx

%define _portsprefix /usr/local

Summary:	Annvix ports package
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://annvix.org/
Group:		System/Configuration/Other
Source0:	README.ports
Source1:	Makefile.ports

BuildRoot:	%{_tmppath}/%{name}-root
BuildArch:	noarch

Requires:	make, cvs, curl, rpm-build


%description
The filesystem layout for the ports packages.

%prep

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_portsprefix}/ports/{ports,packages/{RPMS,SRPMS}}
install -m 0644 %{SOURCE0} %{buildroot}%{_portsprefix}/ports
install -m 0644 %{SOURCE1} %{buildroot}%{_portsprefix}/ports/Makefile

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_portsprefix}/ports
%attr(0775,root,admin) %dir %{_portsprefix}/ports/packages
%attr(0775,root,admin) %dir %{_portsprefix}/ports/packages/RPMS
%attr(0775,root,admin) %dir %{_portsprefix}/ports/packages/SRPMS
%attr(0775,root,admin) %dir %{_portsprefix}/ports/ports
%{_portsprefix}/ports/README.ports
%{_portsprefix}/ports/Makefile

%changelog
* Mon Mar 28 2005 Vincent Danen <vdanen@annvix.org> 1.0-3avx
- Annvix build

* Thu Jun  3 2004 Vincent Danen <vdanen@opensls.org> 1.0-2sls
- Requires: rpm-build

* Fri May 28 2004 Vincent Danen <vdanen@opensls.org> 1.0-1sls
- first package
