%define name	rsync
%define version	2.6.2
%define release	4avx

Summary:	A program for synchronizing files over a network.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/File transfer
URL:		http://rsync.samba.org/
Source:		ftp://rsync.samba.org/pub/rsync/%name-%version.tar.gz
Source1:	rsync.html
Source2:	rsyncd.conf.html
Source4:	ftp://rsync.samba.org/pub/rsync/%name-%version.tar.gz.sig
Source5:	rsync.run
Source6:	rsync-log.run
Patch0:		rsync-2.5.4-draksync.patch.bz2
Patch1:		rsync-2.6.0-nogroup.patch.bz2
Patch2:		rsync-2.6.0-path-sanitize.patch.bz2

BuildRoot:	%_tmppath/%name-root
BuildRequires:	popt-devel

%description
Rsync uses a quick and reliable algorithm to very quickly bring
remote and host files into sync.  Rsync is fast because it just
sends the differences in the files over the network (instead of
sending the complete files). Rsync is often used as a very powerful
mirroring process or just as a more capable replacement for the
rcp command.  A technical report which describes the rsync algorithm
is included in this package.

Install rsync if you need a powerful mirroring program.

%prep
%setup -q
%patch0 -p1 -b .draksync
%patch1 -p1 -b .nogroup
%patch2 -p1 -b .can-2004-0792

%build
%serverbuild
rm -f config.h
%configure2_5x

# hack around bug in rsync configure.in
echo '#define HAVE_INET_NTOP 1' >> config.h
echo '#define HAVE_INET_PTON 1' >> config.h

%make

make test

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT{%_bindir,%_mandir/{man1,man5}}

%makeinstall
install -m644 %SOURCE1 %SOURCE2 .
mkdir -p %{buildroot}%{_srvdir}/rsync/log
install -m 0755 %{SOURCE5} %{buildroot}%{_srvdir}/rsync/run
install -m 0755 %{SOURCE6} %{buildroot}%{_srvdir}/rsync/log/run
mkdir -p %{buildroot}%{_srvlogdir}/rsync

%post
%_post_srv rsync

%preun
%_preun_srv rsync

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc tech_report.tex README COPYING *html
%_bindir/rsync
%dir %{_srvdir}/rsync
%dir %{_srvdir}/rsync/log
%dir %attr(0750,nobody,nogroup) %{_srvlogdir}/rsync
%{_srvdir}/rsync/run
%{_srvdir}/rsync/log/run
%_mandir/man1/rsync.1*
%_mandir/man5/rsyncd.conf.5*

%changelog
* Fri Sep 03 2004 Vincent Danen <vdanen@annvix.org> 2.6.2-4avx
- P2: security fix for CAN-2004-0792

* Wed Jun 22 2004 Vincent Danen <vdanen@annvix.org> 2.6.2-3avx
- remove xinetd support

* Mon Jun 21 2004 Vincent Danen <vdanen@annvix.org> 2.6.2-2avx
- Annvix build

* Mon May 10 2004 Vincent Danen <vdanen@opensls.org> 2.6.2-1sls
- 2.6.2 (security update for CAN-2004-0426)
- rediff P1

* Mon Dec 29 2003 Vincent Danen <vdanen@opensls.org> 2.5.7-3sls
- minor spec cleanups
- remove %%build_opensls macro
- srv macros

* Mon Dec 29 2003 Vincent Danen <vdanen@opensls.org> 2.5.7-3sls
- put supervise scripts in here if %%build_opensls

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 2.5.7-2sls
- OpenSLS build
- tidy spec

* Thu Dec  4 2003 Warly <warly@mandrakesoft.com> 2.5.7-1mdk
- new version (security fix)

* Wed Aug 20 2003 Warly <warly@mandrakesoft.com> 2.5.6-3mdk
- replace nobody group with nogroup

* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.5.6-2mdk
- rebuild
- macroize

* Thu Feb  6 2003 Warly <warly@mandrakesoft.com> 2.5.6-1mdk
- new version

* Sat Aug 10 2002 Pixel <pixel@mandrakesoft.com> 2.5.5-5mdk
- rsync.xinetd: fix description (thanks to allen <aef@prismnet.com>)

* Sun Jun 16 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.5.5-4mdk
- Fix chgrp.test (make test should now finally work).¢

* Sat Jun 15 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.5.5-3mdk
- Fix testsuite. Some tests will incorrectly fail if we don't already have
  an rsync binary installed on the system.

* Tue May 07 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5.5-2mdk
- Automated rebuild in gcc3.1 environment

* Tue Apr 23 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.5.5-1mdk
- new release
- spec simplifications

* Thu Mar 14 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.5.4-2mdk
- draksync patch

* Tue Mar 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.5.4-1mdk
- 2.5.4 (aka fix the security fix)

* Mon Mar 11 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.5.3-1mdk
- 2.5.3

* Wed Feb 27 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.5.2-4mdk
- recompiled with %%serverbuild

* Sat Feb  9 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.5.2-3mdk
- back to internal zlib as it's a non compatible one.

* Fri Feb  8 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.5.2-2mdk
- use dynamic zlib

* Sun Jan 27 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.5.2-1mdk
- 2.5.2

* Tue Jan  8 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.5.1-1mdk
- 2.5.1

* Tue Dec  4 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.5.0-2mdk
- fix build on alpha (and perhaps other platforms) by working
  around bug in configure.in that causes HAVE_INET_NTOP not to be 
  defined.
- do not pass CCOPTFLAGS to make
- use %%make
- use %%configure2_5x to pass --build/--host/--target

* Mon Dec  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.5.0-1mdk
- 2.5.0

* Wed Oct 17 2001 Warly <warly@mandrakesoft.com> 2.4.6-4mdk
- rpmlint fixes

* Sun Oct 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.6-3mdk
- Add xinetd support.

* Sat Sep 09 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.6-2mdk
- do nothing really but rebuild, to fix rsync segfault breakage 
  (David Baudens).
  
* Thu Sep 07 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.6-1mdk
- s|2.4.5|2.4.6|;

* Sun Aug 20 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.5-1mdk
- a new and shiny version.

* Sat Jul 29 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.4-1mdk
- new verison
- rebuild for the BM
- remove stripping of binary (doh!!)

* Mon Jul 10 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 2.4.3-2mdk
- makeinstall macro
- macroszifications

* Fri May 26 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.4.3-1mdk
- 2.4.3

* Tue Mar 21 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.4.1-2mdk
- Fix Group.

* Tue Feb 08 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 2.4.1-1mdk
- updated to 2.4.1

* Thu Nov 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.3.1.
- Add some documentation.

* Thu Nov 04 1999 John Buswell <johnb@mandrakesoft.com>
- Build Release

* Wed May 05 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Wed Apr 07 1999 Bill Nottingham <notting@redhat.com>
- update to 2.3.1.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Tue Mar 16 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.3.0.

* Sat Mar 13 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.3.0 beta.

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- update to 2.2.1

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.1.1

* Mon Aug 17 1998 Erik Troan <ewt@redhat.com>
- updated to 2.1.0

* Thu Aug 06 1998 Erik Troan <ewt@redhat.com>
- buildrooted and attr-rophied
- removed tech-report.ps; the .tex should be good enough

* Mon Aug 25 1997 John A. Martin <jam@jamux.com>
- Built 1.6.3-2 after finding no rsync-1.6.3-1.src.rpm although there
  was an ftp://ftp.redhat.com/pub/contrib/alpha/rsync-1.6.3-1.alpha.rpm
  showing no packager nor signature but giving 
  "Source RPM: rsync-1.6.3-1.src.rpm".
- Changes from 1.6.2-1 packaging: added '$RPM_OPT_FLAGS' to make, strip
  to '%build', removed '%prefix'.

* Thu Apr 10 1997 Michael De La Rue <miked@ed.ac.uk>
- rsync-1.6.2-1 packaged.  (This entry by jam to credit Michael for the
  previous package(s).)
