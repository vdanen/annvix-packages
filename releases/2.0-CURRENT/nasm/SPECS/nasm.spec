#
# spec file for package nasm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		nasm
%define version		0.98.39
%define release		%_revrel

Summary:	The Netwide Assembler, a portable x86 assembler with Intel-like syntax
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		Development/Other
URL:		http://nasm.sourceforge.net
Source:		http://prdownloads.sourceforge.net/nasm/%{name}-%{version}.tar.bz2
Patch0:		nasm-0.98.39-CAN-2005-1194.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	groff, texinfo

%description
NASM is the Netwide Assembler, a free portable assembler for the Intel
80x86 microprocessor series, using primarily the traditional Intel
instruction mnemonics and syntax.


%package rdoff
Summary:	Tools for the RDOFF binary format, sometimes used with NASM
Group:		Development/Other

%description rdoff
Tools for the operating-system independent RDOFF binary format, which
is sometimes used with the Netwide Assembler (NASM).  These tools
include linker, library manager, loader, and information dump.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .can-2005-1194


%build
rm -f config.cache config.status config.log
%configure2_5x
%make
%make rdf

mv rdoff/README README.rdoff
mv rdoff/doc/v1-v2.txt rdoff-v1-v2.txt


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_infodir},%{_mandir}/man1}
%makeinstall install_rdf


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(755,root,root) %{_bindir}/nasm
%attr(755,root,root) %{_bindir}/ndisasm
%{_mandir}/man1/nasm.1*
%{_mandir}/man1/ndisasm.1*

%files rdoff
%defattr(-,root,root)
%{_bindir}/rdfdump
%{_bindir}/ldrdf
%{_bindir}/rdx
%{_bindir}/rdflib
%{_bindir}/rdf2bin
%{_bindir}/rdf2ihx
%{_bindir}/rdf2com

%files doc
%defattr(-,root,root)
%doc COPYING CHANGES TODO AUTHORS README doc/internal.doc
%doc rdoff-v1-v2.txt README.rdoff


%changelog
* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.98.39
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.98.39
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.98.39
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.98.39-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.98.39-3avx
- rebuild for new gcc

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.98.39-2avx
- rebuild

* Wed May 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.98.39-1avx
- 0.98.39 (includes security fix for CAN-2004-1287)
- P0: patch to fix CAN-2005-1194
- fix configure macro

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.98.35-5avx
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 0.98.35-4sls
- minor spec cleanups
- remove %%build_opensls macro

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 0.98.35-3sls
- OpenSLS build
- tidy spec
- use %%build_opensls to not build -doc pkg

* Mon Jul 21 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.98.35-2mdk
- rebuild

* Fri Nov 22 2002 François Pons <fpons@mandrakesoft.com> 0.98.35-1mdk
- 0.98.35.

* Sun Oct 27 2002 Stefan van der Eijk <stefan@eijk.nu> 0.98.34-3mdk
- BuildRequires: ghostscript (ps2pdf)

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.98.34-2mdk
- fix doc subpackage group

* Mon Jun 10 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.98.34-1mdk
- new release

* Fri May 24 2002 François Pons <fpons@mandrakesoft.com> 0.98.32-1mdk
- 0.98.32.

* Tue May 14 2002 François Pons <fpons@mandrakesoft.com> 0.98.31-1mdk
- 0.98.31.

* Mon Apr 22 2002 François Pons <fpons@mandrakesoft.com> 0.98.25alt-2mdk
- updated License tag (LGPL).
- fixed doc reference.

* Mon Mar 25 2002 François Pons <fpons@mandrakesoft.com> 0.98.25alt-1mdk
- re-changed License tag.
- 0.98.25alt.

* Thu Jan 24 2002 François Pons <fpons@mandrakesoft.com> 0.98.22-1mdk
- bzip2-ed nasmdoc.txt and nasmdoc.ps files.
- changed License tag.
- 0.98.22.

* Wed Nov 07 2001 François Pons <fpons@mandrakesoft.com> 0.98.08-1mdk
- 0.98.08.

* Tue Oct 23 2001 François Pons <fpons@mandrakesoft.com> 0.98-9mdk
- small source rpm rework.

* Thu Jul 26 2001 Warly <warly@mandrakesoft.com> 0.98-8mdk
- rebuild

* Fri Jan 12 2001 David BAUDENS <baudens@mandrakesoft.com> 0.98-7mdk
- BuildRequires: texinfo
- Use %%make macro

* Fri Nov 24 2000 Warly <warly@mandrakesoft.com> 0.98-6mdk
- Change license

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.98-5mdk
- BM

* Wed Jul 12 2000 Thierry Vignaud <tvignaud@mandrakesoft.com>  0.98-4mdk
- use new macros
- make package short-circuit compliant ...
- Andrew Lee <andrew@cle.linux.org.tw> : add Enhanced 3D Now! patch
- move post & postun script from -doc in main package since info pages are
  there ...

* Wed Apr 05 2000 Warly <warly@linux-mandrake.com> 0.98-3mdk
- new group: Development/Other
- spec-helper

* Thu Feb 03 2000 Giuseppe Ghibò <ghibo@linux-mandrake.com>
- added BuildPreReq.
- changed doc dirs.

* Mon Aug 23 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- First spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
