%define name	glibc_lsb
%define version 2.3.1
%define release 2sls

Summary:	LSB dynamic loader links.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		System/Libraries
License:	LGPL
URL:		http://www.gnu.org/software/libc/
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Requires:	lsb >= 1.3-5mdk

%description
Provides ld-lsb* dynamic loader links for LSB compliance.

%prep

%build

%install
install -d $RPM_BUILD_ROOT/%{_lib}
%ifarch %{ix86}
ln -sf ld-linux.so.2 $RPM_BUILD_ROOT/%{_lib}/ld-lsb.so.1
%endif
%ifarch ppc
ln -sf ld-linux.so.2 $RPM_BUILD_ROOT/%{_lib}/ld-lsb-ppc32.so.1
%endif

export DONT_SYMLINK_LIBS=1

%clean

%files
%defattr(-, root, root)
%ifarch %{ix86}
/%{_lib}/ld-lsb.so.1
%endif
%ifarch ppc
/%{_lib}/ld-lsb-ppc32.so.1
%endif

%changelog
* Sun Nov 30 2003 Vincent Danen <vdanen@opensls.org> 2.3.1-2sls
- build for OpenSLS
- tidy spec

* Tue Feb 18 2003 Stew Benedict <sbenedict@mandrakesoft.com> 2.3.1-1mdk
- only provide ld-lsb* links, change version to track system glibc

* Tue Sep 17 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.90-11mdk
- RPC XDR security patch

* Fri Sep 13 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.90-10mdk
- really make libz link, no libncurses

* Thu Sep  7 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.90-9mdk
- update /etc/ld-lsb.so.conf to include Xlibs (drop symlinks)
- update /etc/ld-lsb.so.conf to include /usr/lib (upcoming app-battery)
- add symlink for libncurses in /lib/lsb
- run /sbin/ldconfig-lsb in %%post

* Wed Jul 17 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.90-8mdk
- add support for upcoming X based app-battery apps

* Tue Jun 18 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.90-7mdk
- add patch for divdi3 - fails lsblibchk when built with gcc3.1 (P301)

* Fri Jun  7 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.90-6mdk
- rpmlint: hardcoded-library-path
- drop libX11.so.6 link, xv application test is being phased out
- patch for gcc31 build (P300)

* Wed May 29 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.90-5mdk
- new kernel headers
- additional glibc patch to really pass LSB nice tests (P203)
- additonal glibc patch from CVS for LSB readv/writev tests (P204)
- make glibc_lsb-devel, glibc_lsb-devel-static optional builds
- strip static libs, drop remnants of locales, use directory macros
- add symlink /lib/lsb/libX11.so.6 -> /usr/X11R6/lib/libX11.so.6 (xv)

* Thu Mar 14 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.90-4mdk
- new kernel headers, glibc patches for nice, syslog from SuSE
- PATH_MAX patch no longer needed

* Thu Feb 21 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.90-3mdk
- revert to previous CVS - update made LSB results worse

* Wed Feb 20 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.90-2mdk
- new CVS sync, fix locales issue in locating VSX4L psuedo language files
- change return of nl_langinfo(CRNCYSTR) to NULL, when LC_ALL=C

* Fri Feb  8 2002 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.90-1mdk
- update to 2.2.90 from CVS with LSB related patches
- build using modified limits.h in kernel headers with PATH_MAX=4096
 
* Thu Sep 27 2001 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.1-2mdk
- fix broken lsbcc script

* Wed Sep  5 2001 Stew Benedict <sbenedict@mandrakesoft.com> 2.2.1-1mdk
- 1st Mandrake release
