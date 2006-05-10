#
# spec file for package perl-Archive-Tar
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$  

%define	module		Archive-Tar
%define revision	$Rev$
%define	name		perl-%{module}
%define version		1.29
%define release		%_revrel

Summary:	Perl module for manipulation of tar archives
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source0:	http://search.cpan.org/CPAN/authors/id/K/KA/KANE/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
Perl module for manipulation of tar archives.


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
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%{perl_vendorlib}/Archive
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_bindir}/*

%files doc
%doc README


%changelog
* Tue May 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.29
- rebuild against perl 5.8.8
- create -doc subpackage

* Tue Mar 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.29
- first Annvix build (for spamassassin)

* Mon Mar 06 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.29-1mdk
- 1.29

* Wed Jan 25 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.28-1mdk
- 1.28

* Fri Sep 23 2005 Guillaume Rousse <guillomovitch@mandriva.org> 1.26-1mdk
- New release 1.26
- drop patch0 (merged upstream)
- fix directory ownership
- spec cleanup

* Mon Aug 22 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.25-1mdk
- 1.25
- Doesn't depend on IO::String anymore
- Install ptardiff(1) utility (patch0, upstream bug:)

* Tue May 03 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 1.24-1mdk
- 1.24

* Tue Dec 07 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.23-1mdk
- 1.23

* Wed Nov 24 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.22-1mdk
- 1.22

* Tue Nov 16 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.21-1mdk
- 1.21
- fix buildrequires

* Tue Jun 29 2004 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 1.10-1mdk
- 1.10
- cosmetics

* Mon May 24 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 1.09-1mdk
- 1.09
- the ptar utility returns.

* Wed Apr 21 2004 Michael Scherer <misc@mandrake.org> 1.08-1mdk 
- 1.08
- [DIRM]
- rpmbuildupdate aware

* Thu Aug 28 2003 François Pons <fpons@mandrakesoft.com> 1.05-1mdk
- removed ptar no more available.
- 1.05.

* Sat Aug 02 2003 Ben Reser <ben@reser.org> 0.22-9mdk
- mv rm buildroot from %%prep to %%install
- don't need perllocal.pod rm now.

* Sat Aug 02 2003 Ben Reser <ben@reser.org> 0.22-8mdk
- Use %%makeinstall_std now that it works on klama

* Sat Aug 02 2003 Ben Reser <ben@reser.org> 0.22-7mdk
- Use %%makeinstall

* Fri Aug  1 2003 Ben Reser <ben@reser.org> 0.22-6mdk
- Fix man path
- Macroification
- Quiet %%setup
- Fix unpackaged perllocal error

* Wed May 28 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.22-5mdk
- rebuild for new auto{prov,req}

* Fri Apr 25 2003 Pixel <pixel@mandrakesoft.com> 0.22-4mdk
- add "BuildRequires: perl-devel"

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 0.22-3mdk
- rebuild for perl 5.8.0

* Thu Aug 23 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.22-2mdk
- rebuild

* Wed Mar 28 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.22-1mdk
- added by Stefan van der Eijk <s.vandereijk@chello.nl> :
	- new in contrib
