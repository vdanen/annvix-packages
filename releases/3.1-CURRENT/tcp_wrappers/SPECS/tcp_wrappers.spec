#
# spec file for package tcp_wrappers
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		tcp_wrappers
%define version		7.6
%define release		%_revrel

%define major		0
%define minor		7
%define librel		6
%define libname		%mklibname wrap %{major}
%define devname		%mklibname wrap -d

Summary: 	A security tool which acts as a wrapper for TCP daemons
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Group: 		System/Servers	
License: 	BSD
URL:		http://ftp.porcupine.org/pub/security/
Source:	        http://ftp.porcupine.org/pub/security/%{name}_%{version}.tar.bz2
Patch0:		tcpw7.2-config.patch
Patch1:		tcpw7.2-setenv.patch
Patch2:		tcpw7.6-netgroup.patch
Patch3:		tcp_wrappers-7.6-bug11881.patch
Patch4:		tcp_wrappers-7.6-bug17795.patch
Patch5:		tcp_wrappers-7.6-bug17847.patch
Patch6:		tcp_wrappers-7.6-fixgethostbyname.patch
Patch7:		tcp_wrappers-7.6-docu.patch
Patch9:		tcp_wrappers.usagi-ipv6.patch
Patch10:	tcp_wrappers.ume-ipv6.patch
Patch11:	tcp_wrappers-7.6-shared.patch
Patch12:	tcp_wrappers-7.6-sig.patch
Patch13:	tcp_wrappers-7.6-strerror.patch
Patch14:	tcp_wrappers-7.6-ldflags.patch
Patch15:	tcp_wrappers-7.6-fdr-fix_sig-bug141110.patch
Patch16:	tcp_wrappers-7.6-fdr-162412.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildConflicts:	%{name}-devel


%description
The tcp_wrappers package provides small daemon programs which can
monitor and filter incoming requests for systat, finger, ftp, telnet,
rlogin, rsh, exec, tftp, talk and other network services.

Install the tcp_wrappers program if you need a security tool for
filtering incoming network services requests.


%package -n %{libname}
Summary:	A security library which acts as a wrapper for TCP daemons
Group:		System/Libraries
Provides:	libwrap = %{version}-%{release}

%description -n %{libname}
This package contains the shared tcp_wrappers library (libwrap).


%package -n %{devname}
Summary:	A security library which acts as a wrapper for TCP daemons
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	wrap-devel = %{version}-%{release}
Obsoletes:	%{name}-devel
Obsoletes:	%mklibname wrap 0 -d

%description -n %{devname}
This package contains the static tcp_wrappers library (libwrap) and
its header files.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}_%{version}
%patch0 -p1 -b .config
%patch1 -p1 -b .setenv
%patch2 -p1 -b .netgroup
%patch3 -p1 -b .bug11881
%patch4 -p1 -b .bug17795
%patch5 -p1 -b .bug17847
%patch6 -p1 -b .fixgethostbyname
%patch7 -p1 -b .docu
%patch9 -p0 -b .usagi-ipv6
%patch10 -p1 -b .ume-ipv6
%patch11 -p1 -b .shared
%patch12 -p1 -b .sig
%patch13 -p1 -b .strerror
%patch14 -p0 -b .ldflags
%patch15 -p1 -b .fix_sig
%patch16 -p1 -b .162412


%build
%make OPTFLAGS="%{optflags} -fPIC -DPIC -D_REENTRANT -DHAVE_STRERROR" \
    LDFLAGS="-pie" REAL_DAEMON_DIR=%{_sbindir} \
    MAJOR=%{major} MINOR=%{minor} REL=%{librel} linux


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_includedir},%{_libdir},%{_sbindir},%{_mandir}/{man3,man5,man8}}

install -m 0644 hosts_access.3 %{buildroot}%{_mandir}/man3
install -m 0644 hosts_access.5 hosts_options.5 %{buildroot}%{_mandir}/man5
pushd %{buildroot}%{_mandir}/man5
    ln hosts_access.5 hosts.allow.5
    ln hosts_access.5 hosts.deny.5
popd

install -m 0644 tcpd.8 tcpdchk.8 tcpdmatch.8 %{buildroot}%{_mandir}/man8

install -m 0755 libwrap.so.%{major}.%{minor}.%{librel} %{buildroot}%{_libdir}/
ln -s libwrap.so.%{major}.%{minor}.%{librel} %{buildroot}%{_libdir}/libwrap.so.%{major}
ln -s libwrap.so.%{major}.%{minor}.%{librel} %{buildroot}%{_libdir}/libwrap.so

install -m 0644 libwrap.a %{buildroot}%{_libdir}
install -m 0644 tcpd.h %{buildroot}%{_includedir}

install -m 0755 safe_finger %{buildroot}%{_sbindir}
install -m 0755 tcpd %{buildroot}%{_sbindir}
install -m 0755 tcpdchk %{buildroot}%{_sbindir}
install -m 0755 tcpdmatch %{buildroot}%{_sbindir}
install -m 0755 try-from %{buildroot}%{_sbindir}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root,755)
%{_sbindir}/*
%{_mandir}/man*/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{devname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

%files doc
%defattr(-,root,root,755)
%doc BLURB CHANGES README* DISCLAIMER Banners.Makefile


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 7.6
- provides wrap-devel

* Sat Sep 15 2007 Vincent Danen <vdanen-at-build.annvix.org> 7.6
- implement devel naming policy
- implement library provides policy
- don't call ldconfig on the devel packages

* Tue May 01 2007 Vincent Danen <vdanen-at-build.annvix.org> 7.6
- versioned provides

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.6
- libify the package and build the binaries against the shared libs
- updated P11, P14 from Mandriva
- P15: fixed sig patch (RH #141110) (from fedora)
- P16: fixed uninitialized fp in function inet_cfg (RH #162412) (from fedora)
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.6
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.6
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Sep 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.6-29avx
- sync patches with Mandriva (who synced with Fedora)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.6-28avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 7.6-27avx
- bootstrap build

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 7.6-26avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 7.6-25sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 7.6-24sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
