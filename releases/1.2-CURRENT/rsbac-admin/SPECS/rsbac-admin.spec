#
# spec file for package rsbac-admin
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rsbac-admin
%define version		1.2.5
%define release		%_revrel

%define libname_orig	librsbac
%define lib_major	1
%define libname		%mklibname rsbac %{lib_major}

%define build_with_kernel_dir	0
%{expand: %{?kernel_dir:	%%global build_with_kernel_dir 1}}

%if !%{build_with_kernel_dir}
%define kernel_dir	/usr/src/linux
%endif

Summary: 	A set of RSBAC utilities
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
License: 	GPL
Group: 		System/Configuration/Other
URL: 		http://www.rsbac.org/
Source0: 	http://www.rsbac.org/download/code/%{version}/%{name}-%{version}.tar.bz2
Source1:	rsbac.conf
Patch0:		rsbac-admin-1.2.5-soname.patch
Patch1:		rsbac-admin-1.2.5-libdir.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires: 	kernel-source

Requires: 	dialog

%description
RSBAC administration is done via command line tools or dialog menus.
Please see the online documentation at http://www.rsbac.org/instadm.htm
or the %{name}-doc package.


%package doc
Summary:	RSBAC administration documentation
Group:		System/Configuration/Other

%description -n %{name}-doc
RSBAC administration documentation.


%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{libname_orig} = %{version}-%{release}

%description -n %{libname}
This package contains the library needed to run programs dynamically
linked with %{name}.


%package -n %{libname}-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	kernel-source
Requires:	%{libname} = %{version}
Provides:	%{libname_orig}-devel = %{version}-%{release}

%description -n %{libname}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.


%package -n %{libname}-static-devel
Summary:	Static library for developing programs that will use %{name}
Group:		Development/C
Requires:	%{libname}-devel = %{version} 
Provides:	%{libname_orig}-static-devel = %{version}-%{release}

%description -n %{libname}-static-devel
This package contains the static library that programmers will need to develop
applications which will use %{name}.


%package -n pam_rsbac
Summary:	PAM files for RSBAC
Group:		System/Libraries
Requires:	%{name}-%{version}, %{libname}-%{version}

%description -n pam_rsbac
PAM files for use with RSBAC


%package -n nss_rsbac
Summary:	NSS files for RSBAC
Group:		System/Libraries
Requires:	%{name}-%{version}, %{libname}-%{version}

%description -n nss_rsbac
NSS library files for use with RSBAC


%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build
# this is an x86_64 executable which screws up the requires on 32bit
rm -f main/tools/examples/reg/reg_syscall
find . -name Makefile -exec perl -pi -e 's|/usr/local|%{_prefix}|g' {} \;
make build LIBDIR=%{_lib}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
find main/tools/src/scripts -type f -print | xargs chmod a+x 

%makeinstall DESTDIR=%{buildroot} LIBDIR=%{_lib}

mkdir -p %{buildroot}%{_sysconfdir}
install -m 0600 %{SOURCE1} %{buildroot}%{_sysconfdir}/rsbac.conf

# remove the locale files as %%find_lang doesn't seem to pick them up
rm -rf %{buildroot}%{_datadir}/locale

# fixpup
pushd %{buildroot}/%{_libdir}
    ln -s %{libname_orig}.so.%{version} %{libname_orig}.so.%{lib_major} 
popd

# remove _de pam files
rm -f %{buildroot}/%{_lib}/security/*_de*

# Documentation
mkdir -p %{buildroot}/%{_docdir}/%{name}-doc-%{version}
cp -r %{kernel_dir}/Documentation/rsbac/* %{buildroot}%{_docdir}/%{name}-doc-%{version}
rm -rf %{buildroot}%{_prefix}/doc/rsbac-tools*

# /var/lib/rsbac is in setup
mkdir -p %{buildroot}/var/lib/rsbac/tmp

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n nss_rsbac -p /sbin/ldconfig
%postun -n nss_rsbac -p /sbin/ldconfig


%files
%defattr(-,root,root,0755)
%doc README main/tools/examples main/tools/Changes
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/rsbac.conf
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man*/*
%attr(0700,rsbadmin,rsbadmin) %dir /var/lib/rsbac/tmp

%files -n %{name}-doc
%defattr(-,root,root)
%{_docdir}/%{name}-doc-%{version}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/%{libname_orig}.so*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libnss_rsbac.la
%{_includedir}/rsbac

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/%{libname_orig}*.a
%{_libdir}/libnss_rsbac.a

%files -n pam_rsbac
%defattr(-,root,root)
/%{_lib}/security/*so

%files -n nss_rsbac
%defattr(-,root,root)
%{_libdir}/libnss_rsbac*so*


%changelog
* Fri Feb 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.5
- 1.2.5
- some spec changes to accomodate the new way rsbac is built
- rediff P0
- include a pam_rsbac and nss_rsbac package
- drop the locales files
- drop main/tools/examples/reg/reg_syscall as it's an x86_64 executable
  that introduces some bogus 64bit deps on a 32bit package
- P1 for lib64 fixes
- include our own rsbac.conf (S1)
- include /var/lib/rsbac/tmp for temp file usage in the rsbac_menu program
  (mode 0700, owned rsbadmin:rsbadmin)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4-2avx
- bootstrap build (new gcc, new glibc)

* Wed Mar 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.4-1avx
- 1.2.4
- spec cleanups
- include default rsbac.conf file

* Mon Jan 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.2.3-2avx
- apply bugfix #5 (Admin tools/PAX: attr_set_fd does not accept PaX characters)

* Tue Jul 20 2004 Thomas Backlund <tmb@annvix.org> 1.2.3-1avx
- Inital release for Annvix

* Mon Jul 19 2004 Nicolas Planel <nplanel@mandrakesoft.com> 1.2.3-1mdk
- Inital release for Mandrakelinux distribution.

