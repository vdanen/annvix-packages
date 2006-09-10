#
# spec file for package perl-Devel-Symdump
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		perl-%{module}
%define module		Devel-Symdump
%define version 	2.03
%define release 	%_revrel

Summary:	%{module} module for perl
Name:		perl-%{module}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
%{module} module for perl


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/Devel
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc ChangeLog README


%changelog
* Thu May 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.03
- rebuild against perl 5.8.8
- create -doc subpackage

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.03
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.03
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.03-12avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.03-11avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.03-10avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.03-9avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.03-8avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.03-7sls
- rebuild for perl 5.8.4

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 2.03-6sls
- rebuild for new perl
- minor spec cleanups

* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 2.03-5sls
- OpenSLS build
- tidy spec

* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.03-4mdk
- rebuild for new perl
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.03-3mdk
- rebuild for new auto{prov,req}

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 2.03-2mdk
- rebuild for perl 5.8.0

* Mon May 13 2002 François Pons <fpons@mandrakesoft.com> 2.03-1mdk
- 2.03.

* Tue Mar 26 2002 François Pons <fpons@mandrakesoft.com> 2.02-1mdk
- remove filelist and use a right %%files.
- updated License.
- 2.02.

* Tue Oct 16 2001 Stefan van der Eijk <stefan@eijk.nu> 2.01-5mdk
- BuildRequires: perl-devel

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.01-4mdk
- Rebuild this against the latest perl.
- Remove hardcoded references to Distribution and Vendor.

* Tue Mar 13 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.01-3mdk
- BuildArch: noarch
- add docs
- rename spec file
- clean spec a bit
- run automated tests

* Sat Sep 16 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 2.01-2mdk
- Call spec-helper before creating filelist

* Wed Aug 09 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.01-1mdk
- Macroize package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
