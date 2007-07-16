#
# spec file for package perl-CGI
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		CGI
%define revision	$Rev$
%define name		perl-%{module}
%define version		3.29
%define release		%_revrel
%define epoch		1

Summary:        Simple Common Gateway Interface class for Perl
Name:           %{name}
Version:        %{version}
Release:        %{release}
Epoch:		%{epoch}
License:        GPL or Artistic
Group:          Development/Perl
URL:            http://stein.cshl.org/WWW/software/CGI/
Source:		http://search.cpan.org/CPAN/authors/id/L/LD/LDS/CGI.pm-%{version}.tar.gz

BuildRoot:      %{_buildroot}/%{name}-%{version}
BuildArch:      noarch
BuildRequires:  perl-devel

%description
This perl library uses perl5 objects to make it easy to create Web fill-out
forms and parse their contents.  This package defines CGI objects, entities
that contain the values of the current query string and other state
variables.  Using a CGI object's methods, you can examine keywords and
parameters passed to your script, and create forms whose initial values are
taken from the current query (thereby preserving state information).


%package Fast
Group:		Development/Perl
Summary: 	CGI Interface for Fast CGI
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description Fast
CGI::Fast is a subclass of the CGI object created by CGI.pm. It is
specialized to work well with the Open Market FastCGI standard, which
greatly speeds up CGI scripts by turning them into persistently running
server processes.  Scripts that perform time-consuming initialization
processes, such as loading large modules or opening persistent database
connections, will see large performance improvements.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}.pm-%{version}


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
%{perl_vendorlib}/CGI
%exclude %{perl_vendorlib}/CGI/Fast.pm
%{perl_vendorlib}/*.pm
%{_mandir}/man3/*
%exclude %{_mandir}/man3/CGI::Fast.3pm.*

%files Fast
%defattr(-,root,root)
%{perl_vendorlib}/CGI/Fast.pm
%{_mandir}/man3/CGI::Fast.3pm.*

%files doc
%defattr(-,root,root)
%doc Changes README *.html examples


%changelog
* Mon Jul 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.29
- 3.29

* Wed May 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.16
- 3.16
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.05
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.05
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.05-6avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.05-5avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.05-4avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.05-3avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.05-2avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 3.05-1sls
- 3.0.5

* Mon Apr 12 2004 Vincent Danen <vdanen@opensls.org> 3.00-4sls
- fix epoch in requires

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 3.00-3sls
- rebuild for new perl
- small spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 3.00-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
