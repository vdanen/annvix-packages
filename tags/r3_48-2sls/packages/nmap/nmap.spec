%define name	nmap
%define version	3.48
%define release	2sls

Summary:	Network exploration tool and security scanner
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		1
License:	GPL
Group:		Networking/Other
URL:		http://www.insecure.org/nmap/
Source0:	http://download.insecure.org/nmap/dist/%{name}-%version.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	pcre-devel
BuildRequires:	openssl-devel

%description
Nmap is a utility for network exploration or security auditing. It supports
ping scanning (determine which hosts are up), many port scanning techniques
(determine what services the hosts are offering), and TCP/IP fingerprinting
(remote host operating system identification). Nmap also offers flexible target
and port specification, decoy scanning, determination of TCP sequence
predictability characteristics, sunRPC scanning, reverse-identd scanning, and
more.

%prep
%setup -q -n %{name}-%version

%build
%ifarch amd64 x86_64
# nmap doesn't like the amd64 build name
CFLAGS="%{optflags}" ./configure --prefix=%{_prefix} --libdir=%{_libdir} --libexecdir=%{_libdir}
%else
%configure2_5x
%endif
%make 

%install
rm -rf %{buildroot}
%makeinstall nmapdatadir=%{buildroot}%{_datadir}/nmap


%clean
rm -rf %{buildroot}


%files 
%defattr(-,root,root)
%doc docs/README docs/nmap-fingerprinting-article.txt
%doc docs/nmap.deprecated.txt docs/nmap.usage.txt docs/nmap_doc.html
%doc docs/nmap_manpage.html CHANGELOG
%{_bindir}/nmap
%{_datadir}/%{name}
%{_mandir}/man1/nmap.*

%changelog
* Sun Jan 11 2004 Vincent Danen <vdanen@opensls.org> 3.48-2sls
- OpenSLS build
- tidy spec
- don't build the frontend
- don't use %%configure(2_5x) on amd64 since it doesn't like the build name

* Fri Nov 07 2003 Abel Cheung <deaddog@deaddog.org> 3.48-1mdk
- 3.48

* Mon Sep  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.30-2mdk
- recognize amd64

* Tue Jul 01 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.30-1mdk
- new release

* Tue May 13 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.27-1mdk
- new release

* Wed Apr 23 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.25-1mdk
- new release

* Wed Apr 23 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.20-2mdk
- do not include nmapfe.1 in nmap package

* Fri Apr 04 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.20-1mdk
- new release

* Mon Jan 20 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.00-2mdk
- don't reference inexistant doc
- fix unpackaged files

* Mon Aug 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.00-1mdk
- new release

* Mon Jul 29 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.99-0.RC2.1mdk
- RC2

* Tue Jul 23 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.99-0.RC1.1mdk
- RC1 for 3.0

* Mon Jul 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.54-0.beta37.1mdk
- new release
- spec cleaning

* Sun May 12 2002 Yves Duret <yduret@mandrakesoft.com> 2.54-0.beta34.1mdk
- version BETA34

* Mon Apr 08 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.54-0.beta32.1mdk
- New and shiny nmap from www.insecure.org.

* Fri Feb 01 2002 Yves Duret <yduret@mandrakesoft.com> 2.54-0.beta30.2mdk
- xpm -> png icons
- more macros

* Tue Jan 22 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.54-0.beta30.1mdk
- update sources
- build for _target_platform !

* Fri Oct 19 2001 Sebastien Dupont <sdupont@mandrakesoft.com> 2.54-0.beta22.3mdk
- Epoch 1
- just change release name.
- permissions of documentations files

* Mon Jun 18 2001 Stefan van der Eijk <stefan@eijk.nu> 2.54BETA22-2mdk
- BuildRequires:	gtk+-devel
- Remove BuildRequires:	XFree86-devel

* Tue May 29 2001 Yves Bailly <ybailly@mandrakesoft.com> 2.54BETA22-1mdk
- upgrade to 2.54BETA22

* Mon Mar 26 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.53-7mdk
- clean spec: s,bzip2 -dc %%{SOURCE1} | tar -xf -,%%setup -a1

* Mon Mar 26 2001 Vincent Danen <vdanen@mandrakesoft.com> 2.53-6mdk
- don't call tar with -j anymore
- make longtitle in menu entry a little more verbose

* Fri Dec 22 2000 Vincent Danen <vdanen@mandrakesoft.com> 2.53-5mdk
- macros, some spec cleanups
- move manpages for nmapfe/xnmap to frontend package
- patch to build for glibc2.2

* Fri Oct 06 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.53-4mdk
- update for wrong menu entry.
- made icons transparent.

* Tue Aug 29 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.53-3mdk
- use %{_mandir}

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.53-2mdk
- automatically added BuildRequires

* Fri Jun  9 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.53-1mdk
- 2.53

* Fri Apr 28 2000 Vincent Saugey <vince@mandrakesoft.com> 2.30BETA17-3mdk
- add 3 icons for menu
 (Thx to Lenny, but i hadn't problem with stat !!)

* Wed Apr 12 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.30BETA17-3mdk
- add icon
- merge menu file with spec (to help vince' stats !!)

* Fri Mar 31 2000 Vincent Saugey <vince@mandrakesoft.com> 2.30BETA17-2mdk
- Add menu entry

* Fri Mar 31 2000 Vincent Saugey <vince@mandrakesoft.com> 2.3BETA12-1mdk
- Update to 2.3BETA17
- Many change in specfile for spechelper
- Corrected groups

* Thu Jan 20 2000 Lenny Cartier <lenny@mandrakesoft.com>
- v2.3BETA12
- used srpm provided by Dara Hazeghi <dhazeghi@pacbell.net>

* Wed Jan 5 2000 Dara Hazeghi <dhazeghi@pacbell.net>
- Adapted for Mandrake

* Thu Dec 30 1999 Fyodor <fyodor@dhp.com>
- Updated description
- Eliminated source1 (nmapfe.desktop) directive and simply packaged it with Nmap
- Fixed nmap distribution URL (source0)
- Added this .rpm to base Nmap distribution

* Mon Dec 13 1999 Tim Powers <timp@redhat.com>
- based on origional spec file from
	http://www.insecure.org/nmap/index.html#download
- general cleanups, removed lots of commenrts since it made the spec hard to
	read
- changed group to Applications/System
- quiet setup
- no need to create dirs in the install section, "make
	prefix=$RPM_BUILD_ROOT&{prefix} install" does this.
- using defined %{prefix}, %{version} etc. for easier/quicker maint.
- added docs
- gzip man pages
- strip after files have been installed into buildroot
- created separate package for the frontend so that Gtk+ isn't needed for the
	CLI nmap 
- not using -f in files section anymore, no need for it since there aren't that
	many files/dirs
- added desktop entry for gnome

* Sun Jan 10 1999 Fyodor <fyodor@dhp.com>
- Merged in spec file sent in by Ian Macdonald <ianmacd@xs4all.nl>

* Tue Dec 29 1998 Fyodor <fyodor@dhp.com>
- Made some changes, and merged in another .spec file sent in
  by Oren Tirosh <oren@hishome.net>

* Mon Dec 21 1998 Riku Meskanen <mesrik@cc.jyu.fi>
- initial build for RH 5.x

