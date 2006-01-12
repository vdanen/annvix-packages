#
# spec file for package cvs
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		cvs
%define version		1.11.20
%define release		%_revrel

%define _requires_exceptions tcsh

Summary:	A version control system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.cvshome.org/
Source: 	ftp://ftp.cvshome.org/pub/cvs-%{version}/cvs-%{version}.tar.bz2
Source1: 	cvspserver
Source2: 	cvs.conf
Source3: 	ftp://ftp.cvshome.org/pub/cvs-%{version}/cvs-%{version}.tar.bz2.sig
Source4:	cvs.run
Source5:	cvs-log.run
Source6:	06_cvspserver.afterboot
Patch0:		cvs-1.11.19-mdk-varargs.patch
Patch4: 	cvs-1.11.19-zlib.patch
Patch6: 	cvs-1.11.15-errno.patch
Patch8:		cvs-1.11-ssh.patch
Patch11:	cvs-1.11.1-newline.patch
Patch12:	cvs-1.11.4-first-login.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5, texinfo, zlib-devel, krb5-devel

Requires:	ipsvd
Requires(post):	info-install, afterboot, rpm-helper, ipsvd
Requires(preun): info-install, rpm-helper
Requires(postun): afterboot

%description
CVS means Concurrent Version System; it is a version control
system which can record the history of your files (usually,
but not always, source code). CVS only stores the differences
between versions, instead of every version of every file
you've ever created. CVS also keeps a log of who, when and
why changes occurred, among other aspects.

CVS is very helpful for managing releases and controlling
the concurrent editing of source files among multiple
authors. Instead of providing version control for a
collection of files in a single directory, CVS provides
version control for a hierarchical collection of
directories consisting of revision controlled files.

These directories and files can then be combined together
to form a software release.


%prep
%setup -q
%patch0 -p1 -b .varargs
%patch4 -p1 -b .zlib
%patch6 -p1 -b .errno
%patch8 -p1 -b .ssh
%patch11 -p1 -b .newline
%patch12 -p1 -b .first-login


%build
export SENDMAIL="%{_sbindir}/sendmail"

%serverbuild
%configure2_5x --with-tmpdir=/tmp

%make

make -C doc info


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

bzip2 -f doc/*.ps

%makeinstall

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/cvs
install -m 0755 %{SOURCE1} %{buildroot}%{_sbindir}
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/cvs

# get rid of "no -f" so we don't have a Dep on this nonexistant interpretter
perl -pi -e 's/no -f/\/bin\/sh/g' %{buildroot}%{_datadir}/cvs/contrib/sccs2rcs

mkdir -p %{buildroot}%{_srvdir}/cvspserver/{log,peers,env}
install -m 0740 %{SOURCE4} %{buildroot}%{_srvdir}/cvspserver/run
install -m 0740 %{SOURCE5} %{buildroot}%{_srvdir}/cvspserver/log/run
touch %{buildroot}%{_srvdir}/cvspserver/peers/0
chmod 0640 %{buildroot}%{_srvdir}/cvspserver/peers/0

echo "2401" >%{buildroot}%{_srvdir}/cvspserver/env/PORT

mkdir -p %{buildroot}%{_datadir}/afterboot
install -m 0644 %{SOURCE6} %{buildroot}%{_datadir}/afterboot/06_cvspserver


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
if [ -d /var/log/supervise/cvspserver -a ! -d /var/log/service/cvspserver ]; then
    mv /var/log/supervise/cvspserver /var/log/service/
fi
%_post_srv cvspserver
%_install_info %{name}.info
%_install_info cvsclient.info
%_mkafterboot
pushd %{_srvdir}/cvspserver >/dev/null 2>&1
    ipsvd-cdb peers.cdb peers.cdb.tmp peers/
popd >/dev/null 2>&1


%preun
%_preun_srv cvspserver
%_remove_install_info %{name}.info
%_remove_install_info cvsclient.info

%postun
%_mkafterboot


%files
%defattr(-,root,root)
%doc BUGS FAQ MINOR-BUGS NEWS PROJECTS TODO README
%dir %{_sysconfdir}/cvs
%config(noreplace) %{_sysconfdir}/cvs/cvs.conf
%{_bindir}/cvs
%{_bindir}/cvsbug
%{_bindir}/rcs2log
%{_sbindir}/cvspserver
%{_mandir}/man1/cvs.1*
%{_mandir}/man5/cvs.5*
%{_mandir}/man8/cvsbug.8*
%{_infodir}/cvs*
%{_datadir}/cvs
%dir %attr(0750,root,admin) %{_srvdir}/cvspserver
%dir %attr(0750,root,admin) %{_srvdir}/cvspserver/log
%dir %attr(0750,root,admin) %{_srvdir}/cvspserver/peers
%dir %attr(0750,root,admin) %{_srvdir}/cvspserver/env
%attr(0740,root,admin) %{_srvdir}/cvspserver/run
%attr(0740,root,admin) %{_srvdir}/cvspserver/log/run
%attr(0640,root,admin) %{_srvdir}/cvspserver/peers/0
%attr(0640,root,admin) %{_srvdir}/cvspserver/env/PORT
%{_datadir}/afterboot/06_cvspserver


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Tue Sep 27 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.20-3avx
- grab defaults from the tcpsvd environment

* Sun Sep 25 2005 Sean P. Thomas <spt-at-build.annvix.org> 1.11.20-2avx
- use execlineb for run script, and created an envdir.
- fix requires (vdanen)
- supplied default env files (vdanen)
- pre-compile a peers.cdb in %%post (vdanen)

* Sat Sep 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.20-1avx
- 1.11.20
- use execlineb for run scripts
- move logdir to /var/log/service/cvspserver
- run scripts are now considered config files and are not replaceable
- P0: varags fixes for x86_64 (potential, but harmless here) (gbeauchesne)
- drop P13; merged upstream

* Fri Aug 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.19-6avx
- fix perms on run scripts

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.19-5avx
- bootstrap build (new gcc, new glibc)
- remove postscript docs

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.19-4avx
- rebuild

* Thu May 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.19-3avx
- P13: security fix for CAN-2005-0753

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.19-2avx
- no need to lose our cvs.conf; put it back

* Thu Mar 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.19-1avx
- 1.11.19
- use logger for logging
- remove broken P14 (mdk bug #13118) (flepied)

* Tue Jan 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.11.17-5avx
- update the run script; exec tcpsvd so that it will actually stop
  when we want it to
- service name is cvspserver, not cvs

* Tue Oct 05 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.11.17-4avx
- switch from tcpserver to tcpsvd
- Requires: ipsvd
- add the /service/cvspserver/peers directory to, by default, allow
  all connections
- add afterboot snippet

* Mon Sep 20 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.11.17-3avx
- updated run scripts

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.11.17-2avx
- Annvix build
- require packages not files

* Tue Jun 15 2004 Vincent Danen <vdanen@opensls.org> 1.11.17-1sls
- 1.11.17 (security fixes for CAN-2004-0414, CAN-2004-0146, CAN-2004-0417,
  CAN-2004-0418, CAN-2004-0396)
- update P6, P14
- personalize cvs.conf

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 1.11.11-1sls
- 1.11.11
- remove %%build_opensls macro
- supervise macros
- minor spec cleanups
- use %%_post_srv and %%_preun_srv
- merge with 1.11.11-1mdk:
  - DIRM: /etc/cvs (flepied)
  - add localid patch to be able to access xfree86 cvs repository cleanly
    (flepied)

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 1.11.10-2sls
- put supervise run scripts in if %%build_opensls; remove xinetd support

* Tue Dec 09 2003 Vincent Danen <vdanen@opensls.org> 1.11.10-1sls
- OpenSLS build
- tidy spec
- pass tmpdir to configure
- fix a sccs2rcs script in contrib scripts which was making a Req on "no"

* Fri Dec  5 2003 Stew Benedict <sbenedict@mandrakesoft.com> 1.11.10-0.1.92mdk
- security update: drop patch0, patch14 (merged upstream), rework patch6

* Fri Jul 25 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.11.6-3mdk
- rebuild against new kerberos

* Tue Jul 22 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.11.6-2mdk
- don't require tcsh

* Wed Jun  4 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.11.6-1mdk
- 1.11.6

* Tue Jan 21 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.11.5-1mdk
- 1.11.5

* Mon Jan 20 2003 Vincent Danen <vdanen@mandrakesoft.com> 1.11.4-2mdk
- security patch to fix double free() and insecure Update-prog/Checkin-prog
  commands

* Sat Dec 28 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.11.4-1mdk
- 1.11.4

* Thu Dec  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.11.2-3mdk
- corrected behaviour with empty comment

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.11.2-2mdk
- compress postcript documentation

* Wed May  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.11.2-1mdk
- 1.11.2

* Wed Feb 27 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.11.1-10mdk
- libsafe support in cvspserver
- recompiled with %%serverbuild

* Thu Nov 15 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.11.1-9mdk
- fix a bug when the cvsroot is a symlink and using LockDir.

* Thu Nov  8 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.11.1-8mdk
- Build against external zlib; do not build in-source zlib.
- Move aclocal/automake/autoconf/autoheader to %%prep stage

* Sun Oct 28 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.11.1-7mdk
- corrected empty files.

* Sun Sep  9 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.11.1-6mdk
- don't exit on error when ~/.cvspass doesn't exist on first cvs login (#4875).

* Sun Sep  9 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.11.1-5mdk
- correct cvspserver to work with xinetd startup script that removes $HOME.

* Fri Aug 10 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.11.1-4mdk
- compile with kerberos support enabled.

* Tue Jul 10 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.11.1-3mdk
- add a blank line at the beginning of the file created to edit the changes
describing a commit per Pixel request.

* Wed Jun 27 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.11.1-2mdk
- applied patch1 from ftp.cvshome.org (read only access fix)

* Fri Apr 27 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.11.1-1mdk
- 1.11.1

* Tue Mar  6 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.11-5mdk
- apply security patch from rh.
- use ssh by default.

* Fri Jan 12 2001 David BAUDENS <baudens@mandrakesoft.com> 1.11-4mdk
- BuildRequires: texinfo

* Thu Jan 04 2001 Vincent Danen <vdanen@mandrakesoft.com> 1.11-3mdk
- fix cvspserver so that it unsets HOME which prevents pserver from 
  starting

* Wed Dec 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.11-2mdk
- Add xinetd support.

* Mon Oct 16 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.11-1mdk
- 1.11

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.10.8-6mdk
- automatically added BuildRequires

* Sun Jul 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.10.8-5mdk
- Fix postscripts.

* Fri Jul 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.10.8-4mdk
- Add -f to cvspserver (thnks Thierry SAURA).

* Thu Jul 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.10.8-3mdk
- BM.
- Compile with zlib of the system not of cvs.
- Macroszifications.
- Merge rh patches.

* Sat Jul 08 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 1.10.8-2mdk
- fixed makeinstall problem

* Tue Mar 28 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.10.8-1mdk
- 1.10.8
- created %{_sbindir}/cvspserver to launch cvs pserver according to
%{_sysconfdir}/cvs/cvs.conf.

* Fri Mar 24 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.10.7-5mdk
- group fix.

* Thu Nov 11 1999 Jeff Garzik <jgarzik@mandrakesoft.com>
- ...but keep experimental mmap patch in cooker

* Thu Nov 11 1999 Jeff Garzik <jgarzik@mandrakesoft.com>
- Build release, without experimental mmap patch

* Mon Oct 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add patch from Jeff <jgarzik@mandrakesoft.com> :
	src/client.c, src/import.c, src/filesubr.c, src/logmsg.c, src/server.c:
	* mmap support for local file read
	configure.in:
	* AC_PROG_CC handles AC_C_CROSS in modern autoconf, remove it
	* check for mmap()
	src/add.c, src/buffer.c, src/lock.c, src/modules.c, src/rcs.c,
	src/update.c, src/server.c:
	* zero variable to avoid [common, but sometimes spurious] compiler
	warning about an uninitialized variable
	src/client.c:
	* remove BROKEN_READWRITE_CONVERSION, dead feature.  The code used
	fread() to read file data not fgets(), so linefeeds were never
	translated anyway.
	src/cvs.h:
	* conditionally include sys/mman.h for mmap
	src/filesubr.c:
	* mmap support for local file read
	* optimize compare case where file sizes differ (do not open files at
	all)
	src/server.c:
	* update read_and_gzip() call
	src/server.h:
	* update read_and_gzip() prototype
	src/zlib.c:
	* update read_and_gzip() to optionally support reading from an input
	buffer instead of a file
	zlib/*.c:
	* const-ify input data pointer.  smart compilers can use this to further
	optimize
	

* Mon Aug 16 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 1.10.7

* Tue Jul 20 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- add french description from Gregus <gregus@etudiant.net>

* Tue Jul 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Merging with Redhat :
	* Wed Jul 14 1999 Jim Kingdon <http://developer.redhat.com>
	- add the patch to make 1.10.6 usable
  	(http://www.cyclic.com/cvs/dev-known.html).
	

* Wed May 19 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- Fix several .spec bugs
- Update to 1.10.6

* Tue May 18 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Bzipped info files.

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptations

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- updated text in spec file.

* Mon Feb 22 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.10.5.

* Tue Feb  2 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.10.4.

* Tue Oct 20 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.3.

* Mon Sep 28 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.2.

* Wed Sep 23 1998 Jeff Johnson <jbj@redhat.com>
- remove trailing characters from rcs2log mktemp args

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.1

* Mon Aug 31 1998 Jeff Johnson <jbj@redhat.com>
- fix race conditions in cvsbug/rcs2log

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.10.

* Wed Aug 12 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.9.30.

* Mon Jun 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr

* Mon Jun  8 1998 Jeff Johnson <jbj@redhat.com>
- build root
- update to 1.9.28

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Oct 29 1997 Otto Hammersmith <otto@redhat.com>
- added install-info stuff
- added changelog section
