%define name	cracklib
%define version	2.7
%define release	20avx

%define root	crack
%define maj	2
%define libname	%mklibname %root %maj
%define libnamedev %libname-devel

Summary:	A password-checking library.
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Artistic
Group:		System/Libraries
URL:		ftp://coast.cs.purdue.edu/pub/tools/unix/libs/cracklib/
Source:		ftp://coast.cs.purdue.edu/pub/tools/unix/libs/cracklib/cracklib_%{version}.tar.bz2
Patch0:		cracklib-2.7-redhat.patch.bz2
Patch1:		cracklib-2.7-makevars.patch.bz2
Patch2:		cracklib-2.7-includes.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	words

%description
CrackLib tests passwords to determine whether they match certain
security-oriented characteristics. You can use CrackLib to stop
users from choosing passwords which would be easy to guess. CrackLib
performs certain tests: 

* It tries to generate words from a username and gecos entry and 
  checks those words against the password;
* It checks for simplistic patterns in passwords;
* It checks for the password in a dictionary.

CrackLib is actually a library containing a particular
C function which is used to check the password, as well as
other C functions. CrackLib is not a replacement for a passwd
program; it must be used in conjunction with an existing passwd
program.

Install the cracklib package if you need a program to check users'
passwords to see if they are at least minimally secure. If you
install CrackLib, you'll also want to install the cracklib-dicts
package.

%package -n %libname
Summary:	A password-checking library.
Group:		System/Libraries
Provides:	lib%{root}-devel %{root}-devel = %{version}-%{release}
Obsoletes:	cracklib

%description -n %libname
CrackLib tests passwords to determine whether they match certain
security-oriented characteristics. You can use CrackLib to stop
users from choosing passwords which would be easy to guess.

%package dicts
Summary:	The standard CrackLib dictionaries.
Group:		System/Libraries

%description dicts
The cracklib-dicts package includes the CrackLib dictionaries.
CrackLib will need to use the dictionary appropriate to your system,
which is normally put in /usr/share/dict/words.  Cracklib-dicts also contains
the utilities necessary for the creation of new dictionaries.

If you are installing CrackLib, you should also install cracklib-dicts.

%package -n %libnamedev
Summary:	Cracklib link library & header file
Group:		Development/C
Provides:	lib%{root}-devel %{root}-devel = %{version}-%{release} %{root}lib-devel = %{version}-%{release}
Requires:	%{libname} = %version-%release
Obsoletes:	cracklib-devel

%description -n %libnamedev
The cracklib devel package include the needed library link and
header files for development.


%prep
%setup -q -n %{name},%{version}
%patch0 -p1 -b .rh
%patch1 -p1 -b .makevars
%patch2 -p1 -b .includes
perl -p -i -e "s/\) -g/\)/" cracklib/Makefile
chmod -R og+rX .

%build
# the libs don't build properly with SSP enabled
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fno-stack-protector"

make all RPM_OPT_FLAGS="$RPM_OPT_FLAGS" \
	libdir=%{_libdir} datadir=%{_datadir}

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT{%{_sbindir},%{_libdir},%{_includedir}}
make install \
	ROOT=$RPM_BUILD_ROOT \
	sbindir=%{_sbindir} \
	libdir=%{_libdir} \
	includedir=%{_includedir}
ln -sf libcrack.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libcrack.so.%{maj}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%doc README MANIFEST LICENCE HISTORY POSTER
%{_libdir}/libcrack.so.*

%files -n %{libnamedev}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libcrack.so

%files dicts
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/cracklib_dict*

%changelog
* Fri Jun 25 2004 Vincent Danen <vdanen@annvix.org> 2.7-20avx
- Annvix build
- remove %%build_propolice macro; build without ssp by default

* Wed Mar 03 2004 Vincent Danen <vdanen@opensls.org> 2.7-19sls
- minor spec cleanups

* Tue Dec 16 2003 Vincent Danen <vdanen@opensls.org> 2.7-18sls
- OpenSLS build
- tidy spec
- use %%build_propolice macro to set -fno-stack-protector because we get
  build errors if we have it enabled

* Fri Jul 18 2003 Warly <warly@mandrakesoft.com> 2.7-17mdk
- libification

* Tue Jun 25 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.7-16mdk
- Rpmlint fixes: hardcoded-library-path (Patch1)
- Patch2: Add missing includes

* Fri Nov  2 2001 Jeff Garzik <jgarzik@mandrakesoft.com> 2.7-15mdk
- Rebuild.
- Update URL.

* Mon Oct  2 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.7-14mdk
- removed build requires on cracklib-devel.
- added build requires on words and chage the path of the dicts to /usr/share/dict.

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 2.7-13mdk
- automatically added BuildRequires

* Fri Jul 21 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 2.7-12mdk
- BM

* Fri May 19 2000 Pixel <pixel@mandrakesoft.com> 2.7-11mdk
- add soname

* Thu Apr 13 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.7-10mdk
- Devel package.

* Tue Mar 21 2000 Yoann Vandoorselaere <yoann@mandrakesoft.com> 2.7-9mdk
- Fix group.

* Wed Oct 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Strip binaries.
- Add %defattr

* Sun May  2 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- s/V'erification/Verification in french translation - I know it's a
  spelling mistake, but rpm 3.0 doesn't like accents in Summary: lines. :/

* Thu Apr 10 1999 Alexandre Dussart <adussart@mandrakesoft.com>
- French Translation

* Fri Apr  9 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- handle RPM_OPT_FLAGS
- add de locale

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Sat May 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Mar 10 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.7
- build shared libraries

* Mon Nov 03 1997 Donnie Barnes <djb@redhat.com>
- added -fPIC

* Mon Oct 13 1997 Donnie Barnes <djb@redhat.com>
- basic spec file cleanups

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

