#
# spec file for package openswan
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		openswan
%define version		2.3.1
%define release		1avx
%define epoch		1

%define their_version	2.3.1
%define debug_package	%{nil}

Summary:	An implementation of IPSEC & IKE for Linux
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
URL:		http://www.openswan.org/
License:	GPL
Group:		System/Servers
Source0:	http://www.openswan.org/code/openswan-%{their_version}.tar.gz
Source1:	http://www.openswan.org/code/openswan-%{their_version}.tar.gz.asc
Patch0:		openswan-2.3.1.gcc4.patch.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	gmp-devel, pam-devel, bison

Provides:	ipsec-userland
Requires:	iproute2
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
%patch0 -p1 -b .gcc4


%build
%serverbuild

find . -name "Makefile*" | xargs perl -pi -e "s|libexec|%{_lib}|g"

make \
    USERCOMPILE="-g %{optflags}" \
    INC_USRLOCAL=%{_prefix} \
    MANTREE=%{_mandir} \
    INC_RCDEFAULT=%{_initrddir} \
    CONFDIR=%{_sysconfdir}/%{name} \
    FINALCONFDIR=%{_sysconfdir}/%{name} \
    FINALCONFFILE=%{_sysconfdir}/%{name}/ipsec.conf \
    FINALLIBEXECDIR=%{_libdir}/ipsec \
    FINALLIBDIR=%{_libdir}/ipsec \
    programs


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%make \
    DESTDIR=%{buildroot} \
    INC_USRLOCAL=%{_prefix} \
    MANTREE=%{buildroot}%{_mandir} \
    INC_RCDEFAULT=%{_initrddir} \
    INC_USRLOCAL=%{_prefix} \
    INC_RCDEFAULT=%{_initrddir} \
    FINALCONFDIR=%{_sysconfdir}/%{name} \
    FINALLIBEXECDIR=%{_libdir}/ipsec \
    FINALLIBDIR=%{_libdir}/ipsec \
    install

install -d -m 0700 %{buildroot}%{_localstatedir}/run/pluto
install -d %{buildroot}%{_sbindir}

# Remove unpackaged files
rm -rf %{buildroot}%{_defaultdocdir}/freeswan
rm -rf %{buildroot}%{_docdir}/%{name}
rm -rf %{buildroot}%{_sysconfdir}/rc.d/rc*
rm -rf %{buildroot}%{_sysconfdir}/%{name}/ipsec.d/examples

%preun
%_preun_service ipsec

%post
%_post_service ipsec


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc BUGS CHANGES COPYING CREDITS README programs/examples
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ipsec.conf
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}/ipsec.d
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}/ipsec.d/cacerts
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}/ipsec.d/crls
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}/ipsec.d/private
%attr(0700,root,root) %dir %{_sysconfdir}/%{name}/ipsec.d/policies
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ipsec.d/policies/*
%config(noreplace) %{_initrddir}/ipsec
%{_libdir}/ipsec
%{_sbindir}/ipsec
%{_mandir}/*/*
%{_localstatedir}/run/pluto


%changelog
* Wed Aug 24 2005 Ying-Hung Chen <ying@annvix.org> 2.3.1-1avx
- 2.3.1

* Fri Aug 12 2005 Ying-Hung Chen <ying@annvix.org> 1.0.9-3avx
- P0: for x86_64 platform so it will utilize /usr/lib64
- spec cleanups (vdanen)

* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 1.0.9-2avx
- remove des_crypt.3 as it conflicts with man-pages

* Tue Feb 01 2005 Vincent Danen <vdanen@annvix.org> 1.0.9-1avx
- 1.0.9 (fixes iDefense security advisory 01.26.05: Openswan XAUTH/PAM
  Buffer Overflow Vulnerability)

* Wed Aug 25 2004 Vincent Danen <vdanen@annvix.org> 1.0.7-1avx
- drop to the stable 1.x branch (1.0.7)
- fix the filelist

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
