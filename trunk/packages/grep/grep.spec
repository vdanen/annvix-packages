%define theirversion 2.5.1
%define version 2.5.1
%define _bindir /bin
%define release 3mdk

Summary: The GNU versions of grep pattern matching utilities.
Name: grep
Version: %{version}
Release: %{release}
License: GPL
Group: File tools
Source: ftp://ftp.gnu.org/pub/gnu/grep/%{name}-%{theirversion}.tar.bz2
# Chinese locale
Source10: grep-zh_TW.po.bz2
Source11: grep-zh_CN.GB2312.po.bz2
Patch0: grep-2.5-factorize-egrep-and-fgrep.patch.bz2
Patch1: grep-2.5-i18n-patch.bz2
URL: http://www.gnu.org/software/grep/grep.html
Requires: /%{_lib}/libpcre.so.0
Buildroot: %{_tmppath}/%{name}-root
BuildRequires:	bison 
BuildRequires:	gettext
BuildRequires:	libpcre-devel
BuildRequires:  texinfo

%description
The GNU versions of commonly used grep utilities.  Grep searches one or
more input files for lines which contain a match to a specified pattern
and then prints the matching lines.  GNU's grep utilities include grep,
egrep and fgrep.  

You should install grep on your system, because it is a very useful utility
for searching through text files, for system administration tasks, etc.

%package doc
Summary: Grep documentation in info format
Group: Books/Computer books
Prereq: /sbin/install-info

%description doc
The GNU versions of commonly used grep utilities.  Grep searches one or
more input files for lines which contain a match to a specified pattern
and then prints the matching lines.  GNU's grep utilities include grep,
egrep and fgrep.  

You should install grep on your system, because it is a very useful utility
for searching through text files, for system administration tasks, etc.

Install this package if you want info documentation on grep.

%prep
%setup -q -n %{name}-%{theirversion}
# %patch0 -p0
%patch1 -p1 -b .i18n

%build
%configure2_5x --exec-prefix=/ --without-included-regex
%make

# (gb) why does spencer bre test #16 fails?
# (gw) Spencer test #55 has a syntax error: echo '-'| grep -E -e '(*)b'
# (fpons) removed make check as glibc is bogus currently.
#make -k check || echo "make check failed"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# (gc) works with Patch0: grep-2.4.2-factorize-egrep-and-fgrep.patch.bz2
# ln -s grep $RPM_BUILD_ROOT/bin/egrep
# ln -s grep $RPM_BUILD_ROOT/bin/fgrep

mkdir -p $RPM_BUILD_ROOT%_datadir/locale/{zh_TW.Big5,zh_CN.GB2312}/LC_MESSAGES

bzip2 -dc %SOURCE10 > grep-zh_TW.po 
msgfmt grep-zh_TW.po -o $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW.Big5/LC_MESSAGES/%name.mo

bzip2 -dc %SOURCE11 > grep-zh_CN.po
msgfmt grep-zh_CN.po -o $RPM_BUILD_ROOT%{_datadir}/locale/zh_CN.GB2312/LC_MESSAGES/%name.mo

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS THANKS TODO NEWS README ChangeLog
/bin/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc COPYING
%{_infodir}/*.info*

%post doc
%_install_info %{name}.info

%preun doc
%_remove_install_info %{name}.info

%changelog
* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5.1-3mdk
- Requires: /%{_lib}/libpcre.so.0

* Sat Jul 19 2003 G�tz Waschk <waschk@linux-mandrake.com> 2.5.1-2mdk
- some cleanup
- buildrequires texinfo
- drop buildrequirement on recode

* Wed Jul 16 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.5.1-1mdk
- 2.5.1

* Tue Jan 14 2003 Fran�ois Pons <fpons@mandrakesoft.com> 2.5-7mdk
- split info into separate grep-doc package.

* Mon Nov 11 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.5-6mdk
- LI18NUX/LSB compliance (patch1)

* Fri Aug 16 2002 G�tz Waschk <waschk@linux-mandrake.com> 2.5-5mdk
- fix german translation

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5-4mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Sun Jul 21 2002 Stefan van der Eijk <stefan@eijk.nu> 2.5-3mdk
- BuildRequires

* Tue Jun 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.5-2mdk
- Costlessly make check in %%build stage
- Rebuild with gcc3.1

* Tue Apr  2 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.5-1mdk
- final version
- temporary disable patch #0 (factorize code) because integrated
  upstream, but not remove it from SRPM since it should be reverted
  soon (it offends the GNU standard)

* Sun Feb  3 2002 Frederic Lepied <flepied@mandrakesoft.com> 2.5-0.f.3mdk
- requires a libpcre0 release that has its lib in /lib

* Fri Feb  1 2002 Stefan van der Eijk <stefan@eijk.nu> 2.5-0.f.2mdk
- BuildRequires

* Thu Jan 24 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.5-0.f.1mdk
- unecessary to duplicate "grep" for "egrep" and "fgrep", apply a
  patch to factorize code [Patch #0], saves 200 kbytes in /
- base on RH's grep-2.5-1.f.5.i386.rpm, to get a coloured grep :-), and
  the recent Bero work on grep
  - i18n patches seem integrated upstream
- fix no-url-tag

* Thu Jan 24 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.4.2-10mdk

* Wed Sep 12 2001 Warly <warly@mandrakesoft.com> 2.4.2-9mdk
- change distribution tag

* Sun May 06 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.2-8mdk
- Fix the Chinese locale msgfmt problem with gettext (Abel Cheung).

* Tue May 01 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.2-7mdk
- Add yet another i18n patch.
- We have programs with the Chinese po files. Comment that out for the time
  being (too lazy to fix).

* Sun Jan 28 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 2.4.2-6mdk
- put in Chinese translations.

* Tue Sep 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-5mdk
- Fix %post/%postun (thanks flepied).

* Mon Sep 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-4mdk
- Add patch to get the i18n like the old behavior (rh).

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 2.4.2-3mdk
- use find_lang

* Wed Jul 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-2mdk
- BM.
- Macros.
- CLean-up.

* Thu Mar 30 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.2-1mdk
- Clean up specs.
- Adjust groups.
- 2.4.2.

* Tue Mar  7 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.4.1-1mdk
- 2.4.1.

* Fri Dec  3 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- adjust URL.
- 2.4.

* Tue Nov 02 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Prereq install-info.

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.
- Fix buid as user.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Mon Mar 08 1999 Preston Brown <pbrown@redhat.com>
- upgraded to grep 2.3, added install-info %post/%preun for info

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Sat May 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.2

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- updated from 2.0 to 2.1
- spec file cleanups
- added BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
