%define libname_orig lib%{name}
%define libname %mklibname %{name}_ 1
%define buildpdf 0

Summary: Extremely powerful file compression utility
Name: bzip2
Version: 1.0.2
Release: 16mdk
License: BSD
Group: Archiving/Compression
Source: ftp://sourceware.cygnus.com/pub/bzip2/v102/%name-%version.tar.bz2
URL: http://sourceware.cygnus.com/bzip2/
Source1: bzgrep
Source2: bzme
Source3: bzme.1
Patch1: bzip2-2.libtoolizeautoconf.patch.bz2

# P2 implements a progress counter (in %). It also
# display the percentage of the original file the new file is (size). 
# URL: http://www.vanheusden.com/Linux/bzip2-1.0.2.diff.gz
Patch2: bzip2-1.0.2.diff.bz2

BuildRoot: %_tmppath/%name-%version-root
Requires: %libname = %version
%if %buildpdf
BuildRequires: tetex-dvips tetex-latex
%endif
BuildRequires: texinfo

%description
Bzip2 compresses files using the Burrows-Wheeler block-sorting text
compression algorithm, and Huffman coding. Compression is generally
considerably better than that achieved by more conventional LZ77/LZ78-based
compressors, and approaches the performance of the PPM family of statistical
compressors.

The command-line options are deliberately very similar to those of GNU Gzip,
but they are not identical.

%package -n %{libname}
Summary: Libraries for developing apps which will use bzip2.
Group: System/Libraries
%description -n %libname
Library of bzip2 functions, for developing apps which will use the
bzip2 library (aka libz2).


%package -n %{libname}-devel
Summary: Header files for developing apps which will use bzip2.
Group: Development/C
Requires: %libname = %version
Provides: %{libname_orig}-devel = %version-%release
Provides: %name-devel
Obsoletes: %name-devel
%description -n %libname-devel
Header files and static library of bzip2 functions, for developing apps which
will use the bzip2 library (aka libz2).

%prep
%setup -q
cp %SOURCE2 .
%patch1 -p1
%patch2 -p1
cp m4/largefile.m4 .
libtoolize -f --automake
aclocal -I m4
autoconf
automake -a --foreign
autoheader

%build
%configure --libdir=%_libdir
make
%if %buildpdf
texi2dvi --pdf manual.texi
%endif

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
install -m 755 %SOURCE1 bzme $RPM_BUILD_ROOT%_bindir

cat > $RPM_BUILD_ROOT%_bindir/bzless <<EOF
#!/bin/sh
%_bindir/bunzip2 -c "\$@" | %_bindir/less
EOF
chmod 755 $RPM_BUILD_ROOT%_bindir/bzless
install -m 644 %SOURCE3 $RPM_BUILD_ROOT%_mandir/man1/

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root,755)
%doc README LICENSE
%_bindir/*
%_mandir/man1/*

%files -n %libname
%defattr(-,root,root,755)
%doc LICENSE
%_libdir/libbz2.so.*

%files -n %libname-devel
%defattr(-,root,root,755)
%doc *.html LICENSE
%if %buildpdf
%doc manual.pdf
%endif
%_libdir/libbz2.a
%_libdir/libbz2.la
%_libdir/libbz2.so
%_includedir/*.h

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
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

