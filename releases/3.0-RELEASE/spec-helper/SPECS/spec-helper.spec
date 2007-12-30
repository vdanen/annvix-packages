#
# spec file for package spec-helper
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		spec-helper
%define version 	0.27.2
%define release 	%_revrel

Summary:	Tools to ease the creation of rpm packages
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.mandriva.com
Source0:	%{name}-%{version}.tar.bz2
Patch0:		spec-helper-0.27.2-avx-compress_in_usr_local.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	perl
Requires:	ldconfig
Requires:	findutils
Requires:	python
Requires:	gettext

%description
Tools to ease the creation of rpm packages for the Annvix distribution.
Compress man pages using bzip2, strip executables, convert links...


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make install DESTDIR=%{buildroot} bindir=%{_bindir} rpmmacrosdir=%{_sys_macros_dir}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/macroszification
%{_datadir}/spec-helper
%{_sys_macros_dir}/%{name}.macros

%files doc
%defattr(-,root,root)
%doc AUTHORS README NEWS


%changelog
* Mon Dec 10 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.27.2
- P0: compress info and manpages found in /usr/local/share/...

* Mon Oct 01 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.27.2
- 0.27.2
- drop P0; fixed upstream

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.24
- 0.24
- P0: fix issue where pam.d/* symlinks would be turned into regular
  files due to the perl call in fixpamd

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.23
- 0.23
- hack out some %%mkrel junk to make "make" happier
- add -doc subpackage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.11
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.11-4avx
- correct the buildroot

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.11-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.11-2avx
- bootstrap build

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.11-1avx
- 0.11
  - handle filenames starting with - (flepid)
  - other cleanups and speedups (tvignaud)
  - use "" around the section name in spec-helper (flepied)

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.2-6avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 0.9.2-5sls
- minor spec cleanups
- remove %%prefix
- remove %%build_openssls

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 0.9.2-4sls
- OpenSLS build
- tidy spec
- fix URL

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
