#
# spec file for package traceroute
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		traceroute
%define version		1.4a12
%define release		%_revrel

Summary:	Traces the route taken by packets over a TCP/IP network
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Monitoring
URL:		http://www.chiark.greenend.org.uk/ucgi/~richard/cvsweb/debfix/packages/traceroute/
Source:		ftp://ftp.ee.lbl.gov/traceroute-%{version}.tar.bz2
Patch1:		traceroute-1.4a5-secfix.patch
Patch3:		traceroute-1.4a5-autoroute.patch
Patch4:		traceroute-1.4a5-autoroute2.patch
Patch5:		traceroute-1.4a5-unaligned.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The traceroute utility displays the route used by IP packets on their
way to a specified network (or Internet) host.  Traceroute displays
the IP number and host name (if possible) of the machines along the
route taken by the packets.  Traceroute is used as a network debugging
tool.  If you're having network connectivity problems, traceroute will
show you where the trouble is coming from along the route.


%prep
%setup -q
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0


%build
export RPM_OPT_FLAGS="%{optflags} -DHAVE_IFF_LOOPBACK -DUSE_KERNEL_ROUTING_TABLE"
%configure
make 


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_sbindir},%{_mandir}/man8}

install traceroute %{buildroot}%{_sbindir}
cp traceroute.8 %{buildroot}%{_mandir}/man8


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(0755,root,bin) %{_sbindir}/traceroute
%{_mandir}/man8/traceroute.8*


%changelog
* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4a12
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4a12
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.4a12
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Aug 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4a12-9avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.4a12-8avx
- rebuild

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.4a12-7avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.4a12-6sls
- minor spec cleanups
- remove %%prefix

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 1.4a12-5sls
- OpenSLS build
- tidy spec
- remove suid bit

* Fri Jul 18 2003 Warly <warly@mandrakesoft.com> 1.4a12-4mdk
- rebuild

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.4a12-3mdk
- Automated rebuild in gcc3.1 environment

* Tue Dec 11 2001 Warly <warly@mandrakesoft.com> 1.4a12-2mdk
- url tag

* Fri Nov  2 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.4a12-1mdk
- New version.
- Removed patches 0, 2, 6.

* Tue Oct 03 2000 Francis Galiegue <fg@mandrakesoft.com> 1.4a5-14mdk
- Applied security fix patch

* Mon Jul 31 2000 Francis Galiegue <fg@mandrakesoft.com> 1.4a5-13mdk
- More macros
- let spec-helper do its job

* Fri Jul 21 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.4a5-12mdk
- BM, macros

* Wed Apr 05 2000 John Buswell <johnb@mandrakesoft.com> 1.4a5-11mdk
- fix vendor tag

* Thu Mar 30 2000 John Buswell <johnb@mandrakesoft.com> 1.4a5-10mdk
- fix groups
- spec-helper

* Wed Jan 12 2000 Pixel <pixel@mandrakesoft.com>
- fix build as non-root (removed call to make install, done by hand)

* Thu Nov  4 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix wrong patch :-\.

* Wed Jul 21 1999 Gregus <gregus@etudiant.net>
- Add fr

* Tue Jul 12 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- bzip2 manpage

* Thu Jul  8 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Merging with RH patchs :
    * avoid unaligned traps writing into the output data area.
    * fix segfault when host cannot be reached through if (#2819)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- strip binaries.

* Sun Feb 07 1999 Preston Brown <pbrown@redhat.com>
- patch added to automatically determine interface to route through

* Fri Jan 22 1999 Jeff Johnson <jbj@redhat.com>
- use %configure
- fix 64 bit problem on alpha (#919)

* Wed Jan 13 1999 Bill Nottingham <notting@redhat.com>
- configure fix for arm

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Dec 16 1997 Cristian Gafton <gafton@redhat.com>
- updated the security patch (ouch!). Without the glibc fix, it could be
  worthless anyway

* Sat Dec 13 1997 Cristian Gafton <gafton@redhat.com>
- added a security patch fix

* Wed Oct 22 1997 Erik Troan <ewt@redhat.com>
- added fix from Christopher Seawood

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- updated to 1.4a5 for security fixes; release 1 is for RH 4.2, release 2
  is against glibc

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc
