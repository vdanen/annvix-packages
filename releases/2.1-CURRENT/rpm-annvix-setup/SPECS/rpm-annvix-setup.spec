#
# spec file for package rpm-annvix-setup
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		rpm-annvix-setup
%define version		1.24
%define release		%_revrel

Summary:	The Annvix rpm configuration and scripts
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://svn.annvix.org/cgi-bin/viewvc.cgi/tools/rpm-setup/trunk/
Source0:	%{name}-%{version}.tar.bz2

#Requires:	libssp0

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	rpm-devel

%description
The Annvix rpm configuration and scripts.


%package build
Summary:	The Annvix rpm configuration and scripts to build rpms
Group:		System/Configuration
Requires:	spec-helper >= 0.6-5mdk
Requires:	multiarch-utils >= 1.0.3
Requires:	pkgconfig
Requires:	%{name} = %{version}-%{release}
#Requires:	libssp0-devel

%description build
The Annvix rpm configuration and scripts dedicated to build rpms.


%prep
%setup -q


%build
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d


%check
make test


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%dir %{_prefix}/lib/rpm/annvix
%{_prefix}/lib/rpm/annvix/rpmrc
%{_prefix}/lib/rpm/annvix/macros
%{_prefix}/lib/rpm/annvix/rpmpopt
%{_prefix}/lib/rpm/annvix/*-%_target_os
%dir %{_sysconfdir}/rpm/macros.d


%files build
%defattr(-,root,root)
%exclude %{_prefix}/lib/rpm/annvix/rpmrc
%exclude %{_prefix}/lib/rpm/annvix/macros
%exclude %{_prefix}/lib/rpm/annvix/rpmpopt
%exclude %{_prefix}/lib/rpm/annvix/*-%_target_os
%{_prefix}/lib/rpm/annvix/*


%changelog
* Sun May 20 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.24
- 1.24
- buildrequires: rpm-devel
- requires pkgconfig on -build subpackage
- add make test

* Mon Nov 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.22
- revert the SSP changes; I don't think it will play nice until we get
  glibc 2.4 involved

* Tue Oct 31 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.22
- libssp0 is still libssp0 on x86_64 (not lib64ssp0)

* Tue Oct 31 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.22
- 1.22: add -fstack-protector-all to the %%serverbuild macro
- clean spec
- fix URL
- require libssp

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.21
- 1.21: fix %%kill_lang support

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.20
- 1.20: add %%kill_lang support

* Sat Jul 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.19
- 1.19

* Tue May 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.18
- revert the find-provides changes because they didn't pick up things
  like libperl.so in the perl packages

* Tue May 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.18
- sync with mandriva 1.18:
  - find-requires: require only .so that are in standard paths, and use ldd
    instead of objdump to get their list (rafael)
  - don't search perl files for provides if they don't end with .pm (rafael)
  - fix rename macro (don't obsolete what is provided) (Ze)
  - fix automatic deps for some devel packages (guillaume rousse)
  - set _repackage_all_erasures to 0 (rgs)
  - add a way to disable fortify from cflags (nanardon)
  - add a macro to list all sparc-compatible archs (per ayvind karlsen)
  - remove pre flags on python requirements (helio)
  - remove /etc/rpm/macros.* from macros search path (nanardon)
  - add %%py_platlibdir and %%py_purelibdir (misc)
  - set changelog_truncate to "3 years ago" (rafael)
  - restore _query_all_fmt to it's default 4.4.2 value (rafael)
  - add _rpmlock_path to default macros (rafael)
  - ignore perl version requires (rafael)
  - get the correct perl dependencies from "use base" (rafael)
  - insert a dependency on libperl.so for XS perl modules (rafael)
  - fix %%py_libdir for lib64 platforms (gbeauchesne)
  - perl.req: add the proper detection of 'use base qw(Foo::Bar)' construct
    (michael scherer)

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5
- fix group

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.5-5110avx
- pull out the use -fstack-protector-all; SSP is going to wait until
  gcc 4.1 is stable as then we get it for free

* Fri Dec 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5-4825avx
- use %%_revrel
- obfuscate email addresses

* Fri Dec 23 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5-4avx
- add back -fstack-protector-all to %%optflags

* Sun Sep 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5-3avx
- add the %%_mkdepends macro

* Thu Sep 15 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5-2avx
- dropt -Wp,-D_FORTIFY_SOURCE=2 from the optflags because I don't
  know what this does and if it's specific to gcc4 or not (we didn't
  have this prior to this package)

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.5-1avx
- first Annvix build for new rpm

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
