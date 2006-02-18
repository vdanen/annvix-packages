#
# spec file for package perl-Net_SSLeay
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define module		Net_SSLeay
%define revision	$Rev$
%define name 		perl-%{module}
%define version		1.25
%define release		%_revrel

Summary:        Net::SSLeay (module for perl)
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Development/Perl
URL: 		http://www.bacus.pt/Net_SSLeay/index.html
Source: 	%{module}.pm-%{version}.tar.bz2
Patch:		%{module}.pm-1.25.large_tcp_read.patch
Patch1:		Net_SSLeay-nobakus.patch
Patch2:		perl-Net_SSLeay-1.2.5-CVE-2005-0106.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-devel perl-devel

Requires: 	openssl >= 0.9.3a

%description
Net::SSLeay module for perl.


%prep
%setup -q -n %{module}.pm-%{version}
%patch -p1 -b .fpons
%patch1 -p0 -b .nobakus
%patch2 -p1 -b .cve-2005-0106

# openssl_path is /usr here, therefore don't -I/usr/include and
# especially don't (badly) hardcode standard library search path
# /usr/lib
if [[ "%{_prefix}" = "/usr" ]]; then
    perl -pi -e "s@-[LI]\\\$openssl_path[^\s\"]*@@g" Makefile.PL
fi


%build
# note the %{_prefix} which must passed to Makefile.PL, weird but necessary :-(
%{__perl} Makefile.PL %{_prefix} INSTALLDIRS=vendor 
%make OPTIMIZE="%{optflags}"
perl -p -i -e 's|/usr/local/bin|/usr/bin|g;' *.pm examples/*
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc Changes Credits MANIFEST README examples QuickRef
%{perl_vendorarch}/auto/Net/SSLeay
%{perl_vendorarch}/Net/SSLeay*
%{perl_vendorarch}/Net/*.pl
%{_mandir}/*/*


%changelog
* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.25
- P2: security fix for CVE-2005-0106

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.25
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25-11avx
- rebuild against perl 5.8.7

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25-10avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25-9avx
- bootstrap build

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25-8avx
- rebuild against new perl

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.25-7avx
- rebuild against latest openssl

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.25-6avx
- rebuild against new openssl

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.25-5avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 1.25-4sls
- rebuild for perl 5.8.4
- keep autosplitted method, this package does not handle it well if you
  remove them (fpons)

* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 1.25-3sls
- rebuild for new perl
- P1: don't try doing an external test to bakus.pt because it doesn't seem
  to exist and causes the tests to fail

* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 1.25-2sls
- OpenSLS build
- tidy spec

* Thu Aug 21 2003 François Pons <fpons@mandrakesoft.com> 1.25-1mdk
- created patch to allow large Net::SSLeay::tcp_read_all.
- 1.25.

* Thu Aug 14 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.22-4mdk
- rebuild for new perl
- don't use PREFIX
- use %%makeinstall_std macro
- use %%make macro

* Fri Jul 18 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.22-3mdk
- drop Prefix tag, and use %%{_prefix}
- rm -rf $RPM_BUIlD_ROOT in %%install, not %%prep nor %%build
- don't require perl, rpm will figure out this by itself

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.22-2mdk
- rebuild for new auto{prov,req}

* Fri Apr 18 2003 François Pons <fpons@mandrakesoft.com> 1.22-1mdk
- 1.22.

* Mon Nov 04 2002 François Pons <fpons@mandrakesoft.com> 1.21-1mdk
- 1.21.

* Fri Oct 25 2002 François Pons <fpons@mandrakesoft.com> 1.20-1mdk
- 1.20.

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 1.18-3mdk
- rebuild for perl thread-multi

* Wed Jul 31 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.18-2mdk
- openssl_path is /usr here, therefore don't -I/usr/include and
  especially don't (badly) hardcode standard library search path
  /usr/lib

* Fri Jul 19 2002 François Pons <fpons@mandrakesoft.com> 1.18-1mdk
- 1.18.

* Wed Jul 10 2002 Christian Belisle <cbelisle@mandrakesoft.com> 1.17-3mdk
- add 'make test'

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 1.17-2mdk
- cleanup
- rebuild for perl 5.8.0

* Mon Jun 10 2002 François Pons <fpons@mandrakesoft.com> 1.17-1mdk
- 1.17.

* Thu Apr 11 2002 François Pons <fpons@mandrakesoft.com> 1.15-1mdk
- 1.15.

* Tue Apr 09 2002 François Pons <fpons@mandrakesoft.com> 1.14-1mdk
- added missing autosplit.ix file.
- 1.14.

* Tue Mar 26 2002 François Pons <fpons@mandrakesoft.com> 1.13-1mdk
- cleaned %%files (removed .al files).
- 1.13.

* Wed Dec 05 2001 Stefan van der Eijk <stefan@eijk.nu> 1.09-3mdk
- fix files section (stefan sux)

* Mon Dec 03 2001 Stefan van der Eijk <stefan@eijk.nu> 1.09-2mdk
- %%{perl_vendorlib} --> %%{perl_vendorlib}/*

* Thu Nov 08 2001 François Pons <fpons@mandrakesoft.com> 1.09-1mdk
- 1.09.

* Mon Oct 15 2001 Stefan van der Eijk <stefan@eijk.nu> 1.08-2mdk
- BuildRequires: openssl-devel perl-devel

* Thu Sep 20 2001 Philippe Libat <philippe@mandrakesoft.com> 1.08-1mdk
- New version

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.05-4mdk
- Rebuild for the latest perl.

* Fri Sep 1 2000 Philippe Libat <philippe@mandrakesoft.com> 1.05-4mdk
- corrected /usr/local/bin

* Thu Aug 31 2000 Philippe Libat <philippe@mandrakesoft.com> 1.05-3mdk
- doc
- macroszifications.

* Tue Aug 10 1999  Rex Wu <rex@intercept.com.tw>
- Spec file was generated.

