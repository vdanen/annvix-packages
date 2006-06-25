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
%define version         2.0.5
%define release         %_revrel

%define plugindir	%{_libdir}/%{name}

Summary:	A Secure UDP Tunneling Daemon
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Other
URL:		http://openvpn.net/
Source0:	http://openvpn.net/release/%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  openssl-devel, pam-devel, automake1.8
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
    --enable-plugin \
    --disable-lzo

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


%clean
[ %{buildroot} != "/" ] && rm -rf %{buildroot}


%pre
%_pre_useradd %{name} %{_localstatedir}/%{name} /bin/true


%post
%_post_service %{name}


%preun
%_preun_service %{name}


%postun
%_postun_userdel %{name}


%files
%defattr(-,root,root)
%{_mandir}/man8/%{name}.8*
%{_sbindir}/%{name}
%{_datadir}/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_localstatedir}/%{name}
%dir %{plugindir}
%{plugindir}/*.so

%files doc
%defattr(-,root,root)
%doc AUTHORS INSTALL PORTS README
%doc plugin/README.*


%changelog
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

* Mon Jan  9 2006 Olivier Blin <oblin@mandriva.com> 2.0.5-5mdk
- fix typo in initscript

* Mon Jan  9 2006 Olivier Blin <oblin@mandriva.com> 2.0.5-4mdk
- convert parallel init to LSB

* Tue Jan 03 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 2.0.5-3mdk
- add parallel init support
- fix executable-marked-as-config-file
- be sure to wipe out buildroot at the beginning of %%install
- don't ship copyright notice as the package is GPL (see common-licenses)

* Sun Nov 13 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.5-2mdk
- rebuilt against openssl-0.9.8a

* Thu Nov 10 2005 Olivier Thauvin <nanardon@mandriva.org> 2.0.5-1mdk
- 2.0.5

* Sun Oct 16 2005 Olivier Thauvin <nanardon@mandriva.org> 2.0.2-1mdk
- 2.0.2

* Tue Aug 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.1-2mdk
- rebuilt against new openldap-2.3.6 libs

* Wed Aug 24 2005 Olivier Thauvin <nanardon@mandriva.org> 2.0.1-1mdk
- 2.0.1
- ldap patch version 1.0.1
- remove patch3, fix upstream

* Sat Jul 09 2005 Olivier Thauvin <nanardon@mandriva.org> 2.0-4mdk
- rebuild for lzo (#16777)
- add patch3: fix -lzo2 calls

* Wed Jun 22 2005 Olivier Thauvin <nanardon@mandriva.org> 2.0-3mdk
- rebuild for lzo (Thanks Michar)

* Wed May 11 2005 Olivier Thauvin <nanardon@mandriva.org> 2.0-2mdk
- Request by Luis Daniel Lucio Quiroz <dlucio@okay.com.mx>
  - add native plugin
  - add openvpn-auth-ldap plugin (except for amd64)

* Tue Apr 19 2005 Olivier Thauvin <nanardon@mandriva.org> 2.0-1mdk
- 2.0 final

* Thu Apr 07 2005 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.0-0.rc20.1mdk
- 2.0-rc20

* Thu Jan 13 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.6.0-2mdk
- rebuild
- cosmetics

* Mon May 31 2004 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 1.6.0-1mdk
- 1.6.0
- fix buildrequires (lib64..)
- drop GPL license file, there's no reason for us to ship such common
  license files in packages, as we ship them with the common-licenses package!

* Thu Feb 26 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.5.0-2mdk
- used patch from Andre Nathan <andre@digirati.com.br> to ease adding routes

* Tue Nov 26 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.5.0-1mdk
- 1.5.0

* Sun Jun 27 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.4.2-1mdk
- 1.4.2

* Wed Jun 11 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.4.1-2mdk
- macroize
- drop redundant requires on liblzo1, rpm will figure out this itself
- add %%{_sysconfdir}/%{name} to files list
- do parallell build
- run under own user (Patch0)

* Mon Jun 02 2003 Florin <florin@mandrakesoft.com> 1.4.1-1mdk
- 1.4.1

* Fri Feb 07 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.3.2-1mdk
- 1.3.2

* Thu Nov 28 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.3.1-2mdk
- BuildRequires liblzo-devel libopenssl-devel
- add missing initscript

* Sun Sep 22 2002 Han Boetes <han@linux-mandrake.com> 1.3.1-1mdk
- Bump version

* Mon Jun 17 2002 Florin <florin@mandrakesoft.com> 1.2.1-1mdk
- 1.2.1
- first mdk release

* Wed May 22 2002 James Yonan <jim@yonan.net> 1.2.0-1
-- Added mknod for Linux 2.4

* Wed May 15 2002 Doug Keller <dsk@voidstar.dyndns.org> 1.1.1.16-2
- Added init scripts
- Added conf file support

* Mon May 13 2002 bishop clark (LC957) <bishop@platypus.bc.ca> 1.1.1.14-1
- Added new directories for config examples and such

* Sun May 12 2002 bishop clark (LC957) <bishop@platypus.bc.ca> 1.1.1.13-1
- Updated buildroot directive and cleanup command
- added easy-rsa utilities

* Mon Mar 25 2002 bishop clark (LC957) <bishop@platypus.bc.ca> 1.0-1
- Initial build.
