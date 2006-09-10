#
# spec file for package slocate
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		slocate
%define version		3.1
%define release		%_revrel

Summary:	Finds files on a system via a central database
Name:		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		File tools
URL:		http://slocate.trakker.ca/
Source:		http://slocate.trakker.ca/files/%{name}-%{version}.tar.gz
Source1:	slocate.cron
Source3:	updatedb.conf
Source4:	updatedb.sh

Buildroot:	%{_buildroot}/%{name}-%{version}

Requires(pre):	rpm-helper
Requires(postun): rpm-helper


%description
Slocate is a security-enhanced version of locate. Just like locate,
slocate searches through a central database (updated regularly)
for files which match a given pattern. Slocate allows you to quickly
find files anywhere on your system.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
chmod 0644 Changelog notes README


%build
pushd src
    %make CFLAGS="%{optflags}"
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly
mkdir -p %{buildroot}/var/lib/slocate

install src/slocate %{buildroot}%{_bindir}/
ln -s slocate %{buildroot}%{_bindir}/locate
install doc/slocate.1 %{buildroot}%{_mandir}/man1/
install doc/updatedb.1 %{buildroot}%{_mandir}/man1/
ln -s slocate.1.bz2 %{buildroot}%{_mandir}/man1/locate.1.bz2

install -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/cron.weekly/

install -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/
install -m 0755 %{SOURCE4} %{buildroot}%{_bindir}/updatedb


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%pre
%_pre_groupadd slocate 17


%post
if [ "$1" = "0" ]; then
    [ -f /var/lib/slocate/slocate.db ] && rm -f /var/lib/slocate/slocate.db
    touch /var/lib/slocate/slocate.db
fi

%preun
if [ "$1" = "0" ]; then 
    [ -f /var/lib/slocate/slocate.db ] && rm -f /var/lib/slocate/slocate.db || true
fi

%postun
%_postun_groupdel slocate


%files
%defattr(-,root,root,755)
%attr(2755,root,slocate) %{_bindir}/*locate
%attr(-,root,slocate) %{_bindir}/updatedb
%{_mandir}/man1/*
%dir %attr(750,root,slocate) /var/lib/slocate
%config(noreplace) %{_sysconfdir}/cron.weekly/slocate.cron
%config(noreplace) %{_sysconfdir}/updatedb.conf

%files doc
%defattr(-,root,root,755)
%doc README Changelog notes


%changelog
* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1
- 3.1
- fix url/source locations
- drop all patches; fixed upstream
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.7
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.7
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.7-8avx
- correct the buildroot

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.7-7avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.7-6avx
- rebuild

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.7-5avx
- Annvix build

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 2.7-4sls
- minor spec cleanups
- assign slocate a static gid of 17 (%%_post_groupadd/%%_preun_groupdel)

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 2.7-3sls
- OpenSLS build
- tidy spec

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.7-2mdk
- rebuild
- use %%make macro

* Thu Jan 30 2003 Warly <warly@mandrakesoft.com> 2.7-1mdk
- new version

* Wed Jul 17 2002 Warly <warly@mandrakesoft.com> 2.6-5mdk
- add group slocate

* Wed Jul 10 2002 Warly <warly@mandrakesoft.com> 2.6-4mdk
- change description

* Wed Jul 10 2002 Warly <warly@mandrakesoft.com> 2.6-3mdk
- move daily update to weekly update

* Wed Feb 13 2002 Warly <warly@mandrakesoft.com> 2.6-2mdk
- nice updatedb to 19.

* Tue Jan 22 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.6-1mdk
- 2.6.

* Tue Dec  4 2001 Warly <warly@mandrakesoft.com> 2.5-6mdk
- rpmlint fixes

* Fri Apr  6 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.5-5mdk
- Fix segfault when using with regexp.

* Wed Mar 28 2001 Francis Galiegue <fg@mandrakesoft.com> 2.5-4mdk
- Fixes to updatedb.{conf,sh} by mlord@pobox.com

* Tue Jan 09 2001 Francis Galiegue <fg@mandrakesoft.com> 2.5-3mdk

- Exclude devs, usbdevfs, iso9660, vfat, supermount from filesystems
- make cron entry and %{_bindir}/updatedb read from /etc/updatedb.conf... (as a
  side effect, slocate.cron is no more bound to a noreplace tag, since it takes
  its config from aforementioned file)

* Mon Jan 08 2001 Francis Galiegue <fg@mandrakesoft.com> 2.5-2mdk

- Exclude /mnt from scanned directories
- No useless macros

* Sun Dec 31 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.5-1mdk
- put in another source url, whic points to the real one, not the debian one.
- new and shiny source.
- run configure as this new and shiny source supports GNU autoconf.
- debian patch seems obsolete now, removing it.
- port and remake the information patch.

* Mon Dec 18 2000 Vincent Danen <vdanen@mandrakesoft.com> 2.4-1mdk
- 2.4 (many fixes)
- included debian patch:
  - removed chown() that was performed to give the slocate database the
    slocate gid.  This way regular users when making their own databases
    won't have their database auto owned to the slocate group.
  - added an exception  that will exit slocate if a corrupt database is
    detected.  Fixed a segfault occuring on specific data.
- added url

* Wed Nov 15 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-7mdk
- fix glibc2.2 compilation.

* Mon Sep 25 2000 Francis Galiegue <fg@mandrakesoft.com> 2.2-6mdk

- Exclude iso9660, udf and usbdevfs from scanned filesystems


* Wed Sep 20 2000 Francis Galiegue <fg@mandrakesoft.com> 2.2-5mdk

- /etc/cron.daily/slocate.cron is %%config(noreplace)


* Fri Jul 28 2000 Francis Galiegue <fg@mandrakesoft.com> 2.2-4mdk

- More macros
- Some permission fixes

* Tue Jul 18 2000 Francis Galiegue <fg@mandrakesoft.com> 2.2-3mdk

- Oops... Really commented out %post this time...
- made %preun always succeed

* Tue Jul 18 2000 Francis Galiegue <fg@mandrakesoft.com> 2.2-2mdk

- 2.2 doesn't like empty databases - touch not prereq'ed anymore
- /etc/updatedb.conf is %config(noreplace)

* Sat Jul  1 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.2-1mdk
- Remove add/remove/group stuff (move them to the default group from
  setup package).
- Macroszification.
- Correct source url.
- 2.2.

* Fri Apr 28 2000 Pixel <pixel@mandrakesoft.com> 2.1-6mdk
- add symlink slocate -> locate (make it be there as it should, aka fix bug in spec)

* Thu Apr 20 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.1-5mdk
- fixed release tag

* Mon Jan  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.1-4mdk
- Exclude dangerous filesystems by default with updatedb.

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Prereq of /bit/touch.

* Tue Nov  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 2.1.

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Tue Sep 28 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add filesystem to updatedb script to fix loop update.(#76)

* Fri Aug 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Yet another typo fix in updatedb.

* Mon Aug 16 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add fix for updatedb from Randall W. Hron <randall.hron@sprintparanet.com>.

* Wed Jul 21 1999 Gregus <gregus@etudiant.net>
- fr locale

* Thu Jul 01 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 2.0:
    - Converted the original recursive file tree walking code over to the
      newly supported fts() function.  This is the main reason for pushing
      the version to 2.0.  This is much more stable and has fixed a few
      bugs that didn't allow the whole file system to be scanned.  I took
      the fts() code right from glibc so that it may be used on libc5
      systems.
    - Added File System Exclusion option. ( -f "fstype1,fstype2,..." ).
      Now you can exclude NFS, proc, ext2, etc without listing each path.
    - If 'updatedb' is used to update the database, GNU Locate's original
      '/etc/updatedb.conf' will be used to exclude file systems and paths.
      When using 'slocate' to update the database, the '-c' option may now
      be used to parse the '/etc/updatedb.conf' file.
      *NOTE* - This only works under Linux.

* Mon Jun 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- 1.6 versions.
- Remove obsolete patch.

* Mon May 24 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- 1.5
- add fix from bugtraq list
- Fix slocate.cron compatibility with bash2

* Sat May 22 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- Add /var/lib/slocate/slocate.db, if it doesn't exist (required to work)
- Prereq fileutils (we need touch)

* Thu May 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix slocate.cron bugs.

* Tue May 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add a updatedb and a updatedb.conf.

* Tue Apr 13 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Update man-pages.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Mon Feb 15 1999 Bill Nottingham <notting@redhat.com>
- %post groupadd changed to %pre 

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
