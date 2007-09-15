#
# spec file for package pcre
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		pcre
%define version		7.3
%define	release		%_revrel

%define major		0
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname %{name} -d

Summary: 	PCRE is a Perl-compatible regular expression library
Name:	 	%{name}
Version:	%{version}
Release:	%{release}
License: 	BSD-Style
Group: 		File Tools
URL: 		http://www.pcre.org/
Source0:	ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{name}-%{version}.tar.bz2.sig

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	automake

Requires: 	%{libname} = %{version}

%description
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. 
This package contains a grep variant based on the PCRE library.


%package -n %{libname}
Group:		System/Libraries
Summary:	PCRE is a Perl-compatible regular expression library
Provides:	lib%{name} = %{version}-%{release}

%description -n %{libname}
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h. The official POSIX name is
regex.h, but I didn't want to risk possible problems with existing files of
that name by distributing it that way. To use it with an existing program that
uses the POSIX API, it will have to be renamed or pointed at by a link.


%package -n %{devname}
Group:		Development/C
Summary:	Headers and static lib for pcre development
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 0 -d

%description -n %{devname}
Install this package if you want do compile applications using the pcre
library.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%configure2_5x --enable-utf8
%make


%check
export LC_ALL=C
make check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/pcre-config

mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}/%{_libdir}/lib%{name}.so.%{major}.* %{buildroot}/%{_lib}
cd %{buildroot}/%{_libdir}
ln -s ../../%{_lib}/lib%{name}.so.%{major}.* .

# remove unwanted files
rm -rf %{buildroot}%{_docdir}/%{name}/html
rm -f %{buildroot}%{_docdir}/%{name}/{AUTHORS,ChangeLog,COPYING,LICENCE,NEWS,README,pcre{,grep,test,-config}.txt}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
 

%files
%defattr(-,root,root)
%{_mandir}/man1/pcregrep.1*
%{_mandir}/man1/pcretest.1*
%{_bindir}/pcregrep  
%{_bindir}/pcretest

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/lib*.so.*
%{_libdir}/lib*.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/lib*.a
%{_libdir}/lib*.la
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/libpcre.pc
%{_libdir}/pkgconfig/libpcrecpp.pc
%{_includedir}/*.h
%{_bindir}/pcre-config
%multiarch %{multiarch_bindir}/pcre-config
%{_mandir}/man1/pcre-config.1*
%{_mandir}/man3/*.3*

%files doc
%defattr(-,root,root)
%doc AUTHORS NEWS README NON-UNIX-USE


%changelog
* Sat Sep 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 7.3
- 7.3
- implement devel naming policy
- implement library provides policy
- build fixes
- drop P0; no longer required
- add the gpg sig for the source tarball

* Mon Nov 13 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.7
- 6.7
- put the tests inside %%check

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.3
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.3
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-1avx
- 6.3

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.2-1avx
- 6.2
- multiarch
- move pkgconfig file to the devel package
- P0: skip RunTest test #2 as it keeps failing for some reason; all other
  tests check out (TODO: this needs to be fixed!)

* Wed Jul 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.5-4avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.5-3avx
- bootstrap build

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.5-2avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 4.5-1sls
- 4.5
- remove P0
- Requires: automake1.7
- sync with cooker 4.5-4mdk:
  - (gb) fix deps (abel)
  - don't need to regen auto* stuff, cputoolize would do the job (abel)
  - BuildRequires: automake1.7


* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 4.3-7sls
- BuildRequires: autoconf2.5
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 4.3-6sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
