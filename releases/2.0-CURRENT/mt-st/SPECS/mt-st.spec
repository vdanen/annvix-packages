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
%define version		0.8
%define release		%_revrel

Summary:	Programs to control tape device operations
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Archiving
URL:		http://ibiblio.org/pub/Linux
Source:		http://ibiblio.org/pub/Linux/system/backup/%{name}-%{version}.tar.bz2

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


%build
%make CFLAGS="%{optflags} -Wall" MANDIR=%{_mandir}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/{bin,sbin}
mkdir -p %{buildroot}%{_mandir}/man{1,8}
%makeinstall \
    MANDIR=%{buildroot}%{_mandir} \
    BINDIR=%{buildroot}/bin \
    SBINDIR=%{buildroot}/sbin


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
