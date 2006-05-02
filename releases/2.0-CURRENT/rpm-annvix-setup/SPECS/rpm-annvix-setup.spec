#
# spec file for package rpm-annvix-setup
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$
#
# mdk 1.18-1mdk

%define revision	$Rev$
%define name		rpm-annvix-setup
%define version		1.18
%define release		%_revrel

Summary:	The Annvix rpm configuration and scripts
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration
URL:		http://annvix.org/cgi-bin/viewcvs.cgi/tools/rpm-setup/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}

%description
The Annvix rpm configuration and scripts.


%package build
Summary:	The Annvix rpm configuration and scripts to build rpms
Group:		System/Configuration
Requires:	spec-helper >= 0.6-5mdk
Requires:	multiarch-utils >= 1.0.3
Requires:	%{name} = %{version}-%{release}

%description build
The Annvix rpm configuration and scripts dedicated to build rpms.


%prep
%setup -q


%build
%configure
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/rpm/macros.d


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc ChangeLog
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

* Thu Aug 25 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.5-1mdk
- make generation of debug packages work again
- factor out compile flags and build with -D_FORTIFY_SOURCE=2

* Thu Aug 18 2005 Olivier Thauvin <nanardon@mandriva.org> 1.4-1mdk
- fix php.req about include of relatives path (P. Terjan)

* Tue Aug 16 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.3-1mdk
- check-multiarch-files: fix invocation and path (/usr/lib/rpm/check-*),
  default to not check for multiarch files in 2006

* Sun Aug 07 2005 Olivier Thauvin <nanardon@zarb.org> 1.2-1mdk
- add req/prov for php pear
- add conectiva macros

* Sat Jun 25 2005 Olivier Thauvin <nanardon@mandriva.org> 1.1-4mdk
- require multiarch-utils

* Thu Jun 23 2005 Olivier Thauvin <nanardon@mandriva.org> 1.1-3mdk
- enforce requirement to avoid conflict during update

* Wed Jun 22 2005 Olivier Thauvin <nanardon@mandriva.org> 1.1-2mdk
- split package for dep

* Mon Jun 13 2005 Olivier Thauvin <nanardon@zarb.org> 1.1-1mdk
- few connectiva macros
- from Gwenole Beauchesne
  - merge from old ppc64 branch:
  * find-requires: handle ppc64 loaders

* Wed May 25 2005 Olivier Thauvin <nanardon@zarb.org> 1.0-1mdk
- 1.0:
  - disable automatic gpg key query on server
  - add automatic require for ocaml (G. Rousse)

* Thu May 12 2005 Olivier Thauvin <nanardon@mandriva.org> 0.8-1mdk
- 0.8: fix %%_localstatedir

* Thu May 12 2005 Olivier Thauvin <nanardon@mandriva.org> 0.7-1mdk
- 0.7 (integrate spec mode for emacs)

* Tue May 10 2005 Olivier Thauvin <nanardon@mandriva.org> 0.6-1mdk
- 0.6 %%_libexecdir

* Mon May 09 2005 Olivier Thauvin <nanardon@mandriva.org> 0.5-1mdk
- 0.5 (translate pentium[34] => i586)

* Fri May 06 2005 Olivier Thauvin <nanardon@mandriva.org> 0.4-1mdk
- 0.4
  - fix popt options

* Tue May 03 2005 Olivier Thauvin <nanardon@mandriva.org> 0.3-1mdk
- 0.3 (better compatiblity)

* Sun May 01 2005 Olivier Thauvin <nanardon@mandriva.org> 0.2-1mdk
- 0.2 (minor fix)

* Wed Apr 27 2005 Olivier Thauvin <nanardon@mandriva.org> 0.1-1mdk
- First mandriva spec

