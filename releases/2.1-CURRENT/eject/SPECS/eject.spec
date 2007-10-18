#
# spec file for package eject
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		eject
%define version 	2.1.5
%define release		%_revrel

Summary:	A program that ejects removable media using software control
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		http://ca.geocities.com/jefftranter%40rogers.com/eject.html
Source:		http://ca.geocities.com/jefftranter%40rogers.com/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gettext
BuildRequires:	automake1.9

%description
The eject program allows the user to eject removable media
(typically CD-ROMs, floppy disks or Iomega Jaz or Zip disks)
using software control. Eject can also control some multi-
disk CD changers and even some devices' auto-eject features.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}


%build
%configure
%make DEFAULTDEVICE="/dev/cdrom"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

%makeinstall ROOTDIR=%{buildroot} PREFIX=%{buildroot}/%{_prefix}

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/eject
%{_bindir}/volname
%{_mandir}/man1/eject.1*
%{_mandir}/man1/volname.1*

%files doc
%defattr(-,root,root)
%doc README TODO COPYING ChangeLog


%changelog
* Wed Oct 17 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5
- rebuild

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5
- spec cleanups
- remove locales

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5
- really remove docs from main package

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5
- 2.1.5
- add -doc subpackage
- rebuild with gcc4
- remove invalid locale directory

* Wed Jan 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.4
- 2.1.4
- update URL
- BuildRequires: automake1.9

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.13
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.13
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.13
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.13-9avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.13-8avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.13-7avx
- Annvix build

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 2.0.13-6sls
- minor spec cleanups
- remove the supermount patch

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 2.0.13-5sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
