#
# spec file for package openvpn
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision        $Rev$
%define name            openvpn
%define version         2.0.9
%define release         %_revrel

%define plugindir	%{_libdir}/%{name}

Summary:	A Secure UDP Tunneling Daemon
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Other
URL:		http://openvpn.net/
Source0:	http://openvpn.net/release/%{name}-%{version}.tar.gz
Source1:	openvpn.run
Source2:	openvpn-log.run
Source3:	06_openvpn.afterboot

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:  openssl-devel
BuildRequires:	pam-devel
BuildRequires:	automake1.8
BuildRequires:	liblzo-devel

Requires(pre):	rpm-helper
Requires(preun): rpm-helper
Requires(post):	rpm-helper
Requires(postun): rpm-helper


%description
OpenVPN is a robust and highly flexible tunneling application that  uses
all of the encryption, authentication, and certification features of the
OpenSSL library to securely tunnel IP networks over a single UDP port.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
#./pre-touch
aclocal-1.8
automake-1.8
autoconf

CFLAGS="%{optflags} -fPIC" CCFLAGS="%{optflags} -fPIC"

%configure \
    --enable-pthread \
    --enable-plugin 

%make

# plugins
%make -C plugin/down-root
%make -C plugin/auth-pam


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}

cp -pr easy-rsa sample-{config-file,key,script}s %{buildroot}%{_datadir}/%{name}

mkdir -p %{buildroot}%{_localstatedir}/%{name}

#plugins
mkdir -p %{buildroot}%{plugindir}

for pi in down-root auth-pam; do
    cp -f plugin/$pi/README plugin/README.$pi
    install -c -m 0755 plugin/$pi/openvpn-$pi.so %{buildroot}%{plugindir}/openvpn-$pi.so
done

mkdir -p %{buildroot}%{_srvdir}/openvpn/{log,env}
install -m 0740 %{_sourcedir}/openvpn.run %{buildroot}%{_srvdir}/openvpn/run
install -m 0740 %{_sourcedir}/openvpn-log.run %{buildroot}%{_srvdir}/openvpn/log/run
echo "local" >%{buildroot}%{_srvdir}/openvpn/env/NAME

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{_sourcedir}/06_openvpn.afterboot %{buildroot}%{_datadir}/afterboot/06_openvpn


%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}


%pre
%_pre_useradd openvpn %{_localstatedir}/openvpn /bin/true 94


%post
%_post_srv openvpn
%_mkafterboot


%preun
%_preun_srv openvpn


%postun
%_mkafterboot
%_postun_userdel openvpn


%files
%defattr(-,root,root)
%{_mandir}/man8/%{name}.8*
%{_sbindir}/openvpn
%{_datadir}/openvpn
%dir %{_sysconfdir}/openvpn
%dir %{_localstatedir}/openvpn
%dir %{plugindir}
%{plugindir}/*.so
%dir %attr(0750,root,admin) %{_srvdir}/openvpn
%dir %attr(0750,root,admin) %{_srvdir}/openvpn/log
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/openvpn/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/openvpn/log/run
%attr(0640,root,admin) %{_srvdir}/openvpn/env/NAME
%{_datadir}/afterboot/06_openvpn

%files doc
%defattr(-,root,root)
%doc AUTHORS INSTALL PORTS README
%doc plugin/README.*
%doc sample-config-files sample-keys sample-scripts


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.9
- rebuild against new openssl

* Sun Sep 30 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.9
- rebuild against new pam

* Mon May 07 2007 Vincent Danen <vdanen-at-build.annvix.org> 2.0.9
- 2.0.9
- provide default runscripts
- use a static uid/gid (94)
- include sample files
- enable lzo compression support
- in short, finished the dang package (was more or less worthless before)

* Fri Dec 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.5
- rebuild against new pam

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.5
- rebuild against new openssl
- spec cleanups

* Sun Jun 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.5
- rebuild against new pam
- add -doc subpackage
- rebuild with gcc4

* Wed Feb  1 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0.5
- first Annvix build
- don't build with lzo support
- spec cleanups
- don't include the ldap auth plugin if it won't work on all platforms
- drop all patches
- NOTE: the plan is for this to replace openswan if we can
- NOTE: we need to provide some run scripts for a server and for a client
  and note that these are samples only to be copied and customized in order
  to create differing routes

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
