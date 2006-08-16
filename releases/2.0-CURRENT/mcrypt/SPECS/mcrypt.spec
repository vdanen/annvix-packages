#
# spec file for package mcrypt
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mcrypt
%define version 	2.6.4
%define release 	%_revrel

Summary:	Data encryption/decryption program
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		File Tools
URL:		http://mcrypt.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libmhash-devel >= 0.8.15
BuildRequires:	libmcrypt-devel >= 2.5.0
BuildRequires:	libltdl-devel

%description
A replacement for the old unix crypt(1) command. Mcrypt uses the following
encryption (block) algorithms: BLOWFISH, DES, TripleDES, 3-WAY, SAFER-SK64,
SAFER-SK128, CAST-128, RC2 TEA (extended), TWOFISH, RC6, IDEA and GOST. The
unix crypt algorithm is also included, to allow compatibility with the
crypt(1) command.

CBC, ECB, OFB and CFB modes of encryption are supported.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files doc
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS ChangeLog COPYING INSTALL NEWS README THANKS TODO doc/FORMAT doc/magic doc/sample*


%changelog
* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.4
- spec cleanups
- remove locales

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.4
- add -doc subpackage
- rebuild with gcc4
- rebuild against new mhash
- fix description and group

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.4
- Clean rebuild

* Sat Jan 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.4-9avx
- rebuild against new mhash

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.4-8avx
- bootstrap build (new gcc, new glibc)

* Fri Jul 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.4-7avx
- rebuild against new gcc

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.4-6avx
- rebuild
- buildrequires: libltdl-devel

* Thu Aug 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.4-5avx
- use %%configure2_5x
- remove unneeded deps and make deps version specific

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.4-4avx
- Annvix build

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 2.6.4-3sls
- minor spec cleanups
- remove %%prefix

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.6.4-2sls
- OpenSLS build
- tidy spec
