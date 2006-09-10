#
# spec file for package perl-Digest-SHA1
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Digest-SHA1
%define	revision	$Rev$
%define	name		perl-%{module}
%define	version		2.11
%define	release		%_revrel

Summary:	Perl interface to the SHA1 Algorithm	
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source:		http://www.cpan.org/authors/id/GAAS/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel

%description
Digest-SHA1 module for perl.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="%{optflags}"


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{perl_vendorarch}/Digest
%{perl_vendorarch}/auto

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Thu May 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.10
- rebuild against perl 5.8.8
- create -doc subpackage
- remove stupid provides

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.10
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.10
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.10-2avx
- correct the buildroot

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.10-1avx
- 2.10
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.04-8avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.04-7avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.04-6avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.04-5avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.04-4sls
- rebuild for perl 5.8.4

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 2.04-3sls
- rebuild for new perl
- minor spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 2.04-2sls
- OpenSLS build
- tidy spec

* Thu Aug 21 2003 François Pons <fpons@mandrakesoft.com> 2.04-1mdk
- 2.04.

* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.02-3mdk
- rebuild for new perl
- drop Prefix tag
- don't use PREFIX
- use %%makeinstall_std macro
- use %%make macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.02-2mdk
- rebuild for new auto{prov,req}

* Thu Jan 09 2003 François Pons <fpons@mandrakesoft.com> 2.02-1mdk
- 2.02.

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 2.01-3mdk
- rebuild for perl thread-multi

* Tue Jul 09 2002 Christian Belisle <cbelisle@mandrakesoft.com> 2.01-2mdk
- rebuild for perl 5.8.0
- install in vendor_perl

* Thu Jan 03 2002 François Pons <fpons@mandrakesoft.com> 2.01-1mdk
- 2.01.

* Mon Nov 12 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.00-5mdk
- Fix no-url-tag and invalid-packager warnings.

* Tue Oct 16 2001 Stefan van der Eijk <stefan@eijk.nu> 2.00-4mdk
- BuildRequires: perl-devel

* Thu Oct 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.00-3mdk
- Make rpmlint happier.
- Remove Distribution tag.

* Sun Jun 24 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.00-2mdk
- Clean file list.

* Fri Jun 22 2001 Christian Belisle <cbelisle@mandrakesoft.com> 2.00-1mdk
- First release, was in perl-Digest-MD5 package before.

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
