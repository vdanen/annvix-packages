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
%define version		0.20.0
%define release		%_revrel

Summary:	Helper scripts for rpm scriptlets
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://www.mandrivalinux.com/
Source0:	%{name}-%{version}.tar.bz2
Source1:	add-srv
Source2:	del-srv
Source3:	mkdepends
Patch0:		rpm-helper-0.20.0-avx-srv.patch

BuildArch:	noarch
BuildRoot:	%{_buildroot}/%{name}-%{version}

Requires(pre):	setup
Requires:	runit
Requires:	grep
Requires:	shadow-utils
Requires:	coreutils
Requires:	srv >= 0.20
Requires:	findutils

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
cp %{_sourcedir}/{{add,del}-srv,mkdepends} .


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_sys_macros_dir}/%{name}.macros
%config(noreplace) %{_sysconfdir}/sysconfig/ssl

%files doc
%defattr(-,root,root)
%doc README* NEWS AUTHORS


%changelog
* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.20.0
- 0.20.0: provides support for creating ssl certificates
- drop P1, P2: merged upstream
- rediff P0

* Mon Jun 18 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.18.4
- revert the changes to add-srv and del-srv

* Mon Jun 18 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.18.4
- update add-srv and del-srv to handle apparmor reloading (silently)
  without forcing the use of the %%_aa_reload macro

* Wed Apr 18 2007 Vincent Danen <vdanen-at-build.annvix.org> 0.18.4
- 0.18.4
- requires: findutils
- rediff P0 and break out add-srv, del-srv, and mkdepends into their own
  source files
- rediff P2

* Thu Dec 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.15
- update P0 to be silent when del/add upgraded services and to be
  more robust and actually do something if it detects more than one
  symlink

* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.15
- update P0 to make it manage services in the default runlevel

* Sat Oct 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.15
- update P0 to make changes to add-service and del-service to use
  rc-update rather than chkconfig
- requires runit rather than chkconfig

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
