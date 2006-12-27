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
%define version		1.2.7
%define release		%_revrel

%define libname_orig	librsbac
%define lib_major	1
%define libname		%mklibname rsbac %{lib_major}

Summary: 	A set of RSBAC utilities
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
License: 	GPL
Group: 		System/Configuration
URL: 		http://www.rsbac.org/
Source0: 	http://www.rsbac.org/download/code/%{version}/%{name}-%{version}.tar.bz2
Source1:	rsbac.conf
Patch0:		rsbac-admin-1.2.7-libdir.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	pam-devel

Requires: 	dialog

%description
RSBAC administration is done via command line tools or dialog menus.
Please see the online documentation at http://www.rsbac.org/instadm.htm
or the %{name}-doc package.


%package doc
Summary:	RSBAC administration documentation
Group:		System/Configuration

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
Requires:	%{name}-%{version}
Requires:	%{libname}-%{version}

%description -n pam_rsbac
PAM files for use with RSBAC


%package -n nss_rsbac
Summary:	NSS files for RSBAC
Group:		System/Libraries
Requires:	%{name}-%{version}
Requires:	%{libname}-%{version}

%description -n nss_rsbac
NSS library files for use with RSBAC


%prep
%setup -q
%patch0 -p1 -b .lib64


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

# remove _de pam files
rm -f %{buildroot}/%{_lib}/security/*_de*

# Documentation
mv %{buildroot}%{_docdir}/rsbac-tools-%{version}/ docs
find docs/examples -type f | xargs chmod a-x
rm -f docs/examples/reg/reg_syscall

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
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/rsbac.conf
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man*/*
%attr(0700,rsbadmin,rsbadmin) %dir /var/lib/rsbac/tmp

%files -n %{name}-doc
%defattr(-,root,root)
%doc README main/tools/examples main/tools/Changes docs

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/%{libname_orig}.so*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/libnss_rsbac.la
%{_libdir}/%{libname_orig}.so
%{_libdir}/%{libname_orig}.la
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
* Fri Dec 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- rebuild against new ncurses

* Sat Jun 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- rebuild against new pam

* Sat Jun 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- P0: lib64 fixes (again)

* Thu Jun 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.7
- 1.2.7
- move all docs to -doc
- buildrequires: libtool, ncurses-devel, pam-devel
- drop P0 and P1, no longer required
- add -doc subpackage
- rebuild with gcc4

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.2.5
- fix group

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
