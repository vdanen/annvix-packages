%define	name	perl-%{module}
%define	module	BSD-Resource
%define	version	1.22
%define	release	4sls

Summary:	%{module} module for perl 
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	perl-devel

Requires:	perl

%description
%{module} module for perl

%prep
%setup -q -n %{module}-%{version} 
# perl path hack
find . -type f | xargs %{__perl} -p -i -e "s|^#\!/usr/local/bin/perl|#\!/usr/bin/perl|g"

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor </dev/null
%{__make}
%{__make} test

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 
%makeinstall_std

%clean 
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot} 

%files
%defattr(-,root,root)
%doc ChangeLog README
%{perl_vendorlib}
%{_mandir}/man*/*

%changelog
* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 1.22-4sls
- OpenSLS build
- tidy spec

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.22-3mdk
- rebuild for new perl
- don't use PREFIX
- use %%makeinstall_std macro
- cosmetics

* Mon Jul 21 2003 David Baudens <baudens@mandrakesoft.com> 1.22-2mdk
- Rebuild to fix bad signature

* Sat May 31 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.22-1mdk
- initial cooker contrib.
