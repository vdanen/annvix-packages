%define name	autofs
%define version 4.0.0
%define release 0.23avx

%define ver	%{version}pre10

Summary:	A tool for automatically mounting and unmounting filesystems.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Kernel and hardware
URL:		ftp://ftp.kernel.org/pub/linux/daemons/autofs
Source:		ftp://ftp.kernel.org/pub/linux/daemons/autofs/testing-v4/autofs-%{ver}.tar.bz2
Source1:	autofs-ldap-auto-master.c
Patch0:		autofs-4.0.0-doc.patch.bz2
Patch1:		autofs-3.1.4-loop.patch.bz2
Patch2:		autofs-3.1.4-modules.patch.bz2
# updated from autofs-3.1.4-hesiod-bind.patch
Patch3:		autofs-4.0.0-hesiod-bind.patch.bz2
# updated from autofs-3.1.4-linux-2.3.patch
Patch5:		autofs-4.0.0-linux-2.3.patch.bz2
Patch7:		autofs-4.0.0-open_max.patch.bz2
# updated for pre9
Patch8:		autofs-4.0.0-clean.patch.bz2
Patch10:	autofs-4.0.0-init.patch.bz2
Patch12:	autofs.auto.net.patch.bz2
Patch13:	autofs-4.0.0-multiargs.patch.bz2
Patch14:	autofs-4.0.0-fpic.patch.bz2
Patch15:	autofs-3.1.7-schema.patch.bz2
Patch16:	autofs-4.0.0pre10-autofslibdir.patch.bz2
Patch17:	autofs-4.0.0pre10-64bit-fixes.patch.bz2
Patch18:	autofs-4.0.0pre10-supervise.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{ver}-root
BuildRequires:	openldap-devel

PreReq:		chkconfig, rpm-helper
Requires:	bash, mktemp, sed, coreutils, grep, procps
Requires:	nfs-utils-clients, portmap

%description
Autofs controls the operation of the automount daemons. The automount daemons
automatically mount filesystems when you use them and unmount them after a
period of inactivity. Filesystems can include network filesystems, CD-ROMs,
floppies and others.

Install this package if you want a program for automatically mounting and
unmounting filesystems. If your Linux machine is on a network, you should
install autofs.

%prep
%setup -q -n %name-%ver
%patch0 -p1 -b .doc
%patch1 -p1 -b .loop
%patch2 -p1 -b .modules
%patch3 -p1 -b .hesiod-bind
%patch5 -p1 -b .linux-2.3
%patch7 -p1 -b .open_max
%patch13 -p1 -b .multiarg
%patch8 -p1 -b .clean
%patch10 -p1 -b .initd
%patch12 -p0
%patch14 -p1 -b .fpic
%patch15 -p1 -b .schema
%patch16 -p1 -b .autofslibdir
%patch17 -p1 -b .64bit-fixes
%patch18 -p0 -b .supervise

%build
%serverbuild
%configure --with-openldap=/usr
%make initdir="%{_initrddir}" sbindir="%{_sbindir}"
%{__cc} -o autofs-ldap-auto-master $RPM_OPT_FLAGS %{SOURCE1} -lldap -llber

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/autofs
mkdir -p $RPM_BUILD_ROOT%{_mandir}/{man5,man8}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}

%make INSTALLROOT=$RPM_BUILD_ROOT install 
%make -C samples INSTALLROOT=$RPM_BUILD_ROOT initdir=%{_initrddir} install

perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" $RPM_BUILD_ROOT%{_initrddir}/*

install -m 755 autofs-ldap-auto-master $RPM_BUILD_ROOT%{_libdir}/autofs/

export DONT_GPRINTIFY=1

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%pre
grep -q '^alias autofs autofs4'  /etc/modules.conf  || {
	echo "alias autofs autofs4" >> /etc/modules.conf
	}

%post
%_post_service autofs

%preun
%_preun_service autofs

%postun
if [ $1 = "0" ]; then # removal
perl -ni -e 'print unless ( m!^.*autofs.*$! || /^\s*$/)' /etc/modules.conf
fi

%files
%defattr(-, root, root)
%doc COPYRIGHT NEWS README* TODO samples/{auto.master,auto.misc,auto.net}
%config(noreplace) %{_initrddir}/autofs
%config(noreplace) %{_sysconfdir}/auto.master
%config(noreplace) %{_sysconfdir}/auto.misc
%config(noreplace) %{_sysconfdir}/auto.net
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*
%{_sbindir}/automount
%{_mandir}/*/*

%changelog
* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 4.0.0-0.23avx
- Annvix build
- require packages not files

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 4.0.0-0.22sls
- spec cleanups
- fix initscript to work somewhat with supervise (P18)

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 4.0.0-0.21sls
- sync with 0.20mdk (gbeauchesne): lib64 fixes
- sync with 0.21mdk (gbeauchesnet): 64-bit fixes

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 4.0.0-0.20sls
- OpenSLS build
- tidy spec

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 4.0.0-0.19mdk
- rebuild
- drop prefix tag
- drop unapplied P11

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0.0-0.18mdk
- requires s/(sh-|text)utils/coreutils/
- PreReq: rpm-helper

* Tue Feb 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.0.0-0.17mdk
- init script: s/grpintf/gprintf/g (garrick)

* Fri Nov 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.0-0.16mdk
- gprintfy the init script by hand because a lot of echo must not be
gprintified.

* Thu Oct 18 2001 Philippe Libat <philippe@mandrakesoft.com> 4.0.0-0.15mdk
- add multiargs, fpic, schema patch.
- add autofs-ldap-auto-master
- new autofs.init script: determine nis & ldap lookup from nsswitch.conf

* Thu Sep 13 2001 Philippe Libat <philippe@mandrakesoft.com> 4.0.0-0.14mdk
- added nfs-utils-clients require 

* Thu Jul  5 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.0-0.13mdk
- rebuild for new db3.2

* Mon Jul 02 2001 Philippe Libat <philippe@mandrakesoft.com> 4.0.0-0.12mdk
- auto.net patch

* Thu Jun 19 2001 Philippe Libat <philippe@mandrakesoft.com> 4.0.0-0.11mdk
- fix reload/restart init (Sebastian Dransfeld <sebastid@stud.ntnu.no>)

* Thu Jun 19 2001 Philippe Libat <philippe@mandrakesoft.com> 4.0.0-0.10mdk
- ldap initrd

* Mon Jun 11 2001 Vincent Saugey <vince@mandrakesoft.com> 4.0.0-0.9mdk
- rebuild with ldap2 lib

* Tue Apr 10 2001 Renaud Chaillat <rchaillat@mandrakesoft.com> 4.0.0-0.8mdk
- new version (pre10)

* Thu Mar 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.0-0.7mdk
- use the new rpm macros for servers.

* Mon Mar 26 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.0-0.6mdk
- removed /misc and /net

* Mon Nov  6 2000 Renaud Chaillat <rchaillat@mandrakesoft.com> 4.0.0-0.5mdk
- new version
- updated patches and init script

* Tue Sep  5 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.0-0.4mdk
- use condrestart on upgrade.
- enabled again init patch to have a condrestart and to have a start at 18 level.

* Wed Aug 30 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 4.0.0-0.3mdk
- rebuild for the user of _initrddir macro.

* Fri Aug 18 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 4.0.0-0.2mdk
- rebuild to get rid of "if your Red Hat Linux machine is.."
  thanks to Anton Graham <darkimage@bigfoot.com>

* Thu Aug 17 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0.0-0.1mdk
- 4.0.0pre7

* Thu Jul 20 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.5-1mdk
- 3.1.5
- BM
- macroqeivhqowicvjzificationning

* Fri Apr 28 2000 Warly <warly@mandrakesoft.com> 3.1.4-4mdk
- change rc.init value to S72 K08
 
* Tue Mar 22 2000 Daouda Lo <daouda@mandrakesoft.com> 3.1.4-3mdk
- fix wrong date.
- 3.1.4 (new release).
- remove ugly patches.
- add smbmount support.

* Tue Nov 23 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- strip

* Sun Oct 31 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Enable $SMP build/check

* Wed Oct  6 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- checkconfig --del in %preun, not %postun (rh).
- add patch from HJLu to handle NIS auto.master better (rh).

* Fri Sep 24 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Forgot to fix the bloody permissions :/

* Fri Sep 24 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- remove rc patch it's breaking yp
- again with the redhat mergeings:
	* Wed Aug 25 16:00:00 1999 Cristian Gafton <gafton@redhat.com>
	- fix bug #4708
	* Sat Aug 21 16:00:00 1999 Bill Nottingham <notting@redhat.com>
	- fix perms on /usr/lib/autofs/*
	- add support for specifying maptype in auto.master

* Tue Aug 17 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- RedHat Merge:
	* Fri Aug 13 1999 Cristian Gafton <gafton@redhat.com>
	- add patch from rth to avoid an infinite loop

* Wed Jun 23 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Patch from H.J Lu <hjl@varesearch.com> :
	-* fix rc script for /var/lock/subsys.

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Fri Apr 09 1999 Cristian Gafton <gafton@redhat.com>
- enahanced initscript to try to load maps over NIS
- changed the mount point back to misc (there is a reason we leave /mnt
  alone)
- patched back autofs.misc to the version shipped on 5.2 to avoid replacing
  yet one more config file for those who upgrade

* Wed Mar 24 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 3.1.3, fixing smbfs stuff and other things
- changed mountpoint from /misc to /mnt

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 10)

* Mon Feb  8 1999 Bill Nottingham <notting@redhat.com>
- build for kernel-2.2/glibc2.1

* Tue Oct  6 1998 Bill Nottingham <notting@redhat.com>
- fix bash2 breakage in init script

* Sun Aug 23 1998 Jeff Johnson <jbj@redhat.com>
- typo in man page.

* Mon Jul 20 1998 Jeff Johnson <jbj@redhat.com>
- added sparc to ExclusiveArch.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- updated to 3.1.1

* Wed Apr 22 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced initscripts

* Fri Dec 05 1997 Michael K. Johnson <johnsonm@redhat.com>
- Link with -lnsl for glibc compliance.

* Thu Oct 23 1997 Michael K. Johnson <johnsonm@redhat.com>
- exclusivearch for i386 for now, since our kernel packages on
  other platforms don't include autofs yet.
- improvements to initscripts.

* Thu Oct 16 1997 Michael K. Johnson <johnsonm@redhat.com>
- Built package from 0.3.14 for 5.0
