%define name	libpcap
%define version	0.7.2
%define release	3sls

%define	major	0
%define minor	7
%define finalname %{name}%{major}

Summary:        A system-independent interface for user-level packet capture
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Libraries
URL:		http://www.tcpdump.org
Source:		http://www.tcpdump.org/release/libpcap-%{version}.tar.gz

BuildRoot:	%_tmppath/%name-%version-%release-root
BuildRequires:	byacc flex

Obsoletes:	libpcap
Provides:	libpcap
Provides:	libpcap = %{version}

%description
Libpcap provides a portable framework for low-level network monitoring.
Libpcap can provide network statistics collection, security monitoring
and network debugging.  Since almost every system vendor provides a
different interface for packet capture, the libpcap authors created this
system-independent API to ease in porting and to alleviate the need for
several system-dependent packet capture modules in each application.

%package -n %{finalname}
Summary:	A system-independent interface for user-level packet capture
Group:          System/Libraries
Obsoletes:      libpcap
Provides:       libpcap
Provides:	libpcap = %{version}

%description -n %{finalname}
Libpcap provides a portable framework for low-level network monitoring.
Libpcap can provide network statistics collection, security monitoring
and network debugging.  Since almost every system vendor provides a
different interface for packet capture, the libpcap authors created this
system-independent API to ease in porting and to alleviate the need for
several system-dependent packet capture modules in each application.


%package -n %{finalname}-devel
Summary:	Static library and header files for the pcap library
Group:		Development/C
License: 	BSD
Obsoletes:	libpcap-devel
Provides:	libpcap-devel
Provides:	libpcap-devel = %{version}
Requires:	%{finalname} = %version-%release
BuildRequires:	autoconf

%description -n %{finalname}-devel
Libpcap provides a portable framework for low-level network monitoring.
Libpcap can provide network statistics collection, security monitoring
and network debugging.  Since almost every system vendor provides a
different interface for packet capture, the libpcap authors created this
system-independent API to ease in porting and to alleviate the need for
several system-dependent packet capture modules in each application.

This package contains the static pcap library and its header files needed to
compile applications such as tcpdump, etc.

%prep
%setup -q  -n libpcap-%{version}

autoheader
aclocal
autoconf

%build
%configure --enable-ipv6

%make "CCOPT=$RPM_OPT_FLAGS -fPIC"

#
# (fg) FIXME - UGLY - HACK - but libpcap's Makefile doesn't allow to build a
# shared lib...
#

gcc -Wl,-soname,libpcap.so.0 -shared -fpic -o libpcap.so.%{major}.%{minor} *.o

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

mkdir -p $RPM_BUILD_ROOT/{%{_includedir}/net,%{_libdir},%{_mandir}/man3}

%__make DESTDIR=$RPM_BUILD_ROOT install

install -m755 libpcap.so.%{major}.%{minor} $RPM_BUILD_ROOT/%{_libdir}

pushd $RPM_BUILD_ROOT/%{_libdir} && {
	ln -s libpcap.so.%{major}.%{minor} libpcap.so.0
	ln -s libpcap.so.%{major}.%{minor} libpcap.so
} && popd

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post -n %{finalname} -p /sbin/ldconfig

%postun -n %{finalname} -p /sbin/ldconfig

%post -n %{finalname}-devel -p /sbin/ldconfig

%postun -n %{finalname}-devel -p /sbin/ldconfig

%files -n %{finalname}
%defattr(-,root,root)
%doc README* CHANGES CREDITS FILES INSTALL.txt
%doc LICENSE VERSION
%{_libdir}/libpcap.so.*

%files -n %{finalname}-devel
%defattr(-,root,root)
%doc TODO
%{_includedir}/*
%{_libdir}/libpcap.so
%{_libdir}/libpcap.a
%{_mandir}/man3/pcap.3*

%changelog
* Tue Dec 09 2003 Vincent Danen <vdanen@opensls.org> 0.7.2-3sls
- OpenSLS build
- tidy spec

* Thu Jul 31 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.7.2-2mdk
- rebuild

* Fri Feb 28 2003 Vincent Danen <vdanen@mandrakesoft.com> 0.7.2-1mdk
- 0.7.2
- remove P0 (included upstream)

* Sun Feb 09 2003 Stefan van der Eijk <stefan@eijk.nu> 0.7.1-4mdk
- add patch for wireless sniffing (Airsnort & co)
- fix %%doc

* Thu Nov 14 2002 Warly <warly@mandrakesoft.com> 0.7.1-3mdk
- use gz for sources to be able to check md5

* Tue Sep  3 2002 Warly <warly@mandrakesoft.com> 0.7.1-2mdk
- remove obsolete P0 (Oden Eriksson)
- misc spec file fixes (Oden Eriksson)

* Sat Aug 10 2002 Warly <warly@mandrakesoft.com> 0.7.1-1mdk
- new version

* Mon Nov 19 2001 Philippe Libat <philippe@mandrakesoft.com> 0.6.2-3mdk
- fix libpcap link version 0.6 and requires

* Fri Oct 12 2001 Stefan van der Eijk <stefan@eijk.nu> 0.6.2-2mdk
- BuildRequires: byacc flex
- Copyright --> License

* Tue May  8 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 0.6.2-1mdk
- version 0.6.2

* Mon Mar 12 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.6.1-5mdk
- BuildRequires: autoconf

* Tue Feb 27 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.6.1-4mdk
- Add more docs
- Build with fPIC for shared libraries.

* Sat Jan 13 2001 David BAUDENS <baudens@mandrakesoft.com> 0.6.1-3mdk
- Really fix libdification (thanks to Stefan van der Eijk)

* Fri Jan 12 2001 David BAUDENS <baudens@mandrakesoft.com> 0.6.1-2mdk
- Fix libdification
- Provides: libpcap
- Fix Requires section
- Fix name of SRPM

* Tue Jan 09 2001 Geoff <snailtalk@mandrakesoft.com> 0.6.1-1mdk
- new and shiny source.
- add a url for the source.

* Thu Jan 04 2001 Francis Galiegue <fg@mandrakesoft.com> 0.5.2-2mdk
- New lib policy:
  * s,libpcap,&0,
  * fixed requires
  * Obsoletes: libpcap and -devel
  * Serial not needed anymore

* Wed Nov  8 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 0.5.2-1mdk
- Update to release version 0.5.2.

* Fri Jul 21 2000 Francis Galiegue <fg@mandrakesoft.com> 0.5-2mdk
- s,tmpdir,tmppath,
- removed unnecessary version and release in -devel

* Thu Jul 20 2000 Francis Galiegue <fg@mandrakesoft.com> 0.5-1mdk
- 0.5 stable
- Split from tcpdump source to is own source
- %files list cleanup
- Added dynamic lib - dirty hack
- split libpcap and -devel
