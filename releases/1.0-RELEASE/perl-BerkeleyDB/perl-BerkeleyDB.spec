%define module	BerkeleyDB
%define name	perl-%{module}
%define version	0.26
%define release	1avx

Summary:	Perl module for BerkeleyDB 2.x and greater
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/%{module}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot/
BuildRequires:	db4-devel perl-devel

%description
BerkeleyDB is a module which allows Perl programs to make use of the
facilities provided by Berkeley DB version 2 or greater. (Note: if
you want to use version 1 of Berkeley DB with Perl you need the DB_File
module).

Berkeley DB is a C library which provides a consistent interface to a
number of database formats. BerkeleyDB provides an interface to all
four of the database types (hash, btree, queue and recno) currently
supported by Berkeley DB.

For further details see the documentation in the file BerkeleyDB.pod.

%prep
%setup -q -n %{module}-%{version}

%build

CFLAGS="%{optflags}" %{__perl} Makefile.PL INSTALLDIRS=vendor
%make
make test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README Changes
%{perl_vendorlib}/*/Berkeley*
%{perl_vendorlib}/*/auto/Berkeley*
%{_mandir}/*/*

%changelog
* Tue Mar 01 2005 Vincent Danen <vdanen@annvix.org> 0.26-1avx
- first Annvix build

* Mon Nov 15 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.26-2mdk
- Rebuild for new perl. Fix URL

* Tue Oct 12 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.26-1mdk
- 0.26
- Add Changes file in documentation

* Fri Apr 23 2004 Michael Scherer <misc@mandrake.org> 0.25-1mdk
- 0.25
- rpmbuildupdate aware
 
* Sat Aug 16 2003 Götz Waschk <waschk@linux-mandrake.com> 0.23-2mdk
- build with libdb4.1

* Mon Aug 04 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.23-1mdk
- 0.23 (second times, fu... upload script)

* Sat Aug 02 2003 Ben Reser <ben@reser.org> 0.20-4mdk
- Macroize
- mv rm buildroot from %%prep to %%install
- %%makeinstall_std

* Thu Jul 17 2003 Götz Waschk <waschk@linux-mandrake.com> 0.20-3mdk
- rebuild for db4.1

* Wed May 14 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.20-2mdk
- rebuild for new autoprov

* Fri Jan 17 2003 François Pons <fpons@mandrakesoft.com> 0.20-1mdk
- add man pages.
- 0.20.

* Thu Dec 19 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.19-3mdk
- Don't hardcore arch in path

* Tue Aug 06 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.19-2mdk
- rebuild against latest perl.

* Fri Jul 19 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.19-1mdk
- 0.19

* Thu Apr 11 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.18-1mdk
- Initial Mandrake package
