#
# spec file for package hwdata
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		hwdata
%define version		0.152
%define release		%_revrel

Summary:	Hardware identification and configuration data
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL/MIT
Group:		System/Base
Source: 	hwdata-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

%description
hwdata contains various hardware identification and configuration data,
such as the pci.ids database, the XFree86 Cards and MonitorsDb databases.


%prep
%setup -q


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# remove hotplug file, we don't use hotplug or support pcmcia
rm -rf %{buildroot}%{_sysconfdir}/{hotplug,pcmcia}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir /usr/share/hwdata
%config /usr/share/hwdata/*
# This file is screaming to be moved into /usr/share/hwdata sometime <g>
/usr/X11R6/lib/X11/Cards


%changelog
* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.152
- drop the docs (LICENSE, COPYING)... this is standard stuff in common-licenses

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.152
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.152
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.152
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.152-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.152-2avx
- rebuild

* Wed Mar 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.152-1avx
- 0.152

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.145-1avx
- 0.145
- remove config files for pcmcia and hotplug

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.111-2avx
- Annvix build

* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> 0.111-1sls
- first OpenSLS build; from Fedora
