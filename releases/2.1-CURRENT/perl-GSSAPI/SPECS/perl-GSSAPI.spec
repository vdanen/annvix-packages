#
# spec file for package perl-GSSAPI
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id: perl-Authen-SASL.spec 6558 2006-12-27 05:01:51Z vdanen $

%define module		GSSAPI
%define revision	$Rev: 6558 $
%define name		perl-%{module}
%define version 	0.24
%define release 	%_revrel

Summary:	%{module} module for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://search.cpan.org/CPAN/authors/id/A/AG/AGROLMS/%{module}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	gssapi-devel
BuildRequires:	krb5-devel

%description
This module gives access to the routines of the GSSAPI library, as described
in rfc2743 and rfc2744 and implemented by the Kerberos-1.2 distribution from
MIT.

Since 0.14 it also compiles and works with Heimdal. Lacks of Heimdal support
are gss_release_oid(), gss_str_to_oid() and fail of some tests. Have a look
at the tests in t/ directory too see what tests fail on Heimdal ( the *.t tests
are just skipping them at the moment)

The API presented by this module is a mildly object oriented reinterpretation
of the C API, where opaque C structures are Perl objects, but the style of
function call has been left mostly untouched. As a result, most routines modify
one or more of the parameters passed to them, reflecting the C call-by-reference
(or call-by-value-return) semantics.

All users of this module are therefore strongly advised to localize all usage
of these routines to minimize pain if and when the API changes.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="%{optflags}"


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
%{perl_vendorlib}/*

%files doc
%doc Changes README

%changelog
* Mon Jul 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.24
- first Annvix build

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
