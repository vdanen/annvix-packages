%define url ftp://ftp.cvshome.org/pub
%define _requires_exceptions tcsh

Summary:	A version control system
Name:		cvs
Version:	1.11.6
Release:	3mdk
License:	GPL
Group:		Development/Other
URL:		http://www.cvshome.org/
Requires:	/usr/bin/ssh zlib

Source: 	%{url}/cvs-%{version}/cvs-%{version}.tar.bz2
Source1: 	cvspserver
Source2: 	cvs.conf
Source3: 	cvs-xinetd
Patch4: 	cvs-1.11.2-zlib.patch.bz2
Patch6: 	cvs-1.11.6-errno.patch.bz2
Patch8:		cvs-1.11-ssh.patch.bz2
Patch11:	cvs-1.11.1-newline.patch.bz2
Patch12:	cvs-1.11.4-first-login.patch.bz2
Patch13:	cvs-1.11.2-no-zlib.patch.bz2

Prereq:		/sbin/install-info
Buildroot:	%_tmppath/%name-%version-%release-root
BuildRequires:	texinfo, zlib-devel, krb5-devel

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

Install the cvs package if you need to use a version
control system.

%prep
%setup -q
%patch4 -p1 -b .zlib
%patch6 -p1 -b .errno
%patch8 -p1 -b .ssh
%patch11 -p1 -b .newline
%patch12 -p1 -b .first-login
%patch13 -p1 -b .nozlib

%build
%serverbuild
%configure2_5x

%make

make -C doc info

%{?rpmcheck:make check}

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %buildroot/etc/xinetd.d/
install -m644 %{SOURCE3} %buildroot/etc/xinetd.d/%{name}
bzip2 -f doc/*.ps

%makeinstall

mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cvs
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/cvs

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %{name}.info
%_install_info cvsclient.info

%preun
%_remove_install_info %{name}.info

%_remove_install_info cvsclient.info

%files
%defattr(-,root,root)
%doc BUGS FAQ MINOR-BUGS NEWS PROJECTS TODO README
%doc doc/*.ps.bz2
%config(noreplace) /etc/xinetd.d/%{name}
%{_bindir}/cvs
%{_bindir}/cvsbug
%{_bindir}/rcs2log
%{_mandir}/man1/cvs.1*
%{_mandir}/man5/cvs.5*
%{_mandir}/man8/cvsbug.8*
%{_infodir}/cvs*
%{_datadir}/cvs
%{_sbindir}/cvspserver
%config(noreplace) %{_sysconfdir}/cvs/cvs.conf

%changelog
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
