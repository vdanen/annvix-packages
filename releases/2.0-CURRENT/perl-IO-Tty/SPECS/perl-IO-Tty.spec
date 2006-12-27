#
# spec file for package perl-IO-Tty
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		IO-Tty
%define	revision	$Rev$
%define	name		perl-%{module}
%define	version		1.07
%define	release		%_revrel

Summary:	IO-Tty perl module: interface to pseudo tty's
Name: 		%{name}
Version: 	%{version}
Release:	%{release} 
License: 	GPL
Group: 		Development/Perl
URL:		http://www.cpan.org
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/IO/%{module}-%{version}.tar.gz

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel

%description
The IO::Tty and IO::Pty modules provide an interface to pseudo tty's.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
CFLAGS="%{optflags}" perl Makefile.PL INSTALLDIRS=vendor
%make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%dir %{perl_vendorarch}/auto/IO/Tty
%{perl_vendorarch}/auto/IO/Tty/*
%{perl_vendorarch}/IO/*.pm
%dir %{perl_vendorarch}/IO/Tty
%{perl_vendorarch}/IO/Tty/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc ChangeLog README


%changelog
* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.07
- 1.07

* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.02
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.02
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.02
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.02-16avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.02-15avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.02-14avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.02-13avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.02-12avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.02-11sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 1.02-10sls
- rebuild for new perl
- minor spec cleanups

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 1.02-9sls
- sync with 8mdk (gbeauchesne): fix build on amd64

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.02-8sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
