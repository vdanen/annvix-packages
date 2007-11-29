#
# spec file for package mt-st
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mt-st
%define version		0.9b
%define release		%_revrel

Summary:	Programs to control tape device operations
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Archiving
URL:		ftp://metalab.unc.edu/pub/Linux/system/backup/
Source0:	ftp://metalab.unc.edu/pub/Linux/system/backup/mt-st-%{version}.tar.gz
Patch0:		mt-st-0.8-redhat.patch
Patch1:		mt-st-0.7-SDLT.patch
Patch2:		mt-st-0.7-config-files.patch
Patch3:		mt-st-0.9b-manfix.patch
Patch4:		mt-st-0.9b-mtio.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}


%description
The mt-st package contains the mt and st tape drive management
programs. Mt (for magnetic tape drives) and st (for SCSI tape devices)
can control rewinding, ejecting, skipping files and blocks and more.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .redhat
%patch1 -p1 -b .sdlt
%patch2 -p1 -b .configfiles
%patch3 -p1 -b .manfix
%patch4 -p1 -b .mtio


%build
%make CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make install mandir=%{_mandir}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/bin/mt
/sbin/stinit
%{_mandir}/man1/mt.1*
%{_mandir}/man8/stinit.8*

%files doc
%defattr(-,root,root)
%doc COPYING README README.stinit mt-st-%{version}.lsm stinit.def.examples


%changelog
* Wed Nov 28 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.9b
- 0.9b
- sync with Mandriva 0.9b-3 (which was a sync of mt-st-0.9b-4.fc8)

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.8
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.8
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.8
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.8
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.8-1avx
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
