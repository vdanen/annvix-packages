#
# spec file for package perl-BSD-Resource
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	revision	$Rev$
%define	name		perl-%{module}
%define	module		BSD-Resource
%define	version		1.24
%define	release		%_revrel

Summary:	%{module} module for perl 
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel

Requires:	perl

%description
%{module} module for perl


%prep
%setup -q -n %{module}-%{version} 
# perl path hack
find . -type f | xargs %{__perl} -p -i -e "s|^#\!/usr/local/bin/perl|#\!/usr/bin/perl|g"


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor </dev/null
%{__make}
%{__make} test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc ChangeLog README
%{perl_vendorlib}
%{_mandir}/man*/*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.24-1avx
- 1.24
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.22-10avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.22-9avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.22-8avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.22-7avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.22-6sls
- rebuild for perl 5.8.4

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 1.22-5sls
- rebuild for new perl

* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 1.22-4sls
- OpenSLS build
- tidy spec

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.22-3mdk
- rebuild for new perl
- don't use PREFIX
- use %%makeinstall_std macro
- cosmetics

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 1.22-2mdk
- Rebuild to fix bad signature

* Sat May 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.22-1mdk
- initial cooker contrib.
