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
%define version 	2.4.7
%define release 	%_revrel

Summary:	Tools for converting websites from using GIFs to using PNGs
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT style
Group:		Graphics
URL:		http://www.catb.org/~esr/gif2png/
Source:		http://www.catb.org/~esr/gif2png/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libpng-devel zlib-devel

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

* Thu Jul 31 2003 Daouda LO <daouda@mandrakesoft.com> 2.4.7-1mdk
- release 2.4.7
- change url

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.4.6-2mdk
- rebuild
- use %%make macro
- rm -rf %{buildroot} in %%install, not %%prep
- drop Prefix tag

* Fri Dec 27 2002 Daouda LO <daouda@mandrakesoft.com> 2.4.6-1mdk
- release 2.4.6
	o Document masters converted to DocBook
	o Work around an apparent automake bug that produced bad SRPMs
	o Man page typo fix

* Tue Jun 18 2002 Daouda LO <daouda@mandrakesoft.com> 2.4.4-1mdk
- 2.4.4 release

* Thu Oct 18 2001 Daouda LO <daouda@mandrakesoft.com> 2.4.2-2mdk
- s/Copyright/License 
- fix permissions on files

* Mon Jul 30 2001 Daouda LO <daouda@mandrakesoft.com> 2.4.2-1mdk
- release 2.4.2

* Fri Jan 05 2001 Geoff <snailtalk@mandrakesoft.com> 2.4.0-1mdk
- new and shiny source.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.3.2-3mdk
- automatically added BuildRequires

* Sun Jul 23 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.3.2-2mdk
- macroszifications
- full url for src
- rebuilt for BM

* Thu Apr 06 2000 Christopher Molnar <molnarc@mandrakesoft.com> 2.3.2-1mdk
- Updated Version 
- Fixed Group for Mandrake

* Tue Feb 15 2000 Geoffrey Lee <snailtalk@linux-mandrake.com>
- Updated to 2.3.1

* Mon Jan 03 2000 Lenny Cartier <lenny@mandrakesoft.com>
-v2.2.5

* Mon Nov 08 1999 Camille Begnis <camille@mandrakesoft.com>
 
- Upgraded to 2.1.1
               
* Mon Nov 02 1999 Camille Begnis <camille@mandrakesoft.com>

- Upgraded to 2.0.1
					 
* Mon Oct 25 1999 Camille Begnis <camille@mandrakesoft.com>

- Specfile adaptions for Mandrake,
- Add python requirement,
- gz to bz2 compression,	 

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
