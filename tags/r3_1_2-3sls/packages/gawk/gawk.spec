%define name	gawk
%define version	3.1.2
%define release	3sls

Summary:	The GNU version of the awk text processing utility.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Text tools
URL:		http://www.gnu.org/software/gawk/gawk.html
Source0:	http://ftp.gnu.org/gnu/gawk/%{name}-%{version}.tar.bz2
Source1:	http://ftp.gnu.org/gnu/gawk/%{name}-%{version}-ps.tar.bz2
#Patch0:	gawk-3.1.0-debian-security.patch.bz2
Patch1:		gawk-3.1.2-replace-hardlinks-with-softlinks.patch.bz2
Patch2:		gawk-3.1.2-pgawk.patch.bz2
Patch3:		gawk-3.1.2-proc.patch.bz2
Patch4:		gawk-3.1.2-regex.patch.bz2
#Patch:		gawk-3.0-unaligned.patch.bz2
# i18n.
#Patch100:	gawk-3.06-i18n-0.2.patch.bz2
#this patch does not work!

BuildRoot:	%{_tmppath}/%{name}-root

Provides:	awk
Prereq:		/sbin/install-info
Prefix:		%{_prefix}

%description
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs. Gawk should
be upwardly compatible with the Bell Labs research version of awk and
is almost completely compliant with the 1993 POSIX 1003.2 standard for
awk.

Install the gawk package if you need a text processing utility. Gawk is
considered to be a standard Linux tool for processing text.

%package doc
Summary: Documentation about the GNU version of the awk text processing utility
Group: Books/Computer books

%description doc
The gawk packages contains the GNU version of awk, a text processing
utility.  Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs. Gawk should
be upwardly compatible with the Bell Labs research version of awk and
is almost completely compliant with the 1993 POSIX 1003.2 standard for
awk.

%prep
%setup -q -b 1
#%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
#%patch100 -p1 -b .i18n

%build
%configure
%make

# all tests must pass
make check

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall  bindir=$RPM_BUILD_ROOT/bin
%find_lang %{name}

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cd $RPM_BUILD_ROOT%{_datadir}
mkdir awk && 
for  i in *.awk;do
mv -f $i awk
done
cd $RPM_BUILD_ROOT%{_mandir}
mkdir -p man1
for i in *;do
   mv -f $i man1 || true
done
cd man1
ln -sf gawk.1.bz2 awk.1.bz2
cd $RPM_BUILD_ROOT%{_bindir}
ln -sf ../../bin/awk $RPM_BUILD_ROOT%{_bindir}/awk 
ln -sf ../../bin/gawk $RPM_BUILD_ROOT%{_bindir}/gawk 
mv $RPM_BUILD_ROOT/bin/pgawk $RPM_BUILD_ROOT%{_bindir}
rm -f $RPM_BUILD_ROOT/bin/pgawk-%{version}

%post
%_install_info gawk.info

%preun
%_remove_install_info gawk.info

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
/bin/*
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*
%{_libdir}/*
%{_datadir}/awk

%files doc
%defattr(-,root,root)
%doc README COPYING FUTURES INSTALL LIMITATIONS NEWS
%doc README_d POSIX.STD doc/gawk.ps doc/awkcard.ps

%changelog
* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 3.1.2-3sls
- OpenSLS build
- tidy spec

* Mon Nov 17 2003 Vincent Danen <vdanen@mandrakesoft.com> 3.1.2-2.1.92mdk
- added patch from Luca Berra <bluca@vodka.it> to fix segfault when 
  using character classes and locale

* Fri Apr 18 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.2-2mdk
- use rawhide patch to fix parsing of /proc pseudo-files

* Thu Apr 17 2003 Aurelien Lemaire <alemaire@mandrakesoft.com> 3.1.2-1mdk
- New version 3.1.2
- Update Sources Url
- Delete Patch0 : imposible to update this patch
- Update Patch1 to new version
- Add patch2 to fix typo

* Sat Jan 18 2003 Stefan van der Eijk <stefan@eijk.nu> 3.1.1-5mdk
- removed missing files from %%doc (ACKNOWLEDGMENT PORTS)
- add LC_MESSAGES files (unpackaged files)

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.1.1-4mdk
- fix doc subpackage group

* Wed Jul 10 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.1-3mdk
- Costlessly make check in %%build stage

* Fri May 10 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.1-2mdk
- replace hard link from /usr/bin to /bin by soft link to fix problems
  of people having separate /usr (patch #1)

* Thu May  9 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.1-1mdk
- new version
- remove the reducing of optimizations since gcc seems less buggy now

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 3.1.0-4mdk
- Automated rebuild in gcc3.1 environment

* Sun Jan 20 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.0-3mdk
- reduce optimizations to remove gcc bug which makes awk thinking
  that 3 < 2

* Thu Jan 17 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 3.1.0-2mdk
- move pgawk (profiling gawk) from /bin to /usr/bin
- take Debian security patch for igawk (thx pixel), but bugfix the
  patch :-)
- fix no-url-tag

* Fri Jul 06 2001 Etienne Faure <etienne@mandrakesoft.com> 3.1.0-1mdk
- version 3.1.0

* Fri May 04 2001 Etienne Faure <etienne@mandrakesoft.com> 3.0.6-4mdk
- Removed i18n patch

* Tue May 02 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.0.6-3mdk
- I18N patch.

* Sat Jan 20 2001 Etienne Faure  <etienne@mandrakesoft.com> 3.0.6-2mdk
- fixed small things to make rpmlint happy

* Wed Aug 09 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.0.6-1mdk
- s|3.0.5|3.0.6|.

* Sun Aug 06 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 3.0.5-2mdk
- some more macroszifications
- BM 

* Sat Jul 22 2000 Geoffrey Lee <snailtalk@linux-mandrake.com> 3.0.5-1mdk
- new version
- macros
- provides: awk

* Fri Jun 09 2000 Etienne Faure <etienne@mandrakesoft.com> 3.0.4-3mdk
-rebuild on kenobi

* Sat Apr 08 2000 John Buswell <johnb@mandrakesoft.com> 3.0.4-2mdk
- fixed distribution tag

* Thu Mar 30 2000 John Buswell <johnb@mandrakesoft.com> 3.0.4-1mdk
- 3.0.4 
- fixed groups
- spec helper

* Mon Nov 22 1999 Pixel <pixel@linux-mandrake.com>
- moved the doc to gawk-doc

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add defattr.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Fri Feb 19 1999 Jeff Johnson <jbj@redhat.com>
- Install info pages (#1242).

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1
- don't package /usr/info/dir

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 3.0.3
- added documentation and buildroot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

