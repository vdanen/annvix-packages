%define module	Term-ReadLine-Gnu
%define name	perl-%{module}
%define version 1.14
%define release 6sls

Summary:	GNU Readline for perl.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	libtermcap-devel perl-devel readline-devel

Obsoletes:	perl-Term-Readline-Gnu

%description
This is an implementation of the interface to the GNU Readline
Library.  This module gives you input line editing facility, input
history management facility, word completion facility, etc.  It uses
the real GNU Readline Library.  And this module has the interface with
the almost all variables and functions which are documented in the GNU
Readline/History Library.  So you can program your custom editing
function, your custom completion function, and so on with Perl.  This
may be useful for prototyping before programming with C.

%prep
%setup -q -n %{module}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="$RPM_OPT_FLAGS"
if [ -n "$DISPLAY" ]; then
  TERM=linux make test
else
  echo "make test not done because DISPLAY var is not set"
fi

chmod 644 README

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
# Fix bogus dependancy on /usr/local/bin/perl:
perl -pi -e 's!/usr/local/bin/perl!/usr/bin/perl!g' $RPM_BUILD_ROOT%perl_vendorarch/Term/ReadLine/Gnu/{euc_jp,XS}.pm


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%{_mandir}/*/*
%dir %{perl_vendorarch}/Term
%{perl_vendorarch}/Term/ReadLine/Gnu*
%dir %{perl_vendorarch}/auto/Term
%{perl_vendorarch}/auto/Term/ReadLine/Gnu

%changelog
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

* Thu Aug 14 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 1.14-4mdk
- rebuild for new perl
- don't use PREFIX
- use %%makeinstall_std macro

* Fri Jul 18 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 1.14-3mdk
- drop Prefix tag, use %%{_prefix}
- don't require perl, rpm will figure it out by itself

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.14-2mdk
- rebuild for new auto{prov,req}

* Fri Apr 18 2003 Fran�ois Pons <fpons@mandrakesoft.com> 1.14-1mdk
- 1.14.

* Fri Oct 11 2002 Fran�ois Pons <fpons@mandrakesoft.com> 1.13-1mdk
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

* Thu Apr 11 2002 Fran�ois Pons <fpons@mandrakesoft.com> 1.12-1mdk
- 1.12.

* Wed Nov 07 2001 Fran�ois Pons <fpons@mandrakesoft.com> 1.11-1mdk
- removed patch now integrated for filename completion in perl db.
- 1.11.

* Mon Oct 15 2001 Stefan van der Eijk <stefan@eijk.nu> 1.10-3mdk
- BuildRequires: libtermcap-devel perl-devel readline-devel

* Mon Sep 03 2001 Fran�ois Pons <fpons@mandrakesoft.com> 1.10-2mdk
- created patch for filename completion (in perl db).

* Fri Aug 24 2001 Fran�ois Pons <fpons@mandrakesoft.com> 1.10-1mdk
- 1.10.

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.09-4mdk
- Correct the definitely misleading summary aka oh gee someone is on 
  drugs? ;)
- Rebuild for the latest perl.

* Tue Aug 29 2000 Fran�ois Pons <fpons@mandrakesoft.com> 1.09-3mdk
- build release.

* Thu Aug 03 2000 Fran�ois Pons <fpons@mandrakesoft.com> 1.09-2mdk
- macroszifications.
- add doc.

* Tue Jul 18 2000 Fran�ois Pons <fpons@mandrakesoft.com> 1.09-1mdk
- 1.09.
- removed patch for compilation with perl 5.6.0.

* Mon Apr 04 2000 Fran�ois Pons <fpons@mandrakesoft.com> 1.08-2mdk
- added patch for compilation with perl 5.6.0.
- updated spec file and Group.

* Tue Jan  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- First package needed for perl-debug.
