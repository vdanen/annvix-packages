%define name	elfutils
%define version	0.84
%define release	3sls

%define major	1
%define libname	%mklibname %{name} %{major}

%define _gnu	%{nil}
%define _programprefix eu-

%define build_check		1
%{expand: %{?_without_CHECK:	%%define build_check 0}}
%{expand: %{?_with_CHECK:	%%define build_check 1}}

Summary:	A collection of utilities and DSOs to handle compiled objects.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
Source:		elfutils-%{version}.tar.bz2
Requires:	%{libname} = %{version}-%{release}

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	gcc >= 3.2, sharutils, libtool-devel

Requires:	%{libname} = %{version}-%{release}

%description
Elfutils is a collection of utilities, including:

   * %{_programprefix}nm: for listing symbols from object files
   * %{_programprefix}size: for listing the section sizes of an object or archive file
   * %{_programprefix}strip: for discarding symbols
   * %{_programprefix}readelf: the see the raw ELF file structures
   * %{_programprefix}elflint: to check for well-formed ELF files

%package -n %{libname}-devel
Summary:	Development libraries to handle compiled objects.
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel, lib%{name}-devel
Obsoletes:	libelf-devel, libelf0-devel
Provides:	libelf-devel, libelf0-devel

%description -n %{libname}-devel
This package contains the headers and dynamic libraries to create
applications for handling compiled objects.

   * libelf allows you to access the internals of the ELF object file
     format, so you can see the different sections of an ELF file.
   * libebl provides some higher-level ELF access functionality.
   * libdwarf provides access to the DWARF debugging information.
   * libasm provides a programmable assembler interface.

%package -n %{libname}-static-devel
Summary:	Static libraries for development with libelfutils.
Group:		Development/Other
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	%{name}-static-devel, lib%{name}-static-devel
Obsoletes:	libelf-static-devel, libelf0-static-devel
Provides:	libelf-static-devel, libelf0-static-devel

%description -n %{libname}-static-devel
This package contains the static libraries to create applications for
handling compiled objects.

%package -n %{libname}
Summary:	Libraries to read and write ELF files.
Group:		System/Libraries
Provides:	lib%{name}
Obsoletes:	libelf, libelf0
Provides:	libelf, libelf0

%description -n %{libname}
This package provides DSOs which allow reading and writing ELF files
on a high level.  Third party programs depend on this package to read
internals of ELF files.  The programs of the elfutils package use it
also to generate new ELF files.

Also included are numerous helper libraries which implement DWARF,
ELF, and machine-specific ELF handling.

%prep
%setup -q

%build
mkdir build-%{_target_platform}
pushd build-%{_target_platform}
../configure \
  --prefix=%{_prefix} --exec-prefix=%{_exec_prefix} \
  --bindir=%{_bindir} --sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} \
  --datadir=%{_datadir} --includedir=%{_includedir} --libdir=%{_libdir} \
  --libexecdir=%{_libexecdir} --localstatedir=%{_localstatedir} \
  --sharedstatedir=%{_sharedstatedir} --mandir=%{_mandir} \
  --infodir=%{_infodir} --program-prefix=%{_programprefix} --enable-shared
%make
%if %{build_check}
%make check
%endif
popd

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_prefix}

%makeinstall -C build-%{_target_platform}

chmod +x $RPM_BUILD_ROOT%{_libdir}/lib*.so*
chmod +x $RPM_BUILD_ROOT%{_libdir}/elfutils/lib*.so*

# XXX Nuke unpackaged files
{ cd $RPM_BUILD_ROOT
  rm -f .%{_bindir}/eu-ld
  rm -f .%{_includedir}/elfutils/libasm.h
  rm -f .%{_includedir}/elfutils/libdw.h
  rm -f .%{_includedir}/elfutils/libdwarf.h
  rm -f .%{_libdir}/libasm-%{version}.so
  rm -f .%{_libdir}/libasm.a
  rm -f .%{_libdir}/libasm.so
  rm -f .%{_libdir}/libdw-%{version}.so
  rm -f .%{_libdir}/libdw.a
  rm -f .%{_libdir}/libdw.so
  rm -f .%{_libdir}/libdwarf.a
  rm -f .%{_libdir}/libdwarf.so
}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README TODO libdwarf/AVAILABLE
%{_bindir}/eu-elflint
#%{_bindir}/eu-ld
%{_bindir}/eu-nm
%{_bindir}/eu-readelf
%{_bindir}/eu-size
%{_bindir}/eu-strip
%dir %{_libdir}/elfutils
%{_libdir}/elfutils/lib*.so

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/dwarf.h
%{_includedir}/libelf.h
%{_includedir}/gelf.h
%{_includedir}/nlist.h
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/elf-knowledge.h
%{_includedir}/elfutils/libebl.h
#%{_libdir}/libasm.so
#%{_libdir}/libdwarf.so
%{_libdir}/libebl.so
%{_libdir}/libelf.so
#%{_libdir}/libdw.so

%files -n %{libname}-static-devel
%defattr(-,root,root)
#%{_libdir}/libasm.a
%{_libdir}/libebl.a
%{_libdir}/libelf.a
#%{_libdir}/libdw.a

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libelf-%{version}.so
%{_libdir}/libelf*.so.*
#%{_libdir}/libasm-%{version}.so
#%{_libdir}/libasm*.so.*
%{_libdir}/libebl-%{version}.so
%{_libdir}/libebl*.so.*
#%{_libdir}/libdw-%{version}.so
#%{_libdir}/libdw*.so.*
%{_libdir}/libdwarf-%{version}.so
%{_libdir}/libdwarf*.so.*

%changelog
* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 0.84-3sls
- minor spec cleanups
- remove some more unpackaged files

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 0.84-2sls
- OpenSLS build
- tidy spec

* Fri Jul 25 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.84-1mdk
- 0.84

* Wed Jul 16 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.83-1mdk
- 0.83

* Tue Jul  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.80-1mdk
- 0.80

* Tue Jul 08 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.79-2mdk
- rebuild for new provides

* Tue Jun  3 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.79-1mdk
- 0.79
- -static-devel'ize

* Thu Apr  3 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.76-1mdk
- 0.76

* Fri Dec 20 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.72-3mdk
- First Mandrake Linux release adapted from Red Hat package
- BuildRequires: libtool-devel

* Thu Dec 12 2002 Jakub Jelinek <jakub@redhat.com> 0.72-2
- update to 0.72

* Wed Dec 11 2002 Jakub Jelinek <jakub@redhat.com> 0.71-2
- update to 0.71

* Wed Dec 11 2002 Jeff Johnson <jbj@redhat.com> 0.69-4
- update to 0.69.
- add "make check" and segfault avoidance patch.
- elfutils-libelf needs to run ldconfig.

* Tue Dec 10 2002 Jeff Johnson <jbj@redhat.com> 0.68-2
- update to 0.68.

* Fri Dec  6 2002 Jeff Johnson <jbj@redhat.com> 0.67-2
- update to 0.67.

* Tue Dec  3 2002 Jeff Johnson <jbj@redhat.com> 0.65-2
- update to 0.65.

* Mon Dec  2 2002 Jeff Johnson <jbj@redhat.com> 0.64-2
- update to 0.64.

* Sun Dec 1 2002 Ulrich Drepper <drepper@redhat.com> 0.64
- split packages further into elfutils-libelf

* Sat Nov 30 2002 Jeff Johnson <jbj@redhat.com> 0.63-2
- update to 0.63.

* Fri Nov 29 2002 Ulrich Drepper <drepper@redhat.com> 0.62
- Adjust for dropping libtool

* Sun Nov 24 2002 Jeff Johnson <jbj@redhat.com> 0.59-2
- update to 0.59

* Thu Nov 14 2002 Jeff Johnson <jbj@redhat.com> 0.56-2
- update to 0.56

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> 0.54-2
- update to 0.54

* Sun Oct 27 2002 Jeff Johnson <jbj@redhat.com> 0.53-2
- update to 0.53
- drop x86_64 hack, ICE fixed in gcc-3.2-11.

* Sat Oct 26 2002 Jeff Johnson <jbj@redhat.com> 0.52-3
- get beehive to punch a rhpkg generated package.

* Wed Oct 23 2002 Jeff Johnson <jbj@redhat.com> 0.52-2
- build in 8.0.1.
- x86_64: avoid gcc-3.2 ICE on x86_64 for now.

* Tue Oct 22 2002 Ulrich Drepper <drepper@redhat.com> 0.52
- Add libelf-devel to conflicts for elfutils-devel

* Mon Oct 21 2002 Ulrich Drepper <drepper@redhat.com> 0.50
- Split into runtime and devel package

* Fri Oct 18 2002 Ulrich Drepper <drepper@redhat.com> 0.49
- integrate into official sources

* Wed Oct 16 2002 Jeff Johnson <jbj@redhat.com> 0.46-1
- Swaddle.
