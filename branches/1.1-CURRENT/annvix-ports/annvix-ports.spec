#
# spec file for package annvix-ports
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id: annvix-ports.spec,v 1.2 2005/10/03 02:59:26 vdanen Exp $

%define name		annvix-ports
%define version		1.1
%define release		5avx

%define _portsprefix /usr/local

Summary:	Annvix ports package
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://annvix.org/
Group:		System/Configuration/Other
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	cvs, curl, rpm-build


%description
The filesystem layout and builder scripts for Annvix ports.


%prep
%setup -q

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_portsprefix}/ports/{ports,packages/{RPMS,SRPMS},override}
install -m 0644 README %{buildroot}%{_portsprefix}/ports/README
install -m 0754 builder %{buildroot}%{_portsprefix}/ports/builder
install -m 0754 build.sh %{buildroot}%{_portsprefix}/ports/ports/build.sh


%pre
%_pre_useradd builder %{_portsprefix}/ports /bin/sh 403


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{_portsprefix}/ports
%attr(0775,root,admin) %dir %{_portsprefix}/ports/packages
%attr(0775,root,admin) %dir %{_portsprefix}/ports/packages/RPMS
%attr(0775,root,admin) %dir %{_portsprefix}/ports/packages/SRPMS
%attr(2775,root,admin) %dir %{_portsprefix}/ports/ports
%attr(1775,root,admin) %dir %{_portsprefix}/ports/override
%{_portsprefix}/ports/README
%attr(0754,root,admin) %{_portsprefix}/ports/builder
%attr(0754,root,admin) %{_portsprefix}/ports/ports/build.sh


%changelog
* Mon Oct 03 2005 Vincent Danen <vdanen@annvix.org> 1.1-5avx
- fix some wierdness with the spec that turned README into README.ports

* Sun Oct 02 2005 Vincent Danen <vdanen@annvix.org> 1.1-4avx
- add uid/gid 403 for user builder (in prep of a single-uid
  controlled ports build system)

* Wed Aug 10 2005 Vincent Danen <vdanen@annvix.org> 1.1-3avx
- bootstrap build (new gcc, new glibc)

* Fri Aug 05 2005 Vincent Danen <vdanen@annvix.org> 1.1-2avx
- make builder chmod files after checkout from CVS so they're
  writable by group admin
- make /usr/local/ports/ports g+s so any new files are owned by
  user:admin (but since we don't change the umask, we still need
  to chmod)
- make /usr/local/ports/override to mimic the system /override for
  building rpm packages

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
