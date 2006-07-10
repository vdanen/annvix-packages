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
Source2:	rc.apparmor.mandriva
Patch0:		apparmor-parser-2.0-avx-fixes.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libcap-devel

Requires:	sed

%description
The AppArmor Parser is a userlevel program that is used to load in
program profiles to the AppArmor Security kernel module.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p0 -b .avx

# copy our initscripts
cp %{_sourcedir}/rc.aaeventd.mandriva .
cp %{_sourcedir}/rc.apparmor.mandriva .


%build
make clean all CFLAGS="%{optflags}"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
make DESTDIR=%{buildroot} \
     DISTRO=mandriva \
     APPARMOR_BIN_PREFIX=%{buildroot}%{_initrddir} \
     install

mv %{buildroot}%{_initrddir}/rc.apparmor.functions %{buildroot}%{_initrddir}/apparmor.functions
install -m 0750 rc.aaeventd.mandriva %{buildroot}%{_initrddir}/aaeventd

%find_lang %{name}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_service apparmor
%_post_service aaeventd


%preun
%_preun_service apparmor
%_preun_service aaeventd



%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %attr(0640,root,root) %{_sysconfdir}/apparmor/subdomain.conf
%attr(0750,root,root) /sbin/apparmor_parser
%dir %attr(0750,root,root) %{_sysconfdir}/apparmor
%attr(0750,root,root) %{_initrddir}/apparmor.functions
%attr(0750,root,root) %{_initrddir}/apparmor
%attr(0750,root,root) %{_initrddir}/aaeventd
%dir %attr(0750,root,root) /var/lib/apparmor

%files doc
%defattr(-,root,root)
%doc README COPYING.GPL


%changelog
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
