%define name	net-tools
%define version 1.60
%define release 10sls

%define url http://www.tazenda.demon.co.uk/phil/net-tools/

Summary:	The basic tools for setting up networking.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Networking
URL:		%{url}
Source0:	%{url}/net-tools-%{version}.tar.bz2
Source1:	net-tools-1.54-config.h.bz2
Source2:	net-tools-1.54-config.make.bz2
Source3:	net-tools-1.54-config.status.bz2
Source5:	ether-wake.c
Patch1:		net-tools-1.54-ipvs.patch.bz2
Patch2:		net-tools-1.57-bug22040.patch.bz2
Patch3:		net-tools-1.60-manydevs.patch.bz2
Patch4:		net-tools-1.60-virtualname.patch.bz2
Patch5:		net-tools-1.60-gcc-3.3.patch.bz2

BuildRequires:	gettext
BuildRoot:	%{_tmppath}/%{name}-root

%description
The net-tools package contains the basic tools needed for setting up
networking:  ifconfig, netstat, route and others.

%prep
%setup -q
%patch1 -p1 -b .ipvs
%patch2 -p1 -b .bug22040
%patch3 -p0 -b .manydevs
%patch4 -p1 -b .virtualname
%patch5 -p1 -b .gcc3.3
bzcat %SOURCE1 > ./config.h
bzcat %SOURCE2 > ./config.make
bzcat %SOURCE3 > ./config.status

cp %{SOURCE5} .

%build
%make "COPTS=$RPM_OPT_FLAGS"
%make ether-wake CC=gcc CFLAGS="%optflags"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{bin,sbin,%{_mandir}/man{1,5,8}}

make BASEDIR=$RPM_BUILD_ROOT LANG="de_DE en_US fr_FR pt_BR" install

mv $RPM_BUILD_ROOT%{_mandir}/de{_DE,}
mv $RPM_BUILD_ROOT%{_mandir}/fr{_FR,}

install -m 755 ether-wake %{buildroot}/sbin

mv  $RPM_BUILD_ROOT%{_datadir}/locale/et_EE \
	$RPM_BUILD_ROOT%{_datadir}/locale/et

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc README README.ipv6 TODO INSTALLING COPYING ABOUT-NLS
%defattr(-,root,root)
/bin/*
/sbin/*
%{_mandir}/man[158]/*
%lang(de)	%{_mandir}/de/man[158]/*
%lang(fr)	%{_mandir}/fr/man[158]/*
%lang(pt_BR)	%{_mandir}/pt_BR/man[158]/*

%changelog
* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 1.60-10sls
- OpenSLS build
- tidy spec

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.60-9mdk
- fix gcc-3.3 patch (P5)

* Sat Jul 19 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.60-8mdk
- fix gcc-3.3 build (P5), updated S5
- fix invalid locales (s/fr_FR/fr/ & s/de_DE/de/)
- fix url

* Thu Apr 17 2003 Erwan Velu <erwan@mandrakesoft.com> 1.60-7mdk
- New version of ether-wake (1.06)
* Tue Feb 18 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.60-6mdk
- Rebuild

* Wed Aug 21 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.60-5mdk
- merged with rh

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.60-4mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Sun Jun  2 2002 Stefan van der Eijk <stefan@eijk.nu> 1.60-3mdk
- BuildRequires
- Copyright --> License

* Thu Jun 21 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.60-2mdk
- Add ether-wake from donald-becker.
- Clean up specs.
- Fix man-pages.

* Mon Apr 16 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.60-1mdk
- Version 1.60 on Easter Monday.

* Fri Feb 23 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.59-1mdk
- 1.59.

* Thu Feb 22 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.58-4mdk
- Add ipvs patch.

* Fri Feb 16 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.58-3mdk
- Fix ifconfig: don't close a socket that we are going to use.

* Thu Feb 15 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.58-2mdk
- Really put in the i18n man-pages.

* Sun Feb 11 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.58-1mdk
- New and shiny source.
- Dump the fhs patch, as things get intalled in the correct location now.
- Put the i18n man-pages in the location where they should belong.

* Wed Nov  8 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.57-5mdk
- Enable all protocol options.
- Build and install mii-tool.
- Really handle RPM_OPT_FLAGS.
- Add documentation.
- Update description.

* Thu Aug  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.57-4mdk
- Clean-up.

* Fri Jul 21 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.57-3mdk
- More macros.
- Readd man pages :-(

* Thu Jul 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.57-2mdk
- BM.

* Fri Jun 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.57-1mdk
- 1.57.
- Use mandir macros for FHS compatibilty.

* Tue Apr  4 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.55-1mdk
- 1.55.

* Fri Mar 31 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.54-1mdk
- Spec-helper clean-up.
- Merge with rh-patchs.
- use find_lang macros for locales.
- Adjust groups.

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- %lang in man/-locale.
- big spec cleanup.

* Sun Aug 29 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 1.53:	- fixes several buffer overruns
	- adds german man pages
	- adds french ethers.5 translation
	- adds estonian
- fix up .spec

* Mon Jul 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release (8mdk).

* Sat Jul 10 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- moved french manpages from fr_FR to fr
- compressed all man pages
- added french, spanish and wallon descriptions

* Fri Jun 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix potentional bufer overruns.
- patch to recognize ESP and GRE protocols for VPN masquerade
  <jhardin@wolfenet.com>.

* Wed Apr 28 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Update to 1.52

* Tue Apr 13 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add patch from RedHat6.0.
- Update to 1.51.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale
- handle RPM_OPT_FLAGS

* Tue Feb  2 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.50.
- added slattach/plipconfig/ipmaddr/iptunnel commands.
- enabled translated man pages.

* Tue Dec 15 1998 Jakub Jelinek <jj@ultra.linux.cz>
- update to 1.49.

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.48.

* Thu Nov 12 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.47.

* Wed Sep  2 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.46

* Thu Jul  9 1998 Jeff Johnson <jbj@redhat.com>
- build root
- include ethers.5

* Thu Jun 11 1998 Aron Griffis <agriffis@coat.com>
- upgraded to 1.45
- patched hostname.c to initialize buffer
- patched ax25.c to use kernel headers

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Feb 27 1998 Jason Spangler <jasons@usemail.com>
- added config patch

* Fri Feb 27 1998 Jason Spangler <jasons@usemail.com>
- changed to net-tools 1.432
- removed old glibc 2.1 patch
 
* Wed Oct 22 1997 Erik Troan <ewt@redhat.com>
- added extra patches for glibc 2.1

* Tue Oct 21 1997 Erik Troan <ewt@redhat.com>
- included complete set of network protocols (some were removed for
  initial glibc work)

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- updated glibc patch for glibc 2.0.5

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- updated to 1.33
