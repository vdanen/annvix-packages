#
# spec file for package apparmor-parser
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		apparmor-parser
%define version		2.0
%define release		%_revrel

Summary:	AppArmor userlevel parser utility
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
Source0:	%{name}-%{version}-6358.tar.gz
Source1:	rc.aaeventd.mandriva
Source2:	apparmor-avx.init
Patch0:		apparmor-parser-2.0-avx-fixes.patch
Patch1:         apparmor-parser-fix_segv_nonexistant_dir-r30-160330.patch
Patch2:         apparmor-parser-m_flag-code10-175388.patch
Patch3:         apparmor-parser-add_PxUx-code10-172061.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libcap-devel
BuildRequires:	bison
BuildRequires:	flex

Requires:	sed
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description
The AppArmor Parser is a userlevel program that is used to load in
program profiles to the AppArmor Security kernel module.


%package -n apparmor
Summary:	Virtual rpm to install all AppArmor components
Group:		System/Configuration
Requires:	apparmor-parser
Requires:	apparmor-utils
Requires:	apparmor-profiles
Requires:	libapparmor

%description -n apparmor
This package is a virtual rpm that installs all required AppArmor components
with a single command.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0 -b .avx
%patch1 -p3 -b .fix_segv
%patch2 -p3 -b .m_flag
%patch3 -p3 -b .add_PxUx

# copy our initscripts
cp %{_sourcedir}/rc.aaeventd.mandriva rc.aaeventd.annvix
cp %{_sourcedir}/apparmor-avx.init rc.apparmor.annvix


%build
make clean all CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} \
     DISTRO=annvix \
     APPARMOR_BIN_PREFIX=%{buildroot}%{_initrddir} \
     install

mv %{buildroot}%{_initrddir}/rc.apparmor.functions %{buildroot}%{_initrddir}/apparmor.functions
#install -m 0750 rc.aaeventd.annvix %{buildroot}%{_initrddir}/aaeventd

%kill_lang %{name}
%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_service apparmor
#%_post_service aaeventd


%preun
%_preun_service apparmor
#%#_preun_service aaeventd



%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/apparmor/subdomain.conf
%attr(0750,root,root) /sbin/apparmor_parser
%dir %attr(0750,root,root) %{_sysconfdir}/apparmor
%attr(0750,root,root) %{_initrddir}/apparmor.functions
%attr(0750,root,root) %{_initrddir}/apparmor
#%attr(0750,root,root) %{_initrddir}/aaeventd
%dir %attr(0750,root,root) /var/lib/apparmor

%files -n apparmor
%defattr(-,root,root)

%files doc
%defattr(-,root,root)
%doc README COPYING.GPL


%changelog
* Wed Nov 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- add buildrequires of flex and bison

* Sun Oct 22 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- updated the initscript and modified the patch to the functions accordingly
- add a virtual rpm so you can just "apt-get install apparmor" and get all
  the required components

* Tue Sep 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- fix the preun script

* Wed Aug 30 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- sync some patches with SUSE to match support in SLE10:
  - P1: fix segv if profiles directory does not exist
  - P2: add support for the new m flag (mmap w/ PROT_EXEC permission)
  - P3: add support for the new Px/Ux modes which indicate to ld.so that
    sensitive environment variables should be filtered on exec()

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- remove locales

* Wed Aug 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- don't include the aaeventd initscript (runscript is in apparmor-utils)
- requires rpm-helper

* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- fix permissions
- provide our own initscripts for apparmor and aaeventd (S0, S1)
- drop /subdomain (not required since we use /sys/kernel/security)
- update P0 to fix the apparmor.functions

* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- put /lib/apparmor/rc.apparmor.functions in /etc/rc.d/init.d/apparmor.functions

* Tue Jun 27 2006 Vincent Danen <vdanen-at-build.annvix.org> 2.0
- P0: fix installation of initscripts (location) for Annvix/Mandriva
- first Annvix package

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
