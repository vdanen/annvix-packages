%define module	Tk
%define name	perl-%{module}
%define version 800.024
%define release 6sls

%define _requires_exceptions Watch

Summary:	Tk modules for Perl
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.cpan.org
Source:		ftp://sunsite.doc.ic.ac.uk/packages/CPAN/modules/by-module/Tk/Tk%{version}.tar.bz2

Buildroot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	perl-devel XFree86-devel

Provides:	perl/tk ptk pTk
Requires:	perl
Provides:	perl(Tk::LabRadio) perl(Tk::TextReindex)

%description
This package provides the modules and Tk code for Perl/Tk,
as written by Nick Ing-Simmons (pTk), John Ousterhout(Tk),
and Ioi Kim Lam(Tix).
It gives you the ability to develop perl applications using the Tk GUI.
It includes the source code for the Tk and Tix elements it uses.
The licences for the various components differ, so check the copyright.

%package devel
Summary:	Tk modules for Perl (development package)
Group:		Development/C
Requires:	perl-Tk = %{version}

%description devel
This package provides the modules and Tk code for Perl/Tk,
as written by Nick Ing-Simmons (pTk), John Ousterhout(Tk),
and Ioi Kim Lam(Tix).
It gives you the ability to develop perl applications using the Tk GUI.
It includes the source code for the Tk and Tix elements it uses.
The licences for the various components differ, so check the copyright.

This is the development package.

%prep
%setup -q -n Tk%{version}
find . -type f | xargs perl -pi -e 's|^#!.*/bin/perl\S*|#!/usr/bin/perl|'
# Make it lib64 aware, avoid patch
perl -pi -e "s,(/usr/X11(R6|\\*)|\\\$X11|\(\?:)/lib,\1/%{_lib},g" \
  myConfig pTk/mTk/{unix,tixUnix/{itcl2.0,tk4.0}}/configure
#(peroyvind) --center does no longer seem to be working, obsoleted by -c
perl -pi -e "s#--center#-c#" ./Tk/MMutil.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make OPTIMIZE="$RPM_OPT_FLAGS" LD_RUN_PATH=""

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std
%{__chmod} 644 $RPM_BUILD_ROOT%{_mandir}/man3*/*

# Remove unpackaged files, add them if you find a use
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/{Tie/Watch.pm,Tk/prolog.ps}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{ptk{ed,sh},widget}.1*

## compress all .pm files (as using perl-PerlIO-gzip).
#find $RPM_BUILD_ROOT -name "*.pm" | xargs gzip -9

# get rid of all the pod files
rm -f %{buildroot}%{perl_vendorarch}/Tk.pod
rm -f %{buildroot}%{perl_vendorarch}/Tk/*.pod
rm -f %{buildroot}%{perl_vendorarch}/Tk/README.Adjust

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING ToDo Changes README README.linux
%{_bindir}/*
%{_mandir}/man3*/*
%{perl_vendorarch}/Tk.pm*
%dir %{perl_vendorarch}/Tk
%{perl_vendorarch}/Tk/*.pm*
%{perl_vendorarch}/Tk/*.pl
%{perl_vendorarch}/Tk/*.gif
%{perl_vendorarch}/Tk/*.xbm
%{perl_vendorarch}/Tk/*.xpm
%{perl_vendorarch}/Tk/license.terms
%{perl_vendorarch}/Tk/Credits
%{perl_vendorarch}/Tk/DragDrop
%{perl_vendorarch}/Tk/Event
%{perl_vendorarch}/Tk/Menu
%{perl_vendorarch}/Tk/Text
%{perl_vendorarch}/Tk/demos
%{perl_vendorarch}/auto/Tk
%{perl_vendorarch}/fix_4_os2.pl

%files devel
%defattr(-,root,root)
%doc COPYING Funcs.doc INSTALL
%{perl_vendorarch}/Tk/pTk
%{perl_vendorarch}/Tk/*.def
%{perl_vendorarch}/Tk/*.h
%{perl_vendorarch}/Tk/*.m
%{perl_vendorarch}/Tk/*.t
%{perl_vendorarch}/Tk/typemap


%changelog
* Fri Feb 27 2004 Vincent Danen <vdanen@opensls.org> 800.024-6sls
- remove %%build_opensls macro
- rebuild for new perl

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 800.024-5sls
- OpenSLS build
- tidy spec
- use %%build_opensls to not build the -doc package
- remove pwlib-devel as a BuildReq

* Wed Aug 13 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 800.024-4mdk
- rebuild for new perl
- drop Prefix tag
- don't use PREFIX
- use %%makeinstall_std macro
- fix no longer working --center option to pod2man

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 800.024-3mdk
- rebuild for new auto{prov,req}

* Mon Apr 28 2003 François Pons <fpons@mandrakesoft.com> 800.024-2mdk
- removed compressed perl module as it cause problem with
  other module requiring Tk.

* Fri Feb 14 2003 François Pons <fpons@mandrakesoft.com> 800.024-1mdk
- compressed perl module.
- 800.024.

* Mon Dec  2 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 800.023-10mdk
- Make it lib64 aware

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 800.023-9mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Mon Aug  5 2002 Pixel <pixel@mandrakesoft.com> 800.023-8mdk
- rebuild for perl thread-multi

* Thu Jul 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 800.023-7mdk
- Automated rebuild with gcc3.2

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 800.023-6mdk
- fix the require Perl >= 5.00404

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 800.023-5mdk
- rebuild for perl 5.8.0

* Wed May 29 2002 François Pons <fpons@mandrakesoft.com> 800.023-4mdk
- rebuild for new libstdc++.

* Wed Nov 07 2001 François Pons <fpons@mandrakesoft.com> 800.023-3mdk
- added url tag.

* Sat Jul 07 2001 Stefan van der Eijk <stefan@eijk.nu> 800.023-2mdk
- BuildRequires: perl-devel

* Tue Jul 03 2001 François Pons <fpons@mandrakesoft.com> 800.023-1mdk
- reduced description line too long.
- 800.023.

* Sat Jun 23 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 800.022-7mdk
- Add pwlib-devel as a build requirement (Goetz Waschk).

* Sun Jun 17 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 800.022-6mdk
- Rebuild for the latest perl.

* Tue Nov 14 2000 François Pons <fpons@mandrakesoft.com> 800.022-5mdk
- updated license as the perl one.

* Tue Aug 29 2000 François Pons <fpons@mandrakesoft.com> 800.022-4mdk
- build release.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 800.022-3mdk
- automatically added BuildRequires

* Fri Aug 04 2000 François Pons <fpons@mandrakesoft.com> 800.022-2mdk
- macroszifications.
- added perl-Tk-devel and perl-Tk-doc.

* Tue Jul 18 2000 François Pons <fpons@mandrakesoft.com> 800.022-1mdk
- 800.022.

* Wed May 17 2000 David BAUDENS <baudens@mandrakesoft.com> 800.018-3mdk
- Fix buid for i486

* Wed Apr 26 2000 Frederic Lepied <flepied@mandrakesoft.com> 800.018-2mdk
- updated to perl 5.600

* Fri Feb 11 2000 Lenny Cartier <lenny@mandrakesoft.com> 800.018-1mdk
- v800.18
- used srpm provided by Stefan van der Eijk <s.vandereijk@chello.nl>

* Thu Feb 10 2000 Stefan van der Eijk <s.vandereijk@chello.nl>
- update to 800.018

* Wed Jan 19 2000 Pixel <pixel@mandrakesoft.com>
- mandrake creation/adaptation
- removed the ed stuff by perl (what the hell, it's a perl module!)
