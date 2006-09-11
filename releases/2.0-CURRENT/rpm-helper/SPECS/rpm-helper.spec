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
%define version		0.15
%define release		%_revrel

Summary:	Helper scripts for rpm scriptlets
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://www.mandrivalinux.com/
Source0:	%{name}-%{version}.tar.bz2
Patch0:		rpm-helper-0.14-avx-srv.patch
Patch1:		rpm-helper-0.15-avx-fix_chown_syntax.patch
Patch2:		rpm-helper-0.15-avx-fix_preun_shelldel.patch

BuildArch:	noarch
BuildRoot:	%{_buildroot}/%{name}-%{version}

Conflicts:	chkconfig < 1.3.4-10mdk
Requires(pre):	setup
Requires:	chkconfig
Requires:	grep
Requires:	shadow-utils
Requires:	coreutils
Requires:	srv >= 0.20

%description
Helper scripts for rpm scriptlets to help create/remove :
- groups
- services
- shells
- users


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0 -b .avx
%patch1 -p0 -b .chown_syntax
%patch2 -p0 -b .preun_shelldel


%build
chmod 0755 {add,del}-srv mkdepends


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std LIBDIR=%{_datadir}/%{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_sys_macros_dir}/%{name}.macros

%files doc
%defattr(-,root,root)
%doc README* ChangeLog AUTHORS


%changelog
* Sun Sep 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.15
- P2: fix %%_preun_shelldel macro (was missing a %%{1})
- change runsvctrl calls to /sbin/sv calls

* Fri Aug 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.15
- P1: fix chown call in create-files (user:user rather than user.user)
- put a requires(pre) on setup; we want the group/passwd files for the
  user-manipulation stuff rpm-helper needs to do
- spec cleanups

* Tue May 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.15
- 0.15:
  - add-service: handle case when a service name appears several times
- add -doc subpackage

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.14
- fix group

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.14
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.14
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
- own %%_datadir/%%{name}

* Tue Dec 09 2003 Vincent Danen <vdanen@opensls.org> 0.9.1-2sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
