%define	name	matrixssl
%define	version	1.2.2
%define	release	1avx

%define	major	1
%define libname	%mklibname %{name} %{major}

Summary:	MatrixSSL is an embedded SSL implementation
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://www.matrixssl.org/
Source0:	%{name}-1-2-2.tar.gz
Patch0:		matrixssl-1.2-shared_and_static.diff.bz2
Patch1:		matrixssl-1.2-debian.diff.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	dietlibc-devel >= 0.20

%description
PeerSec MatrixSSL is an embedded SSL implementation designed for 
small footprint devices and applications requiring low overhead per 
connection. The library is less than 50K on disk with cipher suites.

It includes SSL client and SSL server support, session resumption, 
and implementations of RSA, 3DES, ARC4, SHA1, and MD5. The source is
well documented and contains portability layers for additional 
operating systems, cipher suites, and cryptography providers. 


%package -n %{libname}
Summary:	MatrixSSL is an embedded SSL implementation
Group:          System/Libraries

%description -n	%{libname}
PeerSec MatrixSSL is an embedded SSL implementation designed for 
small footprint devices and applications requiring low overhead per 
connection. The library is less than 50K on disk with cipher suites.

It includes SSL client and SSL server support, session resumption, 
and implementations of RSA, 3DES, ARC4, SHA1, and MD5. The source is
well documented and contains portability layers for additional 
operating systems, cipher suites, and cryptography providers. 

%package -n %{libname}-devel
Summary:	Static library and header files for the %{name} library
Group:		Development/C
Obsoletes:	%{name}-devel lib%{name}-devel
Provides:	%{name}-devel lib%{name}-devel
Requires:	%{libname} = %{version}-%{release}
Requires:	dietlibc-devel >= 0.20

%description -n	%{libname}-devel
PeerSec MatrixSSL is an embedded SSL implementation designed for 
small footprint devices and applications requiring low overhead per 
connection. The library is less than 50K on disk with cipher suites.

It includes SSL client and SSL server support, session resumption, 
and implementations of RSA, 3DES, ARC4, SHA1, and MD5. The source is
well documented and contains portability layers for additional 
operating systems, cipher suites, and cryptography providers. 

This package contains the static libraries and headers for both
glibc and dietlibc.

%prep

%setup -q -n %{name}
%patch0 -p1 

# prepare for dietlibc
mkdir -p dietlibc
cp -rp src dietlibc/
cp matrixSsl.h dietlibc/
cd dietlibc
%patch1 -p0
cd -

%build

# first make the standard glibc stuff...
make -C src DFLAGS="%{optflags} -fPIC"

# now make the dietlibc static library
make -C dietlibc/src CC="diet -Os gcc" \
    LDFLAGS="-nostdlib" \
    static

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_includedir}
install -d %{buildroot}%{_libdir}/dietlibc/{lib,include}

# install the glibc version
install -m0755 src/lib%{name}.so %{buildroot}%{_libdir}/lib%{name}.so.%{version}
ln -snf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{major}
ln -snf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so
install -m0644 src/lib%{name}.a %{buildroot}%{_libdir}/
install -m0644 matrixSsl.h %{buildroot}%{_includedir}/

# install the dietlibc version
install -m0644 dietlibc/src/lib%{name}.a %{buildroot}%{_libdir}/dietlibc/lib/
install -m0644 dietlibc/matrixSsl.h %{buildroot}%{_libdir}/dietlibc/include/

# cleanup the examples directory
rm -f examples/*.sln
rm -f examples/*.vcproj
rm -f examples/*.pem
rm -f examples/*.p12

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc doc/MatrixSSLApi.pdf
%doc doc/MatrixSSLDeveloperGuide.pdf
%doc doc/MatrixSSLKeyGeneration.pdf
%doc doc/MatrixSSLPortingGuide.pdf
%doc doc/MatrixSSLReadme.pdf
%doc doc/MatrixSSLSocketApi.pdf
%doc examples
%{_includedir}/*
%{_libdir}/dietlibc/include/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/dietlibc/lib/*.a

%changelog
* Wed Oct 13 2004 Vincent Danen <vdanen@annvix.org> 1.2.2-1avx
- 1.2.2

* Sat Sep 11 2004 Vincent Danen <vdanen@annvix.org> 1.2-1avx
- Annvix build; needed for ipsvd

* Wed Aug 04 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 1.2-1mdk
- initial mandrake package
