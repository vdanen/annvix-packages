%define name	rsbac-admin
%define version	1.2.4
%define release	1avx

%define lib_name_orig	librsbac
%define lib_major	1
%define lib_name	%mklibname rsbac %{lib_major}

%define build_with_kernel_dir	0
%{expand: %{?kernel_dir:		%%global build_with_kernel_dir 1}}

%if !%{build_with_kernel_dir}
%define kernel_dir /usr/src/linux
%endif

Summary: 	A set of RSBAC utilities
Name: 		%{name}
Version:	%{version}
Release: 	%{release}
License: 	GPL
Group: 		System/Configuration/Other
URL: 		http://www.rsbac.org/
Source: 	http://www.rsbac.org/download/code/v%{version}/%{name}-v%{version}.tar.bz2
Patch0:		rsbac-admin-v1.2.3-librsbac-soname-major1.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires: 	kernel-source

Requires: 	dialog

%description
RSBAC administration is done via command line tools or dialog menus.
Please see the online documentation at http://www.rsbac.org/instadm.htm
or the %{name}-doc package.

%package -n %{name}-doc
Summary:	RSBAC administration documentation
Group:		System/Configuration/Other

%description -n %{name}-doc
RSBAC administration documentation.

%package -n %{lib_name}
Summary:	Main library for %{name}
Group:		System/Libraries
Provides:	%{lib_name_orig} = %{version}-%{release}

%description -n %{lib_name}
This package contains the library needed to run programs dynamically
linked with %{name}.

%package -n %{lib_name}-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/C
Requires:	kernel-source
Requires:	%{lib_name} = %{version}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}

%description -n %{lib_name}-devel
This package contains the headers that programmers will need to develop
applications which will use %{name}.

%package -n %{lib_name}-static-devel
Summary:	Static library for developing programs that will use %{name}
Group:		Development/C
Requires:	%{lib_name}-devel = %{version} 
Provides:	%{lib_name_orig}-static-devel = %{version}-%{release}

%description -n %{lib_name}-static-devel
This package contains the static library that programmers will need to develop
applications which will use %{name}.

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1 -b .soname

aclocal
automake
%configure --with-kerneldir=%{kernel_dir}

%build
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
find examples -type f | xargs chmod a-x
find src/scripts -type f | xargs chmod a+x 

%makeinstall

mkdir -p %{buildroot}%{_sysconfdir}
install -m 0600 debian/rsbac.conf %{buildroot}%{_sysconfdir}/rsbac.conf

%find_lang %{name}

# fixpup
pushd %{buildroot}/%{_libdir}
ln -s %{lib_name_orig}.so.%{version} %{lib_name_orig}.so.%{lib_major} 
popd

# Documentation
mkdir -p %{buildroot}/%{_docdir}/%{name}-doc-%{version}
cp -r %{kernel_dir}/Documentation/rsbac/* %{buildroot}%{_docdir}/%{name}-doc-%{version}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files -f %name.lang
%defattr(-,root,root,0755)
%doc README Changes examples/*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/rsbac.conf
%{_bindir}/*
%{_mandir}/man*/*

%files -n %{name}-doc
%defattr(-,root,root)
%{_docdir}/%{name}-doc-%{version}

%files -n %{lib_name}
%defattr(-,root,root)
%doc README Changes
%{_libdir}/%{lib_name_orig}.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%{_libdir}/%{lib_name_orig}.so

%files -n %{lib_name}-static-devel
%defattr(-,root,root)
%{_libdir}/%{lib_name_orig}*.a

%changelog
* Wed Mar 09 2005 Vincent Danen <vdanen@annvix.org> 1.2.4-1avx
- 1.2.4
- spec cleanups
- include default rsbac.conf file

* Mon Jan 17 2005 Vincent Danen <vdanen@annvix.org> 1.2.3-2avx
- apply bugfix #5 (Admin tools/PAX: attr_set_fd does not accept PaX characters)

* Tue Jul 20 2004 Thomas Backlund <tmb@annvix.org> 1.2.3-1avx
- Inital release for Annvix

* Mon Jul 19 2004 Nicolas Planel <nplanel@mandrakesoft.com> 1.2.3-1mdk
- Inital release for Mandrakelinux distribution.

