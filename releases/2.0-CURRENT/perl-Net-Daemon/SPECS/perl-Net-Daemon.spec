#
# spec file for package perl-Net-Daemon
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module 		Net-Daemon
%define revision	$Rev$
%define name		perl-%{module}
%define version 	0.39
%define release 	%_revrel

Summary:	%{module} perl module
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}/
Source0:	http://search.cpan.org/CPAN/authors/id/J/JW/JWIED/%{module}-%{version}.tar.bz2

Buildrequires:  perl-devel >= 5.8.0
BuildRoot: 	%{_buildroot}/%{name}-%{version}
Buildarch:	noarch

%description
Net::Daemon is an abstract base class for implementing portable server
applications in a very simple way. The module is designed for Perl 5.005 and
threads, but can work with fork() and Perl 5.004.

The Net::Daemon class offers methods for the most common tasks a daemon needs:
Starting up, logging, accepting clients, authorization, restricting its own
environment for security and doing the true work. You only have to override
those methods that aren't appropriate for you, but typically inheriting will
safe you a lot of work anyways.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%{perl_vendorlib}/Net/*.pm
%{perl_vendorlib}/Net/Daemon/
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc README


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.39
- 0.39
- rebuild against perl 5.8.8
- create -doc subpackage
- update description
- spec cleanups
- can't make test with this one because it wants to talk to syslog

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.38
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.38
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.38-1avx
- 0.38
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.37-10avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.37-9avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.37-8avx
- rebuild against new perl

* Sat Jun 26 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.37-7avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 0.37-6sls
- rebuild for perl 5.8.4

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 0.37-5sls
- rebuild for new perl

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 0.37-4sls
- OpenSLS build
- tidy spec

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.37-3mdk
- rebuild for new perl
- drop $RPM_OPT_FLAGS, noarch..
- use %%makeinstall_std macro

* Fri May 16 2003 Guillaume Rousse <g.rousse@linux-mandrake.com> 0.37-2mdk
- rebuild for dependencies

* Fri Apr 25 2003 François Pons <fpons@mandrakesoft.com> 0.37-1mdk
- 0.37.

* Wed Jan 29 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.36-3mdk
- rebuild

* Wed Jul 31 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.36-2mdk
- rebuild with new perl

* Fri Mar 01 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.36-1mdk
- 0.36

* Wed Aug 29 2001 Lenny Cartier <lenny@mandrakesoft.com> 0.35-1mdk
- added by Christian Zoffoli <czoffoli@linux-mandrake.com> :
	- first mandrake release

