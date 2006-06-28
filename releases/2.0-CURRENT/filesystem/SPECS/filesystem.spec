#
# spec file for package filesystem
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		filesystem
%define version		2.1.6
%define release		%_revrel

Summary:	The basic directory layout for an Annvix system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Base
URL:		http://annvix.org/

Buildroot:	%{_buildroot}/%{name}-%{version}

Requires:	setup

%description
The filesystem package is one of the basic packages that is installed on
an Annvix system.  Filesystem  contains the basic directory layout
for a Linux operating system, including the correct permissions for the
directories.


%prep


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir %{buildroot}

# add /sys when we move to kernel 2.6
pushd %{buildroot}
    mkdir -p media bin boot sys \
        etc/{profile.d,skel,security,ssl,sysconfig/env} \
        home initrd lib/modules %{_lib} mnt media opt proc root sbin srv tmp \
        usr/{bin,etc,include,%{_lib}/gcc-lib,lib/gcc-lib,local/{bin,doc,etc,lib,%{_lib},sbin,src,share/{man/man{1,2,3,4,5,6,7,8,9,n},info},libexec,include,},sbin,share/{doc,info,man/man{1,2,3,4,5,6,7,8,9,n},misc,empty,pixmaps},src,X11R6/{bin,include,lib,%{_lib},man}} \
        var/{empty,lib/misc,local,lock/subsys,log/service,mail,nis,preserve,run,service,spool,tmp,cache/man,opt,yp}

    ln -snf ../X11R6/bin usr/bin/X11
    ln -snf ../X11R6/lib/X11 usr/lib/X11
    ln -snf ../X11R6/%{_lib}/X11 usr/%{_lib}/X11
    ln -snf ../mail var/spool/mail
    ln -snf ../var/tmp usr/tmp
    ln -snf lib/misc var/db
popd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(0755,root,root)
/bin
/boot
%dir /etc
/etc/profile.d
/etc/security
/etc/sysconfig
%attr(0750,root,admin) /etc/sysconfig/env
/etc/ssl
/home
/initrd
/lib
%if %{_lib} != lib
/%{_lib}
%endif
%dir /mnt
%dir /media
%dir /opt
%attr(555,root,root) /proc
%attr(555,root,root) /sys
%attr(750,root,root) /root
/sbin
%attr(1777,root,root) /tmp
/usr
%dir /var
/var/db
%dir %attr(0755,root,root) /var/empty
/var/lib
/var/local
%dir %attr(775,root,root) /var/lock
%attr(755,root,root) /var/lock/subsys
/var/cache
/var/log
%attr(0700,logger,logger) /var/log/service
/var/nis
/var/opt
/var/preserve
/var/run
%dir /var/spool
/var/spool/mail
%dir %attr(1755,root,root) %{_srvdir}
%attr(775,root,mail) /var/mail
%attr(1777,root,root) /var/tmp
/var/yp
/srv


%changelog
* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.6
- add /sys for sysfs

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5
- get rid of /var/spool/lpd; we don't ship any printer software
- get rid of /var/log/supervise; it's all /var/log/service now

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5
- Clean rebuild

* Wed Jan 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5
- Obfuscate email addresses and new tagging
- Uncompress patches

* Mon Aug 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5-5avx
- add /etc/sysconfig/env
- add /var/log/service (NOTE: remove /var/log/supervise when everything
  is switched over)

* Fri Aug 19 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5-4avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.1.5-3avx
- bootstrap build

* Thu Mar 03 2005 Vincent Danen <vdanen@opensls.org> 2.1.5-2avx
- own /var/log/supervise

* Tue Sep 14 2004 Vincent Danen <vdanen@opensls.org> 2.1.5-1avx
- 2.1.5
- remove compatability upgrade scripts
- follow mdk method of spec simplification
- make it lib64 aware (so no more noarch)
- switched to direct build of the directories; drop S0
- add /etc/ssl, /etc/sysconfig, and /var/empty

* Fri Jun 25 2004 Vincent Danen <vdanen@opensls.org> 2.1.4-4avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.1.4-3sls
- grrr... use some %%pre/%%post scripts to solve moving the symlinks around

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.1.4-2sls
- include /srv in the package

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 2.1.4-1sls
- 2.1.4: the great FHS cleanup:
  - remove /etc/xinetd.d, /usr/local/games, /usr/games, /var/games,
    /var/lib/games, /usr/lib/games
  - add /var/service
  - make /var/spool/mail a symlink to /var/mail rather than the other
    way around
  - make /srv
  - make /var/db a symlink to /var/lib/misc
  - create /media/{cdrom,floppy}

* Thu Mar 04 2004 Vincent Danen <vdanen@opensls.org> 2.1.3-13sls
- don't include /etc/xinet.d since we don't ship it or /usr/share/games
  since we don't need it

* Mon Dec 29 2003 Vincent Danen <vdanen@opensls.org> 2.1.3-12sls
- add /var/service so we don't need to prereq supervise-scripts or
  daemontools for every package

* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 2.1.3-11sls
- OpenSLS build
- tidy spec

* Tue Jul  8 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.1.3-10mdk
- own /etc/security and /etc/profile.d too

* Tue Jul  8 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.1.3-9mdk
- own /usr/share/games

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.1.3-8mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Mon Jul  8 2002 Pixel <pixel@mandrakesoft.com> 2.1.3-7mdk
- also remove /mnt/disk
- ensure /mnt/{disk,cdrom,floppy} directories are created when upgrading (via trigger)

* Sun Jul  7 2002 Pixel <pixel@mandrakesoft.com> 2.1.3-6mdk
- remove /mnt/floppy and /mnt/cdrom since:
  - they are created by drakx
  - not everybody has a cdrom or a floppy drive
  - it doesn't handle dvd, multiple cdroms...
  - breaks upgrades when supermounted 

* Wed Jul  3 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.1.3-5mdk
- added /etc/ssl

* Tue Dec  4 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-4mdk
- Make a till happy make /var/spool/lpd like he want.

* Fri Sep 14 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-3mdk
- Rebuild.

* Fri Aug 10 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-2mdk
- Add /var/cache/man

* Mon Aug  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1.3-1mdk
- 2.1.3.

* Thu Aug  2 2001 Stew Benedict <sbenedict@mandrakesoft.com> 2.0.8-2mdk
- add /usr/local/include, /usr/local/share for FHS

* Fri Jun 15 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.8-1mdk
- 2.0.8.

* Tue Mar 27 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.7-2mdk
- clean spec

* Thu Mar  8 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.7-1mdk
- 2.0.7 (add /usr/share/empty).

* Mon Oct  2 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.0.6-2mdk
- Move /usr/dict to /usr/share/dict (thnks: flepied).

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.0.6-1mdk
- merge in RH patches
- For FHS compliance, make the BM (Big Move) (hide children & women :-) ) :
 add /usr/share/{info,man,doc}, remove /usr/{doc,man,info}
- rename /etc/xinet.d to /etc/xinetd.d

* Fri Jul 14 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.5-3mdk
- Add /etc/xinetd.d/

* Wed Mar 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.3.5-2mdk
- Add /mnt/disk.
- Upgrade groups.

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add /opt, /var/state, /var/cache for FHS lords.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- add de locale

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- don't carry X11R6.1 as directory on sparc.
- /var/tmp/build root (#811)

* Wed Jan 13 1999 Preston Brown <pbrown@redhat.com>
- font directory didn't belong, which I previously misunderstood.  removed.

* Fri Nov 13 1998 Preston Brown <pbrown@redhat.com>
- /usr/share/fonts/default added.

* Fri Oct  9 1998 Bill Nottingham <notting@redhat.com>
- put /mnt/cdrom back in

* Wed Oct  7 1998 Bill Nottingham <notting@redhat.com>
- Changed /root to 0750

* Wed Aug 05 1998 Erik Troan <ewt@redhat.com>
- added /var/db
- set attributes in the spec file; don't depend on the ones in the cpio
  archive
- use a tarball instead of a cpioball

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Sep 09 1997 Erik Troan <ewt@redhat.com>
- made a noarch package

* Wed Jul 09 1997 Erik Troan <ewt@redhat.com>
- added /

* Wed Apr 16 1997 Erik Troan <ewt@redhat.com>
- Changed /proc to 555
- Removed /var/spool/mqueue (which is owned by sendmail)
