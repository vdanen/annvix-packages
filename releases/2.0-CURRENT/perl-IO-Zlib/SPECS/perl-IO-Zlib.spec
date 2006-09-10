#
# spec file for package perl-IO-Zlib
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		IO-Zlib
%define revision	$Rev$
%define name		perl-%{module}
%define version		1.04
%define release		%_revrel

Summary:	IO:: style interface to Compress::Zlib
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source0:	http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	perl(Compress::Zlib)
BuildArch:	noarch

%description
IO::Zlib provides an IO:: style interface to Compress::Zlib and hence
to gzip/zlib compressed files. It provides many of the same methods as
the IO::Handle interface.


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


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/IO/*
%{_mandir}/man?/*

%files doc
%defattr(-,root,root)
%doc ChangeLog README


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.04
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Tue Mar 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.04
- first Annvix build (for spamassassin)

* Tue Jun 14 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.04-2mdk
- Rebuild

* Thu Oct 14 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.04-1mdk
- 1.04

* Mon Aug 23 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.03-1mdk
- 1.03

* Wed Jun 30 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.01-1mdk
- first version of rpm.

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
