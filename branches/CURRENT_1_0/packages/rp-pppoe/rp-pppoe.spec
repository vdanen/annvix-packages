%define name	rp-pppoe
%define version	3.5
%define release	4sls

Summary:	ADSL/PPPoE userspace driver
Name:		%{name}
Version:	%{version}
Release: 	%{release}
Source:		http://www.roaringpenguin.com/%{name}-%{version}.tar.bz2
License:	GPL
Group:		System/Servers
URL:		http://www.roaringpenguin.com/pppoe

BuildRoot:	%_tmppath/%name-%version-root
BuildRequires:	ppp

Requires:	ppp >= 2.4.1

%description
PPPoE (Point-to-Point Protocol over Ethernet) is a protocol used by
many ADSL Internet Service Providers. Roaring Penguin has a free
client for Linux systems to connect to PPPoE service providers.

The client is a user-mode program and does not require any kernel
modifications. It is fully compliant with RFC 2516, the official PPPoE
specification.

It has been tested with many ISPs, such as the Canadian Sympatico HSE (High
Speed Edition) service.

%prep
%setup -q

%build
cd src
autoconf
%configure
%make

%install
rm -fr %buildroot
install -d -m 0755 %buildroot

cd src
make install RPM_INSTALL_ROOT=$RPM_BUILD_ROOT
cd ..

perl -pi -e "s/restart/restart\|reload/g;" %{buildroot}%{_initrddir}/adsl

rm -rf %{buildroot}/usr/doc

%clean
rm -fr %buildroot


%files
%defattr(-,root,root)
%doc doc/* README SERVPOET
%config(noreplace) %{_sysconfdir}/ppp/pppoe.conf
%config(noreplace) %{_sysconfdir}/ppp/plugins/README
%config(noreplace) %{_sysconfdir}/ppp/pppoe-server-options
%config(noreplace) %{_sysconfdir}/ppp/firewall-masq
%config(noreplace) %{_sysconfdir}/ppp/firewall-standalone
%{_sbindir}/pppoe
%{_sbindir}/pppoe-server
%{_sbindir}/pppoe-sniff
%{_sbindir}/pppoe-relay
%{_sbindir}/adsl-connect
%{_sbindir}/adsl-start
%{_sbindir}/adsl-stop
%{_sbindir}/adsl-setup
%{_sbindir}/adsl-status
%{_mandir}/man[58]/*
%config(noreplace)%{_initrddir}/adsl


%changelog
* Fri Jan 23 2004 Vincent Danen <vdanen@opensls.org> 3.5-4sls
- OpenSLS build
- tidy spec
- drop gui package

* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.5-3mdk
- rebuild
- macroize

* Thu Feb 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 3.5-2mdk
- rebuild
- misc spec file fixes

- new macros from ADVX-build
* Mon Jul 29 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.5-1mdk
- New and shiny source.

* Fri Jul 05 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.4-2mdk
- /usr/bin/wish dependency for gui package (Vox).

* Tue Jun 25 2002 Christian Belisle <cbelisle@mandrakesoft.com> 3.4-1mdk
- New version 3.4.

* Sun Mar 24 2002 David BAUDENS <baudens@mandrakesoft.com> 3.3-3mdk
- Hum, allow menu entry to be displayed in menu structures...
- Add icon to menu entry

* Fri Feb  1 2002 dam's <damien@mandrakesoft.com> 3.3-2mdk
- added noreplace for /etc/rp-pppoe.conf

* Mon Jan 14 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.3-1mdk
- Bump to 3.3.

* Tue Jul 03 2001 Yves Bailly <ybailly@mandrakesoft.com> 3.1-2mdk
- fixed missing /etc/ppp/rp-pppoe-gui for the gui package (should be done
  at the rp-pppoe level, not here)

* Sat Jun 30 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.1-1mdk
- Bump 3.1 into cooker.

* Fri Apr 13 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.0-1mdk
- Make a new and shiny RPM.
- Don't (noreplace) pppoe.conf as that is incompatible with the older ones.
- Split GUI into a separate package.

* Wed Mar 14 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.8-3mdk
- fix compile (remove ansi-pedantic, fix includes)

* Sun Feb 18 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.8-2mdk
- Include pppoe-relay file.

* Tue Feb 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.8-1mdk
- bump to 2.8.
- change directory to src before doing a configure.
- cleanup of man-pages file list.

* Tue Jan 09 2001 Geoff <snailtalk@mandrakesoft.com> 2.6-1mdk
- new and shiny source.
- remove the perl replacement expression used to replace the default
  optflags with our own.
  
* Wed Dec 20 2000 David BAUDENS <baudens@mandrakesoft.com> 2.5-4mdk
- BuildRequires: ppp
- Use %%make macro
- s/Copyright/License

* Mon Dec 18 2000 Vincent Danen <vdanen@mandrakesoft.com> 2.5-3mdk
- macros
- move /usr/man to /usr/share/man where it belongs

* Sun Dec 17 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 2.5-2mdk
- test with Sympatico HSE
- added missing files in spec (adsl-status, pppoe-snif, etc)

* Sat Dec 16 2000 Vincent Danen <vdanen@mandrakesoft.com> 2.5-1mdk
- 2.5 (security fixes)

* Thu Oct  5 2000 dam's <damien@mandrakesoft.com> 1.7-3mdk
- added patch0. the bogus connection is cleanly removed.

* Tue Sep  5 2000 Etienne Faure  <etienne@mandraksoft.com> 1.7-2mdk
- rebuilt with _mandir and %%doc macros
- run chkconfig

* Fri Apr  7 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.7-1mdk
- changed group
- new version

* Tue Mar  1 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.6-1mdk
- updated to 1.6
- merged my patches with the author so it's in the distribution
 
*Sun Feb 20 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 1.3-1mdk
- First Mandrake release
- require pppoe-linuxconf
