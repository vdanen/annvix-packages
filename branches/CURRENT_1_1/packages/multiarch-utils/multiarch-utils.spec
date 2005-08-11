#
# spec file for package multiarch-utils
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#


%define name		multiarch-utils
%define version		1.0.8
%define release 	2avx
%define multiarch_distro 100

Summary:	Tools to help creation of multiarch binaries and includes
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.mandrivalinux.com/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildArch:	noarch

%description
multiarch-utils is a collection of helper utilities to dispatch
binaries and include files during RPM package build.


%prep
%setup -q


%build


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std MULTIARCH_DIST=%{multiarch_distro}


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc ChangeLog
%{_bindir}/multiarch-platform
%{_bindir}/multiarch-dispatch
%{_includedir}/multiarch-dispatch.h
%{_sysconfdir}/rpm/macros.multiarch
%{_prefix}/lib/rpm/mkmultiarch
%{_prefix}/lib/rpm/check-multiarch-files
%{_prefix}/X11R6/lib/X11/config/multiarch-dispatch-host.def

%changelog
* Wed Aug 10 2005 Vincent Danen <vdanen@annvix.org> 1.0.8-2avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen@annvix.org> 1.0.8-1avx
- 1.0.8

* Thu Jul 21 2005 Vincent Danen <vdanen@annvix.org> 1.0.7-3avx
- set the multiarch_distro tag so multiarch macros work
- change the fact that the Makefile is pulling the value of
  multiarch_distro from the bloody tarball's specfile (huh?!?)

* Thu Jun 02 2005 Vincent Danen <vdanen@annvix.org> 1.0.7-2avx
- bootstrap build

* Tue Mar 01 2005 Vincent Danen <vdanen@mandrakesoft.com> 1.0.7-1avx
- first Annvix build

* Wed Feb 23 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.7-1mdk
- multiarch x11 host.def
- new heuristics for multiarch files checker (ace-config)
- only check for multiarch files in the usual development directories

* Thu Feb 10 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.6-1mdk
- check-multiarch-files: new multiarch hint: BITS_PER_WORD
- check-multiarch-files: handle --libtool in config scripts
- check-multiarch-files: don't match */lib/{font,X11} in headers

* Mon Jan 31 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.5-1mdk
- mkmultiarch: handle ciruclar inclusions (e.g. gd.h)
- check-multiarch-files: better heuristics (gdlib-config, mysql_config)

* Mon Jan 31 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.4-1mdk
- mkmultiarch: handle /usr/include/header.h cases
- mkmultiarch: handle symlinks in binaries to be dispatched
- macros.multiarch: add multiarch_{platform,x11bindir,x11includedir}

* Tue Jan 25 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.3-1mdk
- add %%multiarch_{bin,include}dir aliases
- better os independence, "linux" is detected

* Mon Jan 24 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.2-1mdk
- add check-multiarch-files

* Thu Jan 20 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0.1-1mdk
- add %%multiarch macro to mark %%files that are multiarch enabled;
  that's a helper macro that expands to nothing on older distributions

* Wed Jan 12 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0-1mdk
- initial release
