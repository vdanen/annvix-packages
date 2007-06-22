#
# spec file for package perl-XML-Parser
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		XML-Parser
%define	revision	$Rev$
%define	name		perl-%{module}
%define	version		2.34
%define	release		%_revrel

Summary: 	A perl module for parsing XML documents
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Development/Perl
URL: 		http://www.cpan.org
Source: 	http://www.cpan.org/authors/id/C/CO/COOPERCL/%{module}-%{version}.tar.bz2
Source1:	http://uucode.com/xml/perl/enc.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	chrpath
BuildRequires: 	expat-devel
BuildRequires:	perl-devel
BuildRequires:	perl-libwww-perl
BuildRequires:	perl(HTML::Parser)

%description
A perl module for parsing XML documents.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version} -a 1


%build
perl Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="%{optflags}"


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
install -m 0644 enc/koi8-r.enc %{buildroot}%{perl_vendorarch}/XML/Parser/Encodings
chrpath -d %{buildroot}%{perl_vendorarch}/auto/XML/Parser/Expat/Expat.so


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{perl_vendorarch}/XML/Parser*
%{perl_vendorarch}/auto/XML/Parser*

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Thu Jun 21 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.34
- rebuild against new expat
- nuke the rpath (and buildrequires chrpath as a result)
- drop the requires on libexpat0; the library requires will pick up what
  it needs

* Fri May 26 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.34
- fix the requires so it works on x86_64 too

* Mon May 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.34
- rebuild against perl 5.8.8
- create -doc subpackage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.34
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.34
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.34-10avx
- rebuild against new expat

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.34-9avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.34-8avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.34-7avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.34-6avx
- rebuild against new perl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.34-5avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.34-4sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 2.34-3sls
- rebuild for new perl
- minor spec cleanups

* Mon Dec 13 2003 Vincent Danen <vdanen@opensls.org> 2.34-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
