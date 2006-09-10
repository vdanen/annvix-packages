#
# spec file for package cdialog
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		cdialog
%define version		0.9b
%define release		%_revrel

%define datetag 	20040421

Summary:	A utility for creating TTY dialog boxes
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://invisible-island.net/dialog/
Source:		dialog-%{version}-%{datetag}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel

Obsoletes:	dialog
Provides:	dialog

%description
Dialog is a utility that allows you to show dialog boxes (containing
questions or messages) in TTY (text mode) interfaces.  Dialog is called
from within a shell script.  The following dialog boxes are implemented:
yes/no, menu, input, message, text, info, checklist, radiolist, and
gauge.  


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n dialog-%{version}-%{datetag}


%build
%configure
%make OPTIM="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
%makeinstall \
    BINDIR=%{buildroot}%{_bindir} \
    MANDIR=%{buildroot}%{_mandir}/man1


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/dialog
%{_mandir}/man1/dialog.1*

%files doc
%defattr(-,root,root)
%doc COPYING README samples


%changelog
* Tue Jun 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9b
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9b
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9b
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9b-10avx
- version 0.9b-20040421

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9b-9avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9b-8avx
- bootstrap build

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9b-7avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 0.9b-6sls
- minor spec cleanups

* Thu Dec 18 2003 Vincent Danen <vdanen@opensls.org> 0.9b-5sls
- OpenSLS build
- tidy spec

* Sun Jun  8 2003 Stefan van der Eijk <stefan@eijk.nu> 0.9b-4mdk
- BuildRequires

* Thu Apr  3 2003 Stew Benedict <sbenedict@mandrakesoft.com> 0.9b-3mdk
- update to 20030308

* Mon Dec 30 2002 Stew Benedict <sbenedict@mandrakesoft.com> 0.9b-2mdk
- update to 20020814

* Mon Jun 24 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.9b-1mdk
- New version 0.9b.
- Removed Patch0, merged upstream.
- Removed Patch2, merged upstream.
- Added URL.

* Mon May 27 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.9a-9mdk
- rebuild.
- add patch2 (to print usage without segfaulting).

* Sat Nov  3 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.9a-8mdk
- build with RPM_OPT_FLAGS

* Mon Aug 13 2001 DindinX <odin@mandrakesoft.com> 0.9a-7mdk
- rebuilt

* Wed Dec 27 2000 Vincent Danen <vdanen@mandrakesoft.com> 0.9a-6mdk
- security fix: insecure lock files
- more macros

* Wed Aug 09 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.9a-5mdk
- rebuild for hte macros Stefan: the patch didn't work ... :-(

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.9a-4mdk
- automatically added BuildRequires

* Sat Mar 25 2000 Daouda Lo <daouda@mandrakesoft.com> 0.9a-3mdk
- fix group 

* Sun Nov 28 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- put all make's in the %%build section

* Sun Jul 18 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- cdialog 0.9a
- remove some patches

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 14)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Thu May 7 1998 Michael Maher <mike@redhat.com> 
- Added Sean Reifschneider <jafo@tummy.com> patches for 
  infinite loop problems.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 15 1998 Erik Troan <ewt@redhat.com>
- built against new ncurses

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
