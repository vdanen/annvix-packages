%define patchdate 20021028
%define version 5.3
%define name ncurses
%define release 1.20030215.3mdk
%define lib_major 5
%define lib_name %mklibname %{name} %{lib_major}

Summary:	A CRT screen handling and optimization package
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		System/Libraries
Url:		http://ring.jah.ne.jp/pub/GNU/ncurses/
Source0:	http://ring.jah.ne.jp/pub/GNU/ncurses/%{name}-%{version}.tar.bz2
Source4:	ncurses-resetall.sh
Source5:    	ncurses-usefull-terms
Patch1:		ncurses-5.1-xterm-debian.patch.bz2
Patch2:		ncurses-5.1-setuid2.patch.bz2
Patch3:		ncurses-5.2-64bit.patch.bz2
Patch4:		ncurses-5.3-parallel.patch.bz2

Patch10:         ftp://dickey.his.com/ncurses/%{version}/patch-5.3-20021231.sh
Patch11:         ftp://dickey.his.com/ncurses/%{version}/ncurses-5.3-20030105.patch.gz
Patch12:         ftp://dickey.his.com/ncurses/%{version}/ncurses-5.3-20030111.patch.gz
Patch13:         ftp://dickey.his.com/ncurses/%{version}/ncurses-5.3-20030118.patch.gz
Patch14:         ftp://dickey.his.com/ncurses/%{version}/ncurses-5.3-20030125.patch.gz
Patch15:         ftp://dickey.his.com/ncurses/%{version}/ncurses-5.3-20030201.patch.gz
Patch16:         ftp://dickey.his.com/ncurses/%{version}/ncurses-5.3-20030208.patch.gz
Patch17:         ftp://dickey.his.com/ncurses/%{version}/ncurses-5.3-20030215.patch.gz

BuildRoot:	%{_tmppath}/%{name}-root

PreReq:		/sbin/ldconfig
BuildRequires: gpm-devel sharutils

%description
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

%package -n %{lib_name}
Summary: The development files for applications which use ncurses
Obsoletes:	ncurses3
Requires: ncurses
Group: System/Libraries

%description -n %{lib_name}
The curses library routines are a terminal-independent method of updating
character screens with reasonalble optimization. The ncurses (new curses)
library is a freely distributable replacement for the discontinued 4.4BSD
classic curses library.

%package extraterms
Summary: Some exotic terminal descriptions
Group: System/Libraries
Requires: ncurses

%description extraterms
Install the ncurses-extraterms package if you use some exotic terminals.

%package -n %{lib_name}-devel
Summary: The development files for applications which use ncurses
Group: Development/C
Provides: libncurses-devel ncurses-devel
Obsoletes: libncurses-devel ncurses-devel
Requires: %{lib_name} = %{version}

%description -n %{lib_name}-devel
The header files and libraries for developing applications that use
the ncurses CRT screen handling and optimization package.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

%prep
%setup -q -n ncurses-%{version}

%patch1 -p1

sh %{PATCH10}

%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1

%patch4 -p1 -b .parallel

# in patch5
#%patch2 -p1
# seems to be OK in patch5
#%patch3 -p1
find . -name "*.orig" | xargs rm -f

# fed up of configure script appending ${host_alias}- to gcc commands
perl -pi -e 's|(test -n "\$host_alias" && ac_tool_prefix)=(.*)|\1=""|' ./configure

%build
OPT_FLAGS=`echo "$RPM_OPT_FLAGS -DPURE_TERMINFO" | sed -e "s/-fomit-frame-pointer//g"`
CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" %configure \
	--program-prefix= \
	--with-normal --with-shared --without-debug --without-profile \
	--with-gpm --enable-termcap --enable-getcap \
	--enable-const --enable-hard-tabs --enable-hash-map \
	--enable-no-padding --enable-sigwinch --without-ada

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall prefix=$RPM_BUILD_ROOT/usr \
	includedir=$RPM_BUILD_ROOT/usr/include/ncurses \
	ticdir=$RPM_BUILD_ROOT/%{_datadir}/terminfo

ln -sf ../l/linux $RPM_BUILD_ROOT/%{_datadir}/terminfo/c/console
ln -sf ncurses/curses.h $RPM_BUILD_ROOT/usr/include/ncurses.h
for I in curses unctrl eti form menu panel term; do
	ln -sf ncurses/$I.h $RPM_BUILD_ROOT/usr/include/$I.h
done

# strip $RPM_BUILD_ROOT%{_bindir}/* || :
make clean -C test
# find $RPM_BUILD_ROOT%{_mandir} -type f -exec bzip2 -9f {} \;

# the resetall script
install -m 755 %{SOURCE4} $RPM_BUILD_ROOT/%{_bindir}/resetall
# we don't want this in doc
rm -f c++/demo

mkdir -p $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT/%{_libdir}/libncurses.so* $RPM_BUILD_ROOT/%{_lib}
ln -s /%{_lib}/libncurses.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/libncurses.so.%{version}
ln -s /%{_lib}/libncurses.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/libncurses.so.%{lib_major}
ln -s /%{_lib}/libncurses.so.%{version} $RPM_BUILD_ROOT/%{_libdir}/libncurses.so

ln -s $RPM_BUILD_ROOT/%{_libdir}/libncurses.so.%{version} $RPM_BUILD_ROOT/%{_lib}/libncurses.so.4

#
# FIXME
# OK do not time to debbug it now
#
cp /$RPM_BUILD_ROOT/%{_datadir}/terminfo/x/xterm /$RPM_BUILD_ROOT/%{_datadir}/terminfo/x/xterm2
cp /$RPM_BUILD_ROOT/%{_datadir}/terminfo/x/xterm-new /$RPM_BUILD_ROOT/%{_datadir}/terminfo/x/xterm
#
# FIXME
#

(cd $RPM_BUILD_ROOT ; ls -d usr/share/terminfo/*   | perl -pe 's||%%dir /|') > %{name}.list
(cd $RPM_BUILD_ROOT ; ls    usr/share/terminfo/*/* | perl -pe 's||/|')       > %{name}-extraterms.list
perl -pe 's||%{_datadir}/terminfo/|' %{SOURCE5} >> %{name}.list

perl -ni -e 'BEGIN { open F, "%{name}.list"; /^%/ or $s{$_} = 1 foreach <F>; } print unless $s{$_}' %{name}-extraterms.list

find $RPM_BUILD_ROOT/%{_libdir}/*.a -not -name "*_g.a" -not -name "*_p.a" -type f | sed -e "s#^$RPM_BUILD_ROOT##g" > %{lib_name}-devel.list

mv $RPM_BUILD_ROOT/%{_mandir}/tack.1 $RPM_BUILD_ROOT/%{_mandir}/man1/tack.1

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files -f %{name}.list
%defattr(-,root,root)
%doc README ANNOUNCE
%{_datadir}/tabset
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files -n %{lib_name}
%defattr(-,root,root)
%attr(755,root,root) /%{_lib}/lib*.so.*
%attr(755,root,root) /%{_libdir}/lib*.so.*

%files extraterms -f %{name}-extraterms.list
%defattr(-,root,root)
%doc README

%files -n %{lib_name}-devel -f %lib_name-devel.list
%defattr(-,root,root)
%doc doc c++ test
/%{_lib}/lib*.so
%{_libdir}/lib*.so
/usr/include/ncurses
/usr/include/*.h
%{_mandir}/man3/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jul 09 2003 Laurent MONTEL <lmontel@mandrakesoft.com> 5.3-1.20030215.3mdk
- Rebuild

* Sat May 24 2003 Stefan van der Eijk <stefan@eijk.nu> 5.3-1.20030215.2mdk
- rebuild

* Tue Feb 18 2003 Warly <warly@mandrakesoft.com> 5.3-1.20030215.1mdk
- include latest patches (main changes):
- minor fixes for memory-leak checking when termcap is read.
- correct a potentially-uninitialized value if _read_termtype() does
  not read as much data as expected.
- correct several places where the aclocal.m4 macros relied on cache
variable names which were incompatible (as usual) between autoconf
2.13 and 2.5x, causing the test for broken-linker to give incorrect
results.
- do not try to open gpm mouse driver if standard output is not a tty;
the gpm library does not make this check.
- change several sed scripts to avoid using "\+" since it is not a BRE
(basic regular expression).  One instance caused terminfo.5 to be
misformatted on FreeBSD.

* Tue Dec 31 2002 Warly <warly@.mandrakesoft.com> 5.3-1.20021128.1mdk
- integrate new patches up to 20021128
- fix parallel build

* Thu Dec  5 2002 Warly <warly@mandrakesoft.com> 5.3-1.20021123.1mdk
- new version

* Sat Aug 10 2002 Warly <warly@mandrakesoft.com> 5.2-27mdk
- patch-5.2-20020727 added

* Wed Jul 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.2-26mdk
- Remove compatibility links
- Remove Patch4 (disable c++demo on IA-64)
- Remove experimental/bogus --enable-safe-sprintf
- Build --without-debug, --without-profile

* Fri Jun  7 2002 Warly <warly@mandrakesoft.com> 5.2-25mdk
- fix hardcoded lib path

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.2-24mdk
- Automated rebuild in gcc3.1 environment

* Sat Mar  9 2002 Stew Benedict <sbenedict@mandrakesoft.com> 5.2-23mdk
- add program-prefix="" to have correct program names - PPC too

* Wed Feb 20 2002 Frederic Lepied <flepied@mandrakesoft.com> 5.2-22mdk
- added BuildRequires sharutils

* Fri Feb 15 2002 Warly <warly@mandrakesoft.com> 5.2-21mdk
- add program-prefix="" to have correct program names

* Thu Feb 14 2002 Warly <warly@mandrakesoft.com> 5.2-20mdk
- current development patch to correct mutt pb

* Tue Jan 29 2002 Geoffrey Lee <snailtalk@mandrakesoft.ocm> 5.2-19mdk
- Revert xterm terminfo: it turns out that the original xterm does not have
  color support.
  
* Mon Jan 28 2002 Geoffrey Lee <snailtalk@mandrakesoft.ocm> 5.2-18mdk
- Fix xterm terminfo: who is the @$^& who broke mutt?!

* Thu Jan 10 2002 Warly <warly@mandrakesoft.com> 5.2-17mdk
- rpmlint fixes

* Thu Jul 19 2001 Warly <warly@mandrakesoft.com> 5.2-16mdk
- remove big lib*_{g,p}.a

* Wed Jul  4 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 5.2-15mdk
- rebuild to stop using cross-compile executable names
  (/usr/bin/i586-mandrake-linux-clear versus /usr/bin/clear)

* Tue Jul  3 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 5.2-14mdk
- fix binaries (just recompiled it and now it works, dunno why)
- apply a more conform lib policy

* Mon Jul  2 2001 Matthias Badaire <mbadaire@mandrakesoft.com> 5.2-13mdk
- Fixes for ia64 

* Sat Dec 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.2-12mdk
- Definitives fixes for alpha compilation.

* Tue Dec 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.2-11mdk
- Don't compile with -mieee on alpha.

* Tue Dec 19 2000 Warly <warly@mandrakesoft.com> 5.2-10mdk
- add an obsolete on ncurses-devel

* Tue Dec  5 2000 Warly <warly@mandrakesoft.com> 5.2-9mdk
- add a requires on ncurses in the libs

* Tue Dec  5 2000 Warly <warly@mandrakesoft.com> 5.2-8mdk
- Remove the provides ncurses from the libncurses

* Wed Nov 29 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 5.2-7mdk
- Provides: ncurses and ncurses-devel (warlyscks).

* Tue Nov 28 2000 Warly <warly@mandrakesoft.com> 5.2-6mdk
- add obsoletes tag on libncurses-devel

* Sun Nov 26 2000 Warly <warly@mandrakesoft.com> 5.2-5mdk
- split libraries

* Tue Nov  7 2000 Pixel <pixel@mandrakesoft.com> 5.2-4mdk
- move some doc to -devel

* Fri Nov  3 2000 Warly <warly@mandrakesoft.com> 5.2-3mdk
- fix links again

* Fri Oct 27 2000 Warly <warly@mandrakesoft.com> 5.2-2mdk
- links fix

* Fri Oct 27 2000 Warly <warly@mandrakesoft.com> 5.2-1mdk
- 5.2

* Wed Oct  4 2000 Warly <warly@mandrakesoft.com> 5.1-8mdk
- move xterm-new to xterm waiting for a better solution

* Wed Sep 20 2000 Warly <warly@mandrakesoft.com> 5.1-7mdk
- hum, typo fixes, terminfo comes back (i DO sux)

* Tue Sep 19 2000 Warly <warly@mandrakesoft.com> 5.1-6mdk
- really put ncurses-5.1

* Fri Sep 15 2000 Pixel <pixel@mandrakesoft.com> 5.1-5mdk
- add vt420 and vt510 (tx2Ed :)

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 5.1-4mdk
- move unused terminfo's to extraterms

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 5.1-3mdk
- automatically added BuildRequires

* Wed Jul 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.1-2mdk
- BM
- suprees binary from doc

* Wed Jul 12 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.1-1mdk
- new release
- use new macros

* Wed May 03 2000 Warly <warly@mandrakesoft.com> 5.0-13mdk
- correct links in /lib

* Mon Apr 10 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 5.0-12mdk
- fix license (again) :-/

* Fri Mar 31 2000 Warly <warly@mandrakesoft.com> 5.0-11mdk
- devel group: Development/C

* Fri Mar 31 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 5.0-10mdk
- changed group
- fixed license

* Sun Mar 19 2000 John Buswell <johnb@mandrakesoft.com> 5.0-9mdk
- PPC fixes

* Wed Jan 12 2000 Pixel <pixel@mandrakesoft.com> 5.0-8mdk
- fix for alpha (use egcs instead of gcc-2.95.2)

* Tue Jan 11 2000 Frederic Lepied <flepied@mandrakesoft.com> 5.0-7mdk
- fix xterm entry for 3.3.6

* Sun Dec 25 1999 - David BAUDENS <baudens@mandrakesoft.com>
- Fix build for K6 (another, AMD K6 is not an i686)

* Fri Nov 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add debian term.

* Fri Nov 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add resetall script(r).

* Sun Nov  7 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 5.0 anounced final.

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Wed Sep 29 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- update to 990925

* Mon Sep  6 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- update to 990904

* Fri Jul 16 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Rebuild for new environement (4mdk).

* Mon Jul  5 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- update to 990703

* Wed May 19 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- update to 990516
- Fix the -fomit-frame-pointer problem (using -fno-omit-frame-pointer
  with -pg where needed)

* Mon Apr 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- update to 990410.
- some spec tweaks (yes again ;-))
- removing the patch and build a global ncurses-990410.tar.bz2
- Remove the -fomit-frame-pointer (incompatible with -pg ?)
- Add patch for a bug (?) with two entry in linux-lat.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- add de locale
- update to 990403
- some spec tweaks
- take description + some patches from RH 6.0

* Sun Mar 28 1999 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- update to 990327

* Wed Mar 10 1999 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- update to 990307
- link /lib/libncurses.so* to %{_libdir}

* Sun Feb  7 1999 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- update to 990206

* Fri Jan 15 1999 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- update to 990110
- move libncurses.so.* to /lib, where it belongs (needed by sh)

* Thu Dec 24 1998 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- update to 981220

* Tue Dec 15 1998 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- start with RH release 10
- update to 981212; merge patches in tar file
- bzip2 man pages
- use -fno-omit-frame-pointer -pg rather than just -pg for profiled
  version - that way, we can handle RPM_OPT_FLAGS with -fomit-frame-pointer
- Make compatibility links to libncurses.so.3 (they ARE binary compatible)
- update terminfo file to 10.2.5

* Wed Oct 14 1998 Cristian Gafton <gafton@redhat.com>
- make sure to strip the binaries

* Wed Sep 23 1998 Cristian Gafton <gafton@redhat.com>
- added another zillion of patches. The spec file *is* ugly
- defattr

* Mon Jul 20 1998 Cristian Gafton <gafton@redhat.com>
- added lots of patches. This spec file is starting to look ugly

* Wed Jul 01 1998 Alan Cox <alan@redhat.com>
- Fix setuid trusting. Open termcap/info files as the real user.

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- added terminfo entry for the poor guys using lat1 and/or lat-2 on their
  consoles... Enjoy linux-lat ! Thanks, Erik !

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- new patch to get xterm-color and nxterm terminfo entries
- aliased them to rxvt, as that seems to satisfy everybody

* Sun Apr 12 1998 Cristian Gafton <gafton@redhat.com>
- added %clean section

* Tue Apr 07 1998 Cristian Gafton <gafton@redhat.com>
- removed %{_libdir}/terminfo symlink - we shouldn't need that

* Mon Apr 06 1998 Cristian Gafton <gafton@redhat.com>
- updated to 4.2 + patches
- added BuildRoot

* Sat Apr 04 1998 Cristian Gafton <gafton@redhat.com>
- rebuilt with egcs on alpha

* Wed Dec 31 1997 Erik Troan <ewt@redhat.com>
- version 7 didn't rebuild properly on the Alpha somehow -- no real changes
  are in this version

* Tue Dec 09 1997 Erik Troan <ewt@redhat.com>
- TIOCGWINSZ wasn't used properly

* Tue Jul 08 1997 Erik Troan <ewt@redhat.com>
- built against glibc, linked shared libs against -lc

