%define name	cpio
%define version 2.5
%define release 5sls

Summary:	A GNU archiving program.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Archiving/Backup
URL:		http://www.fsf.org/software/cpio
Source:		ftp://prep.ai.mit.edu/pub/gnu/%{name}-%{version}.tar.bz2
Patch1:		cpio-2.5-glibc.patch.bz2
Patch2:		cpio-2.4.2-mtime.patch.bz2
Patch3:		cpio-2.4.2-svr4compat.patch.bz2
Patch9:		cpio-2.4.2-errorcode.patch.bz2
Patch10:	cpio-2.4.2-fhs.patch.bz2
Patch11:	cpio-2.4.2-man.patch.bz2
Patch12:	cpio-2.5-i18n-0.1.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root-%{version}
BuildRequires:	texinfo

Prereq:		/sbin/install-info, /sbin/rmt

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

Install cpio if you need a program to manage file archives.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .svr4compat
%patch9 -p1 -b .errorcode
%patch10 -p1 -b .fhs
%patch11 -p1 -b .man
%patch12 -p1 -b .i18n

%build
%configure

%make LDFLAGS=-s

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall bindir=$RPM_BUILD_ROOT/bin mandir=$RPM_BUILD_ROOT/%{_mandir}
chmod 644 README NEWS

# (sb) Installed (but unpackaged) file(s)
rm -f $RPM_BUILD_ROOT/bin/mt
rm -f $RPM_BUILD_ROOT%{_libdir}/rmt
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/mt.1

%clean
rm -rf $RPM_BUILD_ROOT

%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info

%files
%defattr(-,root,root)
/bin/cpio
#/bin/mt
%doc README NEWS
%{_infodir}/cpio.*
%{_mandir}/man1/cpio.1*

%changelog
* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 2.5-5sls
- OpenSLS build
- tidy spec

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 2.5-4mdk
- rebuild
- drop Prefix tag
- use %%make macro
- drop unapplied P7

* Sun Nov 17 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.5-3mdk
- LI18NUX/LSB compliance (patch12, disable patch7 - stdout patch)
- Deal with Installed (but unpackaged) file(s) - mt, rmt, man page

* Thu Jul 25 2002 Daouda LO <daouda@mandrakesoft.com> 2.5-2mdk
- better URL

* Wed Jul 24 2002 Daouda LO <daouda@mandrakesoft.com> 2.5-1mdk
- 2.5 release
- patches  #4(glibc 2_1 build), #5 (long dev), #8 (debian fix) merged upstream
- add URL 

* Sun Jun  2 2002 Stefan van der Eijk <stefan@eijk.nu> 2.4.2-21mdk
- BuildRequires

* Mon Jul  9 2001  Daouda Lo <daouda@mandrakesoft.com> 2.4.2-20mdk
- s|Copyright|License| 

* Mon Jul  9 2001  Daouda Lo <daouda@mandrakesoft.com> 2.4.2-19mdk
- apply RH/Debian patches.
- man updates/fixes 
- more fhs compliant.

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.2-18mdk
- fix bad script

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.2-17mdk
- BM
- more macros

* Tue Jul 11 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.4.2-16mdk
- clean a lot the spec (macros, install fix by Stefan van der Eijk
  <s.vandereijk@chello.nl>)
- use spechelper

* Sat Jul 08 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 2.4.2-16mdk
- fixed makeinstall problem
- some hassle getting the manpage in the right dir

* Thu Apr 4 2000 Denis Havlik <denis@mandrakesoft.com> 2.4.2-15mdk
- new Group: Archiving/Backup 


* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Specs files tweaks.
- Merge with rh patchs.
- fix infinite loop unpacking empty files with hard links (r).
- stdout chould contain progress information (r).

* Fri Apr  9 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- longlong dev wrong with "-o -H odc" headers (formerly "-oc").

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to compile on glibc 2.1, where strdup is a macro

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump package.
- Don't include /bin/mt -- use the mt from mt-st package.
- Add prereq's

* Tue Jun 30 1998 Jeff Johnson <jbj@redhat.com>
- fix '-c' to duplicate svr4 behavior (problem #438)
- install support programs & info pages

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot
- removed "(used by RPM)" comment in Summary

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- no longer statically linked as RPM doesn't use cpio for unpacking packages
