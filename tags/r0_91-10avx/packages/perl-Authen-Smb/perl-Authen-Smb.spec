#
# spec file for package perl-Authen-Smb
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define module		Authen-Smb
%define name		perl-%{module}
%define version		0.91
%define release		10avx

Summary:	Authen::Smb Perl module
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL: 		http://search.cpan.org/CPAN/authors/id/P/PM/PMKANE/%{module}-%{version}.tar.gz
Source0:	http://www.cpan.org/modules/by-module/Authen/%{module}-%{version}.tar.gz
Patch0:		Authen-Smb-0.91-64bit-fixes.patch.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel >= 5.6

%description
Authen::Smb is a module to authenticate against an SMB server.


%prep
%setup -q -n %{module}-%{version}
%patch0 -p1 -b .64bit-fxies


%build
CFLAGS="%{optflags}" %{__perl} Makefile.PL INSTALLDIRS=vendor
make
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}
%{_mandir}/man3/*


%changelog
* Thu Aug 11 2005 Vincent Danen <vdanen@annvix.org> 0.91-10avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 0.91-9avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 0.91-8avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen@annvix.org> 0.91-7avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.91-6sls
- rebuild for perl 5.8.4

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 0.91-5sls
- rebuild for new perl
- some spec cleanups

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 0.91-4sls
- OpenSLS build
- tidy spec

* Sat Oct 25 2003 Stefan van der Eijk <stefan@eijk.nu> 0.91-3mdk
- BuildRequires

* Wed Sep 17 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.91-2mdk
- 64-bit fixes

* Fri Aug 08 2003 Florin <florin@mandrakesoft.com> 0.91-1mdk
- first release
