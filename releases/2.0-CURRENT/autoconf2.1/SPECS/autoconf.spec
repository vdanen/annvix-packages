#
# spec file for package autoconf2.1
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		%{pkgname}2.1
%define pkgname		autoconf
%define version		2.13
%define release 	%_revrel
%define epoch		1

# Factorize uses of autoconf libdir home and handle only one exception in rpmlint
%define scriptdir	%{_datadir}/autotools

# we need to patch out the 3 F77 tests before we can re-enable this
%define docheck 0
%{?_without_check: %global docheck 0}

Summary:	A GNU tool for automatically configuring source code
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/autoconf/
Source:		ftp://ftp.gnu.org/pub/gnu/%{pkgname}/%{pkgname}-%{version}.tar.bz2
Source3:	autoconf_special_readme2.1
Patch0:		autoconf-2.12-race.patch
Patch1:		autoconf-2.13-mawk.patch
Patch2:		autoconf-2.13-notmp.patch
Patch3:		autoconf-fix-for-gcc2.96-patch
Patch4:		autoconf-2.13-versioned-info.patch
Patch5:		autoconf-2.13-automake14.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch
BuildRequires:	texinfo m4

Requires(post):	info-install
Requires(preun): info-install
Requires:	gawk, m4, mktemp
Requires:	%{scriptdir}/ac-wrapper.pl
Conflicts:	autoconf2.5 <= 1:2.59-2avx
Obsoletes:	autoconf <= 1:2.13-22avx
Provides:	autoconf = %{epoch}:%{version}-%{release}
# for tests
%if %{docheck}
BuildRequires:	bison, flex
%endif


%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to 
specify various configuration options.

You should install Autoconf if you are developing software and you'd
like to use it to create shell scripts which will configure your 
source code packages. If you are installing Autoconf, you will also
need to install the GNU m4 package.

Note that the Autoconf package is not required for the end user who
may be configuring software with an Autoconf-generated script; 
Autoconf is only required for the generation of the scripts, not
their use.

%{expand:%(cat %{SOURCE3})}


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1 -b .parallel
%patch5 -p1 -b .automake14
install -m 0644 %{SOURCE3} IMPORTANT.README.Annvix


%build
%configure --program-suffix=-%{version}
%make


%check
%if %{docheck}
make check     # VERBOSE=1
%endif


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall

mv %{buildroot}%{_infodir}/autoconf.info %{buildroot}%{_infodir}/autoconf-%{version}.info

# We don't want to include the standards.info stuff in the package,
# because it comes from binutils...
rm -f %{buildroot}%{_infodir}/standards*
cp install-sh %{buildroot}%{_datadir}/autoconf


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info autoconf-%{version}.info


%preun
%_remove_install_info autoconf-%{version}.info


%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/%{pkgname}
%{_infodir}/*

%files doc
%defattr(-,root,root)
%doc README IMPORTANT.README.Annvix


%changelog
* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.13
- add -doc subpackage
- fix pre-req

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.13
- Clean rebuild

* Fri Dec 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.13
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Aug 18 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.13-25avx
- bootstrap build (new gcc, new glibc)
- disable the tests for now until we can patch out for F77/fortran
  tests since they always fail since we don't ship a fortran compiler

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.13-24avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.13-23avx
- now known as autoconf2.1
- wrapper script is in autoconf2.5
- add --with-check option to enable make check
- P5: invoke automake-1.4 and aclocal-1.4 instead of random (abel)
- version of automake/aclocal in autoreconf (abel)
- do make check

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.13-22avx
- Annvix build
- require packages not files

* Sun Feb 29 2004 Vincent Danen <vdanen@opensls.org> 2.13-21sls
- more spec cleanups

* Sat Dec 13 2003 Vincent Danen <vdanen@opensls.org> 2.13-20sls
- OpenSLS build
- tidy spec

* Tue Aug 19 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-19mdk
- own /usr/lib/autoconf, thx to markus pilzecker <pilzecker at free.fr>

* Mon Aug 11 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-18mdk
- autoconf-2.13-talk-about-2.5x-in-info (#4698)

* Fri Apr 11 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-17mdk
- per suggestion of fcrozat, include description info (about the two
  versions of autoconf coexisting) in a readme file

* Thu Feb 27 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-16mdk
- autoconf 2.57 now says "Generated by GNU Autoconf" adding "GNU", patch
  the detection accordingly

* Tue Oct  8 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-15mdk
- merge work on ac-wrapper.pl by gentoo
  - it can work with AC_PREREQ([2.13]) as well as AC_PREREQ(2.13)
  - also check aclocal.m4 for an AC_PREREQ

* Wed Jul 31 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13-14mdk
- Forcibly let ac-wrapper.pl in %{_prefix}/lib/autoconf/. Otherwise,
  the package is no longer noarch

* Wed Jul 31 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.13-13mdk
- rpmlint fixes: hardcoded-library-path

* Tue Apr 16 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-12mdk
- update the `ac-wrapper.pl' script which detects which version of
  autoconf will be automatically selected, adding two cases for
  selecting the 2.5x version:
  - `configure' is already present and was generated by autoconf
    greater than '2.1'
  - `Makefile.in' was generated by automake-1.6 or superior (which
    specifically needs autoconf-2.5x)

* Sat Nov 10 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.13-11mdk
- BuildRequires: m4

* Wed Oct 24 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-10mdk
- manage co-existance of 2.5x through ac-wrapper.pl

* Thu Aug 30 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-9mdk
- rebuild to change distribution tag

* Tue May 01 2001 David BAUDENS <baudens@mandrakesoft.com> 2.13-8mdk
- Use %%{_buildroot} for BuildRoot

* Mon Oct 16 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-7mdk
- fix for compiling c++ code with gcc-2.96 in some cases

* Thu Aug 24 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-6mdk
- rebuild to fix %preun script (pixel sucks)

* Wed Aug 23 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-5mdk
- automatically added packager tag

* Tue Jul 18 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-4mdk
- macros for install-info

* Mon Jul 10 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-3mdk
- cleanup and macros

* Fri Mar 31 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 2.13-2mdk
- new groups

* Mon Mar  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 2.13-1mdk
- Back to last 2.13 and stable version, add a serial.

* Wed Oct 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge change of Jeff package.

* Thu May 13 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- 2.14.1

* Fri Mar 26 1999 Cristian Gafton <gafton@redhat.com>
- add patch to help autoconf clean after itself and not leave /tmp clobbered
  with acin.* and acout.* files (can you say annoying?)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)
- use gawk, not mawk

* Thu Mar 18 1999 Preston Brown <pbrown@redhat.com>
- moved /usr/lib/autoconf to /usr/share/autoconf (with automake)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Tue Jan 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 2.13.

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Mon Oct 05 1998 Cristian Gafton <gafton@redhat.com>
- requires perl

* Thu Aug 27 1998 Cristian Gafton <gafton@redhat.com>
- patch for fixing /tmp race conditions

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- spec file cleanups
- made a noarch package
- uses autoconf
- uses install-info

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- built with glibc


# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
