%define name	chkfontpath
%define version	1.9.10
%define release	5avx

Summary:	Simple interface for editing the font path for the X font server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/XFree86
Source:		%{name}-%{version}.tar.bz2
Patch:		chkfontpath-1.7-unscaled.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	popt-devel

Requires:	XFree86-xfs, SysVinit

%description 
This is a simple terminal mode program for configuring the directories
in the X font server's path. It is mostly intended to be used
`internally' by RPM when packages with fonts are added or removed, but
it may be useful as a stand-alone utility in some instances.

%prep
%setup -q
%patch0 -p1 -b .old

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
perl -pi -e "s!/usr/man!%{_mandir}!g" Makefile man/Makefile
%makeinstall INSTROOT=$RPM_BUILD_ROOT BINDIR=%{_sbindir} MANDIR=%{_mandir}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%attr(-,root,root)/usr/sbin/chkfontpath
%attr(-,root,root)%{_mandir}/man8/chkfontpath.8*

%changelog
* Thu Jun 09 2005 Vincent Danen <vdanen@annvix.org> 1.9.10-5avx
- rebuild

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 1.9.10-4avx
- require packages not files
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 1.9.10-3sls
- minor spec cleanups

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 1.9.10-2sls
- OpenSLS build
- tidy spec

* Thu Jul 10 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.9.10-1mdk
- 1.9.10

* Sun May 25 2003 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.9.5-2mdk
- rebuild for rpm 4.2

* Fri Jun  1 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.9.5-1mdk
- 1.9.5

* Wed Oct 18 2000 dam's <damien@mandrakesoft.com> 1.7-4mdk
- added patch0 (chkfontpath-1.7-unscaled.patch) to be able to add an unscaled fonts dir.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.7-3mdk
- automatically added BuildRequires


* Thu Jul 20 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.7-2mdk
- BM, macros

* Fri Mar 31 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.7-1mdk
- 1.7
- group fix.

* Sun Mar  5 2000 Pixel <pixel@mandrakesoft.com> 1.5-3mdk
- add require pidof

* Mon Sep 14 1999 Sean P. Kane <kane@ca.metsci.com>
- Merged Mandrake 1.4.1 and Redhat 1.5 RPMS.
- Removed Patch

* Fri Aug 15 1999 Preston Brown <pbrown@redhat.com>
- fixed up basename
- default to list, not help
- if trailing slash '/' is appended to paths given, strip it off

* Thu May 22 1999 Alexei Mikhalev <leha@linuxfan.com>
- added "first" option. Fixed first line deletion.

* Thu Apr 29 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adaptations.

* Wed Apr 14 1999 Preston Brown <pbrown@redhat.com>
- preserve permissions on config file

* Thu Apr 07 1999 Preston Brown <pbrown@redhat.com>
- if /proc isn't mounted, don't do a killall

* Tue Mar 30 1999 Preston Brown <pbrown@redhat.com>
- don't use psmisc, use pidof from SysVinit

* Fri Mar 12 1999 Preston Brown <pbrown@redhat.com>
- made psmisc a requirement.

* Tue Mar 09 1999 Preston Brown <pbrown@redhat.com>
- added "quiet" option.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- injected new group / description.

* Tue Feb 16 1999 Preston Brown <pbrown@redhat.com>
- important fix - kill font server with USR1 instead of HUP.

* Mon Feb 15 1999 Preston Brown <pbrown@redhat.com>
- initial spec file
