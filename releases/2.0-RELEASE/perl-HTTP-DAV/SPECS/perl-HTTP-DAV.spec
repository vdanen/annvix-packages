#
# spec file for package perl-HTTP-DAV
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		HTTP-DAV
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.31
%define release		%_revrel

Summary:	PerlDAV -- A WebDAV client library for Perl5
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org/
Source:		http://www.cpan.org/authors/id/P/PC/PCOLLINS/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel
BuildRequires:	perl-libwww-perl
BuildRequires:	perl-XML-DOM
BuildRequires:	perl-Crypt-SSLeay
BuildRequires:	perl-MD5

%description
PerlDAV is a Perl library for modifying content on webservers using the
WebDAV protocol. Now you can LOCK, DELETE and PUT files and much more on
a DAV-enabled webserver.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}
find . -type d -exec chmod 0755 {} \;
find . -type f -exec chmod 0644 {} \;

%build
perl Makefile.PL INSTALLDIRS=vendor
make


%check
# requires a "test server"...
#make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/dave
%{perl_vendorlib}/HTTP/DAV.pm
%{perl_vendorlib}/HTTP/DAV/*.pm
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README Changes TODO


%changelog
* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.31
- first Annvix build (needed by http's make test)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
