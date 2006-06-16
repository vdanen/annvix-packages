#
# spec file for package slang
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		slang
%define version 	1.4.9
%define release 	%_revrel

%define docversion	1.4.8
%define major		1
%define	libname		%mklibname %{name} %{major}

Summary:	The shared library for the S-Lang extension language
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		ftp://space.mit.edu/pub/davis/slang/
Source:		ftp://space.mit.edu/pub/davis/slang/slang-%{version}.tar.bz2
Source1:	ftp://space.mit.edu/pub/davis/slang/slang-%{docversion}-doc.tar.bz2
Source2:	README.UTF-8
# (mpol) utf8 patches from http://www.suse.de/~nadvornik/slang/
Patch1:		slang-debian-utf8.patch
Patch2:		slang-utf8-acs.patch
Patch3:		slang-utf8-fix.patch
Patch4:		slang-utf8-revert_soname.patch
Patch5:		slang-1.4.9-offbyone.patch
Patch6:		slang-1.4.5-utf8-segv.patch
Patch7:		slang-1.4.9-gcc4.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.


%package -n %{libname}
Summary:	The shared library for the S-Lang extension language
Group:		System/Libraries
Provides:	slang
Obsoletes:	slang

%description -n %{libname}
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.


%package -n %{libname}-devel
Summary:	The static library and header files for development using S-Lang
Group:		Development/C
Provides:	lib%{name}-devel slang-devel
Obsoletes:	slang-devel
Requires:	%{libname} = %{version}

%description -n %{libname}-devel
This package contains the S-Lang extension language static libraries
and header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1 -b .revert_soname
%patch5 -p1 -b .offbyone
%patch6 -p1 -b .segv
%patch7 -p1 -b .gcc4

cp %{SOURCE2} .


%build
%configure2_5x	--includedir=%{_includedir}/slang

#(peroyvind) passing this to configure does'nt work..
%make ELF_CFLAGS="%{optflags} -fno-strength-reduce -fPIC" elf
%make all


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_includedir}/slang
make prefix=%{buildroot}%{_prefix} \
    install_lib_dir=%{buildroot}%{_libdir} \
    install_include_dir=%{buildroot}%{_includedir}/slang \
    install-elf install

ln -sf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{major}

rm -f doc/doc/tm/tools/`arch`objs doc/doc/tm/tools/solarisobjs

# Remove unpackages files
rm -rf	%{buildroot}/usr/doc/slang


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/lib*.a
%{_libdir}/lib*.so
%dir %{_includedir}/slang/
%{_includedir}/slang/*.h

%files doc
%defattr(-,root,root)
%doc COPYING COPYRIGHT README changes.txt README.UTF-8 NEWS


%changelog
* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-12avx
- P6: fix a segv (warly)
- P7: gcc4 build support (warly)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-11avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-10avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-9avx
- bootstrap build

* Mon Mar 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-8avx
- fix ownership

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-7avx
- put docs back in
- add utf8 patches from SUSE (mpol)
- make compat symlinks for devel package (mpol)
- P5: fix off-by-one error (mpol)
- spec cleanups

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4.9-6avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.4.9-5sls
- minor spec cleanups
- remove %%build_opensls macro

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 1.4.9-4sls
- OpenSLS build
- tidy spec
- use %%build_opensls to prevent building -doc package

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.9-3mdk
- Fix Requires, factor out lib_name

* Thu Jul 10 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.4.9-2mdk
- rebuild

* Fri May 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.4.9-1mdk
- 1.4.9
- use %%mklibname
- use $RPM_OPT_FLAGS for elf too
- use %%configure2_5x macro
- fix removal of object files in docs, also make install short-circuitable
- give doc package own version

* Sun Jan 19 2003 Stefan van der Eijk <stefan@eijk.nu> 1.4.5-4mdk
- Remove unpackaged files

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.4.5-3mdk
- fix doc subpackage group

* Tue Jun 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4.5-2mdk
- rpmlint fixes: configure-without-libdir-spec

* Mon Apr 08 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.4.5-1mdk
- New and shiny slang.

* Thu Oct  4 2001 Warly <warly@mandrakesoft.com> 1.4.4-3mdk
- remove non built doc example binaries

* Tue Aug 14 2001 Warly <warly@mandrakesoft.com> 1.4.4-2mdk
- remove slang buildrequires

* Mon Feb 26 2001 Warly <warly@mandrakesoft.com> 1.4.4-1mdk
- new version

* Tue Feb 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.4.3-1mdk
- s/1.4.2/1.4.3/;
- updated slangdoc to 1.4.3.
- use -j, not -y to pass the bzip2 filter through tar.
- for slang-devel fix the requires so that it is macro-ized so that you don't
  have to change it for every version.

* Wed Dec  6 2000 Warly <warly@mandrakesoft.com> 1.4.2-2mdk
- new lib policy

* Sun Aug 20 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.4.2-1mdk
- s|1.4.0|1.4.2|.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.4.0-6mdk
- automatically added BuildRequires

* Mon May 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.4.0-5mdk
- Move libslang.so from -devel to normal.

* Fri May 19 2000 Pixel <pixel@mandrakesoft.com> 1.4.0-4mdk
- move .so to devel
- add soname

* Tue May 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.4.0-3mdk
- Add link for alpha.

* Mon Mar 27 2000 Warly <warly@mandrakesoft.com> 1.4.0-2mdk
- fix doc path

* Sun Mar 26 2000 Warly <warly@mandrakesoft.com> 1.4.0-1mdk
- 1.4.0
- new package doc

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Wed Jul 14 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.3.8.

* Mon Jun 07 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 1.3.7.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Wed Oct 21 1998 Bill Nottingham <notting@redhat.com>
- libslang.so goes in -devel

* Sun Jun 07 1998 Prospector System <bugs@redhat.com>

- translations modified for de

* Sat Jun  6 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.2.2 with buildroot.

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat Apr 18 1998 Erik Troan <ewt@redhat.com>
- rebuilt to find terminfo in /usr/share

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Mon Sep 1 1997 Donnie Barnes <djb@redhat.com>
- upgraded to 0.99.38 (will it EVER go 1.0???)
- all patches removed (all appear to be in this version)

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
