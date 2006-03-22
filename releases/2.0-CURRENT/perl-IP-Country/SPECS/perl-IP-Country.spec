#
# spec file for package perl-IP-Country
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#

%define module		IP-Country
%define revision	$Rev$
%define name		perl-%{module}
%define version		2.20
%define release		%_revrel

Summary:	IP::Country modules for Perl 
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	http://cpan.uwinnipeg.ca/cpan/authors/id/N/NW/NWETTERS/%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel, perl-Geography-Countries
BuildArch:	noarch

Requires:	perl-Geography-Countries

%description
IP lookup modules for Perl. This package also provides the ip2cc utility, to
lookup country from IP address or hostname.


%prep
%setup -q -n %{module}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make


%check
%{__make} test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc CHANGES README
%{perl_vendorlib}/IP
%{_mandir}/*/*
%{_bindir}/*


%changelog
* Tue Mar 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.20
- spec cleanups

* Sun Mar 12 2006 Ying-Hung Chen <ying-at-annvix.org> 2.20
- first Annvix build

* Mon May 09 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 2.20-1mdk
- 2.20
- add tests, spec cleanup, rewrite description

* Mon Nov 15 2004 Austin Acton <austin@mandrake.org> 2.18-1mdk
- 2.18

* Sun Dec 14 2003 Abel Cheung <deaddog@deaddog.org> 2.17-1mdk
- 2.17

* Wed May 28 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.11-2mdk
- rebuild for new auto{prov,req}

* Tue Apr 1 2003 Austin Acton <aacton@yorku.ca> 2.11-1mdk
- initial package
