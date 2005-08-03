#
# spec file for package annvix-ports
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#

%define name		annvix-ports
%define version		1.1
%define release		1avx

%define _portsprefix /usr/local

Summary:	Annvix ports package
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://annvix.org/
Group:		System/Configuration/Other
Source0:	README.ports
Source1:	builder.ports
Source2:	build.sh.ports

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	cvs, curl, rpm-build


%description
The filesystem layout and builder scripts for Annvix ports.


%prep

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_portsprefix}/ports/{ports,packages/{RPMS,SRPMS}}
install -m 0644 %{SOURCE0} %{buildroot}%{_portsprefix}/ports
install -m 0754 %{SOURCE1} %{buildroot}%{_portsprefix}/ports/builder
install -m 0754 %{SOURCE2} %{buildroot}%{_portsprefix}/ports/ports/build.sh


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
%attr(0754,root,admin) %{_portsprefix}/ports/builder
%attr(0754,root,admin) %{_portsprefix}/ports/ports/build.sh


%changelog
* Wed Aug 03 2005 Vincent Danen <vdanen@annvix.org> 1.1-1avx
- 1.1 (aka ports should work now even if it's not 100%)

* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 1.0-4avx
- rebuild

* Mon Mar 28 2005 Vincent Danen <vdanen@annvix.org> 1.0-3avx
- Annvix build

* Thu Jun  3 2004 Vincent Danen <vdanen@opensls.org> 1.0-2sls
- Requires: rpm-build

* Fri May 28 2004 Vincent Danen <vdanen@opensls.org> 1.0-1sls
- first package
