%define name	openswan
%define version	2.1.4
%define release	1avx

%define their_version	2.1.4
%define debug_package	%{nil}

Summary:	An implementation of IPSEC & IKE for Linux.
Name:		%{name}
Version:	%{version}
Release:	%{release}
URL:		http://www.openswan.org/
License:	GPL
Group:		System/Servers
Source0:	http://www.openswan.org/code/openswan-%{their_version}.tar.gz
Source1:	http://www.openswan.org/code/openswan-%{their_version}.tar.gz.asc

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	gmp-devel, pam-devel, man

Provides:	ipsec-userland
Requires:	iproute2 ipsec-tools
Prereq:		chkconfig rpm-helper

%description
Openswan is a free implementation of IPSEC & IKE for Linux, a fork of the 
FreeS/WAN project.

IPSEC is Internet Protocol Security and uses strong cryptography to 
provide both authentication and encryption services.  These services 
allow you to build secure tunnels through untrusted networks.  
Everything passing through the untrusted net is encrypted by the ipsec 
gateway machine and decrypted by the gateway at the other end of the 
tunnel.  The resulting tunnel is a virtual private network or VPN.

This package contains the daemons and userland tools for setting up
Openswan on a kernel with either the 2.6 native IPsec code, or 
FreeS/WAN's KLIPS.

%prep
%setup -q -n openswan-%{their_version}

%build
%serverbuild

find . -name "Makefile*" | xargs perl -pi -e "s|libexec|lib|g"

%make \
  USERCOMPILE="-g %{optflags}" \
  INC_USRLOCAL=%{_prefix} \
  MANTREE=%{_mandir} \
  INC_RCDEFAULT=%{_initrddir} \
	CONFDIR=%{_sysconfdir}/%name \
	FINALCONFDIR=%{_sysconfdir}/%name \
	FINALCONFFILE=%{_sysconfdir}/%name/ipsec.conf \
	FINALLIBEXECDIR=%{_libdir}/ipsec \
	FINALLIBDIR=%{_libdir}/ipsec \
  programs


FS=$(pwd)
mkdir -p BUILD.%{_target_cpu}
mkdir -p BUILD.%{_target_cpu}-smp

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%{make} \
  DESTDIR=%{buildroot} \
  INC_USRLOCAL=%{_prefix} \
  MANTREE=%{buildroot}%{_mandir} \
  INC_RCDEFAULT=%{_initrddir} \
	INC_USRLOCAL=%{_prefix} \
  INC_RCDEFAULT=%{_initrddir} \
  FINALCONFDIR=%{_sysconfdir}/%name \
	FINALLIBEXECDIR=%{_libdir}/ipsec \
  FINALLIBDIR=%{_libdir}/ipsec \
  install

install -d -m700 %{buildroot}%{_localstatedir}/run/pluto
install -d %{buildroot}%{_sbindir}
# Remove old documentation for the time being.
rm -rf %{buildroot}%{_defaultdocdir}/freeswan

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc BUGS CHANGES COPYING CREDITS README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ipsec.conf
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}/ipsec.d
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ipsec.d/*/*
%config(noreplace) %{_initrddir}/ipsec
%config(noreplace) %{_sysconfdir}/rc.d/rc*.d/*ipsec
%{_libdir}/ipsec
%{_sbindir}/ipsec
%doc %{_mandir}/*/*
%{_localstatedir}/run/pluto


%preun
%_preun_service ipsec

%post
%_post_service ipsec

%changelog
* Mon Jun 28 2004 Vincent Danen <vdanen@annvix.org> 2.1.4-1avx
- 2.1.4; security fix for CAN-2004-0590

* Tue Jun 22 2004 Vincent Danen <vdanen@annvix.org> 2.1.2-2avx
- require packages, not files
- Annvix build

* Sat May 22 2004 Thomas Backlund <tmb@iki.fi> 2.1.2-1sls
- 2.1.2 final
- first OpenSLS specific build

* Tue May 18 2004 Florin <florin@mandrakesoft.com> 2.1.2-0.rc3.3mdk
- sysconfdir is now /etc/openswan

* Wed Apr 21 2004 Florin <florin@mandrakesoft.com> 2.1.2-0.rc3.2mdk
- add the signature file

* Wed Apr 21 2004 Florin <florin@mandrakesoft.com> 2.1.2-0.rc3.1mdk
- first Mandrake release
