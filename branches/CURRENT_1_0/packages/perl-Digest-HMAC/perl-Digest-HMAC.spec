%define module	Digest-HMAC
%define	name	perl-%{module}
%define	version	1.01
%define	release	16avx

Summary:	Keyed-Hashing for Message Authentication
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source:		http://www.cpan.org/authors/id/GAAS/%{module}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	perl-devel
BuildArch:	noarch

Provides:	perl-HMAC
Requires:	perl perl-Digest-SHA1

%description
Digest-HMAC module for perl.

%prep
%setup -q -n %{module}-%{version}

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
%doc README Changes
%{_mandir}/*/*
%{perl_vendorlib}/Digest

%changelog
* Thu Feb 03 2005 Vincent Danen <vdanen@annvix.org> 1.01-16avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen@annvix.org> 1.01-15avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.01-14sls
- rebuild for perl 5.8.4

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 1.01-13sls
- rebuild for new perl
- minor spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.01-12sls
- OpenSLS build
- tidy spec

* Wed Aug 13 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 1.01-11mdk
- rebuild for new perl
- drop Prefix tag
- drop $RPM_OPT_FLAGS, noarch..
- don't use PREFIX
- use %%makeinstall_std macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.01-10mdk
- rebuild for new auto{prov,req}

* Tue Jul 09 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.01-9mdk
- rebuild with new perl 5.8.0
- install in vendor_perl

* Tue Mar 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.01-7mdk
- should be noarch

* Mon Nov 12 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.01-6mdk
- Remove Distribution tag.
- Rebuild to fix no-url-tag and invalid-packager warnings.

* Tue Oct 16 2001 Stefan van der Eijk <stefan@eijk.nu> 1.01-5mdk
- BuildRequires: perl-devel perl-Digest-MD5

* Thu Oct 11 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.01-4mdk
- Make rpmlint happier.

* Sun Jun 24 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.01-3mdk
- Clean the file list (to build a good cpio). Thanx to Brian.

* Fri Jun 22 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.01-2mdk
- Added a make test for compilation
- Fixed a typo in the changelog's date.
- Added a Require for perl-Digest-SHA1.

* Fri Jun 22 2001 Christian Belisle <cbelisle@mandrakesoft.com> 1.01-1mdk
- First release, was in perl-Digest-MD5 package before.
