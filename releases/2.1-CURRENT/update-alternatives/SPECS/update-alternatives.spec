#
# spec file for package update-alternatives
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# mdk 1.8.4-1mdk
#
# $Id$

%define revision	$Rev$
%define name		update-alternatives
%define version		1.8.4
%define release		%_revrel

Summary:	Alternative management system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://cvs.mandriva.com/cgi-bin/cvsweb.cgi/soft/update-alternatives/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		update-alternatives-1.8.4-avx-annvix.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Conflicts:	rpm < 4.4.1

%description
Utility for managing concurent software. Original version comes from
Debian but has been patched by Mandriva for use with rpm systems.


%prep
%setup -q
%patch0 -p1 -b .avx


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%make install DESTDIR=%{buildroot} prefix=%{_prefix}

mkdir -p %{buildroot}%{_sysconfdir}/alternatives
mkdir -p %{buildroot}%{_localstatedir}/rpm/alternatives


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{_sysconfdir}/alternatives
%{_sbindir}/update-alternatives
%{_mandir}/man8/update-alternatives.8*
%dir %{_localstatedir}/rpm/alternatives


%changelog
* Sat Jun 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.8.4
- 1.8.4
- P0 to remove Mandriva references

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3
- fix group

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.8.3-1avx
- first Annvix build to go with new rpm

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
