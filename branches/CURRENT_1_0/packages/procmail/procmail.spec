%define	name	procmail
%define	version	3.22
%define	release	5sls

Summary:	The procmail mail processing program.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL/Artistic
Group:		System/Servers
URL:		http://www.procmail.org
Source0:	ftp://ftp.procmail.org/pub/procmail/%{name}-%{version}.tar.bz2
Patch1:		%{name}-3.22-lockf.patch.bz2
Patch2:		%{name}-3.22-pixelpb.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root

Provides:	MailTransportAgent

%description
The procmail program is used by Mandrake Linux for all local mail
delivery.  In addition to just delivering mail, procmail can be used
for automatic filtering, presorting and other mail handling jobs.
Procmail is also the basis for the SmartList mailing list processor.

%prep
%setup -q
%patch1 -p1 -b .lockf
%patch2 -p1 -b .warly

find . -type d -exec chmod 755 {} \;

%build
echo -n -e "\n"|  %make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/{man1,man5}

make BASENAME=$RPM_BUILD_ROOT/%{_prefix} install.bin install.man

#move the man pages
mv $RPM_BUILD_ROOT/usr/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1/
mv $RPM_BUILD_ROOT/usr/man/man5/* $RPM_BUILD_ROOT%{_mandir}/man5/

## duplicate in /usr/bin
rm -f examples/mailstat

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%attr(6755,root,mail)	%{_bindir}/procmail
%attr(2755,root,mail)	%{_bindir}/lockfile

%doc FAQ HISTORY README KNOWN_BUGS FEATURES examples

%{_bindir}/formail
%{_bindir}/mailstat

%{_mandir}/man1/*1*
%{_mandir}/man5/*5*

%changelog
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
