%define		pdir	Authen
%define		pnam	Smb
Summary:	Authen::Smb Perl module
Name:		perl-Authen-Smb
Version:	0.91
Release:	3mdk
License:	GPL
Url: 			http://search.cpan.org/CPAN/authors/id/P/PM/PMKANE/%{pdir}-%{pnam}-%{version}.tar.gz
Group:		Development/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
Patch0:		Authen-Smb-0.91-64bit-fixes.patch.bz2
BuildRequires:	perl-devel >= 5.6
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Authen::Smb is a module to authenticate against an SMB server.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}
%patch0 -p1 -b .64bit-fxies

%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
make
make test

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}
%{_mandir}/man3/*

%changelog
* Sat Oct 25 2003 Stefan van der Eijk <stefan@eijk.nu> 0.91-3mdk
- BuildRequires

* Wed Sep 17 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.91-2mdk
- 64-bit fixes

* Fri Aug 08 2003 Florin <florin@mandrakesoft.com> 0.91-1mdk
- first release
