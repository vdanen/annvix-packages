%define module	Locale-gettext
%define name	perl-%{module}
%define version	1.01
%define release	14avx

Summary:	Internationalization for Perl.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org/modules/by-module/Locale
Source:		http://www.cpan.org/modules/by-module/Locale/gettext-%{version}.tar.gz
Patch0:		gettext-1.01-fix-example-in-README.patch.bz2
Patch1:		gettext-1.01-includes.patch.bz2
Patch2:		gettext-1.01-add-iconv.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	gettext-devel perl-devel

Obsoletes:	perl-gettext
Conflicts:	nlpr <= 0.0.1-2mdk, drakfloppy <= 0.43-10mdk, urpmi <= 3.6-4mdk

%description
The gettext module permits access from perl to the gettext() family of
functions for retrieving message strings from databases constructed to
internationalize software. 

It provides gettext(), dgettext(), dcgettext(), textdomain() and
bindtextdomain().

%prep
%setup -q -n gettext-%{version}
%patch0 -p1
%patch1 -p1 -b .includes
%patch2 -p0

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make
make test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%{perl_vendorarch}/Locale/*
%{perl_vendorarch}/auto/Locale/*
%{_mandir}/*/*

%changelog
* Sat Jun 26 2004 Vincent Danen <vdanen@annvix.org> 1.01-14avx
- Annvix build

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 1.01-13sls
- in my "add iconv" patch, tag the SV* as UTF8 when output charset is
  UTF8, to fix #7156 with some modifications in urpmi too (gc)
- rebuild against new libintl

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.01-12sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 1.01-11sls
- rebuild for new perl

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.01-10sls
- OpenSLS build
- tidy spec

* Wed Aug 13 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 1.01-9mdk
- rebuild for new perl
- use %%makeinstall_std macro

* Mon May 12 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.01-8mdk
- rebuild for new perl provides/requires

* Tue Mar  4 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 1.01-7mdk
- add iconv (patch #2) in order to be able to fix #2608 and #2680 from
  within urpmi

* Mon Aug 19 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.01-6mdk
- Patch1: Add missing includes. Aka make urpmi work with locales on x86-64

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 1.01-5mdk
- rebuild for perl thread-multi

* Wed Jul 24 2002 Pixel <pixel@mandrakesoft.com> 1.01-4mdk
- add "Obsoletes: perl-gettext" even it is not true
- but add "Conflicts: nlpr <= 0.0.1-2mdk, drakfloppy <= 0.43-10mdk, urpmi <= 3.6-4mdk"
  to ensure the packages that used perl-gettext gets upgraded

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.01-3mdk
- rebuild for perl 5.8.0

* Tue Jul  2 2002 Pixel <pixel@mandrakesoft.com> 1.01-2mdk
- perl-gettext will be removed as soon as every program has switched to perl-Locale-gettext
- reworked the spec (didn't see that it was already packaged)
- include debian's patch on README

* Fri Mar  8 2002 Arnaud de Lorbeau <adelorbeau@mandrakesoft.com> 1.01-1mdk
- First MandrakeSoft Package
