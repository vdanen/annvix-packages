#
# spec file for package libtermcap
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		libtermcap
%define version		2.0.8
%define release		%_revrel

%define major		2
%define libname_orig	libtermcap
%define libname		%mklibname termcap %{major}

Summary:	A basic system library for accessing the termcap database
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		ftp://metalab.unc.edu/pub/Linux/GCC/
Source:		termcap-%{version}.tar.bz2
Patch0:		termcap-2.0.8-shared.patch
Patch1:		termcap-2.0.8-setuid.patch
Patch2:		termcap-2.0.8-instnoroot.patch
Patch3:		termcap-2.0.8-compat21.patch
Patch4:		termcap-2.0.8-xref.patch
Patch5:		termcap-2.0.8-fix-tc.patch
Patch6:		termcap-2.0.8-ignore-p.patch
Patch7:		termcap-buffer.patch
# This patch is a REALLY BAD IDEA without patch #10 below....
Patch8:		termcap-2.0.8-bufsize.patch
Patch9:		termcap-2.0.8-colon.patch
Patch10:	libtermcap-aaargh.patch
# (gc) conflicting definition of `bcopy' against latest glibc 2.1.95
Patch11:	termcap-fix-glibc-2.2.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo

Requires:	termcap

%description
The libtermcap package contains a basic system library needed to access
the termcap database.  The termcap library supports easy access to the
termcap database, so that programs can output character-based displays in
a terminal-independent manner.


%package -n %{libname}
Summary:        Development tools for programs which will access the termcap database
Group:          System/Libraries
Obsoletes:	%{libname_orig}
Provides:	%{libname_orig}

%description -n %{libname}
The libtermcap package contains a basic system library needed to access
the termcap database.  The termcap library supports easy access to the
termcap database, so that programs can output character-based displays in
a terminal-independent manner.


%package -n %{libname}-devel
Summary:	Development tools for programs which will access the termcap database
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{libname_orig}-devel
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	termcap-devel = %{version}-%{release}

%description -n %{libname}-devel
This package includes the libraries and header files necessary for
developing programs which will access the termcap database.

If you need to develop programs which will access the termcap database,
you'll need to install this package.  You'll also need to install the
libtermcap package.


%prep
%setup -q -n termcap-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .nochown
%patch3 -p1 -b .compat21
%patch4 -p1
%patch5 -p1 -b .fix-tc
%patch6 -p1 -b .ignore-p
%patch7 -p1 -b .buffer
%patch8 -p1 -b .bufsize
%patch9 -p1 -b .colon
%patch10 -p1 -b .aaargh
%patch11 -p0


%build
%make CFLAGS="%{optflags} -I."


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_lib}
install -m 0755 libtermcap.so.* %{buildroot}/%{_lib}/
ln -s libtermcap.so.2.0.8 %{buildroot}/%{_lib}/libtermcap.so
ln -s libtermcap.so.2.0.8 %{buildroot}/%{_lib}/libtermcap.so.2

mkdir -p %{buildroot}%{_libdir}
install -m 0644 libtermcap.a %{buildroot}%{_libdir}/
ln -s ../../%{_lib}/libtermcap.so.2.0.8 %{buildroot}%{_libdir}/libtermcap.so

mkdir -p %{buildroot}%{_infodir}
install -m 0644 termcap.info* %{buildroot}%{_infodir}/

mkdir -p %{buildroot}%{_includedir}
install -m 0644 termcap.h %{buildroot}%{_includedir}

mkdir -p %{buildroot}%{_sysconfdir}
install -m 0644 termcap.src %{buildroot}%{_sysconfdir}/termcap

rm -f %{buildroot}%{_sysconfdir}/termcap


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libname}-devel
/sbin/install-info \
    --section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
    --info-dir=%{_infodir} %{_infodir}/termcap.info.bz2

%postun -n %{libname}-devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete \
	--section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
	--info-dir=%{_infodir} %{_infodir}/termcap.info.bz2
fi


%files -n %{libname}
%defattr(-,root,root)
%doc ChangeLog README
/%{_lib}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
/%{_lib}/*.so
%{_infodir}/termcap.info*
%{_libdir}/libtermcap.a
%{_libdir}/libtermcap.so
%_includedir/termcap.h


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Fri Jan 06 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8-41avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8-40avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8-39avx
- bootstrap build

* Wed Jun 23 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.0.8-38avx
- Annvix build

* Fri Mar 05 2004 Vincent Danen <vdanen@opensls.org> 2.0.8-37sls
- minor spec cleanups

* Wed Dec 17 2003 Vincent Danen <vdanen@opensls.org> 2.0.8-36sls
- OpenSLS build
- tidy spec

* Mon Aug  4 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.8-35mdk
- Put back libtermcap-devel provides as nobody uses termcap-devel

* Thu Jul 10 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.8-34mdk
- Fix libification, mklibname'ize

* Thu Jan 26 2003 Lenny Cartier <lenny@mandrakesoft.com> 2.0.8-33mdk
- rebuild

* Tue Jun 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.8-32mdk
- rpmlint fixes: hardcoded-library-path

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.0.8-31mdk
- Automated rebuild in gcc3.1 environment

* Mon Jul 30 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.0.8-30mdk
- rebuild

* Sun May 27 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.0.8-29mdk
- build with RPM_OPT_FLAGS

* Mon Mar 26 2001 Pixel <pixel@mandrakesoft.com> 2.0.8-28mdk
- eurk, comments are given to ldconfig in %%post :-(

* Mon Mar 26 2001 Pixel <pixel@mandrakesoft.com> 2.0.8-27mdk
- fixed yet again stupid PreReq on bash (post and postun invocation).

* Fri Mar 23 2001 David BAUDENS <baudens@mandrakesoft.com> 2.0.8-26mdk
- Fix Provides and Obsoletes

* Tue Mar 20 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.8-25mdk
- fix provides and obsoletes

* Mon Mar 19 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.0.8-24mdk
- obsoletes libtermcap

* Sat Mar 17 2001 Lenny Cartier <lenny@mandrakesoft.com> 2.0.8-23mdk
- split

* Fri Jan 12 2001 François Pons <fpons@mandrakesoft.com> 2.0.8-22mdk
- fixed stupid PreReq on bash (post and postun invocation).

* Fri Jan 12 2001 David BAUDENS <baudens@mandrakesoft.com> 2.0.8-21mdk
- BuildRequires: texinfo
- Spec clean up

* Fri Oct 27 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.0.8-20mdk
- fix compile with latest glibc

* Thu Aug 31 2000 Etienne Faure <etienne@mandrakesoft.com> 2.0.8-19mdk
- rebuild with %doc and _infodir macros

* Tue Mar 23 2000 Lenny Cartier <lenny@mandrakesoft.com> 2.0.8-18mdk
- fix group

* Sat Mar  4 2000 Pixel <pixel@mandrakesoft.com> 2.0.8-17mdk
- moved the info to libtermcap-devel
(that way libtermcap doesn't require bash which require libtermcap ;-)
- %trigger transformed in %post

* Mon Dec 20 1999 Jerome Martin <jerome@mandrakesoft.com>
- Rebuild for ne environment

* Wed Nov  3 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- RH merges.
- ignore the first argument to tgetent, so the last change doesn't
  keep blowing up programs.(r)
- ignore the second argument to tgetstr() as well.(r)
- increase default size of malloc'ed tgetent buffer from 1024 to 1536.(r)
- don't shrink colons (r).
- add buffer overflow patch from Kevin Vajk <kvajk@ricochet.net>(r)
- permit multiple tc= continuations and ignore unnecessary %p ("push arg") (r)
- fix to make the texi documenattion compile(r)
- use __PMT(...) prototypes (r)

* Wed Apr 14 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add files /lib/libtermcap.so.2

* Mon Apr 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- add patch to for the termcap.texi with a wrong reference.
- Remove typo with bzip2.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Thu Jan 14 1999 Jeff Johnson <jbj@redhat.com>
- use __PMT(...) prototypes (#761)

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Wed Aug 05 1998 Erik Troan <ewt@redhat.com>
- run install-info from a %trigger so we don't have to make it a prereq; as
  termcap is used by bash, the install ordering issues are hairy
- commented out the chown stuff from 'make install' so you don't have to
  be root to build this
- don't run ldconfig if prefix= is used during 'make install'

* Tue Aug  4 1998 Jeff Johnson <jbj@redhat.com>
- build root.

* Tue Jun 30 1998 Alan Cox <alan@redhat.com>
- But assume system termcap is sane. Also handle setfsuid return right.

* Tue Jun 30 1998 Alan Cox <alan@redhat.com>
- TERMCAP environment hole for setuid apps squished.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 14 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Tue Jun 03 1997 Erik Troan <ewt@redhat.com>
- built against glibc
