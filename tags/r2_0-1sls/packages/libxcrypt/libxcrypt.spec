%define name	libxcrypt
%define version	2.0
%define release	1sls

# neededforbuild  
# usedforbuild    aaa_base acl attr bash bind-utils bison bzip2 coreutils cpio cpp cvs cyrus-sasl db devs diffutils e2fsprogs file filesystem fillup findutils flex gawk gdbm-devel glibc glibc-devel glibc-locale gpm grep groff gzip info insserv kbd less libacl libattr libgcc libstdc++ libxcrypt m4 make man mktemp modutils ncurses ncurses-devel net-tools netcfg openldap2-client openssl pam pam-devel pam-modules patch permissions popt ps rcs readline sed sendmail shadow strace syslogd sysvinit tar texinfo timezone unzip util-linux vim zlib zlib-devel autoconf automake binutils cracklib gcc gdbm gettext libtool perl rpm

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
rm -rf %{buildroot}
%makeinstall
# i don't think this is the right way to do this..
pushd %{buildroot}%{_libdir}
mv libxcrypt.1.2.0 libxcrypt.so.1.2.0
rm -f libxcrypt libxcrypt.1
ln -s libxcrypt.so.1.2.0 libxcrypt.so.1
ln -s libxcrypt.so.1.2.0 libxcrypt.so
popd

mkdir -p %{buildroot}/%{_lib}
mv -v %{buildroot}%{_libdir}/libxcrypt.so.* %{buildroot}/%{_lib}
ln -sf ../../%{_lib}/libxcrypt.so.1 %{buildroot}%{_libdir}/libxcrypt.so

%clean
rm -rf %{buildroot}

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

%changelog
* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 2.0-1sls
- first OpenSLS package
- based on SUSE's 2.0-32 package
