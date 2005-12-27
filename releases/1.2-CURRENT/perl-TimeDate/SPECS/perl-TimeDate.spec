#
# spec file for package perl-TimeDate
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		TimeDate
%define	revision	$Rev$
%define	name		perl-%{module}
%define	version		1.16
%define	release		%_revrel

Summary:	%{module} module for perl (Data_Type_Utilities/Time)
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel

Requires:	perl

%description
Simple Time and Date module for perl.


%prep
%setup -q -n %{module}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
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
%doc MANIFEST README ChangeLog
%{perl_vendorlib}/Date
%{perl_vendorlib}/Time
%{_mandir}/*/*


%changelog
* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.16-1avx
- first Annvix build (needed by swatch)

* Tue Jan 18 2005 Abel Cheung <deaddog@mandrake.org> 1.16-4mdk
- rebuild

* Wed Aug 27 2003 Fran�ois Pons <fpons@mandrakesoft.com> 1.16-3mdk
- really use 1.16 (problem of robot building...)

* Mon Aug 18 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 1.16-2mdk
- rebuild for new perl
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Wed Jun 04 2003 Fran�ois Pons <fpons@mandrakesoft.com> 1.16-1mdk
- 1.16.

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.14-2mdk
- rebuild for new auto{prov,req}

* Mon Nov 04 2002 Fran�ois Pons <fpons@mandrakesoft.com> 1.14-1mdk
- 1.14.

* Fri Jul 19 2002 Fran�ois Pons <fpons@mandrakesoft.com> 1.13.01-1mdk
- 1.1301.

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.13-2mdk
- rebuild for perl 5.8.0

* Mon Jun 10 2002 Fran�ois Pons <fpons@mandrakesoft.com> 1.13-1mdk
- 1.13.

* Tue Mar 26 2002 Fran�ois Pons <fpons@mandrakesoft.com> 1.11-1mdk
- updated License.
- added Date and Time directory.
- 1.11.

* Mon Oct 15 2001 Stefan van der Eijk <stefan@eijk.nu> 1.10-4mdk
- BuildRequires: perl-devel

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.10-3mdk
- Rebuild for the latest perl.

* Tue Mar 13 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.10-2mdk
- BuildArch: noarch
- add docs
- rename spec file
- clean up spec a bit

* Mon Nov 13 2000 Gregory Letoquart <gletoquart@mandrakesoft.com> 1.10-1mdk
- Up to 1.10

* Mon Sep  1 2000 Enzo Maggi <enzo@mandrakesoft.com> 1.09-1mdk
- Up to 1.09

* Mon Aug  7 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 1.08-1mdk
- First mandrake package

* Tue May 11 1999 root <root@alien.devel.redhat.com>
- Spec file was autogenerated.
