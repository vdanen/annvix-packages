#
# spec file for package perl-File-Slurp
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		perl-%{module}
%define module		File-Slurp
%define version		9999.12
%define release		%_revrel

Summary:	Efficient Reading/Writing of Complete Files
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Development/Perl
License:	GPL or Artistic
URL:		http://search.cpan.org/dist/%{module}/
Source:		http://search.cpan.org/CPAN/authors/id/U/UR/URI/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildArch:	noarch

%description
This module provides subs that allow you to read or write entire files with one
simple call. They are designed to be simple to use, have flexible ways to pass
in or get the file contents and to be very efficient. There is also a sub to
read in all the files in a directory other than . and ..

These slurp/spew subs work for files, pipes and sockets, and stdio,
pseudo-files, and DATA.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}
chmod 0644 lib/File/Slurp.pm


%build
perl Makefile.PL INSTALLDIRS=vendor
%make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
find %{buildroot} -name "perllocal.pod" | xargs -i rm -f {}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/man3*/*
%{perl_vendorlib}/File

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 9999.12
- rebuild against perl 5.8.8
- create -doc subpackage

* Fri Apr 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 9999.12
- first Annvix build

* Tue Mar 07 2006 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 9999.12-1mdk
- 9999.12

* Wed Jan 25 2006 Guillaume Rousse <guillomovitch@mandriva.org> 9999.11-1mdk
- new version
- spec cleanup
- rpmbuildupdate aware
- fix directory ownership
- better summary and description

* Mon May 02 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 9999.09-1mdk
- 9999.09

* Mon Jan 31 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 9999.07-1mdk
- 9999.07

* Tue Nov 16 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 9999.06-1mdk
- 9999.06

* Wed Apr 21 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 9999.04-1mdk
- 9999.04
- correct license
- spec cosmetics

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2002.1031-3mdk
- rebuild for new perl
- macroize
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Fri Jul 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2002.1031-2mdk
- buildrequires

* Thu Jun 26 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2002.1031-1mdk
- Initial build.
