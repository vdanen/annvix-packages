%define module	Apache-Session
%define version	1.54
%define release	6mdk

Packager:	Jean-Michel Dault <jmdault@mandrakesoft.com>
Vendor:		MandrakeSoft

Summary:	%{module}: Apache persistent user sessions
Name:		perl-%{module}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
Source0:	%{module}-%{version}.tar.bz2
Url:		http://www.cpan.org
BuildRoot:	%{_tmppath}/%{name}-buildroot/
Requires:	perl
BuildRequires:	perl-DB_File perl-DBI perl-devel perl-Digest-MD5
Requires:	perl-Digest-MD5
BuildArch:	noarch

%description
Apache::Session is a persistence framework which is particularly useful
for tracking session data between httpd requests.  Apache::Session is
designed to work with Apache and mod_perl, but it should work under CGI
and other web servers, and it also works outside of a web server alto-
gether.


%prep
%setup -q -n %{module}-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
make
make test

%clean 
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
eval `perl '-V:installarchlib'`
mkdir -p $RPM_BUILD_ROOT/$installarchlib
make PREFIX=$RPM_BUILD_ROOT%{_prefix} install
%__os_install_post
find $RPM_BUILD_ROOT%{_prefix} -type f -print | sed "s@^$RPM_BUILD_ROOT@@g" | grep -v perllocal.pod > %{module}-%{version}-filelist


%files
%defattr(-,root,root)
%doc INSTALL README
%{_mandir}/*/*
%{perl_vendorlib}/Apache/*

%changelog
* Thu Aug 07 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.54-6mdk
- rebuild for new perl

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.54-5mdk
- rebuild for new auto{prov,req}

* Tue Jan 28 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.54-4mdk
- better description & summary

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.54-3mdk
- rebuild for perl 5.8.0

* Mon Nov 26 2001 Stefan van der Eijk <stefan@eijk.nu> 1.54-2mdk
- fix BuildRequires

* Thu Nov 08 2001 François Pons <fpons@mandrakesoft.com> 1.54-1mdk
- removed patch as now integrated.
- 1.54.

* Fri Aug 31 2001 François Pons <fpons@mandrakesoft.com> 1.53-1mdk
- 1.53.
- removed explicit Distribution tag.
- updated license.
- created patch to use Digest::MD5 instead of obsoleted MD5 and
  fix test scripts.

* Tue Mar 13 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.03-3mdk
- BuildArch: noarch
- add docs
- rename spec file
- clean spec a bit
- run automated tests

* Sun Oct  1 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.03-2mdk
- call spec-helper before creating the file list and don't call it after.

* Tue Aug 08 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.03-1mdk
- Macroize package
