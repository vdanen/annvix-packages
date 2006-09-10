#
# spec file for package perl-File-Tail
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		File-Tail
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.99.1
%define release		%_revrel

Summary:	File::Tail module for Perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
Url:		http://search.cpan.org/dist/%{module}/
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel
BuildRequires:	perl(Time::HiRes)

%description
This Perl modules allows to read from continously updated files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{perl_vendorlib}/File
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.99.1
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.99.1
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.99.1
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.99.1-1avx
- first Annvix build (required by swatch)

* Wed Jun 29 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.99.1-2mdk
- Rebuild

* Wed Jan 05 2005 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.99.1-1mdk
- New version
- Update description
- Remove MANIFEST

* Wed Feb 25 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.98-5mdk
- rebuild 

* Wed Aug 13 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 0.98-4mdk
- rebuild for new perl
- drop $RPM_OPT_FLAGS, noarch
- use %%makeinstall_std macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.98-3mdk
- rebuild for new auto{prov,req}

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 0.98-2mdk
- rebuild for perl 5.8.0

* Thu Nov 08 2001 Fran�ois Pons <fpons@mandrakesoft.com> 0.98-1mdk
- updated license.
- 0.98.

* Tue Oct 16 2001 Stefan van der Eijk <stefan@eijk.nu> 0.97-4mdk
- BuildRequires: perl-devel

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.97-3mdk
- Rebuild against the latest perl.

* Tue Mar 13 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.97-2mdk
- BuildArch: noarch
- add docs
- rename spec file
- clean spec a bit

* Mon Nov 13 2000 Gregory Letoquart <gletoquart@mandrakesoft.com> 0.97-1mdk
- Updated to 0.97
- Add doc 

* Fri Sep 1 2000 Enzo Maggi <enzo@mandrakesoft.com> 0.96-1mdk
- Updated to 0.96

* Mon Aug  7 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 0.91-1mdk
- First Mandrake package

* Tue May 11 1999 root <root@alien.devel.redhat.com>
- Spec file was autogenerated. 

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
