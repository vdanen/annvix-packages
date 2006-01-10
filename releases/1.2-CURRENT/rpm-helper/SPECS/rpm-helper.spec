#
# spec file for package rpm-helper
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rpm-helper
%define version		0.14
%define release		%_revrel

Summary:	Helper scripts for rpm scriptlets
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Packaging
URL:		http://www.mandrivalinux.com/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		rpm-helper-0.14-avx-srv.patch

BuildArch:	noarch
BuildRoot:	%{_buildroot}/%{name}-%{version}

Conflicts:	chkconfig < 1.3.4-10mdk
Requires:	chkconfig, grep, shadow-utils, coreutils, srv >= 0.20

%description
Helper scripts for rpm scriptlets to help create/remove :
- groups
- services
- shells
- users


%prep
%setup -q
%patch0 -p0 -b .avx


%build
chmod 0755 {add,del}-srv mkdepends


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std LIBDIR=%{_datadir}/%{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README* ChangeLog AUTHORS
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_sys_macros_dir}/%{name}.macros


%changelog
* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Oct 05 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.14-3avx
- update P0 to accomodate new srv commands

* Sun Sep 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.14-2avx
- update P0 to add mkdepends script

* Thu Sep 22 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.14-1avx
- 0.14
- update P0 to rip out all references to msec

* Wed Sep 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.13-2avx
- update P0 to patch the macros as well to update _pre_useradd and
  _pre_groupadd for our static uid/gid's

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.13-1avx
- 0.13
- provide it's own macro
- regen P0

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.10-12avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.10-2avx
- bootstrap build

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.10-1avx
- 0.10
- tidy spec

* Tue Sep 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1-10avx
- fix add-srv scriptlet again; we need to grep for "run" not "up"

* Tue Sep 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1-9avx
- fix add-srv scriptlet; now we test if a service exists before trying
  to run runsvstat on it, and we also redirect runsvstat's output to
  /dev/null to make it prettier

* Sun Sep 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1-8avx
- update P0: s/svstat/runsvstat/

* Mon Jul 05 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1-7avx
- fix P0; some services were not restarting on upgrade and it was due
  to grep not being quiet

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.1-6avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 0.9.1-5sls
- minor spec cleanups

* Tue Feb 03 2004 Vincent Danen <vdanen@opensls.org> 0.9.1-4sls
- update P0 to add another field to add-group for static gid

* Tue Jan 27 2004 Vincent Danen <vdanen@opensls.org> 0.9.1-3sls
- P0: adds add-srv and del-srv scripts to manage supervised services, also
  adds a sixth field to add-user so we can force a static uid
- own %_datadir/%{name}

* Tue Dec 09 2003 Vincent Danen <vdanen@opensls.org> 0.9.1-2sls
- OpenSLS build
- tidy spec

* Wed Sep 17 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.9.1-1mdk
- don't depend on initscripts anymore

* Tue Jan 14 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.9-1mdk
- added the right requires

* Sun Dec 22 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.8-1mdk
- corrected add-shell to not add the shell multiple times
- corrected add-service when SECURE_LEVEL isn't set
- corrected add-group not to delete supplementary groups already added

* Tue Nov  5 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.7.1-1mdk
- add verify-shell

* Tue Nov  5 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.7-1mdk
- add add-shell and del-shell to update /etc/shells

* Fri Sep  6 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.6-1mdk
- add add-shell and del-shell to update /etc/shells
- add-service: do the security stuff here instead of doing it in chkconfig
to be more flexible.

* Thu Aug  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.5-1mdk
- add-service: on upgrade, restart services that depend of portmap.

* Wed Jul 31 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.4.1-1mdk
- correct add-group when no user is added to the group

* Mon Jul 29 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.4-1mdk
- added del-group and add-group

* Fri Jul 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.3-1mdk
- extend add-user to support extended groups

* Wed Jul 10 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.2-1mdk
- added create-file

* Tue Jul  9 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.1-1mdk
- Initial version

# end of file
