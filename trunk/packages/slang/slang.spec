%define name	slang
%define version 1.4.9
%define release 5sls

%define docversion	1.4.8
%define major		1
%define	lib_name	%mklibname %{name} %{major}
%define	lib_name_devel	%{lib_name}-devel

Summary:	The shared library for the S-Lang extension language.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		ftp://space.mit.edu/pub/davis/slang/
Source:		ftp://space.mit.edu/pub/davis/slang/slang-%{version}.tar.bz2
Source1:	ftp://space.mit.edu/pub/davis/slang/slang-%{docversion}-doc.tar.bz2

BuildRoot:	%{_tmppath}/slang-root

%description
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.

%package -n %{lib_name}
Summary:	The shared library for the S-Lang extension language.
Group:		System/Libraries
Provides:	slang
Obsoletes:	slang

%description -n %{lib_name}
S-Lang is an interpreted language and a programming library.  The
S-Lang language was designed so that it can be easily embedded into
a program to provide the program with a powerful extension language.
The S-Lang library, provided in this package, provides the S-Lang
extension language.  S-Lang's syntax resembles C, which makes it easy
to recode S-Lang procedures in C if you need to.


%package -n %{lib_name_devel}
Summary:	The static library and header files for development using S-Lang.
Group:		Development/C
Provides:	lib%{name}-devel slang-devel
Obsoletes:	slang-devel
Requires:	%{lib_name} = %{version}

%description -n %{lib_name_devel}
This package contains the S-Lang extension language static libraries
and header files which you'll need if you want to develop S-Lang based
applications.  Documentation which may help you write S-Lang based
applications is also included.

Install the slang-devel package if you want to develop applications
based on the S-Lang extension language.


%prep
%setup -q

%build
%configure2_5x	--includedir=%{_includedir}/slang

#(peroyvind) passing this to configure does'nt work..
%make ELF_CFLAGS="$RPM_OPT_FLAGS -fno-strength-reduce -fPIC" elf
%make all

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/slang
make	prefix=$RPM_BUILD_ROOT%{_prefix} \
	install_lib_dir=$RPM_BUILD_ROOT%{_libdir} \
	install_include_dir=$RPM_BUILD_ROOT%{_includedir}/slang \
	install-elf install

ln -sf lib%{name}.so.%{version} $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.%{major}

rm -f doc/doc/tm/tools/`arch`objs doc/doc/tm/tools/solarisobjs

# Remove unpackages files
rm -rf	$RPM_BUILD_ROOT/usr/doc/slang/COPYING \
	$RPM_BUILD_ROOT/usr/doc/slang/COPYING.ART \
	$RPM_BUILD_ROOT/usr/doc/slang/COPYING.GPL \
	$RPM_BUILD_ROOT/usr/doc/slang/COPYRIGHT \
	$RPM_BUILD_ROOT/usr/doc/slang/changes.txt \
	$RPM_BUILD_ROOT/usr/doc/slang/cref.txt \
	$RPM_BUILD_ROOT/usr/doc/slang/cslang.txt \
	$RPM_BUILD_ROOT/usr/doc/slang/slang.txt \
	$RPM_BUILD_ROOT/usr/doc/slang/slangdoc.html \
	$RPM_BUILD_ROOT/usr/doc/slang/slangfun.txt

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libslang.so.*

%files -n %{lib_name_devel}
%defattr(-,root,root)
%{_libdir}/libslang.a
%{_libdir}/libslang.so
%dir %{_includedir}/slang/
%{_includedir}/slang/*.h

%changelog
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
