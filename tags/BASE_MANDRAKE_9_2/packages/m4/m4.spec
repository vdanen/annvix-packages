%define name m4
%define version 1.4ppre2
%define release 4mdk

Summary: The GNU macro processor.
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Group: Development/Other
Url: http://www.seindal.dk/rene/gnu/
Source: ftp://ftp.gnu.org/pub/gnu/m4-1.4.tar.bz2
Patch: m4-1.4-glibc.patch.bz2
Buildroot: %{_tmppath}/%{name}-buildroot
Prereq: /sbin/install-info

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

Install m4 if you need a macro processor.

%prep
%setup -n %name-1.4

%patch -p1

%build

# m4 configure script doesn't support rpm's configure macro,
# so we sanitize the command line as much as possible
CFLAGS="$RPM_OPT_FLAGS" ./configure i586-mandrake-linux --prefix=%_prefix --exec-prefix=%_prefix 

%make

make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%files
%defattr(-,root,root)
%doc NEWS README COPYING BACKLOG INSTALL THANKS ChangeLog
%{_bindir}/m4
%{_infodir}/*

%post
/sbin/install-info %{_infodir}/m4.info.bz2 %{_infodir}/dir

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/m4.info.bz2 %{_infodir}/dir
fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jul 23 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 1.4ppre2-4mdk
- rebuild
- rm -rf $RPM_BUILD_ROOT in %%install, not %%prep

* Thu Jan 16 2003 Lenny Cartier <lenny@mandrakesoft.com> 1.4ppre2-3mdk
- rebuild

* Thu Jan 17 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.4ppre2-2mdk
- url

* Fri Jul 27 2001 Lenny Cartier <lenny@mandrakesoft.com> 1.4ppre2-1mdk
- updated to 1.4ppre2

* Thu Dec  7 2000 Jeff Garzik <jgarzik@mandrakesoft.com> 1.4-19mdk
- Run automated tests at build time
- Use RPM_OPT_FLAGS.  Damn, who forgot that one.

* Fri Nov 10 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.4-18mdk
- build for gcc-2.96

* Tue Aug 29 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.4-17mdk
- BM

* Wed Mar 22 2000 Lenny Cartier <lenny@mandrakesoft.com> 1.4-16mdk
- spechelper fixes
- group fix

* Wed Nov  3 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.
- Fix building as user.

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- Manhattan build

* Wed Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- added info file handling and BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

