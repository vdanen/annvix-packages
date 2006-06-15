#
# spec file for package perl-Term-ReadLine-Gnu
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Term-ReadLine-Gnu
%define revision	$Rev$
%define name		perl-%{module}
%define version 	1.15
%define release 	%_revrel

Summary:	GNU Readline for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libtermcap-devel, perl-devel, readline-devel

Obsoletes:	perl-Term-Readline-Gnu
Provides:	perl-Term-Readline-Gnu

%description
This is an implementation of the interface to the GNU Readline
Library.  This module gives you input line editing facility, input
history management facility, word completion facility, etc.  It uses
the real GNU Readline Library.  And this module has the interface with
the almost all variables and functions which are documented in the GNU
Readline/History Library.  So you can program your custom editing
function, your custom completion function, and so on with Perl.  This
may be useful for prototyping before programming with C.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
find -type f -exec chmod 0644 '{}' \;
perl Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="%{optflags}"


%check
if [ -n "$DISPLAY" ]; then
    TERM=linux make test
else
    echo "make test not done because DISPLAY var is not set"
fi

chmod 0644 README


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
# Fix bogus dependancy on /usr/local/bin/perl:
perl -pi -e 's!/usr/local/bin/perl!/usr/bin/perl!g' %{buildroot}%{perl_vendorarch}/Term/ReadLine/Gnu/{euc_jp,XS}.pm


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%dir %{perl_vendorarch}/Term
%{perl_vendorarch}/Term
%dir %{perl_vendorarch}/auto/Term
%{perl_vendorarch}/auto/Term

%files doc
%defattr(-,root,root)
%doc README


%changelog
* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15
- rebuild against new readline

* Sat May 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15
- rebuild against perl 5.8.8
- create -doc subpackage
- fix permissions
- provide the package we obsolete

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.15
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-5avx
- rebuild against perl 5.8.7

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-4avx
- rebuild against new readline

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-2avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.15-1avx
- 1.15

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.14-9avx
- rebuild against new perl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.14-8avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.14-7sls
- rebuild for perl 5.8.4
- own dir

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 1.14-6sls
- rebuild for new perl
- don't make test if $DISPLAY is not set (it will fail) (thauvin)

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.14-5sls
- OpenSLS build
- tidy spec
- pkg name change from perl-Term-Readline-Gnu to perl-Term-ReadLine-Gnu to
  follow our spec of perl-%%{module}
- Obsoletes perl-Term-Readline-Gnu; anything that requires it will have to
  change their req's as we don't use dumb provides

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.14-4mdk
- rebuild for new perl
- don't use PREFIX
- use %%makeinstall_std macro

* Fri Jul 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.14-3mdk
- drop Prefix tag, use %%{_prefix}
- don't require perl, rpm will figure it out by itself

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.14-2mdk
- rebuild for new auto{prov,req}

* Fri Apr 18 2003 François Pons <fpons@mandrakesoft.com> 1.14-1mdk
- 1.14.

* Fri Oct 11 2002 François Pons <fpons@mandrakesoft.com> 1.13-1mdk
- 1.13.

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 1.12-6mdk
- rebuild for perl thread-multi

* Tue Jul 23 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.12-5mdk
- rebuild for new readline

* Wed Jul 10 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.12-4mdk
- add 'make test'

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 1.12-3mdk
- add missing file :-(

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.12-2mdk
- rebuild for perl 5.8.0
- little %%files cleanup

* Thu Apr 11 2002 François Pons <fpons@mandrakesoft.com> 1.12-1mdk
- 1.12.

* Wed Nov 07 2001 François Pons <fpons@mandrakesoft.com> 1.11-1mdk
- removed patch now integrated for filename completion in perl db.
- 1.11.

* Mon Oct 15 2001 Stefan van der Eijk <stefan@eijk.nu> 1.10-3mdk
- BuildRequires: libtermcap-devel perl-devel readline-devel

* Mon Sep 03 2001 François Pons <fpons@mandrakesoft.com> 1.10-2mdk
- created patch for filename completion (in perl db).

* Fri Aug 24 2001 François Pons <fpons@mandrakesoft.com> 1.10-1mdk
- 1.10.

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.09-4mdk
- Correct the definitely misleading summary aka oh gee someone is on 
  drugs? ;)
- Rebuild for the latest perl.

* Tue Aug 29 2000 François Pons <fpons@mandrakesoft.com> 1.09-3mdk
- build release.

* Thu Aug 03 2000 François Pons <fpons@mandrakesoft.com> 1.09-2mdk
- macroszifications.
- add doc.

* Tue Jul 18 2000 François Pons <fpons@mandrakesoft.com> 1.09-1mdk
- 1.09.
- removed patch for compilation with perl 5.6.0.

* Mon Apr 04 2000 François Pons <fpons@mandrakesoft.com> 1.08-2mdk
- added patch for compilation with perl 5.6.0.
- updated spec file and Group.

* Tue Jan  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- First package needed for perl-debug.
