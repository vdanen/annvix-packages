%define name	mingetty
%define version	1.06
%define release	1sls

Summary: 	A compact getty program for virtual consoles only.
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		System/Base
URL:		ftp://jurix.jura.uni-sb.de/pub/linux/source/system/daemon/
Source0: 	ftp://jurix.jura.uni-sb.de/pub/linux/source/system/daemons/%{name}-%{version}.tar.bz2
Patch0:		mingetty-1.00-opt.patch.bz2

BuildRoot: 	%{_tmppath}/%{name}-root

%description
The mingetty program is a lightweight, minimalist getty program for
use only on virtual consoles.  Mingetty is not suitable for serial
lines (you should use the mgetty program instead for that purpose).

%prep
%setup -q
%patch0 -p1 -b .opt

%build
%make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %buildroot/{sbin,%{_mandir}/man8}

install -m 0755 mingetty %buildroot/sbin/
install -m 0644 mingetty.8 %buildroot/%{_mandir}/man8/

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING
/sbin/mingetty
%{_mandir}/man8/*

%changelog
* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> 1.06-1sls
- 1.06

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.00-5sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 1.00-4sls
- OpenSLS build
- tidy spec
- regen P0 to use RPM_OPT_FLAGS and not RPM_OPTS

* Tue Apr  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.00-3mdk
- Rebuild to hande biarch struct utmp

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.00-2mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Sat Apr 06 2002 Yves Duret <yduret@mandrakesoft.com> 1.00-1mdk
- version 1.00
- removed all patch no more needed
- added patch0 to compile with RPMS_OPT_FLAGS
- no more configure/makeinstall (all is done by hand in %%install)
- adapted %%doc files

* Fri Dec  7 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.9.4-20mdk
- fix build on alpha by using %%configure2_5x and %%makeinstall_std

* Tue Nov 20 2001 Yves Duret <yduret@mandrakesoft.com> 0.9.4-19mdk
- rebuild, fix rpmlint warning
- use new %%makeinstall macro

* Wed Jul 18 2001 Yves Duret <yduret@mandrakesoft.com> 0.9.4-18mdk
- merged various patches (4:fgtec, 5:s390, 6:manpage, 7:syslog) from rh
- more macros
- more spec clean up

* Mon May 21 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.9.4-17mdk
- correct stupid bug in 16mdk

* Mon May 21 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.9.4-16mdk
- convert to autoconf/automake
- more spec clean up

* Tue May  1 2001 Yves Duret <yduret@mandrakesoft.com> 0.9.4-15mdk
- spec clean up : macros, s!Copyright!License!, renamed to mingetty.spec
- files perm
- #1924

* Tue Sep  5 2000 Etienne Faure  <etienne@mandraksoft.com> 0.9.4-14mdk
- rebuilt with _mandir and %%doc macros

* Mon Mar 27 2000 Daouda Lo <daouda@mandrakesoft.com> 0.9.4-13mdk
- fix group

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- fixed build problems on intel and alpha for manhattan

* Tue Oct 21 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
