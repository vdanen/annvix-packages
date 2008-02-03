#
# spec file for package ppp
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		ppp
%define version		2.4.4
%define release		%_revrel

Summary:	The Linux PPP daemon
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD/GPL
Group:		System/Servers
URL:		http://www.samba.org/ppp
Source0:	ftp://ftp.samba.org/pub/ppp/ppp-%{version}.tar.bz2
Source1:	ppp-2.3.5-pamd.conf
Source2:	ppp-2.4.1-mppe-crypto.tar.bz2
Source3:	README.pppoatm
Source4:	ppp.logrotate
Source5:	ppp-dhcpc.tar.bz2
Patch0:		ppp-2.4.3-make.patch
Patch1:		ppp-2.3.6-sample.patch
Patch2:		ppp-2.4.2-wtmp.patch
Patch3:		ppp-2.4.3-makeopt.patch
Patch4:		ppp-options.patch
Patch5:		ppp-2.4.3-pppdump-Makefile.patch
Patch6:		ppp-2.4.3-noexttraffic.patch
# (blino) use external libatm for pppoatm plugin
Patch7:		ppp-2.4.3-libatm.patch
Patch8: 	ppp-2.4.2-pie.patch
Patch10:	ppp-2.4.4-dontwriteetc.patch
# Original from http://www.polbox.com/h/hs001/; ported by blino
Patch11:	ppp-2.4.4-mppe-mppc-1.1.patch
Patch13:	ppp-2.4.2-signal.patch
Patch15:	ppp-2.4.3-pic.patch
Patch16:	ppp-2.4.3-etcppp.patch
Patch18:	ppp-2.4.3-includes-sha1.patch
Patch19:	ppp-2.4.3-makeopt2.patch
Patch21:	ppp-2.4.3-fixprotoinc.patch
Patch22:	ppp-2.4.3-hspeed.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	linux-atm-devel
BuildRequires:	libpcap-devel 
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	pam-devel
BuildRequires:	libtool

Requires:	glibc >= 2.0.6

%description
The ppp package contains the PPP (Point-to-Point Protocol) daemon
and documentation for PPP support.  The PPP protocol provides a
method for transmitting datagrams over serial point-to-point links.


%package devel
Summary:	PPP development files
Group:		Development/C
Requires:	%{name} = %{version}

%description devel
The development files for PPP.


%package pppoatm
Summary:	PPP over ATM plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description pppoatm
PPP over ATM plugin for %{name}.


%package pppoe
Summary:	PPP over ethernet plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description pppoe
PPP over ethernet plugin for %{name}.


%package radius
Summary:	Radius plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}
Requires:	radiusclient-utils

%description radius
Radius plugin for %{name}.


%package dhcp
Summary:	DHCP plugin for %{name}
Group:		System/Servers
Requires:	%{name} = %{version}

%description dhcp
DHCP plugin for %{name}.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup  -q
find -type d -name CVS|xargs rm -rf
%patch0 -p1 -b .make
%patch1 -p1 -b .sample
%patch2 -p1 -b .wtmp
%patch3 -p1 -b .makeopt
%patch4 -p1 -b .options
%patch5 -p1 -b .pppdump-Makefile
# (gg) add noext-traffic option
%patch6 -p1 -b .noext
%patch7 -p1 -b .libatm
%patch8 -p1 -b .pie

tar -xjf %{SOURCE2}
pushd pppd/plugins
    tar -xjf %{SOURCE5}
popd

%patch10 -p1 -b .dontwriteetc
%patch11 -p1 -b .mppe_mppc
#%patch13 -p1 -b .signal
%patch15 -p1 -b .pic
%patch16 -p1 -b .etcppp
%patch18 -p1 -b .incsha1
%patch19 -p1 -b .makeopt2
%patch21 -p1 -b .protoinc
%patch22 -p1 -b .hspeed

# lib64 fixes
perl -pi -e "s|^(LIBDIR.*)\\\$\(DESTDIR\)/lib|\1\\\$(INSTROOT)%{_libdir}|g" pppd/Makefile.linux pppd/plugins/Makefile.linux pppd/plugins/{pppoatm,radius,rp-pppoe}/Makefile.linux
perl -pi -e "s|(--prefix=/usr)|\1 --libdir=%{_libdir}|g" pppd/plugins/radius/Makefile.linux
perl -pi -e "/_PATH_PLUGIN/ and s|/usr/lib|%{_libdir}|"  pppd/pathnames.h
# enable the radius and the dhcp plugins
perl -p -i -e "s|^(PLUGINS :=)|SUBDIRS += dhcp\n\$1|g" pppd/plugins/Makefile.linux

# fix /usr/local in scripts path
perl -pi -e "s|/usr/local/bin/pppd|%{_sbindir}/pppd|g;
	     s|/usr/local/bin/ssh|%{_bindir}/ssh|g;
	     s|/usr/local/bin/expect|%{_bindir}/expect|g" \
    scripts/ppp-on-rsh \
    scripts/ppp-on-ssh \
    scripts/secure-card

# remove zero-length samples
find sample -size 0 -exec rm -f {} \;


%build
# stpcpy() is a GNU extension
OPT_FLAGS="%{optflags} -D_GNU_SOURCE"

perl -pi -e "s/openssl/openssl -DOPENSSL_NO_SHA1/;" openssl/crypto/sha/Makefile

CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" %configure
# remove the following line when rebuilding against kernel 2.4 for multilink
#perl -pi -e "s|-DHAVE_MULTILINK||" pppd/Makefile
make RPM_OPT_FLAGS="$OPT_FLAGS -DDO_BSD_COMPRESS=0" LIBDIR=%{_libdir}
make -C pppd/plugins -f Makefile.linux

# docs
mkdir dhcp-plugin
cp -a pppd/plugins/dhcp/{README,AUTHORS,COPYING} dhcp-plugin/


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/{%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/{ppp/peers,pam.d}}

%make install LIBDIR=%{buildroot}%{_libdir}/pppd/%{version}/ INSTALL=install -C pppd/plugins/dhcp
%make install INSTROOT=%{buildroot} SUBDIRS="pppoatm rp-pppoe radius"

%multiarch_includes %{buildroot}%{_includedir}/pppd/pathnames.h

chmod u+w %{buildroot}%{_sbindir}/*

strip %{buildroot}%{_sbindir}/pppd

# it shouldn't be SUID root be default
chmod 0755 %{buildroot}%{_sbindir}/pppd

chmod go+r scripts/*
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/ppp
install -m 0644 %{SOURCE3} %{_builddir}/%{name}-%{version}

touch %{buildroot}/var/log/ppp/connect-errors
touch %{buildroot}/var/run/ppp/resolv.conf
ln -s ../../var/log/ppp/connect-errors %{buildroot}/etc/ppp/connect-errors
ln -s ../../var/run/ppp/resolv.conf %{buildroot}/etc/ppp/resolv.conf


# logrotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/ppp

rm -rf %{buildroot}%{_sbindir}/*rad*
rm -rf %{buildroot}%{_sysconfdir}/*rad*
rm -rf %{buildroot}%{_includedir}/*rad*
rm -rf %{buildroot}%{_libdir}/*rad*


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_sbindir}/chat
%{_sbindir}/pppdump
%attr(0755,root,root)	%{_sbindir}/pppd
%attr(0755,root,daemon)	%{_sbindir}/pppstats
%dir %{_libdir}/pppd
%{_libdir}/pppd/%{version}
%exclude %{_libdir}/pppd/%{version}/pppoatm.so
%exclude %{_libdir}/pppd/%{version}/rp-pppoe.so
%exclude %{_libdir}/pppd/%{version}/rad*
%exclude %{_libdir}/pppd/%{version}/dhcpc.so
%dir /var/run/ppp
/var/run/ppp/*
%attr(0700,root,root) %dir /var/log/ppp
/var/log/ppp/*
%dir %{_sysconfdir}/ppp
%attr(0600,root,daemon) %config(noreplace) %{_sysconfdir}/ppp/chap-secrets
%attr(0600,root,daemon) %config(noreplace) %{_sysconfdir}/ppp/options
%attr(0600,root,daemon) %config(noreplace) %{_sysconfdir}/ppp/pap-secrets
%attr(0600,root,daemon) %{_sysconfdir}/ppp/connect-errors
%attr(0600,root,daemon) %{_sysconfdir}/ppp/resolv.conf
%attr(755,root,daemon) %dir %{_sysconfdir}/ppp/peers
%{_mandir}/man*/*
%config(noreplace) %{_sysconfdir}/pam.d/ppp
%config(noreplace) %{_sysconfdir}/logrotate.d/ppp

%files devel
%defattr(-,root,root)
%{_includedir}/pppd/*
%multiarch %{multiarch_includedir}/pppd/pathnames.h

%files pppoatm
%defattr(-,root,root)
%{_libdir}/pppd/%{version}/pppoatm.so

%files pppoe
%defattr(-,root,root)
%{_libdir}/pppd/%{version}/rp-pppoe.so
%attr(755,root,root) %{_sbindir}/pppoe-discovery

%files radius
%defattr(-,root,root)
%{_libdir}/pppd/%{version}/rad*.so
%{_mandir}/man8/*rad*

%files dhcp
%defattr(-,root,root)
%{_libdir}/pppd/%{version}/dhcpc.so

%files doc
%defattr(-,root,root)
%doc FAQ PLUGINS README* scripts sample dhcp-plugin


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.4.4
- rebuild against new openssl

* Sun Sep 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.4.4
- rebuild against new pam

* Sun Sep 16 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.4.4
- rebuild against new libpcap
- fix buildreq's

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.4
- rebuild against new pam

* Thu Dec 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.4
- 2.4.4; fixes CVE-2006-2194
- dropped P9, P17; merged upstream
- updated P10
- fix the plugin installation

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.3
- rebuild against new openssl
- spec cleanups

* Sun Jun 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.3
- rebuild against new pam and update pam config

* Sat Jun 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.3
- add -doc subpackage
- rebuild with gcc4
- remove zero-length sample files

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.3
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.4.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.3-1avx
- 2.4.3
- sync with cooker 2.4.3-9mdk: (way too much crap to note)

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.2-4avx
- bootstrap build (new gcc, new glibc)
- get rid of the symlinks in /etc/ppp for connect-errors and resolv.conf;
  they don't point to anything anyways and there's no point to dangling
  symlinks

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.2-3avx
- rebuild

* Thu Jan 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.4.2-2avx
- rebuild against new openssl

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.2-1avx
- 2.4.2
- own directories
- strip suid bit from pppd; we don't need it since users shouldn't
  be connecting to the internet on a server system
- pass -fPIC if compiling on x86_64
- merge with cooker 2.4Ã.2-2mdk (florin):
  - update the make, makeopt, wtmp patches
  - remove the pam_sessions, zfree, mppe, includes, libdir, filter
    pppoe, disconnect, gcc, pcap, varargs obsolete patches
  - add the include files
  - add the README.pppoatm FAW PLUGINS files
  - add the logrotate patch and file (rh)
  - add the pie, dontwriteetc patches (rh)
  - use a different pppoatm patch

* Sun Jun 27 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.4.1-15avx
- Annvix build
- P16: need to include pcap-bpf.h instead of net/bpf.h

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 2.4.1-14sls
- minor spec cleanups

* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 2.4.1-13sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
