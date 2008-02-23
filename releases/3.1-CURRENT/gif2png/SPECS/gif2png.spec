#
# spec file for package gif2png
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		gif2png
%define version 	2.5.1
%define release 	%_revrel

Summary:	Tools for converting websites from using GIFs to using PNGs
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT style
Group:		Graphics
URL:		http://www.catb.org/~esr/gif2png/
Source:		http://www.catb.org/~esr/gif2png/%{name}-%{version}.tar.gz
Patch0:		gif2png-2.5.1-gentoo-libpng_compile_fixes.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	png-devel
BuildRequires:	zlib-devel

Requires:	python

%description 
Tools for converting GIFs to PNGs.  The program gif2png converts GIF files 
to PNG files.  The Python script web2png converts an entire web tree, 
also patching HTML pages to keep IMG SRC references correct.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0


%build
%configure
%make
 

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root,0755)
%{_mandir}/*/*
%{_bindir}/*

%files doc
%defattr(-,root,root,0755)
%doc README NEWS COPYING AUTHORS			 


%changelog
* Fri Feb 22 2008 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1
- rebuild against new libpng
- fix buildrequires

* Fri Nov 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.5.1
- 2.5.1
- P0: patch from Gentoo to build against libpng 1.2.12+

* Wed Apr 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7
- rebuild against new libpng

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7
- Clean rebuild

* Thu Jan 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7-7avx
- rebuild against new libpng

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7-6avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7-5avx
- rebuild

* Thu Jun 24 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.7-4avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.4.7-3sls
- minor spec cleanups
- get rid of the french and spanish descriptions

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.4.7-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
