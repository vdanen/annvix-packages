%define name	utempter
%define version	0.5.2
%define release	13sls

%define major		0
%define lib_name_orig	%mklibname utempter
%define lib_name	%{lib_name_orig}%{major}


Summary:	Priviledged helper for utmp/wtmp updates
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Libraries
URL:		http://www.redhat.com
Source:		%{name}-%{version}.tar.bz2
Patch0:		utempter-0.5.2-makevars.patch.bz2
Patch1:		utempter-0.5.2-biarch-utmp.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root

Prereq:		/usr/sbin/groupadd, /sbin/ldconfig, fileutils
Requires:	%{lib_name} = %{version}

%description
Utempter is a utility which allows some non-privileged programs to
have required root access without compromising system
security. Utempter accomplishes this feat by acting as a buffer
between root and the programs.

%package -n %{lib_name}
Summary:	Library used by %{name}
Group:		System/Libraries

%description -n %{lib_name}
Libutempter is an library which allows some non-privileged
programs to have required root access without compromising system
security. It accomplishes this feat by acting as a buffer
between root and the programs.

%package -n %{lib_name}-devel
Summary:	Devel files for %{name}
Group:		Development/C
Provides:	libutempter-devel %{name}-devel
Requires:	%{lib_name} = %{version}

%description -n %{lib_name}-devel
Header files for writing apps using libutempter

%prep
%setup -q
%patch0 -p1 -b .makevars
%patch1 -p1 -b .biarch-utmp

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

ln -sf lib%{name}.so.%{version} $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.%{major}

%clean
rm -rf $RPM_BUILD_ROOT

%pre 
%{_sbindir}/groupadd -g 22 -r -f utmp

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc COPYING
%attr(02755, root, utmp) %{_sbindir}/utempter

%files -n %{lib_name}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libutempter.so.*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc COPYING
%{_libdir}/libutempter.so
%{_includedir}/utempter.h


%changelog
* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 0.5.2-13sls
- OpenSLS build
- tidy spec

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.5.2-12mdk
- mklibname

* Mon Apr 14 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.5.2-11mdk
- Revert s/fileutils/coreutils/
- Patch1: Handle biarch struct utmp

* Fri Jan 03 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5.2-10mdk
- build release

* Thu Nov 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5.2-9mdk
- requires s/fileutils/coreutils/

* Mon Oct 28 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5.2-8mdk
- rpmlint fixes

* Wed Aug 14 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.5.2-7mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Tue Jun 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.5.2-6mdk
- Patch0: Use regular make variables, now use %%makeinstall

* Tue Jan 08 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5.2-5mdk
- fix license (Goetz Bock)

* Mon Aug 06 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5.2-4mdk
- add COPYING to %%libname

* Mon Jul 23 2001 Stefan van der Eijk <stefan@eijk.nu> 0.5.2-3mdk
- -devel package Provides: %%{name}-devel

* Thu Jul 12 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5.2-2mdk
- no need to do initscript job on /var/{log/wtmp,run/utmp}
- libify
- fix -devel group
- add license file

* Tue Jun 12 2001 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5.2-1mdk
- new release

* Tue Jul 25 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.5.1-4mdk
- BM

* Fri May 19 2000 Pixel <pixel@mandrakesoft.com> 0.5.1-3mdk
- add -devel
- add soname
- spec helper cleanup

* Sat Apr 08 2000 Christopher Molnar <molnarc@mandrakesoft.com> 0.5.1-2mdk
- changed group

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- 0.5.1
- fix utmp as group 22.
- strip utempter.
- defattr to root.

* Thu Jun 10 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Fri Jun  4 1999 Jeff Johnson <jbj@redhat.com>
- ignore SIGCHLD while processing utmp.
