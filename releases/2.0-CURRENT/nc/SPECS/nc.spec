#
# spec file for package nc
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision        $Rev$
%define name            nc
%define version         1.10
%define release         %_revrel

Summary: 	Reads and writes data across network connections using TCP or UDP
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Networking/Other
URL:		http://www.vulnwatch.org/netcat/
Source0:	http://www.vulnwatch.org/netcat/nc110.tar.bz2
Source1: 	nc.1
Patch0: 	nc-1.10-arm.patch
Patch1: 	nc-1.10-resolv.patch
Patch2:		nc-1.10-posix_setjmp.patch
Patch3:		nc-1.10-nopunt.patch
Patch4:		nc-1.10-nosleep.patch
Patch5:		nc-1.10-single_verbose.patch
Patch6:		nc-1.10-use_getservbyport.patch
Patch7:		nc-1.10-read_overflow.patch
Patch8:		nc-1.10-inet_aton.patch
Patch9:		nc-1.10-udp_broadcast.patch
Patch10:	nc-1.10-quit.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}

Provides:	netcat = %{version}

%description
The nc package contains Netcat (the program is now netcat), a simple
utility for reading and writing data across network connections, using
the TCP or UDP protocols. Netcat is intended to be a reliable back-end
tool which can be used directly or easily driven by other programs and
scripts.  Netcat is also a feature-rich network debugging and exploration
tool, since it can create many different connections and has many
built-in capabilities.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -c -n nc -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1


%build
# Make linux is supported, but it makes a static binary. 
# don't build with -DGAPING_SECURITY_HOLE
%make CFLAGS="%{optflags}" \
      DFLAGS='-DLINUX' generic


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man1}

install -m 0755 nc %{buildroot}%{_bindir}
(cd %{buildroot}%{_bindir}; ln -s nc netcat)

install -m 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/nc
%{_bindir}/netcat
%{_mandir}/man1/nc.1*

%files doc
%defattr(-,root,root)
%doc README Changelog
%doc scripts


%changelog
* Sat Jul 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.10
- add -doc subpackage
- rebuild with gcc4

* Sat Feb 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.10
- first Annvix build
- major spec cleanups
- use the correct URL

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.10-20mdk
- Rebuild

* Fri Jun 17 2005 Olivier Blin <oblin@mandriva.com> 1.10-19mdk
- fix Summary ended with dot

* Fri Apr 02 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.10-18mdk
- fix url (#9355)

* Fri Aug 08 2003 Ben Reser <ben@reser.org> 1.10-17mdk
- Use debians patch to fix arm issue (which is better because
  it actually fixes the problem as opposed to just working 
  around it).  http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=56390
  Applied as patch 0 
- Applied posix_setjmp patch to fix multiple timeouts with glibc from 
  Debian.  http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=97583
  Applied as patch 2
- Applied no_punt patch from debian to get rid of the annoying punt
  output. http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=45669
  Applied as patch 3
- Applied no_sleep patch from debian to avoid the 1 second delay
  on a interupt. http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=45669
  Applied as patch 4
- Applied single_verbose patch to show "connection refused" messages
  without -v.  http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=65413
  Applied as patch 5
- Applied us_getservbyport patch to lookup services even if resolving
  hostnames with DNS is disabled. 
  http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=98902
  Applied as patch 6
- Applied read_overflow patch from debian/openbsd to avoid buffer overflow
  issue. http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=145801
  Applied as patch 7
- Applied UDP broadcast patch from NetBSD and inet_aton from debian
  http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=108182
  Applied as patche 8 & 9
- Applied quit patch from debian to allow netcat to quit on EOF.
  Also closes Mandrake bug 4529
  http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=45675
  Applied as patch 10
- Symlink %%{_bindir}/netcat to %%{_bindir}/nc
- Provide netcat for easier urpmi'ing
- Update man page to match debians.
- Remove %%ifarch for arm (not necessary with debians better patch)
- Built with GAPING_SECURITY_HOLE, since I agree with Debian it isn't
  a GAPING security hole added warning to description about it (borrowed
  from Debian)
- Added -DLINUX to the build to enable some of the debian patches
- Added -DTELNET to build to enable -t option.
- Macroized
- rm build root in %%install

* Tue Jun  3 2003 Damien Chaumette <dchaumette@mandrakesoft.com> 1.10-16mdk
- rebuild (fix rpmReadSignature failed)

* Wed Jul 11 2001 Yves Duret <yduret@mandrakesoft.com> 1.10-15mdk
- updated source and url tag
- rebuild

* Mon Apr  9 2001 Yves Duret <yduret@mandrakesoft.com>  1.10-14mdk
- renamed back nc to nc :)
- added the man page
- added %%ifarch arm (yes arm!)

* Tue Mar 27 2001 Yves Duret <yduret@mandrakesoft.com> 1.10-13mdk
- rename nc to netcat (conflict with nedit) : patch2

* Tue Mar 27 2001 Yves Duret <yduret@mandrakesoft.com> 1.10-12mdk
- fixed header for new glibc (res_init()) : patch1

* Wed Dec 20 2000 Yves Duret <yduret@mandrakesoft.com> 1.10-11mdk
- macros

* Fri Aug 04 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.10-10mdk
- rebuild with macros

* Tue Apr 11 2000 Maurizio De Cecco <maurizio@mandrakesoft.com>
- Fixed Distribution name

* Mon Apr 10 2000 Maurizio De Cecco  <maurizio@mandrakesoft.com>
- Fixed error in Group 

* Thu Mar 16 2000 Maurizio De Cecco  <maurizio@mandrakesoft.com>
- Adapted to the new Group structure

* Wed Nov 10 1999 Jerome Martin <jerome@mandrakesoft.com>
- Build for new environment

* Wed May 05 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- make it build on the arm

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0
