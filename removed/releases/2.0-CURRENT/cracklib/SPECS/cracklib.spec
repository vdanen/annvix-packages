#
# spec file for package cracklib 
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id: cracklib.spec 5248 2006-02-28 05:12:35Z vdanen $

%define revision	$Rev: 5248 $
%define name		cracklib
%define version		2.8.3
%define release		%_revrel

%define root		crack
%define maj		2
%define libname		%mklibname %{root} %{maj}

Summary:	A password-checking library
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Artistic
Group:		System/Libraries
URL:		http://sourceforge.net/projects/cracklib/
Source:		http://prdownloads.sourceforge.net/cracklib/cracklib-%{version}.tar.bz2
Source1:	http://prdownloads.sourceforge.net/cracklib/cracklib-words.bz2
Source10:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/Domains.bz2
Source11:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/Dosref.bz2
Source12:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/Ftpsites.bz2
Source13:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/Jargon.bz2
Source14:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/common-passwords.txt.bz2
Source15:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/etc-hosts.bz2
Source16:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/movieTV/Movies.bz2
Source17:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/movieTV/Python.bz2
Source18:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/movieTV/Trek.bz2
Source19:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/LCarrol.bz2
Source20:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/Paradise.Lost.bz2
Source21:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/cartoon.bz2
Source22:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/myths-legends.bz2
Source23:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/sf.bz2
Source24:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/shakespeare.bz2
Source25:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/names/ASSurnames.bz2
Source26:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/names/Congress.bz2
Source27:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/names/Family-Names.bz2
Source28:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/names/Given-Names.bz2
Source29:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/names/famous.bz2
Source30:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/names/fast-names.bz2
Source31:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/names/female-names.bz2
Source32:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/names/male-names.bz2
Source33:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/names/names.french.bz2
Source34:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/names/names.hp.bz2
Source35:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/names/other-names.bz2
Source36:	ftp://ftp.cerias.purdue.edu/pub/dict/wordlists/names/surnames.finnish.bz2

BuildRoot:	%{_buildroot}/%{name}-root


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


%package -n %{libname}
Summary:	A password-checking library
Group:		System/Libraries
Provides:	lib%{root}-devel %{root}-devel = %{version}-%{release}
Obsoletes:	cracklib

%description -n %{libname}
CrackLib tests passwords to determine whether they match certain
security-oriented characteristics. You can use CrackLib to stop
users from choosing passwords which would be easy to guess.


%package dicts
Summary:	The standard CrackLib dictionaries
Group:		System/Libraries

%description dicts
The cracklib-dicts package includes the CrackLib dictionaries.
CrackLib will need to use the dictionary appropriate to your system,
which is normally put in /usr/share/dict/words.  Cracklib-dicts also contains
the utilities necessary for the creation of new dictionaries.


%package -n %{libname}-devel
Summary:	Cracklib link library & header file
Group:		Development/C
Provides:	lib%{root}-devel %{root}-devel = %{version}-%{release} %{root}lib-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Obsoletes:	cracklib-devel

%description -n %{libname}-devel
The cracklib devel package include the needed library link and
header files for development.


%prep
%setup -q

for dict in %{SOURCE1} %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} \
    %{SOURCE15} %{SOURCE16} %{SOURCE17} %{SOURCE18} %{SOURCE19} %{SOURCE20} %{SOURCE21} \
    %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25} %{SOURCE26} %{SOURCE27} %{SOURCE28} \
    %{SOURCE29} %{SOURCE30} %{SOURCE31} %{SOURCE32} %{SOURCE33} %{SOURCE34} %{SOURCE35} \
    %{SOURCE36} %{SOURCE1}; do
    cp ${dict} dicts/
done
bunzip2 dicts/*.bz2


%build
%configure2_5x
%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

./util/cracklib-format dicts/* | ./util/cracklib-packer %{buildroot}%{_datadir}/cracklib/pw_dict

ln -s cracklib-format %{buildroot}%{_sbindir}/mkdict
ln -s cracklib-packer %{buildroot}%{_sbindir}/packer

ln -s %{_datadir}/cracklib/pw_dict.hwm %{buildroot}%{_libdir}/cracklib_dict.hwm
ln -s %{_datadir}/cracklib/pw_dict.pwd %{buildroot}%{_libdir}/cracklib_dict.pwd
ln -s %{_datadir}/cracklib/pw_dict.pwi %{buildroot}%{_libdir}/cracklib_dict.pwi

install -m644 lib/packer.h %{buildroot}%{_includedir}/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README* doc/LICENCE
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/*.a

%files dicts
%defattr(-,root,root)
%{_sbindir}/*
%dir %{_datadir}/cracklib
%{_datadir}/cracklib/cracklib.magic
%{_datadir}/cracklib/pw_dict*
%{_libdir}/cracklib_dict.*


%changelog
* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Tue Jan 03 2006 Vincent Danen <vdanen-at-build.annvix.org>
- 2.8.3
- new URL
- drop patches, implemented upstream
- add lots of dictionary files, no longer requires words
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.7-22avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 2.7-21avx
- bootstrap build
- re-enable stack protection

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.7-20avx
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

