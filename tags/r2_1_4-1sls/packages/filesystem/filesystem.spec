%define name	filesystem
%define version	2.1.4
%define release	1sls

Summary:	The basic directory layout for a Linux system.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Base
Source0:	filesystem-%{version}.tar.bz2

Buildroot:	%{_tmppath}/%{name}-root
BuildArch:	noarch

Requires:	setup

%description
The filesystem package is one of the basic packages that is installed on
an OpenSLS system.  Filesystem  contains the basic directory layout
for a Linux operating system, including the correct permissions for the
directories.

%prep

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir $RPM_BUILD_ROOT

tar xfj %{SOURCE0} -C $RPM_BUILD_ROOT

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(0755,root,root)
/bin
/boot
%dir %{_sysconfdir}
%dir %{_sysconfdir}/profile.d
%dir %{_sysconfdir}/security
/home
/initrd
/lib
%dir /mnt
%dir /media
%dir /opt
%attr(555,root,root) /proc
%attr(750,root,root) /root
/sbin
%attr(1777,root,root) /tmp
%dir /usr
/usr/[^s]*
/usr/sbin
%dir /usr/share
/usr/share/doc
%attr(555,root,root) %dir /usr/share/empty
/usr/share/info
/usr/share/man
/usr/share/misc
/usr/share/pixmaps
/usr/src
%dir /var
/var/db
/var/lib
/var/local
%dir %attr(775,root,root) /var/lock
%attr(755,root,root) /var/lock/subsys
/var/cache
/var/log
/var/nis
/var/opt
/var/preserve
/var/run
%dir /var/spool
/var/spool/mail
%dir %attr(1755,root,root) %{_srvdir}
%attr(0755,root,daemon) %dir /var/spool/lpd
%attr(775,root,mail) /var/mail
%attr(1777,root,root) /var/tmp
/var/yp

%changelog
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
