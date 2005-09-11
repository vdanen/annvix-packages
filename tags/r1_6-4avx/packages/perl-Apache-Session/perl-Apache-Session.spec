#
# spec file for package perl-Apache-Session
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		perl-%{module}
%define module		Apache-Session
%define version		1.6
%define release		4avx
%define epoch		1

Summary:	%{module}: Apache persistent user sessions
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-DB_File perl-DBI perl-devel perl-Digest-MD5
BuildArch:	noarch

Requires:	perl
Requires:	perl-Digest-MD5

%description
Apache::Session is a persistence framework which is particularly useful
for tracking session data between httpd requests.  Apache::Session is
designed to work with Apache and mod_perl, but it should work under CGI
and other web servers, and it also works outside of a web server alto-
gether.


%prep
%setup -q -n %{module}-%{version}


%build
CFLAGS="%{optflags}" %{__perl} Makefile.PL INSTALLDIRS=vendor
make
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
eval `perl '-V:installarchlib'`
mkdir -p %{buildroot}/$installarchlib
make PREFIX=%{buildroot}%{_prefix} install
%__os_install_post
find %{buildroot}%{_prefix} -type f -print | sed "s@^%{buildroot}@@g" | grep -v perllocal.pod > %{module}-%{version}-filelist


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc INSTALL README
%{_mandir}/*/*
%{perl_vendorlib}/Apache/*


%changelog
* Sat Sep 10 2005 Vincent Danen <vdanen@annvix.org> 1.6-4avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen@annvix.org> 1.6-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 1.6-2avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen@annvix.org> 1.6-1avx
- 1.6
- spec cleanups
- set epoch or rpm thinks that 1.54 > 1.6

* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 1.54-11avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen@annvix.org> 1.54-10avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.54-9sls
- rebuild for perl 5.8.4

* Wed Feb 25 2004 Vincent Danen <vdanen@opensls.org> 1.54-8sls
- rebuild for new perl
- some spec cleanups

* Sat Jan 03 2004 Vincent Danen <vdanen@opensls.org> 1.54-7sls
- OpenSLS build
- tidy spec

* Thu Aug 07 2003 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 1.54-6mdk
- rebuild for new perl

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.54-5mdk
- rebuild for new auto{prov,req}

* Tue Jan 28 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.54-4mdk
- better description & summary

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.54-3mdk
- rebuild for perl 5.8.0

* Mon Nov 26 2001 Stefan van der Eijk <stefan@eijk.nu> 1.54-2mdk
- fix BuildRequires

* Thu Nov 08 2001 Fran�ois Pons <fpons@mandrakesoft.com> 1.54-1mdk
- removed patch as now integrated.
- 1.54.

* Fri Aug 31 2001 Fran�ois Pons <fpons@mandrakesoft.com> 1.53-1mdk
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
