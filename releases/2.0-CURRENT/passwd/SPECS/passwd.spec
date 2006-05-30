#
# spec file for package passwd
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		passwd
%define version		0.68
%define release		%_revrel

Summary:	The passwd utility for setting/changing passwords using PAM
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		System/Base
# This url is stupid, someone come up with a better one _please_!
URL:		http://www.freebsd.org
Source0:	passwd-%{version}.tar.bz2
Patch:		passwd-0.67-manpath.patch
Patch1:		passwd-0.68-sec.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	glib2-devel, libuser-devel, pam-devel, popt-devel

Requires:	pam >= 0.59, pwdb >= 0.58, libuser

%description
The passwd package contains a system utility (passwd) which sets
and/or changes passwords, using PAM (Pluggable Authentication
Modules).


%prep


%setup -q
%patch -p1
%patch1 -p0 -b .sec


%build
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_mandir}/man1

%makeinstall_std

install -D -m 0644 passwd.pamd %{buildroot}%{_sysconfdir}/pam.d/passwd
perl -p -i -e 's|use_authtok nullok|use_authtok nullok md5|' %{buildroot}%{_sysconfdir}/pam.d/passwd
rm -f %{buildroot}%{_bindir}/{chfn,chsh}
rm -f %{buildroot}%{_mandir}/man1/{chfn.1,chsh.1}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/pam.d/passwd
%attr(4511,root,root) %{_bindir}/passwd
%{_mandir}/man1/passwd.1*

		
%changelog
* Tue May 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.68
- rebuild against new libuser
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.68
- Clean rebuild

* Mon Jan 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.68
- Obfuscate email addresses and new tagging
- Uncompress patches

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.68-11avx
- rebuild against new glib2.0

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.68-10avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.68-9avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.68-8avx
- rebuild against new libuser and glib2

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.68-7avx
- Annvix build

* Fri Jun 11 2004 Vincent Danen <vdanen@opensls.org> 0.68-6sls
- Requires: libuser, not /etc/libuser.conf

* Mon May 17 2004 Vincent Danen <vdanen@opensls.org> 0.68-5sls
- security fixes from Steve Grubb

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 0.68-4sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 0.68-3sls
- OpenSLS build
- tidy spec

* Mon Jul 21 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.68-2mdk
- rebuild
- rm -rf %{buildroot} at the beginning of %%install
- use %%makeinstall_std macro

* Thu Dec 26 2002 Daouda LO <daouda@mandrakesoft.com> 0.68-1mdk
- release 0.68 
  o implement aging adjustments for pwdb

- patch makefile to not build chfn and chsh (in util-linux).	

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.67-5mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Thu Aug  8 2002 Stefan van der Eijk <stefan@eijk.nu> 0.67-4mdk
- BuildRequires.

* Mon Aug  5 2002 Stew Benedict <sbenedict@mandrakesoft.com> 0.67-3mdk
- Requires: /etc/libuser.conf (thx Goetz Waschk)

* Mon Aug  5 2002 Stew Benedict <sbenedict@mandrakesoft.com> 0.67-2mdk
- Requires: libuser (for /etc/libuser.conf - passwd aging fails - LSB)

* Mon Jul 29 2002 Daouda LO <daouda@mandrakesoft.com> 0.67-1mdk
- 0.67
- rebuilt against latest libuser

* Thu Dec 06 2001 Florin <florin@mandrakesoft.com> 0.64.1-9mdk
- add use_authtok nullok mdk5 in the pam file to use md5 for changing passwords

* Thu Sep 27 2001 Stew Benedict <sbenedict@mandrakesoft.com> 0.64.1-8mdk
- patch to emulate shadow-utils version behavior for LSB compliance

* Mon May 21 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 0.64.1-7mdk
- BuildRequires: pwdb-devel

* Fri Jan 05 2001 David BAUDENS <baudens@mandrakesoft.com> 0.64.1-6mdk
- BuildRequires: pam-devel
- Spec clean up

* Wed Nov 15 2000 Daouda Lo <daouda@mandrakesoft.com> 0.64.1-5mdk 
- make rpmlint happier.
- More macros

* Mon Sep 18 2000 Francis Galiegue <fg@mandrakesoft.com> 0.64.1-4mdk
- More macros
- Let spec helper do its job

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.64.1-3mdk
- automatically added BuildRequires

* Mon Jul 31 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.64.1-2mdk
- BM
- let spechelper compress man-pages

* Mon Apr  3 2000 Adam Lebsack <adam@mandrakesoft.com> 0.64.1-1mdk
- Update to version 0.64.1, from RH 6.2

* Tue Jan 11 2000 Pixel <pixel@linux-mandrake.com>
- fix build as non-root

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 0.63.

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- add de locale

* Wed Feb 03 1999 Cristian Gafton <gafton@redhat.com>
- rebuild for glibc 2.1

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 31 1997 Cristian Gafton <gafton@redhat.com>
- added passwd.1 man page (stolen from SimpleApps-0.56 and modified)
- fixed the Url

* Thu Oct 02 1997 Michael K. Johnson <johnsonm@redhat.com>
- Change to follow new version of PAM standard for pam_strerror().
- BuildRoot

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Wed Apr 23 1997 Michael K. Johnson <johnsonm@redhat.com>
- Fix patch so that we actually USE the more intelligent getlogin() again.

* Tue Apr 22 1997 Michael K. Johnson <johnsonm@redhat.com>
- Don't default to migrating passwords to /etc/shadow

* Mon Apr 21 1997 Michael K. Johnson <johnsonm@redhat.com>
- Also link against pwdb to use its more intelligent getlogin().

* Tue Apr 15 1997 Michael K. Johnson <johnsonm@redhat.com>
- Change passwords even if getlogin() can't find the login name.

* Mon Mar 03 1997 Michael K. Johnson <johnsonm@redhat.com>
- Moved from pam.conf to pam.d

