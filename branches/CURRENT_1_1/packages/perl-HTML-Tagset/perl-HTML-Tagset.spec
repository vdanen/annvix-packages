#
# spec file for package perl-HTML-Tagset
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define	module		HTML-Tagset
%define name		perl-%{module}
%define	version		3.03
%define	release		14avx

Summary: 	This module contains data tables useful in dealing with HTML
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Development/Perl
URL:		http://www.cpan.org
Source:		http://www.cpan.org/authors/id/S/SB/SBURKE/%{module}-%{version}.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel

Requires: 	perl


%description
This module contains data tables useful in dealing with HTML.

It provides no functions or methods.


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
%doc README ChangeLog
%{_mandir}/*/*
%{perl_vendorlib}/HTML


%changelog
* Thu Aug 11 2005 Vincent Danen <vdanen@annvix.org> 3.31-14avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 3.31-13avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 3.31-12avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen@annvix.org> 3.31-11avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 3.03-10sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 3.03-9sls
- rebuild for new perl

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 3.03-8sls
- OpenSLS build
- tidy spec

* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.03-7mdk
- rebuild against new perl
- drop Prefix tag
- drop $RPM_OPT_FLAGS, noarch..
- don't use PREFIX
- use %%makeinstall_std macro
- drop %%real_name macro, use the already existing %%module macro in stead

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.03-6mdk
- rebuild for new auto{prov,req}

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 3.03-5mdk
- rebuild for perl 5.8.0

* Tue Mar 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.03-4mdk
- should be noarch

* Mon Nov 12 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.03-3mdk
- Remove Distribution Tag.
- Fix no-url-tag and invalid-packager warnings.

* Mon Oct 15 2001 Stefan van der Eijk <stefan@eijk.nu> 3.03-2mdk
- BuildRequires: perl-devel

* Wed Jun 20 2001 Christian Belisle <cbelisle@mandrakesoft.com> 3.03-1mdk
- First Mandrake Release.
