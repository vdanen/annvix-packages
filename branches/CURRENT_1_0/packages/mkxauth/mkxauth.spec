%define name	mkxauth
%define version	1.7
%define release	9sls

Summary:	A utility for managing .Xauthority files.
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		File tools
URL:		http://www.tummy.com/krud/packages/mkxauth.html
Source: 	%{name}-%{version}.tar.bz2

BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
BuildArch:	noarch

Requires: 	/usr/X11R6/bin/xauth textutils fileutils sh-utils procps gzip
Prefix: 	%{_prefix}/X11R6

%description
The mkxauth utility helps create and maintain X authentication
databases (.Xauthority files).  Mkxauth is used to create an
.Xauthority file or to merge keys from another local or remote
.Xauthority file.  .Xauthority files are used by the xauth
user-oriented access control program, which grants or denies
access to X servers based on the contents of the .Xauthority
file.

The mkxauth package should be installed if you're going to use
user-oriented access control to provide security for your X Window
System (a good idea).

%prep

%setup

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_prefix}/X11R6/bin
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

install -m 0755 mkxauth $RPM_BUILD_ROOT%{_prefix}/X11R6/bin/mkxauth
install -m 0444 mkxauth.1x.bz2 $RPM_BUILD_ROOT%{_mandir}/man1/mkxauth.1x.bz2

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_prefix}/X11R6/bin/mkxauth
%{_mandir}/man1/*

%changelog
* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 1.7-9sls
- OpenSLS build
- tidy spec

* Sun May 25 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.7-8mdk
- rebuild for rpm 4.2

* Mon Nov 12 2001 Yves Duret <yduret@mandrakesoft.com> 1.7-7mdk
- added url tag and rebuild for sir rpmlint

* Wed Jul 18 2001 Yves Duret <yduret@mandrakesoft.com> 1.7-6mdk
- spec clean up: s#Copyright#License#
- macros : man page, define, source...

* Wed Dec 20 2000 Yves Duret <yduret@mandrakesoft.com> 1.7-5mdk
- macros
- fixed man/lib/bin path according to the FHS.

* Mon Mar 27 2000 Daouda Lo <daouda@mandrakesoft.com> 1.7-4mdk
- fix group

* Mon Nov 29 1999 Florent Villard <warly@mandrakesoft.com>
- better packaging

* Wed May 12 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- Mandrake adaptations

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 11)

* Tue Jan 19 1999 Michael K. Johnson <johnsonm@redhat.com>
- rebuild, change spec file name

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Michael K. Johnson <johnsonm@redhat.com>
- Added more dependency information.

* Thu Jul 31 1997 Erik Troan <ewt@redhat.com>
- made a noarch package
