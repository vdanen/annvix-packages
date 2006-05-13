#
# spec file for package perl-Net-DNS
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Net-DNS
%define revision	$Rev$
%define name		perl-%{module}
%define version		0.53
%define release		%_revrel

Summary:	Perl interface to the DNS resolver
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://search.cpan.org/dist/%{module}
Source0:	http://search.cpan.org/CPAN/authors/id/O/OL/OLAF/%{module}-%{version}.tar.bz2

BuildRequires:	perl-devel
BuildRequires:	perl(Digest::HMAC)
BuildRequires:	perl(Net::IP)

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
Net::DNS is a collection of Perl modules that act as a Domain Name System (DNS)
resolver. It allows the programmer to perform DNS queries that are beyond the
capabilities of gethostbyname and gethostbyaddr.

The programmer should be somewhat familiar with the format of a DNS packet and
its various sections. See RFC 1035 or DNS and BIND (Albitz & Liu) for details.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{module}-%{version} 


%build
perl Makefile.PL INSTALLDIRS=vendor </dev/null
%make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_mandir}/*/*
%{perl_vendorarch}/auto/Net
%{perl_vendorarch}/Net

%files doc
%defattr(-,root,root)
%doc README Changes


%changelog
* Fri May 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.57
- 0.57
- rebuild against perl 5.8.8
- create -doc subpackage
- perl policy
- redirect from /dev/null rather than using yes

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.53
- use yes to enable tests or the Makefile will stall waiting for input
  and mess up any rebuilding scripts

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.53
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.53
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.53
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.53-1avx
- first build for Annvix (required by spamd)

* Mon Oct 03 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.53-1mdk
- new version
- %%mkrel

* Tue Sep 27 2005 Guillaume Rousse <guillomovitch@mandriva.org> 0.52-2mdk
- rpmbuildupate aware
- spec cleanup
- better summary and description
- drop useless requires exception

* Fri Jul 15 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.52-1mdk
- 0.52

* Thu Jun 23 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.51-2mdk
- BuildRequires perl-Net-IP

* Tue Jun 14 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.51-1mdk
- 0.51

* Mon May 02 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 0.49-1mdk
- 0.49

* Tue Nov 16 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.48-3mdk
- rebuild for new perl

* Mon Aug 30 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.48-2mdk
- add BuildRequires: perl-Digest-HMAC

* Mon Aug 23 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.48-1mdk
- 0.48.
- Add make test.

* Thu Apr 15 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 0.47-1mdk
- 0.47.

* Fri Aug 22 2003 François Pons <fpons@mandrakesoft.com> 0.39-2mdk
- added requires exceptions on perl(Win32::Registry).

* Thu Aug 21 2003 François Pons <fpons@mandrakesoft.com> 0.39-1mdk
- removed noarch as there is now a shared object.
- 0.39.

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.34-3mdk
- rebuild for new perl
- don't use PREFIX
- use %%makeinstall_std macro

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.34-2mdk
- rebuild for new auto{prov,req}

* Fri Apr 18 2003 François Pons <fpons@mandrakesoft.com> 0.34-1mdk
- 0.34.

* Fri Jan 17 2003 François Pons <fpons@mandrakesoft.com> 0.33-1mdk
- 0.33.

* Thu Jan 16 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.30-2mdk
- build release

* Wed Nov 13 2002 Oden Eriksson <oden.eriksson@linux-mandrake.com> 0.30-1mdk
- new version

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 0.14-2mdk
- rebuild for perl 5.8.0

* Fri Mar 01 2002 Lenny Cartier <lenny@mandrakesoft.com> 0.14-1mdk
- 0.14

* Mon Nov 26 2001 Oden Eriksson <oden.eriksson@linux-mandrake.com> 0.12-1mdk
- initial cooker contrib.
