#
# spec file for package perl-Pg
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define module		Pg
%define name		perl-%{module}
%define version		2.1.1
%define release		1avx

Summary:	A libpq-based PostgreSQL interface for Perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://gborg.postgresql.org/project/pgperl/projdisplay.php
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	postgresql-devel
BuildRequires:	postgresql-libs-devel

%description
pgperl is an interface between Perl and PostgreSQL. This uses the
Perl5 API for C extensions to call the PostgreSQL libpq interface.
Unlike DBD:pg, pgperl tries to implement the libpq interface as
closely as possible.

You have a choice between two different interfaces: the old
C-style interface and a new one, using a more Perl-ish style. The
old style has the benefit that existing libpq applications can
easily be ported to perl. The new style uses class packages and
might be more familiar to C++ programmers.


%prep
%setup -q -n %{module}-%{version}
# perl path hack
find . -type f | xargs %{__perl} -p -i -e "s|^#\!/usr/local/bin/perl|#\!/usr/bin/perl|g"


%build
export POSTGRES_INCLUDE=`pg_config --includedir`
export POSTGRES_LIB=`pg_config --libdir`
%{__perl} Makefile.PL INSTALLDIRS=vendor </dev/null
%make
# make test needs a running PostgreSQL server
#%{__make} test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc Changes README
%{perl_vendorlib}/*/*/Pg/Pg.so
%{perl_vendorlib}/*/*/Pg/autosplit.ix
%{perl_vendorlib}/*/Pg.pm
%{_mandir}/man3*/*


%changelog
* Sat Sep 10 2005 Vincent Danen <vdanen@annvix.org> 2.1.1-1avx
- 2.1.1
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen@annvix.org> 2.0.2-11avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 2.0.2-10avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen@annvix.org> 2.0.2-9avx
- rebuild against new perl

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 2.0.2-8avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.0.2-7sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 2.0.2-6sls
- rebuild for new perl

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 2.0.2-5sls
- OpenSLS build
- tidy spec

* Thu Sep 04 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.2-4mdk
- fix buildrequires

* Thu Aug 14 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 2.0.2-3mdk
- rebuild for new perl
- drop redundant requires
- drop PREFIX tag
- use %%makeinstall_std macro
- use %%make macro

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 2.0.2-2mdk
- Rebuild to fix bad signature

* Thu Jun 26 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.2-1mdk
- initial cooker contrib.
