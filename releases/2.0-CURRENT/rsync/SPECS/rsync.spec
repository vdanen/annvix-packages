#
# spec file for package rsync
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rsync
%define version		2.6.8
%define release		%_revrel

Summary:	A program for synchronizing files over a network
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/File transfer
URL:		http://rsync.samba.org/
Source:		http://rsync.samba.org/ftp/rsync/%{name}-%{version}.tar.gz
Source1:	rsync.html
Source2:	rsyncd.conf.html
Source4:	http://rsync.samba.org/ftp/rsync/%{name}-%{version}.tar.gz.asc
Source5:	rsync.run
Source6:	rsync-log.run
Source7:	07_rsync.afterboot

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	popt-devel

Requires:	ipsvd
Requires(post):	afterboot, rpm-helper, ipsvd
Requires(postun): afterboot
Requires(preun): afterboot, rpm-helper

%description
Rsync uses a quick and reliable algorithm to very quickly bring
remote and host files into sync.  Rsync is fast because it just
sends the differences in the files over the network (instead of
sending the complete files). Rsync is often used as a very powerful
mirroring process or just as a more capable replacement for the
rcp command.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q


%build
%serverbuild
rm -f config.h
%configure2_5x

# hack around bug in rsync configure.in
#echo '#define HAVE_INET_NTOP 1' >> config.h
#echo '#define HAVE_INET_PTON 1' >> config.h

%make


%check
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/{man1,man5}}

%makeinstall
install -m 0644 %{SOURCE1} %{SOURCE2} .
mkdir -p %{buildroot}%{_srvdir}/rsync/{log,peers,env}
install -m 0740 %{SOURCE5} %{buildroot}%{_srvdir}/rsync/run
install -m 0740 %{SOURCE6} %{buildroot}%{_srvdir}/rsync/log/run
touch %{buildroot}%{_srvdir}/rsync/peers/0
chmod 0640 %{buildroot}%{_srvdir}/rsync/peers/0

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE7} %{buildroot}%{_datadir}/afterboot/07_rsync

echo "873" >%{buildroot}%{_srvdir}/rsync/env/PORT


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
if [ -d /var/log/supervise/rsync -a ! -d /var/log/service/rsync ]; then
    mv /var/log/supervise/rsync /var/log/service/
fi
%_post_srv rsync
%_mkafterboot
pushd %{_srvdir}/rsync >/dev/null 2>&1
    ipsvd-cdb peers.cdb peers.cdb.tmp peers/
popd


%preun
%_preun_srv rsync

%postun
%_mkafterboot


%files
%defattr(-,root,root)
%{_bindir}/rsync
%dir %attr(0750,root,admin) %{_srvdir}/rsync
%dir %attr(0750,root,admin) %{_srvdir}/rsync/log
%dir %attr(0750,root,admin) %{_srvdir}/rsync/peers
%dir %attr(0750,root,admin) %{_srvdir}/rsync/env
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/rsync/run
%config(noreplace) %attr(0740,root,admin) %{_srvdir}/rsync/log/run
%config(noreplace) %attr(0640,root,admin)%{_srvdir}/rsync/peers/0
%config(noreplace) %attr(0640,root,admin)%{_srvdir}/rsync/env/PORT
%{_mandir}/man1/rsync.1*
%{_mandir}/man5/rsyncd.conf.5*
%{_datadir}/afterboot/07_rsync

%files doc
%defattr(-,root,root)
%doc tech_report.tex README COPYING *html


%changelog
* Sat Jun 17 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.8
- 2.6.8
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.6
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.6.6
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.6-3avx
- execline for runscript
- env dirs
- compile peers.cdb in %%post

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.6-2avx
- s/supervise/service/ in log/run

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.6-1avx
- 2.6.6
- drop all patches; P1 not needed anymore, P0 was for draksync which
  we obviously don't ship
- use execlineb for run scripts
- move logdir to /var/log/service/rsync
- run scripts are now considered config files and are not replaceable

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.3-4avx
- fix perms on run scripts

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.3-3avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.3-2avx
- rebuild

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.6.3-1avx
- 2.6.3
- use logger for logging
- drop P2; no longer needed

* Fri Oct 08 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.2-6avx
- switch from tcpserver to tcpsvd
- Requires: ipsvd
- add the /service/rsync/peers directory to, by default, allow all
  connections
- add afterboot snippet

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.2-5avx
- update run scripts

* Fri Sep 03 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.2-4avx
- P2: security fix for CAN-2004-0792

* Wed Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.2-3avx
- remove xinetd support

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.6.2-2avx
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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
