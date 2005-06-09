%define name	curl
%define version 7.13.0
%define release	2avx

%define major	3
%define libname %mklibname %{name} %{major}

# Define to make check (default behavior)
%define do_check 1
%define __libtoolize /bin/true

# Enable --with[out] <feature> at rpm command line
%{?_with_CHECK: %{expand: %%define do_check 1}}
%{?_without_CHECK: %{expand: %%define do_check 0}}

Summary:	Gets a file from a FTP, GOPHER or HTTP server
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	MIT
Group:		Networking/Other
URL:		http://curl.haxx.se/
Source:		http://curl.haxx.se/download/%{name}-%{version}.tar.bz2
Patch1:		curl-7.10.4-compat-location-trusted.patch.bz2
Patch2:		curl-7.13.0-64bit-fixes.patch.bz2
Patch3:		curl-7.13.0-CAN-2005-0490.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	bison groff-for-man openssl-devel zlib-devel

Provides:	webfetch

%description 
curl is a client to get documents/files from servers, using any of the
supported protocols. The command is designed to work without user
interaction or any kind of interactivity.

curl offers a busload of useful tricks like proxy support, user
authentication, ftp upload, HTTP post, file transfer resume and more.

This version is compiled with SSL (https) support.


%package -n %{libname}
Summary:	A library of functions for file transfer
Group:		Networking/Other
Provides:	curl-lib = %{version}-%{release}
Obsoletes:	curl-lib

%description  -n %{libname}
libcurl is a library of functions for sending and receiving files through 
various protocols, including http and ftp.

You should install this package if you plan to use any applications that 
use libcurl.


%package -n %{libname}-devel
Summary:	Header files and static libraries for libcurl
Group:		Networking/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}, lib%{name}-devel
Obsoletes:	%{name}-devel

%description -n %{libname}-devel
libcurl is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you wish to develop applications that 
utilize libcurl.


%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1 -b .64bit-fixes
%patch3 -p0 -b .can-2005-0490

# fix test517 with correct results according to curl_getdate() specs
cat > ptrsize.c << EOF
#include <time.h>
#include <stdio.h>
int main(void)
{
  printf("%d\n", sizeof(time_t));
  return 0;
}
EOF
%{__cc} -o ptrsize ptrsize.c
case `./ptrsize` in
4) ;;
8) mv -f ./tests/data/test517{.64,} ;;
*) exit 1 ;;
esac

%build
%configure2_5x --with-ssl
%make

skip_tests="241"
[ -n "$skip_tests" ] && {
  mkdir ./tests/data/skip/
  for t in $skip_tests; do
    mv ./tests/data/test$t ./tests/data/skip/
  done
}
%if %{do_check}
# At this stage, all tests must pass
make check
%endif

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%make install DESTDIR="$RPM_BUILD_ROOT"

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/curl
%attr(0644,root,root) %{_mandir}/man1/curl.1*
%dir %{_datadir}/curl
%{_datadir}/curl/*

%files -n %{libname}
%defattr(-,root,root)
%doc docs/BUGS docs/KNOWN_BUGS docs/CONTRIBUTE docs/FAQ CHANGES
%doc docs/FEATURES docs/RESOURCES docs/TODO docs/THANKS
%{_libdir}/libcurl.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc docs/examples docs/INTERNALS
%attr(0755,root,root) %{_bindir}/curl-config
%attr(0644,root,root) %{_mandir}/man1/curl-config.1*
%{_libdir}/libcurl.so
%dir %{_includedir}/curl
%{_includedir}/curl/*
%{_libdir}/libcurl*a
%{_mandir}/man3/*

%changelog
* Fri Jun 03 2005 Vincent Danen <vdanen@annvix.org> 7.13.0-2avx
- bootstrap build

* Mon Feb 28 2005 Vincent Danen <vdanen@annvix.org> 7.13.0-1avx
- 7.13.0
- P2: 64bit fixes in the testsuite for curl_getdate() with 64bit
  time_t (gbeauchesne)
- P3: fix for CAN-2005-0490

* Wed Dec 22 2004 Vincent Danen <vdanen@annvix.org> 7.12.3-1avx
- 7.12.3
- remove P0
- skip new test #241 on both archs
- skip tests 23 118 119 125 145 201 205 223 517 on x86_64

* Tue Aug 17 2004 Vincent Danen <vdanen@annvix.org> 7.12.1-1avx
- 7.12.1
- remove fpons' "dynamic patch"
- set %%__libtoolize to /bin/true

* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 7.11.1-2avx
- Annvix build

* Sat Apr 24 2004 Vincent Danen <vdanen@opensls.org> 7.11.1-1sls
- 7.11.1
- drop P2; applied upstream
- get rid of %%real_version macro, we'll never ship anything other than a
  release
- own %%_includedir/curl

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 7.10.7-4sls
- minor spec cleanups

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 7.10.7-3sls
- OpenSLS build
- tidy spec

* Mon Sep  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 7.10.7-2mdk
- Patch2: Still more 64-bit fixes

* Tue Aug 26 2003 Fran�ois Pons <fpons@mandrakesoft.com> 7.10.7-1mdk
- dropped patch2 now integrated.
- 7.10.7.

* Tue Aug 12 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 7.10.6-2mdk
- Patch2: Enough of 64-bit fixes to let regression testsuite
  pass. But, there are undoubtedly other defects yet to fix.

* Mon Jul 28 2003 Fran�ois Pons <fpons@mandrakesoft.com> 7.10.6-1mdk
- removied patch2 now official.
- 7.10.6.

* Thu Jul 24 2003 Fran�ois Pons <fpons@mandrakesoft.com> 7.10.6-0.pre4.2mdk
- fixed ftp from absolute directory (created patch2).

* Tue Jul 22 2003 Fran�ois Pons <fpons@mandrakesoft.com> 7.10.6-0.pre4.1mdk
- 7.10.6-pre4 (proxy environment handling added).

* Tue Jul 08 2003 Fran�ois Pons <fpons@mandrakesoft.com> 7.10.5-1mdk
- 7.10.5.

* Tue Jul  8 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 7.10.4-3mdk
- rebuild for new devel provides

* Wed Jun 04 2003 Stefan van der Eijk <stefan@eijk.nu> 7.10.4-2mdk
- rebuild for new deps

* Wed Apr 02 2003 Fran�ois Pons <fpons@mandrakesoft.com> 7.10.4-1mdk
- removed location trusted patch now intergrated.
- added backward compability with gc patch for location trusted.
- 7.10.4.

* Thu Mar 27 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 7.10.3-2mdk
- add --location-trusted so that we can have working MandrakeClub
  downloads (they use redirection & authentication) in urpmi/curl and
  rpmdrake (grpmi)

* Thu Jan 16 2003 Fran�ois Pons <fpons@mandrakesoft.com> 7.10.3-1mdk
- 7.10.3.

* Wed Nov 27 2002 Stefan van der Eijk <stefan@eijk.nu> 7.10.2-2mdk
- BuildRequires: zlib-devel

* Wed Nov 20 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.10.2-1mdk
- 7.10.2.

* Tue Nov 12 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.10.1-2mdk
- added missing certificate. (Thanks to Gerard Patel)

* Wed Oct 16 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.10.1-1mdk
- 7.10.1.

* Thu Jul 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 7.9.8-2mdk
- Make check in %%build stage
- Patch2: Fix Curl_getaddrinfo() from upstream CVS

* Thu Jun 13 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.8-1mdk
- 7.9.8.

* Mon May 13 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.7-1mdk
- 7.9.7.

* Mon Apr 15 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.6-1mdk
- 7.9.6.

* Wed Apr 03 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.5-2mdk
- added missing curl-config.

* Tue Mar 26 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.5-1mdk
- removed patch10 and patch11.
- 7.9.5.

* Sat Feb 16 2002 Stefan van der Eijk <stefan@eijk.nu> 7.9.4-4mdk
- BuildRequires

* Wed Feb 06 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.4-3mdk
- added patch11 from curl authors to fix content type parsing.

* Tue Feb 05 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.4-2mdk
- added patch10 from curl authors to fix SSL hangs in some case.

* Tue Feb 05 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.4-1mdk
- removed patch10 and patch11.
- 7.9.4.

* Thu Jan 31 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.3-4mdk
- fix latest patch (!).

* Wed Jan 30 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.3-3mdk
- added another patch from curl author to fix SSL on some case,
  until next release is out.

* Wed Jan 30 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.3-2mdk
- added patch from curl author to fix SEGV on some case,
  until next release is out.

* Fri Jan 25 2002 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.3-1mdk
- 7.9.3.

* Thu Jan  3 2002 Jeff Garzik <jgarzik@mandrakesoft.com> 7.9.2-2mdk
- Update Patch1 (fix prototype) for further 64-bit build fix

* Thu Dec 13 2001 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.2-1mdk
- 7.9.2.

* Sat Dec  1 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 7.9.1-2mdk
- add Patch1: correct return type of function, to fix 64-bit build
- use %%configure2_5x macro to provide --build/--host/--target

* Wed Nov 28 2001 Fran�ois Pons <fpons@mandrakesoft.com> 7.9.1-1mdk
- updated documentation.
- added provides to webfetch.
- 7.9.1.

* Thu Oct  4 2001 DindinX <odin@mandrakesoft.com> 7.9-1mdk
- 7.9

* Wed Aug 29 2001 DindinX <odin@mandrakesoft.com> 7.8.1-1mdk
- 7.8.1
- removed patch 1 (merged upstream)

* Mon Jun 11 2001 DindinX <odin@mandrakesoft.com> 7.8-3mdk
- major soname==2 is back!

* Mon Jun 11 2001 DindinX <odin@mandrakesoft.com> 7.8-2mdk
- rebuild with a major of 1

* Fri Jun  8 2001 DindinX <odin@mandrakesoft.com> 7.8-1mdk
- 7.8

* Tue May  8 2001 Guillaume Cottenceau <gc@mandrakesoft.com> 7.7.3-1mdk
- version 7.7.3
- ameliorate BuildRequires
- have docs/examples in its directory

* Wed Apr 25 2001 Frederic Lepied <flepied@mandrakesoft.com> 7.7.2-1mdk
- new version with fix for ftp resume

* Sun Apr 15 2001 Frederic Lepied <flepied@mandrakesoft.com> 7.6.1-2mdk
- libification

* Fri Feb 16 2001 DindinX <odin@mandrakesoft.com> 7.6.1-1mdk
- 7.6.1

* Mon Jan 29 2001 DindinX <odin@mandrakesoft.com> 7.6-1mdk
- 7.6

* Tue Jan  9 2001 DindinX <odin@mandrakesoft.com> 7.5.2-2mdk
- change license, according to the author's will (reported by F. Crozat)
- added some sample codes to the -devel package

* Tue Jan  9 2001 DindinX <odin@mandrakesoft.com> 7.5.2-1mdk
- 7.5.2
- small spec updates

* Mon Dec 18 2000 DindinX <odin@mandrakesoft.com> 7.5.1-2mdk
- corrected URL

* Wed Dec 13 2000 DindinX <odin@mandrakesoft.com> 7.5.1-1mdk
- 7.5.1

* Thu Dec 07 2000 Geoffrey lee <snailtalk@mandrakesoft.com> 7.5-2mdk
- manually include fcntl.h, strangely, it has been left out (sucky!!!).

* Mon Dec 04 2000 Geoffrey lee <snailtalk@mandrakesoft.com> 7.5-1mdk
- new and shiny source.
- requires: curl = %%{version}

* Wed Nov 15 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 7.4.2-5mdk
- really 7.4.2.
- well we compile with ssl now, so obviously description is wrong (daoudascks)

* Mon Nov 13 2000 Daouda Lo <daouda@mandrakesoft.com> 7.4.2-4mdk
- compiled with ssl (from TitiSux)

* Mon Nov 13 2000 Daouda Lo <daouda@mandrakesoft.com> 7.4.2-3mdk
- relase pre4.

* Fri Nov 10 2000 Lenny Cartier <lenny@mandrakesoft.com> 7.4.2-2mdk
- fiw requires


* Tue Nov 07 2000 Daouda Lo <daouda@mandrakesoft.com> 7.4.2-1mdk
- new release

* Fri Nov 03 2000 DindinX <odin@mandrakesoft.com> 7.4.1-1mdk
- 7.4.1

* Mon Aug 28 2000 Lenny Cartier <lenny@mandrakesoft.com> 7.1-1mdk
- used srpm from Anton Graham <darkimage@bigfoot.com> :
	- new version
	- new -lib and -devel packages

* Mon Aug 28 2000 Lenny Cartier <lenny@mandrakesoft.com> 6.5.2-3mdk
- change description
- clean spec 

* Tue Jul 11 2000 Anton Graham <darkimage@bigfoot.com> 6.5.2-2mdk
- Macroification
  
* Wed May 03 2000 Anton Graham <darkimage@bigfoot.com> 6.5.2-1mdk
- First Mandrake build
