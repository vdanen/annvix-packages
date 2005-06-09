%define name	termcap
%define version 11.0.1
%define release 12avx

Summary:	The terminal feature database used by certain applications.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	none
Group:		System/Libraries
Source0:	http://www.ccil.org/~esr/terminfo/termtypes.tc.bz2
Patch0:		termcap-linuxlat.patch.bz2
Patch1:		termcap-xtermchanges.patch.bz2
Patch2:		termcap-utf8.patch.bz2
# (fc) 11.0.1-4mdk patch to correctly handle Home/End with X11R6 keycode
Patch3:		termcap-xtermX11R6.patch.bz2
# (vdanen) 11.0.1-6mdk patch so Eterm is seen as a color-capable term
Patch4:		termcap-Eterm.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root

%ifarch sparc
Obsoletes:	termfiles_sparc
Provides:	termfiles_sparc
%endif

%description
The termcap package provides the /etc/termcap file.  /etc/termcap is
a database which defines the capabilities of various terminals and
terminal emulators.  Certain programs use the /etc/termcap file to
access various features of terminals (the bell, colors, and graphics,
etc.).

%prep

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
bzcat %{SOURCE0} > $RPM_BUILD_ROOT%{_sysconfdir}/termcap
pushd $RPM_BUILD_ROOT%{_sysconfdir} && {
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
} && popd
# Remove unpackaged file(s)
rm -rf	$RPM_BUILD_ROOT%{_sysconfdir}/termcap.orig

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/termcap

%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 11.0.1-12avx
- bootstrap build

* Sat Jun 19 2004 Vincent Danen <vdanen@annvix.org> 11.0.1-11avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 11.0.1-10sls
- minor spec cleanups

* Tue Dec 09 2003 Vincent Danen <vdanen@opensls.org> 11.0.1-9sls
- OpenSLS build
- tidy spec

* Thu Jul 24 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 11.0.1-8mdk
- rebuild
- fix use-of-RPM_SOURCE_DIR (rpmlint)

* Sun Jan 19 2003 Stefan van der Eijk <stefan@eijk.nu>  11.0.1-7mdk
- Remove unpackaged file(s)
- Copyright --> License

* Fri Aug 23 2002 Vincent Danen <vdanen@mandrakesoft.com> 11.0.1-6mdk
- P4 so that Eterm is seen as a color-capable terminal

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 11.0.1-5mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Thu Mar 22 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 11.0.1-4mdk
- Patch 3 to correctly handle X11R6 Home/End key (for GNOME/KDE)

* Thu Aug 10 2000 Frederic Crozat <fcrozat@mandrakesoft.com> 11.0.1-3mdk
- Add noreplace to make rpmlint happy

* Wed Jun 28 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 11.0.1-2mdk
- compatibility-mode UTF-8 patch from <Alastair.McKinstry@compaq.com>

* Thu Apr  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 11.0.1-1mdk
- Fix xterm backspace suppr...
- 11.0.1

* Thu Mar 23 2000 Daouda Lo <daouda@mandrakesoft.com> 10.2.6-2mdk
- fix group 

* Fri Nov 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 10.2.6.
- Add support for xterm-debian.

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Merge with rh.
- Fix building as user.

* Sun Apr 11 1999 Bernhard Rosenkraenzer <bero@microsoft.sucks.eu.org>
- update to 10.2.5
- restore de,fr,tr locales from 5.3

* Fri Mar 12 1999 Jeff Johnson <jbj@redhat.com>
- merge sparc console termcap (from termfiles_sparc).

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- rebuild for glibc 2.1

* Thu May 07 1998 Erik Troan <ewt@redhat.com>
- added linux-lat entry
- build rooted

* Fri May 01 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- made a noarch package

