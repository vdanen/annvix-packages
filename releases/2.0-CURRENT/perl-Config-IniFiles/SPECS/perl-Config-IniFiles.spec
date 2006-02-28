#
# spec file for package perl-Config-IniFiles
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Config-IniFiles
%define revision	$Rev$
%define name		perl-%{module}
%define version		2.38
%define release		%_revrel

Summary:	Config-IniFiles module for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License: 	GPL
Group: 		Development/Perl
URL:           	http://www.cpan.org/
Source: 	Config-IniFiles-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires: 	perl-devel >= 5.8.0

%description
This perl module allows you to access to config files written in the 
.ini style. 


%prep
%setup -q -n %{module}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
chmod 0644 README
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README
%{perl_vendorlib}/Config
%{_mandir}/*/*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.38-4avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.38-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.38-2avx
- bootstrap build

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.38-1avx
- first Annvix build, for rpmtools

* Tue Feb 15 2005 Michael Scherer <misc@mandrake.org> 2.38-3mdk
- Rebuild
- Fix description, and rpmlint warning.

* Wed Feb 25 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.38-2mdk
- rebuild
- fix url
- own dir
- cosmetic

* Wed Aug 27 2003 François Pons <fpons@mandrakesoft.com> 2.38-1mdk
- 2.38.

* Fri Aug 15 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.37-3mdk
- rebuild for new perl
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Wed May 28 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.37-2mdk
- rebuild for new auto{prov,req}

* Fri Apr 25 2003 François Pons <fpons@mandrakesoft.com> 2.37-1mdk
- 2.37.

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 2.27-2mdk
- rebuild for perl 5.8.0

* Wed May 22 2002 Buchan Milne <bgmilne@.cae.co.za> 2.27-1mdk
- Mandrake package
