%define name	%mklibname net 1.0
%define version 1.0.2a
%define release 5avx

Summary:	A C library for portable packet creation
Name:		%{name}-devel
Version:	%{version}
Release:	%{release}
License:	BSD style
Group:		System/Libraries
URL:		http://www.packetfactory.net/libnet
Source:		http://www.packetfactory.net/libnet/dist/libnet-%{version}.tar.bz2
Patch0:		libnet-1.0.2a-strings.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildPreReq:	libpcap
BuildRequires:	libtool

Conflicts:	libnet, %{_lib}net1.1-devel
Provides:	net-devel = %version-%release

%description
Libnet is an API to help with the construction and handling of network
packets. It provides a portable framework for low-level network
packet writing and handling (use libnet in conjunction with libpcap and
you can write some really cool stuff).  Libnet includes packet creation
at the IP layer and at the link layer as well as a host of supplementary
and complementary functionalty. Libnet is avery handy with which to
write network tools and network test code.  See the manpage and sample
test code for more detailed information

%prep
%setup -n Libnet-%{version} -q
%patch0 -p1 -b .strings

%build

%configure --with-pf_packet=yes 

%make CFLAGS="%optflags"
%make test CFLAGS="%optflags"

# remove CVS files
find . -type 'd' -name "CVS" -print | xargs /bin/rm -rf

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/{bin,%_lib,include}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man3
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="/usr/bin/install" MAN_PREFIX=%_mandir/man3
rm -f $RPM_BUILD_ROOT/%{_libdir}/libpwrite

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr (0644,root,root,0755)
%doc doc/* example
%attr(0755,root,root) %{_bindir}/*
%{_mandir}/man3/*
%{_libdir}/*.a
%{_includedir}/libnet.h
%dir %{_includedir}/libnet
%{_includedir}/libnet/*

%changelog
* Wed Jun 23 2004 Vincent Danen <vdanen@annvix.org> 1.0.2a-5avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 1.0.2a-4sls
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 1.0.2a-3sls
- OpenSLS build
- tidy spec

* Wed Aug 20 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.0.2a-2mdk
- libified

* Tue Nov 13 2001 Florin <florin@mandrakesoft.com> 1.0.2a-1mdk
- 1.0.2a

* Mon Sep 24 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.0.2-7mdk
- fix permissions

* Sun Jul 29 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.0.2-6mdk
- rebuild

* Wed May 23 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.0.2-5mdk
- BuildRequires: libtool

* Sun Apr 08 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0.2-4mdk
- Rebuild and up to 4mdk to get back the libnet main binary package.

* Tue Feb 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0.2-2mdk
- fix the broken makefile which generated a broken rpm.
- no need to manually install libnet-config.

* Tue Feb 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0.2-1mdk
- new and shiny source.
- put a versioning on the source tarball.
- put a url in the source tag.
- quiet setup so we don't get a load of crap.
- removed libpwrite.a -> libnet.a symbolic linking.
- removed buildroot before doing an %%install.
- use the install command, not mv, when installing the manual page.
- manually install libnet-config into /usr/bin.

* Fri Nov 10 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.0.1b-4mdk
- more macros
- rebuild for gcc-2.96
- delete CVS files

* Thu Aug 24 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.0.1b-3mdk
- add macros
- BM

* Tue Apr 18 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.0.1b-2mdk
- v1.0.1b

* Tue Mar 23 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.0.1-1mdk
- v1.0.1

* Sat Nov 13 1999 Giuseppe Ghib� <ghibo@linux-mandrake.com>
- first SPEC file for Mandrake.
