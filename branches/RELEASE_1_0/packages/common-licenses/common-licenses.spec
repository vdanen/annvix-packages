%define name	common-licenses
%define version 1.0
%define release 10avx

Summary:	Contains the various common licenses uses by the distribution
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Base
Source0:	%{name}.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildArch:	noarch

%description
Contains the various common licenses uses by the distribution. Instead of
including the COPYING file in every package, just refer to this one.

%prep
%setup -q

%build

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
install -d %{buildroot}%{_datadir}
cp -a %{name} %{buildroot}%{_datadir}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/%{name}


%changelog
* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 1.0-10avx
- Annvix build

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 1.0-9sls
- minor spec cleanups

* Fri Nov 28 2003 Vincent Danen <vdanen@opensls.org> 1.0-8sls
- OpenSLS build
- tidy spec

* Tue Jul 22 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 1.0-7mdk
- rebuild
- drop Prefix tag
- quiet setup

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.0-6mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Thu Sep  6 2001 Pixel <pixel@mandrakesoft.com> 1.0-5mdk
- rebuild


* Sun Jan 21 2001 Francis Galiegue <fg@mandrakesoft.com> 1.0-4mdk

- BuildArch: noarch

* Fri Nov 17 2000 Pixel <pixel@mandrakesoft.com> 1.0-3mdk
- cleanup

* Fri Nov 17 2000 Daouda Lo <daouda@mandrakesoft.com> 1.0-2mdk
- add Mozilla Public License  (MPL).

* Fri Nov 17 2000 Pixel <pixel@mandrakesoft.com> 1.0-1mdk
- initial spec


# end of file
