#
# spec file for package mpage
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mpage
%define version		2.5.5
%define release		%_revrel

Summary:	A tool for printing multiple pages of text on each printed page
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Configuration
URL:		http://www.mesa.nl/pub/mpage
Source:		http://www.mesa.nl/pub/mpage/%{name}-%{version}.tgz
Patch0:		mpage-2.5.4-config.patch
# Japanese patch.bz2
Patch10:	mpage-2.5.3-j.patch
Patch20:	mpage-mfix.patch
Patch21:	mpage-psprint.patch
Patch22:	mpage-2.5.3-japanese-fix.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The mpage utility takes plain text files or PostScript(TM) documents
as input, reduces the size of the text, and prints the files on a
PostScript printer with several pages on each sheet of paper.  Mpage
is very useful for viewing large printouts without using up tons of
paper.  Mpage supports many different layout options for the printed
pages.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .config
%patch10 -p1 -b .jp
%patch20 -p1 -b .fix
%patch21 -p1
%patch22 -p0


%build
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/mpage
%{_mandir}/man1/mpage.1*
%dir %{_datadir}/mpage
%{_datadir}/mpage/*

%files doc
%defattr(-,root,root)
%doc CHANGES Copyright README NEWS TODO


%changelog
* Sat Dec 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.5
- 2.5.5
- drop P1; no longer needed

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4
- fix group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.4-1avx
- 2.5.4
- P1: gcc4 & makefilery fixes (gbeauchesne)
- move encodings where that are expected to be: %%_datadir/mpage (gbeauchesne)

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.3-10avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.5.3-9avx
- rebuild

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.5.3-8avx
- Annvix build

* Sun Mar 07 2004 Vincent Danen <vdanen@opensls.org> 2.5.3-7sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.5.3-6sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
