Summary: The /bin/mail program, which is used to send mail via shell scripts.
Name: mailx
Version: 8.1.1
Release: 23mdk
License: BSD
Group: Networking/Mail
Source: ftp://ftp.debian.org/pub/debian/hamm/source/mail/mailx-8.1.1.tar.bz2
# not strictly debian patch, i modified it --Geoff
Patch0: mailx-8.1.1.debian.patch.bz2
Patch1: mailx-8.1.1.security.patch.bz2
Patch2: mailx-8.1.1.nolock.patch.bz2
Patch3: mailx-8.1.1.debian2.patch.bz2
Patch4: mailx-noroot.patch.bz2
#Patch5: mailx-geoffdiff.patch.bz2
Patch6: mailx-8.1.1-version.patch.bz2
Patch7: mailx-8.1.1-forbid-shellescape-in-interactive-and-setuid.patch.bz2
Patch8: mailx-8.1.1-help-files.patch.bz2
Patch9: mailx-8.1.1-makefile-create-dirs.patch.bz2
Patch10: mailx-8.1.1-includes.patch.bz2 
Patch11: mailx-8.1.1-fseek.patch.bz2
BuildRoot: %{_tmppath}/%{name}-root

%description
The mailx package installs the /bin/mail program, which is used to send
quick email messages (i.e., without opening up a full-featured mail user
agent). Mail is often used in shell scripts.

You should install mailx because of its quick email sending ability, which
is especially useful if you're planning on writing any shell scripts.

%prep
%setup -q

%patch0 -p1 -b .debian
%patch1 -p1 -b .security
%patch2 -p1 -b .nolock
%patch3 -p1 -b .debian2
%patch4 -p1 -b .noroot
#%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1 -b .help-files
%patch9 -p1 -b .makefile-create-dirs
%patch10 -p1 -b .includes
%patch11 -p1 -b .fseek

%build
# We can't compile mailx with Optimisation

CFLAGS=$(echo $RPM_OPT_FLAGS|sed 's/-O.//g')
make CFLAGS="$CFLAGS -D_GNU_SOURCE"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -sf ../../bin/mail $RPM_BUILD_ROOT%{_bindir}/Mail
ln -sf mail.1 $RPM_BUILD_ROOT%{_mandir}/man1/Mail.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(755,root,mail)	/bin/mail
%{_bindir}/Mail
%dir %{_datadir}/mailx
%{_datadir}/mailx/mail.help
%{_datadir}/mailx/mail.tildehelp
%config(noreplace) %{_sysconfdir}/mail.rc
%{_mandir}/man1/*

%changelog
* Mon Jul 21 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 8.1.1-23mdk
- rebuild
- use %%makeinstall_std macro
- be sure to own %%{_datadir}/mailx

* Tue Dec 10 2002 Giuseppe Ghibò <ghibo@mandrakesoft.com> 8.1.1-22mdk
- Added Patch11 to avoid fseek crash on large mailbox.
- s/Copyright/License/.

* Mon Nov 11 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 8.1.1-21mdk
- Patch8: Move help files to /usr/share/mailx/
- Patch9: Do use usual configure-style macros for mandir et al.
- Patch10: Add missing includes

* Mon Oct 08 2001 Ludo <lfrancois@mandrakesoft.com> 8.1.1-20mdk
- Fix segv on ia64. Add flags to gcc.

* Tue Mar 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 8.1.1-19mdk
- Do nothing but rebuild.

* Thu Aug 10 2000 Pixel <pixel@mandrakesoft.com> 8.1.1-18mdk
- cleanup
- add noreplace
- yet again another patch: i patched the patch so that all capital variables can
have access to the environment (the way it should be!)

* Tue Aug  8 2000 Pixel <pixel@mandrakesoft.com> 8.1.1-17mdk
- better security fix:
	- Do not lookup options in the environment.
  	- Do not read rc files when running with uid != euid
	- Unset interactive when sending mail with uid != euid
	  or when stdin is not a tty.

* Mon Aug  7 2000 Pixel <pixel@mandrakesoft.com> 8.1.1-16mdk
- security fix (don't allow shell escapes in case of non-interactive use, where
"interactive" environment variable is set, if you really want it, use option -I)

* Sat Jul 22 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 8.1.1-15mdk
- big move
- macros
- fix the version 
* Thu Jul 13 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 8.1.1-14mdk
- add path to fix paths
- tmppath

* Fri Apr 07 2000 Christopher Molnar <molnarc@mandrakesoft.com> 8.1.1-13mdk
- new group id.

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- rh merge.
- fix pathnames(r).
- take out makefile install crud(r).

* Fri Apr 16 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix a segfault if we compile with a -0? optimisation.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Thu Aug 27 1998 Alan Cox <alan@redhat.com>
- Synchronized with the Debian people (more small edge case cures)

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Wed Jun 24 1998 Alan Cox <alan@redhat.com>
- Switched dotlocking off. This fits the Red Hat model of not having setgid
  mail agents and fixes the "lock" problem reported.

* Mon Jun 22 1998 Alan Cox <alan@redhat.com>
- Buffer overrun patches. These dont bite us when we don't run mailx setgid
  but do want to be in as mailx needs to be setgid

* Fri Jun 12 1998 Alan Cox <alan@redhat.com>
- Moved from 5.5 to the OpenBSD 8.1 release plus Debian patches

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Thu Jun 12 1997 Erik Troan <ewt@redhat.com>
- built against glibc
