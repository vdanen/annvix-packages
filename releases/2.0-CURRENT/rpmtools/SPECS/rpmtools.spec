#
# spec file for package rpmtools
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rpmtools
%define version		5.0.28
%define release 	%_revrel

Summary:	Contains various rpm command-line tools
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://cvs.mandriva.com/cgi-bin/cvsweb.cgi/soft/rpmtools
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	rpm-devel >= 4.0.3
BuildRequires:	perl(Compress::Zlib)
BuildRequires:	perl(MDV::Packdrakeng)
BuildRequires:	perl(MDV::Distribconf)

Requires:	rpm >= 4.2.3
Requires:	bzip2 >= 1.0
Conflicts:	rpmtools-compat <= 2.0
Conflicts:	rpmtools-devel <= 2.0
Provides:	perl(packdrake)

%description
Various tools needed by urpmi and drakxtools for handling rpm files.


%prep
%setup -q


%build
perl Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="%{optflags}"


%check
%make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/dumpdistribconf
%{_bindir}/packdrake
%{_bindir}/parsehdlist
%{_bindir}/rpm2header
%{_bindir}/gendistrib
%{_bindir}/genhdlist
%{_bindir}/rpm2cpio.pl
%{perl_vendorlib}/Distribconf*
%{perl_vendorlib}/packdrake.pm
%{perl_vendorlib}/Packdrakeng.pm
%{perl_vendorlib}/Packdrakeng
%{perl_vendorlib}/Packdrakeng/zlib.pm
%{_mandir}/*/*


%changelog
* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.0.28
- rebuild against perl 5.8.8

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.0.28
- fix group

* Fri Apr 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.0.28
- 5.0.28
- fix requires, including deps on new perl-MDV-{Packdrakeng,Distribconf} modules

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.0.24
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.0.24
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.0.24-1avx
- 5.0.24

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.0.23-1avx
- 5.0.23

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.0.18-4avx
- bootstrap build (new gcc, new glibc)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.0.18-3avx
- build for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.0.18-2avx
- bootstrap build

* Thu Mar 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.0.18-1avx
- 5.0.18

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.0.16-1avx
- 5.0.16:
  - generate hdlists and synthesis as hard links in <name>/media_info subdirs
  - handle new hdlists format
  - generate MD5SUM files
  - add Distribconf.pm and dumpdistribconf to manage distrib config
  - gendistrib uses Distribconf.pm
  - gendistrib skip media if suppl or askmedia is set
  - Distribconf manage pubkey
  - fix undefined handle in write_hdlists
  - generate VERSION
  - split Distribconf with Build
  - gendistrib: --skipmissingdir
  - gendistrib: perform little check
  - packdrake: report size of toc
  - parsehdlist: add support to output SQL statements (Leon Brooks)
- NOTE: unlike mdk, we are not breaking out packdrake into it's own pkg

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.0.9-1avx
- 5.0.9 (sync with 1mdk):
  - add rpm2cpio.pl
  - BuildRequires: perl-Compress-Zlib
  - drop the requirement on Compress::Zlib for packdrake

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.5-17avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 4.5-16sls
- sync with 20mdk:
  - add some options to gendistrib/genhdlist (thauvin)
  - add provides perl(packdrake) (warly)
  - add --dest option to genhdlist (thauvin)
  - fix dir parsing (Thx Pascal Terjan) (thauvin)
  - fix genhdlist without arg (thauvin)
  - add a --quiet option to packdrake (rafael)
  - add a dep on perl-base (rafael)

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 4.5-15sls
- minor spec cleanups
- remove %%prefix

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 4.5-14sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
