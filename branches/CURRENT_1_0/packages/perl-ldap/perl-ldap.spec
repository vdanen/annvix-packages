%define name perl-ldap
%define version 0.29
%define real_version 0.29
%define release 1mdk

Summary: Perl module for ldap
Name: %{name}
Version: %{version}
Release: %{release}
URL: http://www.cpan.org
Source0: http:///www.cpan.org/authors/id/G/GB/GBARR/%{name}-%{real_version}.tar.bz2
License: Artistic
Group: Development/Perl
BuildRequires: perl-devel >= 5.8.0
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: perl-Authen-SASL >= 2.00 perl-XML-Parser perl-Convert-ASN1 >= 0.07

%description
The perl-ldap distribution is a collection of perl modules 
which provide an object orientated interface to LDAP servers. 

The perl-ldap distribution has several advantages 

-By using the perl object interface the perl-ldap modules 
provide programmers with an interface which allows complex 
searches of LDAP directories with only a small amount of code. 
-All the perl-ldap modules are written entirely in perl, which 
means that the library is truly cross-platform compatible. 

%prep
%setup -q -n %{name}-%{real_version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc CREDITS README RELEASE_NOTES
%{_mandir}/*/*
%{perl_vendorlib}/LWP/*
%{perl_vendorlib}/Bundle/*
%{perl_vendorlib}/Net/*

%changelog
* Thu Aug 21 2003 François Pons <fpons@mandrakesoft.com> 0.29-1mdk
- 0.29.

* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.28-2mdk
- rebuild for new perl
- drop Prefix tag
- don't use PREFIX
- use %%makeinstall_std macro
- drop $RPM_OPT_FLAGS, noarch..
- quiet setup

* Fri May 23 2003 François Pons <fpons@mandrakesoft.com> 0.28-1mdk
- 0.28.

* Fri Apr 25 2003 François Pons <fpons@mandrakesoft.com> 0.27.01-2mdk
- added missing requires to perl-Convert-ASN1 (bug 3473).

* Tue Jan 28 2003 François Pons <fpons@mandrakesoft.com> 0.27.01-1mdk
- 0.2701.

* Sun Jul 21 2002 Pixel <pixel@mandrakesoft.com> 0.26-2mdk
- fix require

* Fri Jul 19 2002 François Pons <fpons@mandrakesoft.com> 0.26-1mdk
- 0.26.

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 0.25-2mdk
- rebuild for perl 5.8.0

* Thu Nov 08 2001 François Pons <fpons@mandrakesoft.com> 0.25-1mdk
- make it noarch.
- added documentation.
- added url tag.
- removed perllocal.pod.
- 0.25.

* Mon Oct 15 2001 Stefan van der Eijk <stefan@eijk.nu> 0.24-2mdk
- BuildRequires: perl-devel
- Copyright --> License

* Wed Aug  8 2001 Vincent Saugey <vince@mandrakesoft.com> 0.24-1mdk
- First mdk release
