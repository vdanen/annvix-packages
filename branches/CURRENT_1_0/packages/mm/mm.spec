%define name	mm
%define version	1.3.0
%define release	5sls

%define	major		1
%define libname		%mklibname %name %major
%define libnamedev	%{libname}-devel
%define libnamestatic	%{libname}-static-devel

Summary:	Shared Memory Abstraction Library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-Style
Group:		Development/C
URL:		http://www.engelschall.com/sw/mm/
Source:		http://www.engelschall.com/sw/mm/mm-%{version}.tar.bz2
Patch:		mm-1.1.3-shtool.patch.bz2

BuildRoot:	%{_tmppath}/mm-%{version}-buildroot

%description
The MM library is a 2-layer abstraction library which simplifies the usage of
shared memory between forked (and this way strongly related) processes under
Unix platforms. On the first layer it hides all platform dependent
implementation details (allocation and locking) when dealing with shared
memory segments and on the second layer it provides a high-level malloc(3)-
style API for a convenient and well known way to work with data-structures
inside those shared memory segments.

The library is released under the term of an open-source (BSD-style) license
because it's originally written for a proposed use inside next versions of
the Apache webserver as a base library for providing shared memory pools to
Apache modules (because currently Apache modules can only use heap-allocated
memory which isn't shared accross the pre-forked server processes). The
requirement actually comes from comprehensive modules like mod_ssl, mod_perl
and mod_php which would benefit a lot from easy to use shared memory pools.
Mostly all functionality (except for shared locks in addition to exclusive
locks and multi-segment memory areas instead of single-segment memory areas)
is already implemented and the library already works fine under FreeBSD,
Linux and Solaris and should also adjust itself for most other Unix platforms
with it's GNU Autoconf and GNU Libtool based configuration and compilation
procedure. 

%package -n %libname
Summary:	Shared Memory Abstraction Library
Group:		Development/C
Obsoletes:	mm
Provides:	mm = %{version}
Provides:       ADVXpackage

%description -n %libname
The MM library is a 2-layer abstraction library which simplifies the usage of
shared memory between forked (and this way strongly related) processes under
Unix platforms. On the first layer it hides all platform dependent
implementation details (allocation and locking) when dealing with shared
memory segments and on the second layer it provides a high-level malloc(3)-
style API for a convenient and well known way to work with data-structures
inside those shared memory segments.

The library is released under the term of an open-source (BSD-style) license
because it's originally written for a proposed use inside next versions of
the Apache webserver as a base library for providing shared memory pools to
Apache modules (because currently Apache modules can only use heap-allocated
memory which isn't shared accross the pre-forked server processes). The
requirement actually comes from comprehensive modules like mod_ssl, mod_perl
and mod_php which would benefit a lot from easy to use shared memory pools.
Mostly all functionality (except for shared locks in addition to exclusive
locks and multi-segment memory areas instead of single-segment memory areas)
is already implemented and the library already works fine under FreeBSD,
Linux and Solaris and should also adjust itself for most other Unix platforms
with it's GNU Autoconf and GNU Libtool based configuration and compilation
procedure. 

%package -n %libnamedev
Summary:	Development files for mm.
Group:		Development/C
Requires:	%libname = %{version}
Obsoletes:	mm-devel
Provides:	%libnamedev, libmm-devel = %{version}, mm-devel = %{version}
Provides:       ADVXpackage

%description -n %libnamedev
The MM library is a 2-layer abstraction library which simplifies the usage of
shared memory between forked (and this way strongly related) processes under
Unix platforms. On the first layer it hides all platform dependent
implementation details (allocation and locking) when dealing with shared
memory segments and on the second layer it provides a high-level malloc(3)-
style API for a convenient and well known way to work with data-structures
inside those shared memory segments.

This package contain files that are needed to develop applications which use
the MM shared memory library.

%package -n %libnamestatic
Summary:	Development files for mm.
Group:		Development/C
Requires:	%libname = %{version}
Obsoletes:	mm-static-devel
Provides:	%libnamedev, libmm-static-devel = %{version}, mm-static-devel = %{version}
Provides:       ADVXpackage

%description -n %libnamestatic
The MM library is a 2-layer abstraction library which simplifies the usage of
shared memory between forked (and this way strongly related) processes under
Unix platforms. On the first layer it hides all platform dependent
implementation details (allocation and locking) when dealing with shared
memory segments and on the second layer it provides a high-level malloc(3)-
style API for a convenient and well known way to work with data-structures
inside those shared memory segments.

This package contain files that are needed to develop applications which use
the MM shared memory library.

%prep
%setup -q
%patch0 -p0

#not needed with 1.2 series
#%patch1 -p1 -b .tmpfile
libtoolize -f

%build
%serverbuild
%configure2_5x
#%make
#%make test
#JMD 22 Feb 2002 - mm doesn't like the -j2...
make
make test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
perl -pi -e "s|/(.*)buildroot||g;" $RPM_BUILD_ROOT/usr/bin/mm-config

rm -f %{buildroot}%{_libdir}/*.la

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -p /sbin/ldconfig -n %libname
%postun -p /sbin/ldconfig -n %libname

%files -n %libname
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %libnamedev
%defattr(-,root,root)
%doc README LICENSE ChangeLog INSTALL PORTING THANKS
%{_bindir}/*
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %libnamestatic
%defattr(-,root,root)
%{_libdir}/*.a

%changelog
* Sat Jan 04 2004 Vincent Danen <vdanen@opensls.org> 1.3.0-4sls
- minor spec cleanups
- remove %%prefix

* Sat Jan 04 2004 Vincent Danen <vdanen@opensls.org> 1.3.0-4sls
- OpenSLS build
- tidy spec

* Thu Aug 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.3.0-3mdk
- fix mklibname

* Mon Jul 21 2003 David BAUDENS <baudens@mandrakesoft.com> 1.3.0-2mdk
- Rebuild to fix bad signature

* Fri May 09 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.0-1mdk
- 1.3.0

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.2.2-2mdk
- use %%mklibname

* Thu Jan 02 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.2.2-1mdk
- new mm version
- Add Provides: ADVXpackage, all ADVX package will have this tag, 
  so we can easily do a rpm --whatprovides ADVXpackage to find out
  what ADVX packages a user has installed on his system. 

* Fri Nov 08 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.2.1-2mdk
- Rebuilt for Cooker

* Mon Oct 28 2002 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.2.1-1mdk
- New version

* Thu Aug  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.1.3-10mdk
- security update
- static file split

* Fri Feb 22 2002 Jean-Michel Dault <jgarzik@mandrakesoft.com> 1.1.3-9mdk
- Remove the make macro because it crashes with -j2
- Put all doc and manpages in -devel package
- s/Copyright/License

* Sat Jul  7 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.1.3-8mdk
- new lib policy.  replaces package mm.
- remove packager/distro/etc tags
- clean up spec a bit
- Use %%configure and %%make macros
- Regenerate libtool at build time

* Sat Apr 14 2001 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.1.3-7mdk
- serverbuild
- rebuild (on a machine that does not have libsafe!!!!)

* Tue Sep 27 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.1.3-6mdk
- fixed library name - thanks to GOMEZ Henri <hgomez@slib.fr>!

* Wed Aug 31 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.1.3-5mdk
- Fixed mm-config. There was a line in it that said:
  prefix="/home/tv/rpm/tmp/mm-1.1.3-buildroot/usr", and it was propagated 
  in all apache-related packages!!!
- Re-Added the packager, etc.. tags, so everyone knows I'm the maintainer
  and that if they fix the package, I sould be advised, because otherwise
  apache will be broken!!!

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1.3-4mdk
- remove Packager, Distribution, Vendor (jmd scks!)

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1.3-3mdk
- BM

* Fri Jul 14 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 1.1.3-2mdk
- macro-ize spec
- spin off devel package
- full url for source
- jmdault merged modifications from chmouel@mandrakesoft.com and Mikhail 
  Zabaluev (Mandrake Russian Extensions from IPlabs.ru)
  PS: -Chmouel- the %configure macro does not work for this package (uses
  different libtool)

* Fri Jul 07 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.1.3-1mdk
- new release

* Mon Apr 17 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.0.12-3mdk
- put full path to ldconfig
- fixed badly broken specfile

* Mon Apr 17 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.0.12-2mdk
- added the include files
- put it in main distribution since Apache now needs it

* Wed Apr 05 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.0.12-1mdk
- fix group
- fix files section
- full url for source
- misc spec fixes

* Sun Mar 26 2000 Oden Eriksson <oden@kvikkjokk.com>
- cpu optimizations

* Sat Jan 22 2000 Edward S. Marshall <emarshal@logic.net>
- updated for mm 1.0.12

* Tue Sep 7 1999 Nicolai Schleifer <ns@dom.de>
- using buildroot feature
- using -f feature of the files macro
- started from scratch
