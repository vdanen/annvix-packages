%define module	Authen-Smb
%define name	perl-%{module}
%define version	0.91
%define release	6sls

Summary:	Authen::Smb Perl module
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Perl
URL: 		http://search.cpan.org/CPAN/authors/id/P/PM/PMKANE/%{module}-%{version}.tar.gz
Source0:	http://www.cpan.org/modules/by-module/Authen/%{module}-%{version}.tar.gz
Patch0:		Authen-Smb-0.91-64bit-fixes.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	perl-devel >= 5.6

%description
Authen::Smb is a module to authenticate against an SMB server.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1 -b .64bit-fxies

%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
make
make test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%{makeinstall_std}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}
%{_mandir}/man3/*

%changelog
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
