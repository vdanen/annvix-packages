#
# spec file for package imap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		imap
%define version		2006j
%define release		%_revrel

%define major		0
%define libname		%mklibname c-client %{major}
%define devname		%mklibname c-client -d
%define soname		c-client-php

Summary:	An IMAP server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Apache License
Group:		System/Servers
URL:		http://www.washington.edu/imap/
Source0:	ftp://ftp.cac.washington.edu/mail/imap-%{version}2.tar.Z
Source1:	flock.c
Patch0: 	imap-2002e-ssl.patch
Patch1: 	imap-2006c1-linux.diff
Patch2:		imap-2001a-disable-mbox.patch
Patch3:		imap-2001a-redhat.patch
Patch4: 	imap-2006c1-flock.diff
Patch5:		imap-2006c1-glibc-2.2.2.diff
Patch6:		imap-2001a-overflow.patch
Patch7:		imap-2004a-shared.patch
Patch8:		imap-2002e-authmd5.patch
# (oe) the annotate patch is implemented upstream and needed by kolab2
Patch9:		imap-2006c1-annotate.diff
# (oe) http://www.gadgetwiz.com/software/hash_reset.html
Patch10:	imap-2004g-hash_reset.diff
Patch11:	imap-yes.diff

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	openssl-devel
BuildRequires:	pam-devel

%description
The imap package provides server daemons for both the IMAP (Internet
Message Access Protocol) and POP (Post Office Protocol) mail access
protocols.  The POP protocol uses a "post office" machine to collect mail
for users and allows users to download their mail to their local machine
for reading. The IMAP protocol provides the functionality of POP, but
allows a user to read mail on a remote machine without downloading it to
their local machine.


%package devel
Summary:	Libraries, includes, etc to develop IMAP applications
Group:		Development/C

%description devel
The imap-devel package contains the header files and static libraries for
developing programs which will use the IMAP (Internet Message Access
Protocol) library.


%package -n %{libname}
Summary:	C-client mail access routines for IMAP and POP protocols
Group:		System/Libraries
Provides:	c-client = %{version}-%{release}
Provides:	libc-client = %{version}-%{release}

%description -n	%{libname}
C-client is a common API for accessing mailboxes. It is used internally by
the popular PINE mail reader, the University of Washington's IMAP server
and PHP.

This package contains the shared c-client library.


%package -n %{devname}
Summary:	Development files for the c-client library
Group:		Development/C
Requires:	%{libname} = %{version}
Requires:	imap-devel = %{version}
Provides:	libc-client-php-devel = %{version}-%{release}
Provides:	libc-client-devel = %{version}-%{release}

%description -n	%{devname}
C-client is a common API for accessing mailboxes. It is used internally by
the popular PINE mail reader, the University of Washington's IMAP server
and PHP.

This package contains development files for the c-client library.

%prep
%setup -q -n %{name}-%{version}

rm -rf RCS

%patch0 -p0 -b .ssl
%patch1 -p0 -b .linux
%patch2 -p1 -b .mbox
%patch3 -p1 -b .redhat
%patch4 -p0 -b .flock
install -m 0644 %{_sourcedir}/flock.c  src/osdep/unix/flock.c
%patch5 -p1 -b .glibc
%patch6 -p1 -b .overflow
%patch7 -p1 -b .shared
%patch8 -p1 -b .authmd5
%patch9 -p1 -b .annotate
%patch10 -p1 -b .hash_reset
%patch11 -p0 -b .yes


%build
%serverbuild
EXTRACFLAGS="$EXTRACFLAGS -I%{_includedir}/openssl"
EXTRALDFLAGS="$EXTRALDFLAGS -L%{_libdir}"

touch ip6

%make RPM_OPT_FLAGS="%{optflags} -D_REENTRANT -DDIC -fPIC -fno-omit-frame-pointer" lnp \
	EXTRACFLAGS="$EXTRACFLAGS" \
	EXTRALDFLAGS="$EXTRALDFLAGS" \
	SSLDIR=%{_libdir}/ssl \
	SSLINCLUDE=%{_includedir}/openssl \
	SSLLIB=%{_libdir} \
	LOCKPGM=%{_sbindir}/mlock \
	SSLTYPE=unix.nopwd \
	BASECFLAGS="%{optflags} -D_REENTRANT -DDIC -fPIC -fno-omit-frame-pointer" \
	IP=6

mv -f c-client/c-client.a c-client-ssl.a
make clean

# build a useable c-client.a for PHP
EXTRACFLAGS="$EXTRACFLAGS -DDISABLE_POP_PROXY=1 -DIGNORE_LOCK_EACCES_ERRORS=1"
EXTRACFLAGS="$EXTRACFLAGS -I%{_includedir}/openssl"
EXTRALDFLAGS="$EXTRALDFLAGS -L%{_libdir}"
make RPM_OPT_FLAGS="%{optflags} -D_REENTRANT -DDIC -fPIC -fno-omit-frame-pointer" slx \
	EXTRACFLAGS="$EXTRACFLAGS" \
	EXTRALDFLAGS="$EXTRALDFLAGS" \
	SSLDIR=%{_libdir}/ssl \
	SSLINCLUDE=%{_includedir}/openssl \
	SSLLIB=%{_libdir} \
	LOCKPGM=%{_sbindir}/mlock \
	SSLTYPE=unix \
	SHLIBBASE=%{soname} \
	SHLIBNAME=lib%{soname}.so.%{major} \
	BASECFLAGS="%{optflags} -D_REENTRANT -DDIC -fPIC -fno-omit-frame-pointer" \
	IP=6

mv -f c-client/c-client.a %{soname}.a
mv -f c-client/lib%{soname}.so.%{major} .


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# all we care about are the libs and development files
mkdir -p %{buildroot}{%{_libdir},%{_includedir}/imap}

# install headers
install -m 0644 c-client/*.h %{buildroot}%{_includedir}/imap/
install -m 0644 src/osdep/tops-20/shortsym.h %{buildroot}%{_includedir}/imap/

# install static libraries
install -m 0644 c-client-ssl.a %{buildroot}%{_libdir}/libc-client.a
# rh - Added linkage.c to fix (#34658) <mharris>
install -m 0644 c-client/linkage.c %{buildroot}%{_includedir}/imap/

# install php stuff
install -m 0644 lib%{soname}.so.%{major} %{buildroot}%{_libdir}/
ln -snf lib%{soname}.so.%{major} %{buildroot}%{_libdir}/lib%{soname}.so
install -m 0644 %{soname}.a %{buildroot}%{_libdir}/lib%{soname}.a


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files devel
%defattr(-,root,root)
%doc docs/internal.txt
%{_libdir}/libc-client.a
%{_includedir}/imap

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib%{soname}.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_libdir}/lib%{soname}.a
%{_libdir}/lib%{soname}.so


%changelog
* Thu Sep 20 2007 Vincent Danen <vdanen-at-build.annvix.org> 2006j
- build an imap development package based on 2006j so that we can build
  php-imap from the main imap package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
