%define name	ipsec-tools
%define version	0.2.5
%define release	1sls

%define LIBMAJ		0
%define libname		%mklibname %name %LIBMAJ
%define libnamedev	%{libname}-devel

Summary:	Tools for configuring and using IPSEC
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Networking/Other
URL:		http://ipsec-tools.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/ipsec-tools/ipsec-tools-%{version}.tar.bz2
Source1:	ipsec.h
Source2:	pfkeyv2.h
Source3:	racoon.conf
Source4:	psk.txt
Source5:	xfrm.h

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildPrereq:	openssl-devel, krb5-devel

Requires:	%{libname} = %{version}

%description
This is the IPsec-Tools package.  You need this package in order to
really use the IPsec functionality in the linux-2.5 and above kernels.  
This package builds:
 
	- libipsec, a PFKeyV2 library
	- setkey, a program to directly manipulate policies and SAs
	- racoon, an IKEv1 keying daemon

%package -n %{libname}
Summary:	The shared libraries used by ipsec-tools
Group:		System/Libraries
Prereq:		grep, sh-utils

%description -n %{libname}
These are the shared libraries for the IPsec-Tools package.

%prep
%setup -q

mkdir -p kernel-headers/linux
cp %{SOURCE1} %{SOURCE2} %{SOURCE5} kernel-headers/linux

%build
CFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=/usr --exec-prefix=/ \
 --libdir=/%{_lib} \
 --sysconfdir=%{_sysconfdir} \
 --mandir=%{_mandir} \
 --with-kernel-headers=`pwd`/kernel-headers
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# no devel stuff for now
rm -rf $RPM_BUILD_ROOT/%{_lib}/libipsec.{a,la} \
      $RPM_BUILD_ROOT/%{_includedir} \
      $RPM_BUILD_ROOT/%{_mandir}/man3

rm -f $RPM_BUILD_ROOT%{_sysconfdir}/racoon/{psk.txt,psk.txt.dist,racoon.conf,racoon.conf.dist}
install -m 600 %{SOURCE3} \
  $RPM_BUILD_ROOT%{_sysconfdir}/racoon/racoon.conf
install -m 600 %{SOURCE4} \
  $RPM_BUILD_ROOT%{_sysconfdir}/racoon/psk.txt
mkdir -m 0700 -p $RPM_BUILD_ROOT%{_sysconfdir}/racoon/certs

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc ChangeLog NEWS README
%doc src/racoon/samples/racoon.conf src/racoon/samples/psk.txt
%doc src/racoon/doc/FAQ
/sbin/*
%{_mandir}/man*/*
%dir %{_sysconfdir}/racoon
%dir %{_sysconfdir}/racoon/certs
%config(noreplace) %{_sysconfdir}/racoon/psk.txt
%config(noreplace) %{_sysconfdir}/racoon/racoon.conf

%files -n %{libname}
%defattr(-,root,root)
%doc ChangeLog NEWS README
/%{_lib}/*

%changelog
* Tue May 25 2004 Vincent Danen <vdanen@opensls.org> 0.2.5-1sls
- first OpenSLS package
- tidy spec

* Thu Apr 08 2004 Florin <florin@mandrakesoft.com> 0.2.5-1mdk
- 0.2.5 (security update)
- /sbin now contains the binaries and not %{_sbindir} anymore

* Wed Jan 21 2004 Florin <florin@mandrakesoft.com> 0.2.3-1mdk
- first mandrake release
