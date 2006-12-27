#
# spec file for package perl-File-Slurp
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		perl-%{module}
%define module		File-Slurp
%define version		9999.12
%define release		%_revrel

Summary:	Efficient Reading/Writing of Complete Files
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Development/Perl
License:	GPL or Artistic
URL:		http://search.cpan.org/dist/%{module}/
Source:		http://search.cpan.org/CPAN/authors/id/U/UR/URI/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
This module provides subs that allow you to read or write entire files with one
simple call. They are designed to be simple to use, have flexible ways to pass
in or get the file contents and to be very efficient. There is also a sub to
read in all the files in a directory other than . and ..

These slurp/spew subs work for files, pipes and sockets, and stdio,
pseudo-files, and DATA.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}
chmod 0644 lib/File/Slurp.pm


%build
perl Makefile.PL INSTALLDIRS=vendor
%make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
find %{buildroot} -name "perllocal.pod" | xargs -i rm -f {}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/man3*/*
%{perl_vendorlib}/File

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 9999.12
- rebuild against perl 5.8.8
- create -doc subpackage

* Fri Apr 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 9999.12
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
