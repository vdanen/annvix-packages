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
%define version		1.08
%define release		%_revrel

Summary:	IO:: style interface to Compress::Zlib
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source0:	http://www.cpan.org/modules/by-module/IO/%{module}-%{version}.tar.gz

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
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.08
- 1.08

* Wed Dec 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.04
- spec cleaning

* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.04
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Tue Mar 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.04
- first Annvix build (for spamassassin)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
