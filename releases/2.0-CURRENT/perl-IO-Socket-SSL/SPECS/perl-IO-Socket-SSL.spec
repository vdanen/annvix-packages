#
# spec file for package perl-IO-Socket-SSL
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	module		IO-Socket-SSL
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.97
%define release		%_revrel

Summary:	%{module} perl module
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/IO/
Source0:	%{module}-%{version}.tar.bz2

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	perl(Net::SSLeay)
BuildArch:	noarch

Requires:	perl(Net::SSLeay) >= 1.08

%description
IO::Socket::SSL is a class implementing an object oriented
interface to SSL sockets. The class is a descendent of
IO::Socket::INET and provides a subset of the base class's
interface methods.


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


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{perl_vendorlib}/IO/Socket/*

%files doc
%defattr(-,root,root)
%doc README Changes util docs certs


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org>  0.97
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy
- BuildRequires: perl(Net::SSLeay)

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.97
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.97
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.97-1avx
- first Annvix build (for new spamassassin)

* Mon Jul 18 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.97-1mdk
- 0.97

* Mon Jul 12 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.96-1mdk
- 0.96.
- Removed MANIFEST.

* Wed Aug 27 2003 François Pons <fpons@mandrakesoft.com> 0.95-1mdk
- 0.95.

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.92-5mdk
- rebuild for new perl
- don't use PREFIX
- use %%makeinstall_std macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.92-4mdk
- rebuild for new auto{prov,req}

* Mon May 05 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.92-3mdk
- buildrequires

* Wed Jan 29 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.92-2mdk
- rebuild

* Fri Jan 17 2003 François Pons <fpons@mandrakesoft.com> 0.92-1mdk
- 0.92.

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 0.81-2mdk
- rebuild for perl 5.8.0

* Tue Jun 18 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.81-1mdk
- updated by David Walser <luigiwalser@yahoo.com> :
	- 0.81

* Thu Aug 23 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.80-1mdk
- updated to 0.80

* Mon Jul 16 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.79-1mdk
- updated by Christian Zoffoli <czoffoli@linux-mandrake.com> :
	- 0.79

* Mon May 14 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.78-1mdk
- added in contribs by Christian Zoffoli <czoffoli@linux-mandrake.com>

* Thu Apr 19 2001 Christian Zoffoli <czoffoli@linux-mandrake.com> 0.77-1mdk
- First Mandrake release
