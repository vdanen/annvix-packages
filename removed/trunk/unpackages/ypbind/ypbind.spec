Summary: The NIS daemon which binds NIS clients to an NIS domain.
Name: ypbind
Version: 1.12
Release: 3mdk
Epoch: 3
License: GPL
Group: System/Servers
URL: http://www.linux-nis.org/nis/ypbind-mt/index.html
Source0: ftp.kernel.org:/pub/linux/utils/net/NIS/ypbind-mt-%{PACKAGE_VERSION}.tar.bz2
Source1: ypbind.init
Source2: yp.conf
Prereq: /sbin/chkconfig, rpm-helper
Requires: portmap
Requires: yp-tools
Buildroot: %{_tmppath}/ypbind-root

%description
The Network Information Service (NIS) is a system which provides
network information (login names, passwords, home directories, group
information) to all of the machines on a network.  NIS can enable
users to login on any machine on the network, as long as the machine
has the NIS client programs running and the user's password is
recorded in the NIS passwd database.  NIS was formerly known as Sun
Yellow Pages (YP).

This package provides the ypbind daemon.  The ypbind daemon binds NIS
clients to an NIS domain.  Ypbind must be running on any machines
which are running NIS client programs.

Install the ypbind package on any machines which are running NIS client
programs (included in the yp-tools package).  If you need an NIS server,
you'll also need to install the ypserv package to a machine on your
network.

%prep
%setup -q -n ypbind-mt-%version

%build
%serverbuild
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# Rename /usr/sbin to /sbin (cheap way to move ypbind)
mv $RPM_BUILD_ROOT%{_sbindir} $RPM_BUILD_ROOT/sbin
strip $RPM_BUILD_ROOT/sbin/ypbind

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/ypbind
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/yp.conf
mkdir -p $RPM_BUILD_ROOT/var/yp/binding

perl -pi -e "s|/etc/rc.d/init.d|%{_initrddir}|" $RPM_BUILD_ROOT%{_initrddir}/*

# Remove unpackaged files
rm -rf $RPM_BUILD_ROOT/usr/share/locale/de/LC_MESSAGES/ypbind-mt.mo

%clean
rm -rf $RPM_BUILD_ROOT

%post

%_post_service ypbind

%preun

%_preun_service ypbind

%files
%defattr(-,root,root)
/sbin/ypbind
%{_mandir}/*/*
%config(noreplace) %{_initrddir}/*
%config(noreplace) %{_sysconfdir}/yp.conf
%dir /var/yp/binding
%doc README

%changelog
* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.12-3mdk
- rebuild
- use %%make macro

* Sat Jan 25 2003 Stefan van der Eijk <stefan@eijk.nu> 1.12-2mdk
- Remove unpackaged file

* Fri Jul 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.12-1mdk
- 1.12

* Thu Mar 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 3.3-29mdk
- use the new rpm macros for servers.

* Tue Oct 24 2000 Vincent Danen <vdanen@mandrakesoft.com> 3.3-28mdk
- security fix

* Wed Aug 30 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.3-27mdk
- rebuild for the use of the _initrddir macro.

* Mon Aug 28 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.3-26mdk
- added restart and stop at package upgrade and removal.
- %%postun => %%preun
- %%config(noreplace)

* Sun Jul 23 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 3.3-25mdk
- macroszifications
- BM

* Thu Mar 30 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.3-24mdk
- new group scheme
- use spechelper

* Sun Nov 28 1999 Pixel <pixel@linux-mandrake.com>
- replaced chkconfig value `-' by `345'

* Fri Oct 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge rh patchs.
- Fix init script.

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Thu Apr 15 1999 Cristian Gafton <gafton@redhat.com>
- requires yp-tools, because ypwhich is part of that package

* Tue Apr 13 1999 Bill Nottingham <notting@redhat.com>
- don't run ypwhich script if ypbind doesn't start

* Wed Apr 07 1999 Bill Nottingham <notting@redhat.com>
- add a 10 second timeout for initscript...

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binary

* Thu Apr 01 1999 Preston Brown <pbrown@redhat.com>
- fixed init script to wait until domain is really bound (bug #1928)

* Thu Mar 25 1999 Cristian Gafton <gafton@redhat.com>
- revert to stabdard ypbind; ypbind-mt sucks.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Sat Feb 13 1999 Cristian Gafton <gafton@redhat.com>
- build as ypbind instead of ypbind-mt

* Fri Feb 12 1999 Michael Maher <mike@redhat.com>
- addressed bug #609

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- provides ypbind
- switch to ypbind-mt instead of plain ypbind
- build for glibc 2.1

