#
# spec file for package liblzo
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		liblzo
%define	version		2.02
%define release 	%_revrel

%define major		2_2
%define libname		%mklibname lzo %{major}

Summary:	Data compression library with very fast (de-)compression
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://www.oberhumer.com/opensource/lzo/
Source0:	http://www.oberhumer.com/opensource/lzo/download/lzo-%{version}.tar.gz

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libtool

%description
LZO is a portable lossless data compression library written in ANSI C. 
It offers pretty fast compression and *very* fast decompression. 
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while 
still decompressing at this very high speed.


%package -n %{libname}
Summary:	Data compression library with very fast (de-)compression
Group:		System/Libraries
Provides:       %{name} = %{version}

%description -n %{libname}
LZO is a portable lossless data compression library written in ANSI C. 
It offers pretty fast compression and *very* fast decompression. 
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while 
still decompressing at this very high speed.


%package -n %{libname}-devel
Summary:	Development tools for programs which will use the lzo library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	liblzo2-devel = %{version}
Provides:	%{name}-devel = %{version}

%description -n %{libname}-devel
LZO is a portable lossless data compression library written in ANSI C. 
It offers pretty fast compression and *very* fast decompression. 
Decompression requires no memory. In addition there are slower
compression levels achieving a quite competitive compression ratio while 
still decompressing at this very high speed.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n lzo-%{version}


%build
%configure2_5x \
    --enable-shared

%make


%check
make check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/*a

%files doc
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README THANKS
%doc doc/*


%changelog
* Mon May 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.02
- first Annvix build (for openvpn)

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
