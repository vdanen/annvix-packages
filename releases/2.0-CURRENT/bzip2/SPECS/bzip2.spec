#
# spec file for package bzip2
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		bzip2
%define version		1.0.3
%define release		%_revrel

%define libname_orig	lib%{name}
%define libname		%mklibname %{name}_ 1

Summary:	Extremely powerful file compression utility
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Archiving
URL:		http://www.bzip.org/
Source:		http://www.bzip.org/1.0.3/%{name}-%{version}.tar.gz
Source2:	bzme
Source3:	bzme.1
Patch0:		bzip2-1.0.2-mdv-mktemp.patch
Patch1:		bzip2-1.0.3-mdv-makefile.patch
# P2 implements a progress counter (in %). It also
# display the percentage of the original file the new file is (size). 
# URL: http://www.vanheusden.com/Linux/bzip2-1.0.2.diff.gz
Patch2:		bzip2-1.0.2.diff
Patch3:		bzip2-1.0.2-CAN-2005-0953.patch
Patch4:		bzip2-1.0.2-bzgrep.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo

Requires:	%{libname} = %{version}, mktemp

%description
Bzip2 compresses files using the Burrows-Wheeler block-sorting text
compression algorithm, and Huffman coding. Compression is generally
considerably better than that achieved by more conventional LZ77/LZ78-based
compressors, and approaches the performance of the PPM family of statistical
compressors.

The command-line options are deliberately very similar to those of GNU Gzip,
but they are not identical.


%package -n %{libname}
Summary:	Libraries for developing apps which will use bzip2
Group:		System/Libraries

%description -n %libname
Library of bzip2 functions, for developing apps which will use the
bzip2 library (aka libz2).


%package -n %{libname}-devel
Summary:	Header files for developing apps which will use bzip2
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel
Obsoletes:	%{name}-devel

%description -n %libname-devel
Header files and static library of bzip2 functions, for developing apps which
will use the bzip2 library (aka libz2).


%prep
%setup -q
cp %{SOURCE2} .
%patch0 -p1 -b .mktemp
%patch1 -p1 -b .makefile
%patch2 -p1
%patch3 -p1 -b .can-2005-0953
%patch4 -p1 -b .cve-2005-0758

echo "lib = %{_lib}" >>config.in
echo "CFLAGS = %{optflags}" >>config.in


%build
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall
install -m 0755 bzme %{buildroot}%{_bindir}
install -m 0755 bzgrep %{buildroot}%{_bindir}
install -m 0644 bzgrep.1 %{buildroot}%{_mandir}/man1

cat > %{buildroot}%{_bindir}/bzless <<EOF
#!/bin/sh
%{_bindir}/bunzip2 -c "\$@" | %{_bindir}/less
EOF
chmod 0755 %{buildroot}%{_bindir}/bzless
install -m 0644 %{SOURCE3} %{buildroot}%{_mandir}/man1/

install -m 0644 bzlib_private.h %{buildroot}%{_includedir}/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files
%defattr(-,root,root,755)
%doc README LICENSE
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{libname}
%defattr(-,root,root,755)
%doc LICENSE
%{_libdir}/libbz2.so.*

%files -n %{libname}-devel
%defattr(-,root,root,755)
%doc *.html LICENSE
%{_libdir}/libbz2.a
%{_libdir}/libbz2.la
%{_libdir}/libbz2.so
%{_includedir}/*.h


%changelog
* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- fix group

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- P4: security fix for CVE-2005-0758 (bzgrep)
- drop S1; use the bundled bzgrep instead and install the manpage

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3-4avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3-3avx
- rebuild against new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3-2avx
- bootstrap build

* Wed May 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.0.3-1avx
- 1.0.3 (fixes CAN-2005-1260)
- P1: mktemp support (Requires: mktemp); rediffed from Mandriva
- P2: get rid of the automake stuff (gbeauchesne)
- P3: patch to fix CAN-2005-0953
- spec cleanups
- include bzdiff and bzmore
- bzme: allow to force compression with -F option (mandriva bug #11183);
  patch from Michael Scherer (oblin)
- fix URL/source URL
- make sure bzlib_private.h still gets included

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.0.2-19avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 1.0.2-18sls
- remove %%buildpdf
- minor spec cleanups

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 1.0.2-17sls
- OpenSLS build
- tidy spec

* Tue Jul 08 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.0.2-16mdk
- rebuild for new provides

* Fri May 23 2003 Stefan van der Eijk <stefan@eijk.nu> 1.0.2-15mdk
- BuildRequires
- quiet setup
- rebuild

* Mon Apr 14 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.2-14mdk
- let use %%mklibname
- remove now useless "chmod +x ./configure" that mistakely confuse rpmlint's
  configure_libdir_spec_regex
- fix -devel provides

* Tue Feb 04 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.2-13mdk
- kill stupid message

* Tue Feb 04 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.2-12mdk
- implements a progress counter (in %) and display the percentage of the
  original file the new file size is (Oden Eriksson)

* Thu Jan 02 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.2-11mdk
- add missing headers

* Thu Jul 25 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.2-10mdk
- fix configure-without-libdir-spec
- gcc3.2 rebuild

* Mon Jul 08 2002 Geoffrey Lee <snailtalk@mandrakesoft.com> 1.0.2-9mdk
- Removed utterly wrong provides in main package.

* Sat May 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.2-8mdk
- bzme-1.8: handle gziped files with trailling characters

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.2-7mdk
- Automated rebuild in gcc3.1 environment

* Tue Apr 30 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.2-6mdk
- bzme-1.7: handle file names with spaces

* Wed Apr 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.2-5mdk
- add bzme(1) man page
- bzme-1.6:
  - print error message on stderr rather than on stdin
  - factorize/simplify zip method (fix erase temp files on bzip2ing
    error)
  - typo fixes
  - simplify for_each(file) loop
  - add "Know bugs" and TODO sections
  - add -h and -k options
  - if -k (keep) option is used, keep all files

* Wed Mar 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.2-4mdk
- bzme:
    * make zip method acting as *z one (remove orginal file,
      keeping only smalest file, displaying size gain, ...)
      thus giving occasion to factorize some common code
    * check that the source file exists
    * handle corrupted zip file
    * comment the script and verbos-ize() some old changes
    * use cheaper shell tests
    * add GPL reference
    * update online help to reflect optional options and newer
      supported formats
    * remove dependancy on sed by using ${1%old}new_extension

* Tue Mar 05 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.2-3mdk
- bzme: add zip support

* Thu Feb 14 2002 Stefan van der Eijk <stefan@eijk.nu> 1.0.2-2mdk
- BuildRequires

* Fri Feb 01 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.2-1mdk
- new release

* Thu Jan 24 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-18mdk
- add chmou force option to bzme to overwrite existing bzip2 files
  note that it won't force switch from gzip to bzip2 format
  if disk space is larger

* Tue Oct 30 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-17mdk
- build release

* Wed Oct 10 2001 Stefan van der Eijk <stefan@eijk.nu> 1.0.1-16mdk
- fix Provides and Obsoletes: bzip2-devel

* Tue Oct 09 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-15mdk
- fixes for lord rpmlint
- since we obsoletes it, provides also bzip2-devel

* Mon Aug 06 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-14mdk
- add license in %%_docdir

* Tue Jun 26 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.0.1-13mdk
- regenerate libtool/autoconf/automake at build time, to fix build
- remove --enable-shared and --enable-static configure args, redundant

* Wed May 30 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-12mdk
- new bzme : use less cpu time

* Tue May 08 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-11mdk
- s!Copyright!License
- bzme: fix error path when eof (or any other decompressing error); then we
  keep the {{{t,}g,}}{z,Z} one, not the bzip2 one

* Sat Mar 24 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.1-10mdk
- fixed changelog comment (macro expansion).

* Thu Mar 22 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.0.1-9mdk
- use of %%configure.
- rebuild with large file support.

* Mon Feb 12 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 1.0.1-8mdk
- devel package has to provide the libname without major name

#- bump soname version to 2
* Wed Dec 06 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-7mdk
- split libbz2 in %{libname} and headers in %{libname}devel
- fix %%{tmppatch}

* Tue Jul 25 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-6mdk
- BM

* Thu Jul 06 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-5mdk
- let my bzme script handle old .Z archives

* Wed Jul 05 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-4mdk
- increase the .so version for compatibility reason (to force upgrades)
  (thanks Fred)
- let spec-helper bzip2 man-pages (and let packager use shrtcrt)

* Tue Jul 04 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-3mdk
- fix my bzme script so that an error in a batch won't stop the processing of
  the remaining files to compress

* Mon Jul 03 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-2mdk
- bzip2 a gziped patch (saves 48k on SRPMS cd :-) )

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.0.1-1mdk
- 1.0.1 release
- add URL
- fix libbzip2 API

* Fri May  5 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.9.5d-9mdk
- corrected shlib patch to have a correct soname.

* Wed Apr 19 2000 François Pons <fpons@mandrakesoft.com> 0.9.5d-8mdk
- remove 1.0pre5 of bzip2, titi sucks ?

* Wed Mar 22 2000 Pixel <pixel@mandrakesoft.com> 0.9.5d-7mdk
- remove provides bzip2

* Wed Mar 21 2000 Daouda LO <daouda@mandrakesoft.com> 0.9.5d-6mdk
- change to new group architecture

* Sat Mar  4 2000 Pixel <pixel@mandrakesoft.com> 0.9.5d-5mdk
- remove the silly commented out chmod in %post
  (that way, bzip2 don't need /bin/sh anymore)

* Thu Mar 02 2000 Thierry Vignaud <tvignaud@mandrakesoft.com>
- fix bzme script : now it use a lot less disk space.

* Thu Oct 21 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- add bzme script

* Tue Oct 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Thu Sep 16 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 0.9.5d (sanity fixes such as warnings killers casts)

* Wed Aug 25 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- No really, allow users into the docdir.. (don't put %%attr on %%doc files)

* Wed Aug 25 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- %%defattr(-,root,root,755)

* Tue Aug 17 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- fix a bug in the spec
- clean spec

* Fri Aug 13 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- fix bogus permissions on doc

* Wed Aug 11 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- 0.9.5c

* Thu Aug 05 1999 Thierry Vignaud <tvignaud@mandrakesoft.com>
- updated to 0.9.5b
- remove unused patch
- merge all packages in one
- clean spec

* Tue Jul  6 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- added overly redundant provides to help clean up install.log's

* Fri May 14 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add a bzgrep script.

* Fri Apr 16 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adaptations.
- Add patch to permit the bunzip2 on link.

* Thu Jan 14 1999 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- version 0.9.0c

* Sun Nov 29 1998 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- remove CC="egcs" - we want to compile with pgcc
- bzip2 manpages
- build a shared libbz2.so; move libbz2 and bzlib.h to bzip2-devel

* Wed Sep 30 1998 Cristian Gafton <gafton@redhat.com>
- force compilation with egcs to avoid gcc optimization bug (thank God 
  we haven't been beaten by it)

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- version 0.9.0b

* Tue Sep 08 1998 Cristian Gafton <gafton@redhat.com>
- updated to 0.9.0

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- first build for Manhattan

