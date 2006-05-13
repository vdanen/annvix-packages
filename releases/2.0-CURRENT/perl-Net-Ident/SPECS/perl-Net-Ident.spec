#
# spec file for package perl-Net-Ident
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module          Net-Ident
%define revision        $Rev$
%define name            perl-%{module}
%define version         1.20
%define release         %_revrel

%define _provides_exceptions perl(FileHandle)

Summary:	Net::Ident - lookup the username on the remote end of a TCP/IP connection
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2

Buildroot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
Net::Ident is a module that looks up the username on the remote
side of a TCP/IP connection through the ident (auth/tap) protocol
described in RFC1413 (which supersedes RFC931). Note that this
requires the remote site to run a daemon (often called identd) to
provide the requested information, so it is not always available
for all TCP/IP connections.


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
# tests are broken
#make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/Net/Ident.pm
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc Changes README


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.20
- rebuild against perl 5.8.8
- create -doc subpackage

* Tue Mar 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.20
- first Annvix build (for spamassassin)

* Thu Sep 15 2005 Oden Eriksson <oeriksson@mandriva.com> 1.20-1mdk
- initial Mandriva package
