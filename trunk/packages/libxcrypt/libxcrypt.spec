%define name	libxcrypt
%define version	2.0
%define release	2sls

Summary:	Crypt library for DES, MD5, and blowfish
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
Source:		libxcrypt-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
Libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, and passwords with blowfish
encryption.

%package devel
Summary:	Development files for Crypt library
Group:		Development/Libraries/C and C++
Requires:	libxcrypt = %{version}

%description devel
libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports, beside DES crypt and MD5, passwords with blowfish
encryption.

This package contains the header files and static libraries, which are
necessary to develop your own software using libxcrypt.


%prep
%setup -q

%build
%configure2_5x
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
# i don't think this is the right way to do this..
pushd %{buildroot}%{_libdir}
mv libxcrypt.1.2.0 libxcrypt.so.1.2.0
ln -s libxcrypt.so.1.2.0 libxcrypt.so.1
ln -s libxcrypt.so.1.2.0 libxcrypt.so
popd

mkdir -p %{buildroot}/%{_lib}
mv -v %{buildroot}%{_libdir}/libxcrypt.so.* %{buildroot}/%{_lib}
ln -sf ../../%{_lib}/libxcrypt.so.1 %{buildroot}%{_libdir}/libxcrypt.so

# remove unpackaged files
rm -f %{buildroot}%{_libdir}/libxcrypt
rm -f %{buildroot}%{_libdir}/libxcrypt.1

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README NEWS README.ufc-crypt AUTHORS THANKS
/%{_lib}/libxcrypt.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libxcrypt.a
%{_libdir}/libxcrypt.la
%{_libdir}/libxcrypt.so
/%{_lib}/libxcrypt.1

%changelog
* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.0-2sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.0-1sls
- first OpenSLS package
- based on SUSE's 2.0-32 package
