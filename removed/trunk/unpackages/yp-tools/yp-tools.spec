%define name	yp-tools
%define version	2.8
%define release	4avx

Summary:	NIS (or YP) client programs
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Networking
URL:		http://www.linux-nis.org/nis/
Source:		ftp://ftp.kernel.org/pub/linux/utils/net/NIS/yp-tools-%{version}.tar.bz2
Source1:	ftp://ftp.kernel.org/pub/linux/utils/net/NIS/yp-tools-%{version}.tar.bz2.sign
Patch1:		yp-tools-2.7-md5.patch.bz2

Buildroot:	%{_tmppath}/%{name}-root

Requires:	ypbind

%description
The Network Information Service (NIS) is a system which provides
network information (login names, passwords, home directories, group
information) to all of the machines on a network.  NIS can enable
users to login on any machine on the network, as long as the machine
has the NIS client programs running and the user's password is
recorded in the NIS passwd database.  NIS was formerly known as Sun
Yellow Pages (YP).

This package's NIS implementation is based on FreeBSD's YP and is a
special port for glibc 2.x and libc versions 5.4.21 and later.  This
package only provides the NIS client programs.  In order to use the
clients, you'll need to already have an NIS server running on your
network. An NIS server is provided in the ypserv package.

Install the yp-tools package if you need NIS client programs for machines
on your network.  You will also need to install the ypbind package on
every machine running NIS client programs.  If you need an NIS server,
you'll need to install the ypserv package on one machine on the network.

%prep
%setup -q
%patch1 -p1 -b .md5

%build
%configure --disable-domainname
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR="$RPM_BUILD_ROOT" install

%find_lang %{name}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc AUTHORS COPYING README ChangeLog NEWS etc/nsswitch.conf
%doc THANKS TODO
%{_bindir}/*
%{_mandir}/*/*
%{_sbindir}/*
/var/yp/nicknames

%changelog
* Fri Jun 18 2004 Vincent Danen <vdanen@annvix.org> 2.8-4avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 2.8-3sls
- OpenSLS build
- tidy spec

* Mon Jul 21 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.8-2mdk
- removed Obsoletes/Provides yppasswd and yp-clients (Andi Payn)

* Sat Feb  8 2003 Frederic Lepied <flepied@mandrakesoft.com> 2.8-1mdk
- removed patch2 (merged upstream)
- 2.8

* Thu Dec  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.7-1mdk
- updated URL
- 2.7

* Tue Dec  4 2001 Stefan van der Eijk <stefan@eijk.nu> 2.6-2mdk
- Removed %%dir /var/yp from %%files (directory owned by filesystem)

* Fri Nov 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.6-1mdk
- 2.6

* Fri Jul 27 2001 Frederic Lepied <flepied@mandrakesoft.com> 2.5-1mdk
- 2.5

* Tue Oct 10 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4-1mdk
- Merging with redhat changes.
- 2.4.

* Mon Aug 28 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.3-7mdk
- corrected URL.
- use %%find_lang

* Fri Jul 28 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.3-6mdk
- macroszifications
- rebuild for the BM

* Tue Apr 18 2000 Warly <warly@mandrakesoft.com> 2.3-5mdk
- New group: System/Configuration/Networking

* Thu Mar 30 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.3-4mdk
- new group scheme
- use spechelper

* Fri Oct 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with rh patchs.

* Sat Jul 17 1999 Axalon Bloodstone <axalon@linux-mandrake.com>

- added various summary/descriptions (fr/de/tr)
- removed "make distclean" from %clean
- 2.3 :
	1999-05-18  Thorsten Kukuk  <kukuk@suse.de>
        * release version 2.3
        * src/ypcat.c (print_data): Mark indata as unused.
	1999-05-01  Thorsten Kukuk  <kukuk@suse.de>
        * man/nicknames.5.in: Fix typo.
	1999-02-28  Thorsten Kukuk  <kukuk@suse.de>
        * src/yppasswd.c: Add prototype for getrpcport if needed.
        * src/ypset.c: Likewise.
	1999-02-17  Thorsten Kukuk  <kukuk@suse.de>
        * src/Makefile.am: Fix rule for installing links for domainname.
        * po/de.po: Fix typos.


* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Fri Apr 16 1999 Cristian Gafton <gafton@redhat.com>
- version 2.2
- make it obsolete older yp-clients package

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2/1
- version 2.1
- require ypbind

* Fri Jun 12 1998 Aron Griffis <agriffis@coat.com>
- upgraded to 2.0

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Apr 13 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.4.1

* Thu Dec 04 1997 Cristian Gafton <gafton@redhat.com>
- put yppasswd again in the package, 'cause it is the right thing to do
  (sorry djb!)
- obsoletes old, unmaintained yppasswd package

* Sat Nov 01 1997 Donnie Barnes <djb@redhat.com>
- removed yppasswd from this package.

* Fri Oct 31 1997 Donnie Barnes <djb@redhat.com>
- pulled from contrib into distribution (got fresh sources).  Thanks
  to Thorsten Kukuk <kukuk@vt.uni-paderborn.de> for the original.
- used fresh sources
