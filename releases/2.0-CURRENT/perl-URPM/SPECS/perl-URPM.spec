#
# spec file for package perl-URPM
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		URPM
%define revision	$Rev$
%define name		perl-%{module}
%define version 	1.44
%define release 	%_revrel

%define _require_exceptions perl(URPM::DB)\\|perl(URPM::Package)\\|perl(URPM::Transaction)

Summary:	URPM module for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://cvs.mandriva.com/cgi-bin/cvsweb.cgi/soft/perl-URPM
Source:		%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	rpm-devel >= 4.0.3

Requires:	rpm >= 4.2.3
Requires:	perl(MDV::Packdrakeng)
Provides:	perl(URPM::Build) = %{version}-%{release}
Provides:	perl(URPM::Resolve) = %{version}-%{release}
Provides:	perl(URPM::Signature) = %{version}-%{release}

%description
The URPM module allows you to manipulate rpm files, rpm header files and
hdlist files and manage them in memory.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
make OPTIMIZE="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorarch}/URPM.pm
%{perl_vendorarch}/URPM
%dir %{perl_vendorarch}/auto/URPM
%{perl_vendorarch}/auto/URPM/URPM.so
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc README ChangeLog


%changelog
* Tue Jul 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.44
- 1.44
- remove pre-Annvix changelog

* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.41
- rebuild against perl 5.8.8
- create -doc subpackage

* Tue May 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.41
- 1.41

* Fri Apr 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.40
- 1.40
- update requires

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.28
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.28
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Oct 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.28-1avx
- 1.28

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.27-2avx
- rebuild against new rpm

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.27-1avx
- 1.27
- rebuild against perl 5.8.7
- spec cleanups

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11-3avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11-2avx
- bootstrap build

* Thu Mar 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11-1avx
- 1.11

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.09-1avx
- 1.09

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.07-1avx
- 1.07
- remove unused requires (rgarciasuarez)
- include ChangeLog
- Requires: rpmtools >= 5.0.0
- Requires: perl-base >= 5.8.6

* Tue Sep 14 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.03-1avx
- 1.03

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.94-14avx
- Annvix build

* Sat Jun 11 2004 Vincent Danen <vdanen@opensls.org> 0.94-13sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 0.94-12sls
- rebuild for new perl
- remove %%build_opensls macros
- remove %%prefix tag

* Fri Dec 18 2003 Vincent Danen <vdanen@opensls.org> 0.94-11sls
- OpenSLS build
- tidy spec
- don't use %%real_release
- don't set Distribution tag

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
