#
# spec file for package perl-ldap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		perl-ldap
%define version 	0.34
%define release 	%_revrel

Summary:	Perl module for ldap
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%name/
Source:		http://www.cpan.org/authors/id/G/GB/GBARR/%{name}-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel >= 5.8.0
BuildRequires:	perl(Convert::ASN1) >= 0.07
BuildRequires:	perl(IO::Socket::SSL)
BuildRequires:	perl(GSSAPI)
BuildRequires:	perl(Digest::MD5)
BuildRequires:	perl(Digest::HMAC_MD5)
BuildRequires:	perl(URI::ldap)
BuildRequires:	perl(IO::Socket::SSL)
BuildRequires:	perl(MIME::Base64)

Requires:	perl(Authen::SASL) >= 2.00
Requires:	perl(XML::Parser)
Requires:	perl(Convert::ASN1) >= 0.07

%description
The perl-ldap distribution is a collection of perl modules
which provide an object-oriented interface to LDAP servers.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}

# fix the perl path
find -type f | xargs perl -pi -e "s|/usr/local/bin/perl|%{_bindir}/perl|g"
chmod 0644 contrib/*

cat > test.cfg << EOF
\$SERVER_EXE = "%{_sbindir}/slapd";
\$SERVER_TYPE = "openldap2+ssl+ipc+sasl";
\$HOST = "localhost";
\$SCHEMA_DIR = "%{_datadir}/openldap/schema";
\$EXTERNAL_TESTS = 0;
1;
EOF


%build
perl Makefile.PL INSTALLDIRS=vendor </dev/null
%make


%check
%make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{perl_vendorlib}/LWP
%{perl_vendorlib}/Bundle
%{perl_vendorlib}/Net

%files doc
%defattr(-,root,root)
%doc CREDITS README contrib


%changelog
* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.34
- enable all the tests

* Mon Jul 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.34
- 0.34
- updated buildrequires

* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.33
- 0.33
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy
- update description
- fix license
- BuildRequires: perl(Convert::ASN1), perl(IO::Socket::SSL)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.31
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.31
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.31-6avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.31-5avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.31-4avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.31-3avx
- rebuild against new perl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.31-2avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.31-1sls
- 0.31
- own dirs

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 0.29-3sls
- rebuild for new perl

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 0.29-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
