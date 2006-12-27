#
# spec file for package perl-FCGI
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define modname		FCGI
%define revision	$Rev$
%define name		perl-%{modname}
%define version		0.67
%define release 	%_revrel

Summary:	A Fast CGI module for Perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Distributable
Group:		Development/Perl
URL:		http://cpan.valueclick.com/authors/id/SKIMO/
Source0:	%{modname}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel

%description
This is a Fast CGI module for perl. It's based on the FCGI module that
comes with Open Market's FastCGI Developer's Kit, but does not require
you to recompile perl.

See <http://www.fastcgi.com/> for more information about fastcgi.
Lincoln D. Stein's perl CGI module also contains some information
about fastcgi programming.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{modname}-%{version}
chmod 0644 LICENSE.TERMS


%build
# Choose not to build a pure Perl implementation
# (default answer [n] -> return)
echo | CFLAGS="%{optflags}" perl Makefile.PL INSTALLDIRS=vendor
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{perl_vendorarch}/FCGI*
%{perl_vendorarch}/auto/FCGI

%files doc
%defattr(-,root,root)
%doc README LICENSE.TERMS ChangeLog


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org>  0.67
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.67
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.67
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.67-11avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.67-10avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.67-9avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.67-8avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.67-7avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.67-6sls
- rebuild for perl 5.8.4

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 0.67-5sls
- rebuild for new perl
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 0.67-4sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
