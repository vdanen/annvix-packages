%define name	pkgconfig
%define version	0.15.0
%define release	5sls

Summary:	Pkgconfig helps make building packages easier.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
URL:		http://www.freedesktop.org/software/pkgconfig
Source:		http://www.freedesktop.org/software/pkgconfig/releases/pkgconfig-%version.tar.bz2

BuildRoot:	%{_tmppath}/%{name}-root

%description
pkgconfig is a program which helps you gather information to make
life easier when you are compiling a program for those programs which support
it.

In fact, it's required to build certain packages.

%prep
%setup -q

%build
%{?__cputoolize: %{__cputoolize} -c glib-1.2.8}
%configure
%make
# all tests must pass
make check

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL README ChangeLog
%{_bindir}/pkg-config
%{_libdir}/pkgconfig
%{_datadir}/aclocal/*
%{_mandir}/man1/*

%changelog
* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 0.15.0-5sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 0.15.0-4sls
- OpenSLS build
- tidy spec

* Wed Jul 30 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.15.0-3mdk
- cputoolize since pkgconfig people don't use a single config.* script

* Wed Jul 23 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.15.0-2mdk
- rebuild
- don't rm -rf $RPM_BUILD_ROOT in %%prep

* Tue Jan 21 2003 Frederic Crozat <fcrozat@mandrakesoft.com> 0.15.0-1mdk
- Release 0.15.0

* Tue Oct 29 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.14.0-1mdk
- Release 0.14.0

* Tue Oct  8 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.13.0-1mdk
- Release 0.13

* Tue Jul 16 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.12.0-2mdk
- Costlessly make check in %%build stage

* Wed Mar 20 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.12.0-1mdk
- Release 0.12.0

* Mon Feb  4 2002 Frederic Crozat <fcrozat@mandrakesoft.com> 0.10.0-1mdk
- Release 0.10.0

* Sat Aug 25 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.8.0-2mdk
- Sanity build for 8.1.

* Thu Jul 12 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.8.0-1mdk
- Release 0.8.0

* Tue Jun 12 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.7.0-1mdk
- s/Copyright/License/;

* Mon Jun 11 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.7.0-1mdk
- Release 0.7
- new URL
- Add missing files

* Sun Apr 29 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.5.0-3mdk
- Take out some snailtalk favored pkgconfig aka remove the buildroot
  from the binary (DindinX).
  
* Fri Apr 20 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.5.0-2mdk
- Change the description (Abel Cheung), yes it's terribly misleading.

* Thu Apr 19 2001 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.5.0-1mdk
- Made an RPM for the purposes of compiling glib2.

