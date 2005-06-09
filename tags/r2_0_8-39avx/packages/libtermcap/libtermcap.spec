%define name	libtermcap
%define version	2.0.8
%define release	39avx

%define lib_major	2
%define lib_name_orig	libtermcap
%define lib_name	%mklibname termcap %{lib_major}

Summary:	A basic system library for accessing the termcap database
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Libraries
URL:		ftp://metalab.unc.edu/pub/Linux/GCC/
Source:		termcap-%{version}.tar.bz2
Patch0:		termcap-2.0.8-shared.patch.bz2
Patch1:		termcap-2.0.8-setuid.patch.bz2
Patch2:		termcap-2.0.8-instnoroot.patch.bz2
Patch3:		termcap-2.0.8-compat21.patch.bz2
Patch4:		termcap-2.0.8-xref.patch.bz2
Patch5:		termcap-2.0.8-fix-tc.patch.bz2
Patch6:		termcap-2.0.8-ignore-p.patch.bz2
Patch7:		termcap-buffer.patch.bz2
# This patch is a REALLY BAD IDEA without patch #10 below....
Patch8:		termcap-2.0.8-bufsize.patch.bz2
Patch9:		termcap-2.0.8-colon.patch.bz2
Patch10:	libtermcap-aaargh.patch.bz2
# (gc) conflicting definition of `bcopy' against latest glibc 2.1.95
Patch11:	termcap-fix-glibc-2.2.patch.bz2

BuildRoot:	%_tmppath/%name-%version-%release-root
BuildRequires:	texinfo

Requires:	%_sysconfdir/termcap

%description
The libtermcap package contains a basic system library needed to access
the termcap database.  The termcap library supports easy access to the
termcap database, so that programs can output character-based displays in
a terminal-independent manner.

%package -n %{lib_name}
Summary:        Development tools for programs which will access the termcap database
Group:          System/Libraries
Obsoletes:	%{lib_name_orig}
Provides:	%{lib_name_orig}

%description -n %{lib_name}
The libtermcap package contains a basic system library needed to access
the termcap database.  The termcap library supports easy access to the
termcap database, so that programs can output character-based displays in
a terminal-independent manner.

%package -n %{lib_name}-devel
Summary:	Development tools for programs which will access the termcap database
Group:		Development/C
Requires:	%{lib_name} = %version-%release
Obsoletes:	%{lib_name_orig}-devel
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	termcap-devel = %{version}-%{release}

%description -n %{lib_name}-devel
This package includes the libraries and header files necessary for
developing programs which will access the termcap database.

If you need to develop programs which will access the termcap database,
you'll need to install this package.  You'll also need to install the
libtermcap package.

%prep
%setup -q -n termcap-2.0.8
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
%make CFLAGS="$RPM_OPT_FLAGS -I."

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
# (gb) They should do proper Makefiles

mkdir -p $RPM_BUILD_ROOT/%{_lib}
install -m 755 libtermcap.so.* $RPM_BUILD_ROOT/%{_lib}/
ln -s libtermcap.so.2.0.8 $RPM_BUILD_ROOT/%{_lib}/libtermcap.so
ln -s libtermcap.so.2.0.8 $RPM_BUILD_ROOT/%{_lib}/libtermcap.so.2

mkdir -p $RPM_BUILD_ROOT%{_libdir}
install -m 644 libtermcap.a $RPM_BUILD_ROOT%{_libdir}/
ln -s ../../%{_lib}/libtermcap.so.2.0.8 $RPM_BUILD_ROOT%{_libdir}/libtermcap.so

mkdir -p $RPM_BUILD_ROOT%{_infodir}
install -m 644 termcap.info* $RPM_BUILD_ROOT%{_infodir}/

mkdir -p $RPM_BUILD_ROOT%{_includedir}
install -m 644 termcap.h $RPM_BUILD_ROOT%{_includedir}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 termcap.src $RPM_BUILD_ROOT%{_sysconfdir}/termcap

rm -f $RPM_BUILD_ROOT%_sysconfdir/termcap

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

# pixel: KEEP LDCONFIG WITH "-p" OR COME TALK TO ME 
%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%post -n %{lib_name}-devel
/sbin/install-info \
	--section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
	--info-dir=%{_infodir} %{_infodir}/termcap.info.bz2

%postun -n %{lib_name}-devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete \
	--section="Libraries" --entry="* Termcap: (termcap).               The GNU termcap library." \
	--info-dir=%{_infodir} %{_infodir}/termcap.info.bz2
fi

%files -n %{lib_name}
%defattr(-,root,root)
%doc ChangeLog README
/%{_lib}/*.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
/%{_lib}/*.so
%{_infodir}/termcap.info*
%_libdir/libtermcap.a
%_libdir/libtermcap.so
%_includedir/termcap.h

%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 2.0.8-39avx
- bootstrap build

* Wed Jun 23 2004 Vincent Danen <vdanen@annvix.org> 2.0.8-38avx
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
