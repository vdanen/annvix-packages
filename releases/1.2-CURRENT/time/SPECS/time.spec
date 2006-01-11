#
# spec file for package time
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		time
%define version		1.7
%define release		%_revrel

Summary:	A GNU utility for monitoring a program's use of system resources
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Monitoring
URL:		http://www.gnu.org/directory/GNU/time.html
Source:		http://ftp.gnu.org/pub/gnu/time/%{name}-%{version}.tar.bz2
Patch0:		time-1.7.info.patch
Patch1:		time-1.7-ressource.patch
Patch2:		time-1.7-quiet.1.patch
Patch3:		time-1.7-fixinfo.patch 
Patch4:		time-1.7-build.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	texinfo

Requires(post):	info-install
Requires(preun): info-install

%description
The GNU time utility runs another program, collects information about
the resources used by that program while it is running and
displays the results.

Time can help developers optimize their programs.

The resources that `time' can report on fall into the general
categories of time, memory, I/O, and IPC calls.

The GNU version can format the output in arbitrary ways by using a 
printf-style format string to include various resource measurements.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p0

export FORCE_AUTOCONF_2_5=1
aclocal-1.4
autoconf
automake-1.4 -a
autoheader


%build
%configure
make LDFLAGS=-s


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info

%preun
%_remove_install_info %{name}.info


%files
%defattr(-,root,root)
%doc NEWS README
%{_bindir}/time
%{_infodir}/%{name}.info*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sun Oct 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7-31avx
- fix requires

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7-30avx
- bootstrap build (new gcc, new glibc)

* Sat Jun 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.7-29avx
- bootstrap build
- force use of autoconf2.5 and automake-1.4 (peroyvind)
- spec cleanups

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.7-28avx
- require info-install rather than a file
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 1.7-27sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 1.7-26sls
- OpenSLS build
- tidy spec

* Mon Apr 07 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.7-25mdk
- force install ordering for post-scripts (#3413)

* Fri Jan 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.7-24mdk
- build release

* Tue Oct 29 2002 Stefan van der Eijk <stefan@eijk.nu> 1.7-23mdk
- change URL to projects current location (Yura Gusev)

* Tue Oct 29 2002 Stefan van der Eijk <stefan@eijk.nu> 1.7-22mdk
- BuildRequires: texinfo

* Mon Oct 28 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.7-21mdk
- patch 1 : remove jeff hack, better use sys/resource.h,
  fix build on alpha btw
- patch 2 : add -q|--quiet option
- patch 3 : fix info entry
- patch 4 : fix build system

* Mon Oct 28 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.7-21mdk
- enhanced description

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.7-20mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Wed May 22 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.7-19mdk
- remove useless prefix
- sanitize

* Mon Jun 25 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 1.7-18mdk
- patch configure.in to workaround broken wait3 check.
- regenerate autoconf/automake on every build, to enable
  new patched configure.in.
- use acconfig.h for two missing autoconf's symbols.

* Fri Sep  1 2000 Pixel <pixel@mandrakesoft.com> 1.7-17mdk
- fix info

* Fri Jul 28 2000 Francis Galiegue <fg@mandrakesoft.com> 1.7-16mdk
- Use %*info* macros

* Thu Jul 27 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.7-15mdk
- BM

* Tue Jun 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.7-14mdk
- Use makeinstall macros.

* Wed Apr 05 2000 John Buswell <johnb@mandrakesoft.com> 1.7-13mdk
- fixed vendor tag

* Thu Mar 30 2000 John Buswell <johnb@mandrakesoft.com> 1.7-12mdk
- Fixed group
- spec-helper

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Build release.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Mon Aug 10 1998 Erik Troan <ewt@redhat.com>
- buildrooted and defattr'd

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 27 1997 Cristian Gafton <gafton@redhat.com>
- fixed info handling

* Thu Oct 23 1997 Cristian Gafton <gafton@redhat.com>
- updated the spec file; added info file handling

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
