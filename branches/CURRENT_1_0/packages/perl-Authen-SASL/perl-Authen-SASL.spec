%define module	Authen-SASL
%define name	perl-%{module}
%define version 2.04
%define release 7avx

Summary:	%{module} module for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot/
BuildRequires:	perl-devel
BuildArch:	noarch

Requires:	perl

%description
%{module} module for perl

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
%doc ChangeLog api.txt
%{_mandir}/*/*
%{perl_vendorlib}/Authen

%changelog
* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 2.04-7avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen@annvix.org> 2.04-6avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.04-5sls
- rebuild for perl 5.8.4

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 2.04-4sls
- rebuild for new perl
- some spec cleanups

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 2.04-3sls
- OpenSLS build
- tidy spec

* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.04-2mdk
- rebuild for new perl
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Fri May 23 2003 François Pons <fpons@mandrakesoft.com> 2.04-1mdk
- 2.04.

* Fri Jan 24 2003 François Pons <fpons@mandrakesoft.com> 2.03-1mdk
- 2.03.

* Fri Jul 19 2002 François Pons <fpons@mandrakesoft.com> 2.02-1mdk
- initial release (needed by perl-ldap >= 0.26).
