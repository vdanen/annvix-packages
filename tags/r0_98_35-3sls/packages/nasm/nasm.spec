%define name	nasm
%define version	0.98.35
%define release	3sls

%{!?build_opensls:%global build_opensls 0}

Summary:	The Netwide Assembler, a portable x86 assembler with Intel-like syntax
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		Development/Other
URL:		http://nasm.2y.net
Source:		%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	groff, texinfo
%if !%{build_opensls}
BuildRequires:	ghostscript
%endif

%description
NASM is the Netwide Assembler, a free portable assembler for the Intel
80x86 microprocessor series, using primarily the traditional Intel
instruction mnemonics and syntax.

%if !%{build_opensls}
%package doc
Summary:	Extensive documentation for NASM
Group:		Books/Computer books
Prereq:		/sbin/install-info

%description doc
Extensive documentation for the Netwide Assembler, NASM, in HTML,
PostScript, RTF and text formats.
%endif

%package rdoff
Summary:	Tools for the RDOFF binary format, sometimes used with NASM
Group:		Development/Other

%description rdoff
Tools for the operating-system independent RDOFF binary format, which
is sometimes used with the Netwide Assembler (NASM).  These tools
include linker, library manager, loader, and information dump.

%prep

%setup -q

%build
rm -f config.cache config.status config.log
%configure
%if %{build_opensls}
%make
%make rdf
%else
%make everything
%endif

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_bindir},%{_infodir},%{_mandir}/man1}
%makeinstall install_rdf
%if !%{build_opensls}
cd doc
install info/* $RPM_BUILD_ROOT/%{_infodir}/
bzip2 -9f nasmdoc*.txt nasmdoc*.ps||true
cd html
ln -sf nasmdoc0.html index.html
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if !%{build_opensls}
%post
%_install_info nasm.info

%preun
%_remove_install_info nasm.info
%endif

%files
%defattr(-,root,root)
%doc COPYING CHANGES TODO AUTHORS README doc/internal.doc
%attr(755,root,root) %{_bindir}/nasm
%attr(755,root,root) %{_bindir}/ndisasm
%{_mandir}/man1/nasm.1*
%{_mandir}/man1/ndisasm.1*
%if !%{build_opensls}
%{_infodir}/nasm.info*
%endif

%if !%{build_opensls}
%files doc
%defattr(-,root,root)
%doc doc/nasmdoc.ps.bz2 doc/nasmdoc.txt.bz2 doc/nasmdoc.rtf doc/html
%endif

%files rdoff
%defattr(-,root,root)
%doc rdoff/README rdoff/doc/v1-v2
%{_bindir}/rdfdump
%{_bindir}/ldrdf
%{_bindir}/rdx
%{_bindir}/rdflib
%{_bindir}/rdf2bin
%{_bindir}/rdf2ihx
%{_bindir}/rdf2com

%changelog
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
