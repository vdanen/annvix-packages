#
# spec file for package perl-Compress-Zlib
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		Compress-Zlib
%define	revision	$Rev$
%define	name		perl-%{module}
%define	version		2.008
%define	release		%_revrel

Summary:	Perl interface to the zlib compression library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/Compress/Compress-Zlib-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	zlib-devel
BuildRequires:	perl(IO::Compress::Gzip) >= %{version}
BuildRequires:	perl(Compress::Raw::Zlib) >= %{version}
BuildArch:	noarch

%description
The Compress::Zlib module provides a Perl interface to the zlib compression
library.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{perl_vendorlib}/Compress
%{perl_vendorlib}/auto/Compress

%files doc
%defattr(-,root,root)
%doc README


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.008
- 2.008
- this is a noarch package
- fix buildrequires

* Mon Jul 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.005
- 2.005
- updated buildrequires

* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.42
- 1.42

* Wed May 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.41
- rebuild against perl 5.8.8
- create -doc subpackage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.41
- 1.41
- minor spec cleanups

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.37
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.37
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.37
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.37-1avx
- 1.37
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.35-2avx
- bootstrap build (new gcc, new glibc)

* Thu Jul 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.35-1avx
- 1.35

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.33-2avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.33-1avx
- first Annvix build (required for rpmtools)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
