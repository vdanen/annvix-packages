%define name	perl-%{module}
%define module	DB_File
%define version	1.808
%define release	2avx

%define perl_archlib %(eval "`perl -V:installarchlib`"; echo $installarchlib)

Summary:	Perl module for use of the Berkeley DB version 1
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/DB_File/
Source0:	%{module}-%{version}.tar.bz2
Patch:		%{module}-1.805-makefile.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot/
BuildRequires:	db-devel perl-devel

%description
DB_File is a module which allows Perl programs to make use of the
facilities provided by Berkeley DB version 1. (DB_File can be built with
version 2 or 3 of Berkeley DB, but it will only support the 1.x
features), 

If you want to make use of the new features available in Berkeley DB
2.x or 3.x, use the Perl module BerkeleyDB instead. 

Berkeley DB is a C library which provides a consistent interface to a 
number of database formats. DB_File provides an interface to all three
of the database types (hash, btree and recno) currently supported by
Berkeley DB.

For further details see the documentation included at the end of the
file DB_File.pm.                

%prep
%setup -q -n %{module}-%{version}
%patch -p1

%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
%make
make test

%clean 
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
eval `perl '-V:installarchlib'`
mkdir -p $RPM_BUILD_ROOT/$installarchlib
%makeinstall_std

%files
%defattr(-,root,root)
%doc README
%{perl_vendorarch}/*.pm
%{perl_vendorarch}/auto/DB_File
%_mandir/man3*/DB_File.*

%changelog
* Sat Jun 26 2004 Vincent Danen <vdanen@annvix.org> 1.808-2avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.808-1sls
- 1.808
- fix url

* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 1.806-6sls
- OpenSLS build
- tidy spec

* Thu Sep 04 2003 Fran�ois Pons <fpons@mandrakesoft.com> 1.806-5mdk
- use db-devel instead of libdb4.1-devel.

* Thu Aug 14 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 1.806-4mdk
- rebuild against db4.1 and new perl
- use %%make macro
- use %%makeinsta_std macro
- enable tests

* Sat Jul 19 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 1.806-3mdk
- rebuild

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.806-2mdk
- disable broken test for now
- rebuild for new auto{prov,req}

* Fri Oct 25 2002 Fran�ois Pons <fpons@mandrakesoft.com> 1.806-1mdk
- removed patch to manage perl context as now integrated.
- 1.806.

* Wed Oct 16 2002 Fran�ois Pons <fpons@mandrakesoft.com> 1.805-1mdk
- added patch to manage perl context correctly for callback.
- added patch to install in right directory.
- 1.805.

* Wed Aug 07 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.804-3mdk
- rebuild for latest perl.

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.804-2mdk
- rebuild for perl 5.8.0

* Mon Jun 10 2002 Fran�ois Pons <fpons@mandrakesoft.com> 1.804-1mdk
- 1.804.

* Tue Mar 26 2002 Fran�ois Pons <fpons@mandrakesoft.com> 1.803-1mdk
- 1.803.

* Fri Jan 18 2002 Fran�ois Pons <fpons@mandrakesoft.com> 1.802-1mdk
- 1.802.

* Thu Nov 08 2001 Fran�ois Pons <fpons@mandrakesoft.com> 1.79-1mdk
- 1.79.

* Tue Oct 16 2001 Stefan van der Eijk <stefan@eijk.nu> 1.78-2mdk
- BuildRequires: db3-devel perl-devel

* Fri Aug 31 2001 Fran�ois Pons <fpons@mandrakesoft.com> 1.78-1mdk
- 1.78.
- remove filelist, now use globing and macros.

* Tue Aug 28 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.73-5mdk
- Clean rebuild against libdb-3.2

* Thu Jul 19 2001 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.73-4mdk
- rebuild with new libdb-3.2
- sanitize spec file (s/Copyright/License, distribution tag, docs, license)
- renamed spec file to perl-DB_File.spec

* Wed Apr 25 2001 Pixel <pixel@mandrakesoft.com> 1.73-3mdk
- rebuild with new perl

* Sat Sep 16 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 1.73-2mdk
- Call spec-helper before creating filelist

* Wed Aug 09 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.73-1mdk
- Completely re-made (macroize) package for 1.73 (update)

