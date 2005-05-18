%define name	multiarch-utils
%define version	1.0.3
%define release 1avx

Summary:	Tools to help creation of multiarch binaries and includes
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.mandrakelinux.com/
Source0:	%{name}-%{version}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch

%description
multiarch-utils is a collection of helper utilities to dispatch
binaries and include files during RPM package build.

%prep
%setup -q

%build

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

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

%changelog
* Wed Feb 02 2005 Vincent Danen <vdanen@annvix.org> 1.0.3-1avx
- first Annvix build

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
