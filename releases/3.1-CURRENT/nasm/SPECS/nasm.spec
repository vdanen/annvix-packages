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
%define version		2.02
%define release		%_revrel

Summary:	The Netwide Assembler, a portable x86 assembler with Intel-like syntax
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		Development/Other
URL:		http://nasm.sourceforge.net
Source:		http://prdownloads.sourceforge.net/nasm/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	groff
BuildRequires:	texinfo
BuildRequires:	glibc-static-devel

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


%build
rm -f config.cache config.status config.log
%configure2_5x
make
make rdf
 
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
%{_mandir}/man1/ldrdf.1*
%{_mandir}/man1/rd*.1*

%files doc
%defattr(-,root,root)
%doc COPYING CHANGES TODO AUTHORS README doc/internal.doc
%doc rdoff-v1-v2.txt README.rdoff


%changelog
* Wed Mar 05 2008 Vincent Danen <vdanen-at-build.annvix.org> 2.02
- 2.02

* Thu Dec 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.00
- 2.00
- buildrequires: glibc-static-devel

* Sat Oct 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.99.01
- 0.99.01
- drop P0; merged upstream

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
