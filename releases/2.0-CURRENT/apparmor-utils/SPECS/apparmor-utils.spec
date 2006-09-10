#
# spec file for package apparmor-utils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		apparmor-utils
%define version		2.0
%define release		%_revrel

%define _requires_exceptions perl(Immunix::Ycp)

Summary:	AppArmor userlevel utilities that are useful in creating AppArmor profiles
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	LGPL
Group:		System/Configuration
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	%{name}-%{version}-6377.tar.gz
Patch0:		apparmor-utils-2.0-avx-socklog.patch
Patch1:		apparmor-utils-2.0-avx-nofork.patch
Patch2:         apparmor-utils-2.0-suse-logprof-m-support.diff
Patch3:         apparmor-utils-2.0-suse-logprof-PXUX-support.diff
Patch4:         apparmor-utils-2.0-suse-aaeventd-tail.diff  
Patch5:         apparmor-utils-2.0-suse-changing_profile-check.diff


BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

Requires:	perl(Date::Parse)
Requires:	perl(DBI)
Requires:	perl(File::Tail)
Requires:	perl(DBD::SQLite)
Requires:	apparmor-parser
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description
This package provides the aa-logprof, aa-genprof, aa-autodep,
aa-enforce, and aa-complain tools to assist with profile authoring;
this package also provides the aa-unconfined server information tool
and the aa-eventd event reporting system.


%prep
%setup -q
%patch0 -p0 -b .avx-socklog
%patch1 -p0 -b .avx-nofork
%patch2 -p2 -b .logprof_m
%patch3 -p2 -b .logprof_pxux
%patch4 -p2 -b .aaeventd-tail
%patch5 -p2 -b .changing_profile-check


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} \
     BINDIR=%{buildroot}%{_sbindir} \
     PERLDIR=%{buildroot}%{perl_vendorlib}/Immunix \
     install

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %attr(0640,root,root) /etc/apparmor/logprof.conf
%config(noreplace) %attr(0640,root,root) /etc/apparmor/severity.db
%attr(0750,root,root) %{_sbindir}/*
%{perl_vendorlib}/Immunix
%dir %attr(0700,root,root) /var/log/apparmor


%changelog
* Wed Aug 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- sync some patches with SUSE to match support in SLE10:
  - P2: add support for the new m mode
  - P3: add support for the new Px/Ux modes
  - P4: make aaeventd process all of the events in the log file, not
    just those that occur after it's already running
  - P5: look for the changing_profile hint on the next AppArmor or audit
    line in the log file, not strictly the very next line in the file

* Wed Aug 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- drop aaeventd; we don't need or want it
- update P0 again to change everything looking for /var/log/audit/audit.log to
  /var/log/system/audit/current
- make the config files noreplace

* Tue Aug 29 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- update P0 to a) fix a syntax error and b) to use the right log
  file

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- spec cleanups
- remove locales

* Wed Aug 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- S1: run script for aa-eventd
- P0: use /var/log/system/kmsg/current instead of /var/log/messages
- P1: don't fork aa-eventd
- requires rpm-helper

* Sun Jul 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- drop P0 as we've moved logger to /bin

* Wed Jun 28 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- P0: fix location of logger in genprof
- fix permissions

* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
