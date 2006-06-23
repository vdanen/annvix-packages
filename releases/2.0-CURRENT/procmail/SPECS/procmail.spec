#
# spec file for package procmail
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define	revision	$Rev$
%define	name		procmail
%define	version		3.22
%define	release		%_revrel

Summary:	The procmail mail processing program
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL/Artistic
Group:		System/Servers
URL:		http://www.procmail.org
Source0:	ftp://ftp.procmail.org/pub/procmail/%{name}-%{version}.tar.bz2
Patch1:		%{name}-3.22-lockf.patch
Patch2:		%{name}-3.22-pixelpb.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}

Provides:	MailTransportAgent

%description
The procmail program can be used for all local mail delivery.  In
addition to just delivering mail, procmail can be used for automatic
filtering, presorting and other mail handling jobs.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch1 -p1 -b .lockf
%patch2 -p1 -b .warly

find . -type d -exec chmod 755 {} \;


%build
echo -n -e "\n"|  %make CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_mandir}/{man1,man5}

make BASENAME=%{buildroot}/%{_prefix} install.bin install.man

#move the man pages
mv %{buildroot}/usr/man/man1/* %{buildroot}%{_mandir}/man1/
mv %{buildroot}/usr/man/man5/* %{buildroot}%{_mandir}/man5/

## duplicate in /usr/bin
rm -f examples/mailstat


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%attr(6755,root,mail) %{_bindir}/procmail
%attr(2755,root,mail) %{_bindir}/lockfile
%{_bindir}/formail
%{_bindir}/mailstat
%{_mandir}/man1/*1*
%{_mandir}/man5/*5*

%files doc
%defattr(-,root,root)
%doc FAQ HISTORY README KNOWN_BUGS FEATURES examples


%changelog
* Thu Jun 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.22
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.22
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.22
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix description

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.22-9avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.22-8avx
- rebuild

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 3.22-7avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.22-6sls
- minor spec cleanups

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 3.22-5sls
- OpenSLS build
- tidy spec

* Sat Jul 12 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 3.22-4mdk
- rebuild
- cosmetics
- drop useless Prefix tag

* Thu Jan 10 2002 Warly <warly@mandrakesoft.com> 3.22-3mdk
- rpmlint fixes

* Thu Nov 29 2001 Warly <warly@mandrakesoft.com> 3.22-2mdk
- fix the pixel segfault pb

* Tue Sep 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.22-1mdk
- Make a build from a new and shiny source.
- Port the old lockf patch to 3.22 (Do we still need it?).

* Sun Jul 01 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.21-1mdk
- Build a new and shiny source.
- It is dually licensed under the GPL v2 and Artistic, we love the GPL, blah.

* Tue Jan 23 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.15.1-2mdk
- remove the mailstat script from the examples directory  (chmou).

* Thu Jan 11 2001 Geoff <snailtalk@mandrakesoft.com> 3.15.1-1mdk
- new and shiny source.
- build with our own optimizations.

* Mon Nov 13 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 3.15-1mdk
- new and shiny release.
- add a url for this package.

* Wed Oct 11 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.14-4mdk
- provide MailTransportAgentMailTransportAgent for fetchmail

* Thu Aug 31 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 3.14-3mdk
- Copyright: Artistic

* Wed Aug 30 2000  Etienne Faure <etienne@mandrakesoft.com> 3.14-2mdk
- rebuilt with new %doc and _mandir macro

* Sat Jul  1 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.14-1mdk
- 3.14.
- macroszification.

* Sun May 07 2000 Jerome Martin <jerome@mandrakesoft.com> 3.13.1-6mdk
- Fixing groups, spec-helper and distribution tag

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- merge with rh changes.
- turn on GROUP_PER_USER(r).
- fix doc perms(r).

* Thu Apr  8 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- 3.13.1
- Mandrake adaptions
- bzip2 man pages
- fix handling of RPM_OPT_FLAGS
- get rid of "press return to continue"
- add de locale

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
