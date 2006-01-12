#
# spec file for package perl-libwww-perl
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		libwww-perl
%define revision	$Rev$
%define name		perl-%{module}
%define version 	5.803
%define release 	%_revrel

%define _requires_exceptions Authen::NTLM\\|HTTP::GHTTP\\|Win32

Summary:	Libwww-perl module for perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source0:	%{module}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	perl-devel, perl-HTML-Parser, perl-URI, rpm-build >= 4.2-7mdk

Requires:	perl, perl-HTML-Parser, perl-URI >= 1.10, perl-MIME-Base64, perl-libnet, perl-Digest-MD5


%description
libwww-perl module for perl


%prep
%setup -q -n %{module}-%{version}


%build
/usr/bin/yes | %{__perl} Makefile.PL INSTALLDIRS=vendor
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README README.SSL Changes
%{_bindir}/*
%{_mandir}/*/*
%{perl_vendorlib}/LWP.pm
%{perl_vendorlib}/*.pod
%{perl_vendorlib}/Net
%{perl_vendorlib}/File
%{perl_vendorlib}/HTML
%{perl_vendorlib}/WWW
%{perl_vendorlib}/HTTP
%{perl_vendorlib}/Bundle
%{perl_vendorlib}/LWP


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Dec 27 2005 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.803-4avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.803-3avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.803-2avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.803-1avx
- 5.803
- restore installation of GET, HEAD, and POST in /usr/bin (rgarciasuarez)

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.79-3avx
- rebuild against new perl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.79-2avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 5.79-1sls
- 5.79
- remove P0; merged upstream
- minor spec cleanups

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 5.69-4sls
- rebuild for new perl
- remove %%{prefix} tag

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 5.69-3sls
- OpenSLS build
- tidy spec
- comment out make test for the time being

* Tue May 13 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 5.69-2mdk
- rebuild for new perl provides/requires
- put some exceptions for unavailable perl modules

* Tue Jan 28 2003 François Pons <fpons@mandrakesoft.com> 5.69-1mdk
- 5.69.

* Thu Jan 09 2003 François Pons <fpons@mandrakesoft.com> 5.68-1mdk
- 5.68.

* Sat Aug 10 2002 Stefan van der Eijk <stefan@eijk.nu> 5.65-4mdk
- BuildRequires

* Wed Jul 10 2002 Christian Belisle <cbelisle@mandrakesoft.com> 5.65-3mdk
- add 'make test'

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 5.65-2mdk
- rebuild for perl 5.8.0

* Mon Jun 10 2002 François Pons <fpons@mandrakesoft.com> 5.65-1mdk
- 5.65.

* Mon Mar 25 2002 François Pons <fpons@mandrakesoft.com> 5.64-1mdk
- 5.64.

* Tue Dec 18 2001 François Pons <fpons@mandrakesoft.com> 5.63-2mdk
- added patch from Brian J. Murrell for HTTP POST of empty content.

* Mon Dec 17 2001 François Pons <fpons@mandrakesoft.com> 5.63-1mdk
- 5.63.

* Mon Nov 12 2001 François Pons <fpons@mandrakesoft.com> 5.60-2mdk
- fixed missing Net files (thanks to Jochem Wichers Hoeth).

* Wed Nov 07 2001 François Pons <fpons@mandrakesoft.com> 5.60-1mdk
- 5.60.

* Sat Jul 07 2001 Stefan van der Eijk <stefan@eijk.nu> 5.53-2mdk
- BuildRequires: perl-devel

* Tue Jul 03 2001 François Pons <fpons@mandrakesoft.com> 5.53-1mdk
- 5.53.

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 5.50-2mdk
- Rebuild for the latest perl.

* Tue Jan 30 2001 François Pons <fpons@mandrakesoft.com> 5.50-1mdk
- added requires on perl-URI >= 1.10.
- 5.50.

* Tue Nov 14 2000 François Pons <fpons@mandrakesoft.com> 5.48-3mdk
- fixed typo in summary.

* Thu Aug 03 2000 François Pons <fpons@mandrakesoft.com> 5.48-2mdk
- macroszifications.
- noarch.
- add doc.

* Tue Jun 27 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 5.48-1mdk
- updated to 5.48

* Thu Apr 20 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 5.47-3mdk
- fixed release tag

* Fri Mar 31 2000 Pixel <pixel@mandrakesoft.com> 5.47-2mdk
- remove file list
- rebuild for 5.6.0

* Mon Jan  3 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- final cleanup for Mandrake 7

* Thu Dec 30 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to 5.47

* Sun Aug 29 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- bzip2'd sources
- updated to 5.44

* Tue May 11 1999 root <root@alien.devel.redhat.com>
- Spec file was autogenerated. 
