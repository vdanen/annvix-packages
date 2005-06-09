%define name	bdflush
%define version 1.5
%define release 28avx
%define url	ftp://tsx-11.mit.edu/pub/linux/sources/system/v1.2

Summary:	The process which starts the flushing of dirty buffers back to disk
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Public Domain
Group:		System/Kernel and hardware
URL:		%{url}
Source:		%{url}/bdflush-1.5.tar.bz2
Patch:		bdflush-1.5-axp.patch.bz2
Patch1:		bdflush-1.5-glibc.patch.bz2
Patch2:		bdflush-1.5-no-bdflush.patch.bz2
Patch3:		bdflush-1.5-limit.patch.bz2
Patch4:		bdflush-1.5_include_errno.patch.bz2

Buildroot:	%{_tmppath}/%{name}-%{version}-buildroot

Obsoletes:	bdflush-lowmem
Provides:	bdflush-lowmem

%description
The bdflush process starts the kernel daemon which flushes dirty
buffers back to disk (i.e., writes all unwritten data to disk).
This helps to prevent the buffers from growing too stale.

Bdflush is a basic system process that must run for your system
to operate properly.

%prep
%setup -q

%patch -p1
%patch1 -p1 -b .glibc
%patch2 -p1 -b .no-bdflush
%patch3 -p1 -b .limit
%patch4 -p1 -b .errno

perl -p -i -e "s/-Wall -O2/$RPM_OPT_FLAGS/" Makefile

%build
%make bdflush

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}{/sbin,%{_mandir}/man8}

install -m 755 bdflush %{buildroot}/sbin/update
install -m 644 bdflush.8 %{buildroot}/%{_mandir}/man8/update.8

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
/sbin/update
%{_mandir}/man8/update.8*

%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 1.5-28avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 1.5-27avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 1.5-26sls
- minor spec cleanups
- since the binary is named update, not bdflush, don't have a manpage named
  bdflush

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 1.5-25sls
- OpenSLS build
- tidy spec

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.5-24mdk
- rebuild
- cosmetics
- quiet setup

* Mon Dec 30 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.5-23mdk
- rebuild for new glibc/rpm - patch for errno (patch4)

* Sun Dec  8 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.5-22mdk
- New Patch2: We have no bdflush syscall on ia64 nor on x86-64

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.5-21mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Fri Jun  7 2002 Stew Benedict <sbenedict@mandrakesoft.com> 1.5-20mdk
- rpmlint: add URL, s/Copyright/License/, permissions on .spec

* Fri Sep 28 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.5-19mdk
- Rpmlint clean-up.

* Tue Nov 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.5-17mdk
- Spec tweak.
- Change license.

* Wed Jul 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.5-16mdk
- Obsoletes -lowmem package (who use it ?)
- BM.
- Merge with last rh patches.

* Wed Mar 29 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.5-15mdk
- Add doc for lowmem package.
- Make static link symbolic.
- Clean-up specs.
- Upgrade groups.

* Wed Nov 24 1999 Pixel <pixel@linux-mandrake.com>
- re-alpha adaptation (i386<>i586)
- alpha adaptation (no lowmem)
- removed the stupid asnonroot patch

* Tue Oct 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Build release.

* Fri Apr  9 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- handle RPM_OPT_FLAGS
- add de locale
- build lowmem version

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- glibc 2.1

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- spec file cleanups
- uses a build root
- user %attr()

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- alpha patch should be applied on all architectures

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

