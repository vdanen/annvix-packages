%define module	Authen-SASL
%define version 2.04
%define release 2mdk

Summary:	%{module} module for perl
Name:		perl-%{module}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
Source0:	%{module}-%{version}.tar.bz2
Url:		http://www.cpan.org
BuildRequires:	perl-devel
BuildRoot:	%{_tmppath}/%{name}-buildroot/
Requires:	perl
BuildArch:	noarch

%description
%{module} module for perl

%prep
%setup -q -n %{module}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make
make test

%clean 
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%files
%defattr(-,root,root)
%doc ChangeLog api.txt
%{_mandir}/*/*
%{perl_vendorlib}/Authen

%changelog
* Wed Aug 13 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 2.04-2mdk
- rebuild for new perl
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Fri May 23 2003 Fran�ois Pons <fpons@mandrakesoft.com> 2.04-1mdk
- 2.04.

* Fri Jan 24 2003 Fran�ois Pons <fpons@mandrakesoft.com> 2.03-1mdk
- 2.03.

* Fri Jul 19 2002 Fran�ois Pons <fpons@mandrakesoft.com> 2.02-1mdk
- initial release (needed by perl-ldap >= 0.26).
