#
# spec file for package openssl
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		openssl
%define version		0.9.8
%define release		%_revrel

%define maj		0.9.8
%define libname 	%mklibname %{name} %{maj}
%define libnamedev	%{libname}-devel
%define libnamestatic	%{libname}-static-devel

Summary:	Secure Sockets Layer communications libs & utils
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		System/Libraries
URL:		http://www.openssl.org/

Source:		ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz.asc
# (fg) 20010202 Patch from RH: some funcs now implemented with ia64 asm
Patch1:		openssl-0.9.7-mdk-ia64-asm.patch
# (gb) 0.9.7b-4mdk: Handle RPM_OPT_FLAGS in Configure
Patch2:		openssl-0.9.7g-mdk-optflags.patch
# (gb) 0.9.7b-4mdk: Make it lib64 aware. TODO: detect in Configure
Patch3:		openssl-0.9.8-avx-lib64.patch
Patch4:		openssl-0.9.8-CAN-2005-2946.patch
Patch5:		openssl-0.9.7-CAN-2005-2969.patch
Patch6:		openssl-CVE-2006-4339.patch
Patch7:		openssl-0.9.8b-CVE-2006-2937.patch
Patch8:		openssl-Bodo-CVE-2006-2940.patch
Patch9:		openssl-0.9.8b-CVE-2006-3738.patch
Patch10:	openssl-CVE-2006-4343.patch
Patch11:	openssl-0.9.8b-CVE-2006-2940-2.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	multiarch-utils >= 1.0.3

Requires:	%{libname} = %{version}-%{release}
Requires:	perl

%description
The openssl certificate management tool and the shared libraries that provide
various encryption and decription algorithms and protocols, including DES, RC4,
RSA and SSL.  This product includes software developed by the OpenSSL Project
for use in the OpenSSL Toolkit (http://www.openssl.org/).  This product
includes cryptographic software written by Eric Young (eay@cryptsoft.com).
This product includes software written by Tim Hudson (tjh@cryptsoft.com).


%package -n %{libnamedev}
Summary:	Secure Sockets Layer communications static libs & headers & utils
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	libopenssl-devel openssl-devel = %{version}-%{release}
Obsoletes:	openssl-devel

%description -n %{libnamedev}
The static libraries and include files needed to compile apps with support
for various cryptographic algorithms and protocols, including DES, RC4, RSA
and SSL.  This product includes software developed by the OpenSSL Project
for use in the OpenSSL Toolkit (http://www.openssl.org/).  This product
includes cryptographic software written by Eric Young (eay@cryptsoft.com).
This product includes software written by Tim Hudson (tjh@cryptsoft.com).

Patches for many networking apps can be found at: 
	ftp://ftp.psy.uq.oz.au/pub/Crypto/SSLapps/


%package -n %{libnamestatic}
Summary:	Secure Sockets Layer communications static libs & headers & utils
Group:		Development/Other
Requires:	%{libnamedev} = %{version}-%{release}
Provides:	libopenssl-static-devel openssl-static-devel = %{version}-%{release}

%description -n %{libnamestatic}
The static libraries and include files needed to compile apps with support
for various cryptographic algorithms and protocols, including DES, RC4, RSA
and SSL.  This product includes software developed by the OpenSSL Project
for use in the OpenSSL Toolkit (http://www.openssl.org/).  This product
includes cryptographic software written by Eric Young (eay@cryptsoft.com).
This product includes software written by Tim Hudson (tjh@cryptsoft.com).

Patches for many networking apps can be found at: 
	ftp://ftp.psy.uq.oz.au/pub/Crypto/SSLapps/


%package -n %{libname}
Summary:	Secure Sockets Layer communications libs
Group:		System/Libraries
Conflicts:	openssh < 3.5p1-4mdk

%description -n %{libname}
The libraries files are needed for various cryptographic algorithms
and protocols, including DES, RC4, RSA and SSL.  This product includes
software developed by the OpenSSL Project for use in the OpenSSL Toolkit
(http://www.openssl.org/).  This product includes cryptographic software
 written by Eric Young (eay@cryptsoft.com).  This product includes software
written by Tim Hudson (tjh@cryptsoft.com).

Patches for many networking apps can be found at: 
	ftp://ftp.psy.uq.oz.au/pub/Crypto/SSLapps/


%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .ia64-asm
#%patch2 -p0 -b .optflags
%patch3 -p0 -b .lib64
%patch4 -p1 -b .can-2005-2946
%patch5 -p1 -b .can-2005-2969
%patch6 -p0 -b .cve-2006-4339
%patch7 -p1 -b .cve-2006-2937
%patch8 -p0 -b .cve-2006-2940
%patch9 -p1 -b .cve-2006-3738
%patch10 -p0 -b .cve-2006-4343
%patch11 -p1 -b .cve-2006-2940

perl -pi -e "s,^(LIB=).+$,\1%{_lib}," Makefile.org
perl -pi -e "s,^(LIB=).+$,\1%{_lib}," engines/Makefile


%build 
# Don't carry out asm optimization on Alpha for now
%ifarch alpha amd64 x86_64 sparc sparc64
    # [gb] likewise on amd64: seems broken and no time to review
    # [stefan@eijk,nu] ditto for sparc/sparc64
    NO_ASM="no-asm"
%endif
sh config $NO_ASM --prefix=%{_prefix} --openssldir=%{_libdir}/ssl shared
make
# All tests must pass
export LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
make test


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall INSTALL_PREFIX=%{buildroot} MANDIR=%{_mandir}

cp -aRf *.so* %{buildroot}/%{_libdir}
cp -aRf *.a %{buildroot}/%{_libdir}

# openssl was named ssleay in "ancient" times.
ln -sf openssl %{buildroot}/%{_bindir}/ssleay

# The man pages rand.3 and passwd.1 conflict with other packages
# Rename them to ssl-* and also make a symlink from openssl-* to ssl-*
mv %{buildroot}/%{_mandir}/man1/passwd.1 %{buildroot}/%{_mandir}/man1/ssl-passwd.1
ln -sf ssl-passwd.1.bz2 %{buildroot}/%{_mandir}/man1/openssl-passwd.1.bz2

for i in rand err; do
    mv %{buildroot}/%{_mandir}/man3/$i.3 %{buildroot}/%{_mandir}/man3/ssl-$i.3
    ln -sf ssl-$i.3.bz2 %{buildroot}/%{_mandir}/man3/openssl-$i.3.bz2
done

rm -rf {main,devel}-doc-info
mkdir -p {main,devel}-doc-info
cat - << EOF > main-doc-info/README.Annvix-manpage
Warning:
The man page of passwd, passwd.1, has been renamed to ssl-passwd.1
to avoid a conflict with passwd.1 man page from the package passwd.
EOF

cat - << EOF > devel-doc-info/README.Annvix-manpage
Warning:
The man page of rand, rand.3, has been renamed to ssl-rand.3
to avoid a conflict with rand.3 from the package man-pages
The man page of err, err.3, has been renamed to ssl-err.3
to avoid a conflict with err.3 from the package man-pages
EOF

rm -f %{buildroot}%{_libdir}/libssl.so.0
rm -f %{buildroot}%{_libdir}/libcrypto.so.0
cd %{buildroot}%{_libdir}
ln -sf libssl.so.0.* libssl.so
ln -sf libcrypto.so.0.* libcrypto.so

chmod 0755 %{buildroot}%{_libdir}/pkgconfig

%multiarch_includes %{buildroot}%{_includedir}/openssl/opensslconf.h

rm -f %{buildroot}%{_mandir}/man7/Modes*

# get rid of dangling symlinks in /usr/lib for 64bit arches
%ifarch x86_64 amd64 ppc64
rm -rf %{buildroot}%{_prefix}/lib
%endif


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files 
%defattr(-,root,root)
%doc LICENSE CHANGES FAQ NEWS README
%doc main-doc-info/README*
%{_bindir}/*
%dir %{_libdir}/ssl
%{_libdir}/ssl/*
%{_mandir}/man[157]/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*
%dir %{_libdir}/engines
%{_libdir}/engines/*

%files -n %{libnamedev}
%defattr(-,root,root)
%doc doc/*
%doc devel-doc-info/README*
%dir %{_includedir}/openssl/
%multiarch %{multiarch_includedir}/openssl/opensslconf.h
%{_includedir}/openssl/*
%{_libdir}/lib*.so
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*

%files -n %{libnamestatic}
%defattr(-,root,root)
%{_libdir}/lib*.a


%changelog
* Mon Oct 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8
- P7: security fix for CVE-2006-2937
- P8: security fix for CVE-2006-2940
- P9: security fix for CVE-2006-3738
- P10: security fix for CVE-2006-4343
- P11: security fix for CVE-2006-2940 (final fix)

* Wed Sep 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8
- P6: security fix for CVE-2006-4339

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Clean rebuild

* Sun Jan 08 2006 Vincent Danen <vdanen-at-build.annvix.org>
- Obfuscate email addresses and new tagging
- Uncompress patches

* Wed Oct 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8-3avx
- P4: enhanced fix for CAN-2005-2946 (0.9.8 already defaults to a
  default_md of sha1, but we also add it to the [req] section as well)
- P5: fix for CAN-2005-2969

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8-2avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8-1avx
- 0.9.8
- drop P4; code is gone
- multiarch support
- disable P2; use openssl's default compiler options
- rediff P3
- drop P5; applied upstream

* Sat Jun 11 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.7e-3avx
- P5: security fix for CAN-2005-0109
- spec cleanups

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 0.9.7e-2avx
- bootstrap build

* Sat Dec 04 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.7e-1avx
- 0.9.7e
- use original sources and include gpg sig
- updated P2 and P3 from mdk
- spec cleanups

* Sat Dec 04 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.7d-3avx
- P4: security fix for CAN-2004-0975

* Tue Aug 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.7d-2avx
- remove "Modes of Des.7" manpage since it's a symlink to des_modes.7
- change README.Mandrake-manpage to README.Annvix-manpage

* Fri Aug 13 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.7d-1avx
- 0.9.7d
- don't use broken sparc/sparc64 asm optimizations for now (stefan)
- rediff P3 (jmdault)
- remove P4, P5, P6, P7; included upstream
- patch policy

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 0.9.7b-8avx
- require packages not files
- Annvix build

* Wed Mar 17 2004 Vincent Danen <vdanen@opensls.org> 0.9.7b-7sls
- remove %%french_policy macro
- security fixes for CAN-2004-0079 and CAN-2004-0112
- minor spec cleanups

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 0.9.7b-6sls
- merge gbeauchesne's amd64 fix for broken asm optimizations (5mdk)

* Mon Dec 02 2003 Vincent Danen <vdanen@opensls.org> 0.9.7b-5sls
- OpenSLS build
- tidy spec

* Tue Sep 30 2003 Vincent Danen <vdanen@mandrakesoft.com> 0.9.7b-4.1.92mdk
- security fixes: CAN-2003-0543, CAN-2003-0544, CAN-2003-0545

* Thu Jul 31 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.9.7b-4mdk
- Patch2: Make sure to handle RPM_OPT_FLAGS in Configure

* Tue Jul  8 2003 Guillaume Cottenceau <gc@mandrakesoft.com> 0.9.7b-3mdk
- rebuild for new devel provides

* Sat May 10 2003 Stefan van der Eijk <stefan@eijk.nu> 0.9.7b-2mdk
- add Provides to static-devel package
- Removed BuildRequires: /usr/bin/perl --> is Required by rpm-build

* Wed May 07 2003 Yves Duret <yves@zarb.org> 0.9.7b-1mdk
- doing the work.
- %%ifarch ia64 x86_64 patch1 and2
- removed patch 7, 8 merged upstream.

* Wed May  7 2003 Frederic Crozat <fcrozat@mandrakesoft.com> - 0.9.7a-3mdk
- Add missing pkgconfig file in devel package

* Tue Apr 1 2003 Vincent Danen <vdanen@mandrakesoft.com> 0.9.7a-2mdk
- security update

* Sat Feb 22 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.9.7a-1mdk
- new security release, fixes timing-based attack on CBC ciphersuites in
  SSL and TLS. See: http://www.openssl.org/news/secadv_20030219.txt
- use %%mklibname

* Tue Jan 14 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.9.7-3mdk
- removed libssl.so.0

* Tue Jan 14 2003 Frederic Lepied <flepied@mandrakesoft.com> 0.9.7-2mdk
- conflicts with openssh < 3.5p1-4md

* Mon Jan 13 2003 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.9.7-1mdk
- new version
- rediff p0 and p2
- remove p3 (what was that for?)

* Mon Dec 09 2002 François Pons <fpons@mandrakesoft.com> 0.9.6h-1mdk
- rebuild using make instead of %%make, sorry this is much faster to fix.
- 0.9.6h.

* Fri Aug 15 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.9.6g-1mdk
- 0.9.6g
- include md5 signature
- rediff patch2

* Thu Aug  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 0.9.6e-1mdk
- removed patch6 (integrated upstream)
- rediff patch3
- split static lib
- 0.9.6e

* Wed Jun 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.9.6d-6mdk
- fix err.3 conflict

* Mon Jun 24 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.9.6d-5mdk
- Sanitize specfile (factorization)
- Make sure tests are always run and don't let them fail
- Patch6: Use -dumpversion to get gcc3 version
- Patch7: Add 64-bit config support

* Sun May 26 2002 Yves Duret <yduret@mandrakesoft.com> 0.9.6d-4mdk
- openssl requires libopenssl = %{version}-%{release}.
- more spec clean up.
- rpmlint: license is BSD-like as say the LICENSE file instead of the unprecise OpenSource term.

* Wed May 22 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.9.6d-3mdk
- Fix Requires/BuildRequires.

* Thu May 16 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.9.6d-2mdk
- Little spec cleanup.

* Thu May 16 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.9.6d-1mdk
- Release 0.9.6d.
- Remake the patches.

* Mon Feb 04 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.9.6c-2mdk
- Don't apply patch for the SSL ciphers limit.

* Mon Jan 21 2002 Christian Belisle <cbelisle@mandrakesoft.com> 0.9.6c-1mdk
- Release 0.9.6c.
- Remake the patches

* Wed Jan  9 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.9.6b-6mdk
- Remove Patch6 as all SSH implementations are required to support
  SSH_CIPHER_DES and SSH_CIPHER_3DES. The latter turns out to be
  Triple-Key Triple-DES.

* Tue Jan  8 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.9.6b-5mdk
- 2 patches to follow French policy:
  - Patch5: Limit SSL ciphers available to 128 bits
  - Patch6: Temptatively disable triple-key triple DES but keep
    double-key triple DES

* Wed Dec 05 2001 Christian Belisle <cbelisle@mandrakesoft.com> 0.9.6b-4mdk
- gzip the source (for the sig file).

* Wed Dec 05 2001 Christian Belisle <cbelisle@mandrakesoft.com> 0.9.6b-3mdk
- Patch for gcc3 (thanks to fcrozat)
- bzip2 the source.

* Wed Oct 10 2001 Christian Belisle <cbelisle@mandrakesoft.com> 0.9.6b-2mdk
- Added missing files (thanx to jacco2_at_dds.nl)

* Sun Sep  2 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.9.6b-1mdk
- new version

* Thu Jul 12 2001 Stew Benedict <sbenedict@mandrakesoft.com> 0.9.6a-4mdk
- PPC configure patch

* Mon Jun 25 2001 Matthias Badaire <mbadaire@mandrakesoft.com> 0.9.6a-3mdk
- ia64 patch for configure

* Mon May  7 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.9.6a-2mdk
- libopenssl0-devel Obsoletes openssl-devel

* Thu May  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 0.9.6a-1mdk
- libification
- 0.9.6a

* Fri Mar 23 2001 David BAUDENS <baudens@mandrakesoft.com> 0.9.6-7mdk
- PPC: build with gcc

* Thu Mar 22 2001 Pixel <pixel@mandrakesoft.com> 0.9.6-6mdk
- require /usr/bin/perl (aka perl-base) instead of perl

* Fri Feb 02 2001 Francis Galiegue <fg@mandrakesoft.com> 0.9.6-5mdk
- Added patch from RH (ia64 asm stuff)
- ia64 fails at make test, disable it for now

* Thu Jan  4 2001 Till Kamppeter <till@mandrakesoft.com> 0.9.6-4mdk
- moved /usr/lib/ssl/ directory from the devel package to the main package,
  it is needed for creating certificates.

* Fri Dec 22 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 0.9.6-3mdk
- fixed %%ifarch statement ( %%alpha --> alpha)
- fixed perl replace statement (alpha)

* Wed Dec 20 2000 David BAUDENS <baudens@mandrakesoft.com> 0.9.6-2mdk
- PPC: build with egcs. Compilation doesn't failed with gcc-2.96 but
  "make test" does. So...
- Use optimizations on all archs supported by LMDK
- Some spec clean up

* Sat Dec 02 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 0.9.6-1mdk
- new and shiny source.

* Sun Oct  1 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.9.5a-8mdk
- added BuildRequires on bc.

* Sun Sep 24 2000 Alexander Skwar <ASkwar@DigitalProjects.com> 0.9.5a-7mdk
- As suggested by Chmou, *all* man pages for ssl are beneath
  %{_mandir}, but the offending man pages (rand.3 and passwd.1) have been
  renamed to ssl-rand.3 and ssl-passwd.1
- Added README.Mandrake-manpage to warn/inform users about the conflicting
  man pages
- Removed de and fr summaries and decriptions

* Sun Sep 24 2000 Alexander Skwar <ASkwar@DigitalProjects.com> 0.9.5a-6mdk
- bzip2 the man pages

* Sun Sep 24 2000 Alexander Skwar <ASkwar@DigitalProjects.com> 0.9.5a-5mdk
- Re-add the man pages, which were left out in -4mdk
- Man pages in /usr/lib/ssl as passwd.1 conflicts with the man page for passwd from
  the package passwd and because rand.3 conflicts with rand.3 from man-pages
- Some more clean up
- More doc files

* Fri Sep 22 2000 Alexander Skwar <ASkwar@DigitalProjects.com> 0-9-5a-4mdk
- Use macros
- Doc's in /usr/share/doc
- Man pages in /usr/share/man, no longer "hidden" in /usr/lib/ssl/man
- Quiet setup
- Clean up a lot (chmou).

* Wed May 24 2000 Frederic Lepied <flepied@mandrakesoft.com> 0.9.5a-3mdk
- corrected configure on sparc.

* Mon May 08 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.9.5a-3mdk
- forgot libcrypto.a in devel (DOH!) Put it back again

* Thu Apr 27 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.9.5a-2mdk
- mv /usr/local/ssl to /usr/lib/ssl

* Wed Apr 26 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.9.5a-1mdk
- re-did package for 0.9.5a 

* Tue Feb 29 2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.9.5-1mdk
- updated to 0.9.5

* Sat Feb 26  2000 Jean-Michel Dault <jmdault@mandrakesoft.com> 0.9.4-9mdk
- removed brokenmips and linux.sh search&replace because they are
  not in the source anymore

* Mon Jan  3 2000 Jean-Michel Dault <jmdault@netrevolution.com>
- final cleanup for Mandrake 7

* Thu Dec 30 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- rebuild on 7.0

* Sat Aug 14 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to 0.9.4
- cleaned SPEC file to compile on Solaris/UltraSparc
- added SSL_USE_SDBM to avoid segfaults

* Sat Jul 31 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- made a link from openssl to ssleay because many sites have old
  documentation

* Thu Jul 22 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- added fr summary

* Thu Jun 24 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- permit SMP build

* Sat May 29 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to 0.9.3a
- added fr locale

* Sun May 23 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- handle RPM_OPT_FLAGS
- add de locale

* Sat May 22 1999 Jean-Michel Dault <jmdault@netrevolution.com>
  Updated the compiler flags

* Fri May 21 1999 Jean-Michel Dault <jmdault@netrevolution.com>
  Packaged for Linux-Mandrake
  
* Mon May 17 1999 Henri Gomez <gomez@slib.fr>
  BIO_set_fp patch added. (no more core under RH6.0).
  Correct rm -rf of /var/tmp

* Mon Mar 22 1999 rse
- function names recently changed - consistency.

- Be consistent: 0.9.2b

* Mon Mar 22 1999 Ben Laurie, problem pointed out by Holger Reif, Bodo Moeller (and ???)
- Fix security hole.

* Sat Mar 20 1999 Ulf Moeller <ulf@fitug.de>
- Some more source tree cleanups (removed obsolete files 
  crypto/bf/asm/bf586.pl, test/test.txt and crypto/sha/asm/f.s; changed 
  permission on "config" script to be executable) and a fix for the 
  INSTALL document.    Submitted by: Ulf Moeller <ulf@fitug.de> Reviewed 
  by: Ralf S. Engelschall

* Sun Mar 14 1999 Lennart Bang <lob@netstream.se>, with minor changes by Steve
- Remove some references which called malloc and free instead of Malloc 
  and Free.

* Fri Mar 12 1999 Ulf Moeller <ulf@fitug.de>
- Fail if test fails.

* Fri Mar 12 1999 Matthias Loepfe <Matthias.Loepfe@AdNovum.CH>
- Solaris shared library support.

* Fri Mar 12 1999 Ben Laurie
- Use the right compiler for ctx_size.

* Fri Mar 12 1999 Steve Henson
- Delete NULL ciphers from 'ALL' in the cipher list aliases. This means 
  that NULL ciphers specifically have to be enabled with e.g. 
  "DEFAULT:eNULL". This prevents cipher lists from inadvertantly having 
  NULL ciphers at the top of their list (e.g. the default ones) because 
  they didn't have to be taken into account before.

* Thu Mar 11 1999 Steve Henson
- Fix for RSA private key encryption if p < q. This took ***ages*** to 
  track down.

* Wed Mar 10 1999 Matthias Loepfe <Matthias.Loepfe@adnovum.ch>
- Be less restrictive and allow also `perl util/perlpath.pl 
  /path/to/bin/perl' in addition to `perl util/perlpath.pl /path/to/bin', 
  because this way one can also use an interpreter named `perl5' (which 
  is usually the name of Perl 5.xxx on platforms where an Perl 4.x is 
  still installed as `perl').    Submitted by: Matthias Loepfe 
  <Matthias.Loepfe@adnovum.ch> Reviewed by: Ralf S. Engelschall
- Let util/clean-depend.pl work also with older Perl 5.00x versions.    
  Submitted by: Matthias Loepfe <Matthias.Loepfe@adnovum.ch> Reviewed by: 
  Ralf S. Engelschall

* Wed Mar 10 1999 Steve Henson
- Fix couple of ANSI declarations and prototypes

* Wed Mar 10 1999 steve
- Make CC,CFLAG etc get passed to make links and various Win32 fixes.

* Tue Mar  9 1999 Ben Laurie
- Fix quad checksum bug.

* Tue Mar  9 1999 Steve Henson
- Comment out two unimplemented functions from bio.h. Attempt to get 
  the Win32 test batch file going again.

* Mon Mar  8 1999 steve
- Add missing funtions from non ANSI section of header files and add 
  missing ordinals to libeay.num.

* Mon Mar  8 1999 Ralf S. Engelschall
- Make `openssl version' output lines consistent.
- Fix Win32 symbol export lists for BIO functions: Added 
  BIO_get_ex_new_index, BIO_get_ex_num, BIO_get_ex_data and 
  BIO_set_ex_data to ms/libeay{16,32}.def. I'm not a Win32 hacker, but I 
  think I've done it correctly.    Steve or Ben: can you confirm that 
  it's correct? I don't want to break any Win32 stuff.
- Second round of fixing the OpenSSL perl/ stuff. It now at least 
  compiled fine under Unix and passes some trivial tests I've now added. 
  But the whole stuff is horribly incomplete, so a README.1ST with a 
  disclaimer was added to make sure no one expects that this stuff really 
  works in the OpenSSL 0.9.2 release. Additionally I've started to clean 
  the XS sources up and fixed a few little bugs and inconsistencies in 
  OpenSSL.{pm,xs} and openssl_bio.xs.    PS: I'm still not convinces 
  whether we should try to make this finally running or kick it out and 
  replace it with some other module.... 

* Sun Mar  7 1999 ben
- Don't make links on Windoze.

* Sun Mar  7 1999 Kenji Miyake <kenji@miyake.org>, integrated by Ben Laurie
- Fix perl assembler.

* Sun Mar  7 1999 John Tobey <jtobey@channel1.com>
- Linux MIPS support.

* Sun Mar  7 1999 Ben Laurie
- Always make links.

* Sat Mar  6 1999 steve
- Added support for adding extensions to CRLs, also fix a memory leak 
  and make 'req' check the config file syntax before it adds extensions. 
  Added info in the documentation as well.

* Sat Mar  6 1999 Ralf S. Engelschall
- Add a useful kludge to allow package maintainers to specify compiler 
  and other platforms details on the command line without having to patch 
  the Configure script everytime: One now can use ``perl Configure 
  <id>:<details>'', i.e. platform ids are allowed to have details 
  appended to them (seperated by colons). This is treated as there would 
  be a static pre-configured entry in Configure's %table under key <id> 
  with value <details> and ``perl Configure <id>'' is called.  So, when 
  you want to perform a quick test-compile under FreeBSD 3.1 with pgcc 
  and without assembler stuff you can use ``perl Configure 
  "FreeBSD-elf:pgcc:-O6:::"'' now, which overrides the FreeBSD-elf entry 
  on-the-fly.      (PS: Notice that the same effect _cannot_ be achieved 
  by using ``make CC=pgcc ..'' etc, because you cannot override all 
  things from there.)

* Sat Mar  6 1999 Ben Laurie
- Disable new TLS1 ciphersuites.

* Sat Mar  6 1999 Ralf S. Engelschall
- Allow DSO flags like -fpic, -fPIC, -KPIC etc. to be specified on the 
  `perl Configure ...' command line. This way one can compile OpenSSL 
  libraries with Position Independent Code (PIC) which is needed for 
  linking it into DSOs.

* Sat Mar  6 1999 Ben Laurie
- Fix export ciphersuites, again.

* Sat Mar  6 1999 rse
- just a little typo

* Sat Mar  6 1999 Ralf S. Engelschall
- Cleaned up the LICENSE document: The official contact for any license 
  questions now is the OpenSSL core team under openssl-core@openssl.org.  
  And add a paragraph about the dual-license situation to make sure 
  people recognize that _BOTH_ the OpenSSL license _AND_ the SSLeay 
  license apply to the OpenSSL toolkit.  
- General source tree makefile cleanups: Made `making xxx in yyy...' 
  display consistent in the source tree and replaced `/bin/rm' by `rm'.  
  Additonally cleaned up the `make links' target: Remove unnecessary 
  semicolons, subsequent redundant removes, inline point.sh into 
  mklink.sh to speed processing and no longer clutter the display with 
  confusing stuff. Instead only the actually done links are displayed.

* Sat Mar  6 1999 Ben Laurie
- Permit null ciphers.

* Fri Mar  5 1999 Steve Henson
- Fix the PKCS#7 stuff: signature verify could fail if attributes 
  reordered, the detached data encoding was wrong and free up public keys.

* Fri Mar  5 1999 steve
- Workaround for a Win95 console bug triggered by the password read 
  stuff.

* Thu Mar  4 1999 Steve Henson
- Deleted my str_dup() function from X509V3: the same functionality is 
  provided by BUF_MEM_strdup(). Added text documentation to the BUF_MEM 
  stuff.

* Thu Mar  4 1999 Ralf S. Engelschall
- Added the new `Includes OpenSSL Cryptography Software' button as 
  doc/openssl_button.{gif,html} which is similar in style to the old 
  SSLeay button and can be used by applications based on OpenSSL to show 
  the relationship to the OpenSSL project.    PS: This beast caused me 
  three hours to create, because of the size I had to hand-paint the 7pt 
  fonts in Photoshop.

* Thu Mar  4 1999 Lennart Bong <lob@kulthea.stacken.kth.se>
- Remove confusing variables in function signatures in files 
  ssl/ssl_lib.c and ssl/ssl.h. At least the double ctx-variable confused 
  some compilers.    Submitted by: Lennart Bong 
  <lob@kulthea.stacken.kth.se> Reviewed by: Ralf S. Engelschall
- Don't install bss_file.c under PREFIX/include/.  It was introduced by 
  Eric between SSLeay 0.8 and 0.9 and just looks useless and confusing.   
 Pointed out by: Lennart Bong <lob@kulthea.stacken.kth.se> Submitted 
  by: Ralf S. Engelschall

* Wed Mar  3 1999 Steve Henson
- Fix the Win32 compile environment and add various changes so it will 
  now compile under Win32 (9X and NT) again. Note: some signed/unsigned 
  changes recently checked in were killing the Win32 compile.

* Sun Feb 28 1999 Ben Laurie
- Add functions to add certs to stacks, used for CA file/path stuff in 
  servers.
- Experiment with doxygen documentation.

* Sat Feb 27 1999 Ralf S. Engelschall, pointed out by Carlos Amengual
- Get rid of remaining C++-style comments which strict C compilers 
  hate. (Pointed out by Carlos Amengual).

* Fri Feb 26 1999 Steve Henson
- BN_RECURSION causes the stuff in bn_mont.c to fall over for large 
  keys. For now change it to BN_RECURSION_MONT so it isn't compiled in.

* Thu Feb 25 1999 Ralf S. Engelschall
- Add a bunch of SSL_xxx() functions for configuring the temporary RSA 
  and DH private keys and/or callback functions which directly correspond 
  to their SSL_CTX_xxx() counterparts but work on a per-connection basis. 
  This is needed for applications which have to configure certificates on 
  a per-connection basis (e.g. Apache+mod_ssl) instead of a per-context 
  basis (e.g. s_server).      For the RSA certificate situation is makes 
  no difference, but for the DSA certificate situation this fixes the "no 
  shared cipher" problem where the OpenSSL cipher selection procedure 
  failed because the temporary keys were not overtaken from the context 
  and the API provided no way to reconfigure them.    The new functions 
  now let applications reconfigure the stuff and they are in detail: 
  SSL_need_tmp_RSA, SSL_set_tmp_rsa, SSL_set_tmp_dh, 
  SSL_set_tmp_rsa_callback and SSL_set_tmp_dh_callback.  Additionally a 
  new non-public-API function ssl_cert_instantiate() is used as a helper 
  function and also to reduce code redundancy inside ssl_rsa.c.    
  Submitted by: Ralf S. Engelschall Reviewed by: Ben Laurie
- Move s_server -dcert and -dkey options out of the undocumented 
  feature area because they are useful for the DSA situation and should 
  be recognized by the users. Thanks to Steve for the original hint.

* Thu Feb 25 1999 Richard Levitte <levitte@stacken.kth.se>
- Fix the cipher decision scheme for export ciphers: the export bits 
  are *not* within SSL_MKEY_MASK or SSL_AUTH_MASK, they are within 
  SSL_EXP_MASK.  So, the original variable has to be used instead of the 
  already masked variable.    Submitted by: Richard Levitte 
  <levitte@stacken.kth.se> Reviewed by: Ralf S. Engelschall
- Fix 'port' variable from `int' to `unsigned int' in 
  crypto/bio/b_sock.c    Submitted by: Richard Levitte 
  <levitte@stacken.kth.se> Reviewed by: Ralf S. Engelschall
- Change type of another md_len variable in 
  pk7_doit.c:PKCS7_dataFinal() from `int' to `unsigned int' because it's 
  a length and initialized by EVP_DigestFinal() which expects an 
  `unsigned int *'.    Submitted by: Richard Levitte 
  <levitte@stacken.kth.se> Reviewed by: Ralf S. Engelschall

* Thu Feb 25 1999 Ralf S. Engelschall
- Don't hard-code path to Perl interpreter on shebang line of Configure 
  script. Instead use the usual Shell->Perl transition trick.

* Wed Feb 24 1999 Ralf S.  Engelschall
- Make `openssl x509 -noout -modulus' functional also for DSA 
  certificates (in addition to RSA certificates) to match the behaviour 
  of `openssl dsa -noout -modulus' as it's already the case for `openssl 
  rsa -noout -modulus'.  For RSA the -modulus is the real "modulus" while 
  for DSA currently the public key is printed (a decision which was 
  already done by `openssl dsa -modulus' in the past) which serves a 
  similar purpose.  Additionally the NO_RSA no longer completely removes 
  the whole -modulus option; it now only avoids using the RSA stuff. Same 
  applies to NO_DSA now, too.

* Tue Feb 23 1999 Arne Ansper <arne@ats.cyber.ee>
- Add reliable BIO.

* Tue Feb 23 1999 Steve Henson
- Redo the way 'req' and 'ca' add objects: add support for oid_section.

* Mon Feb 22 1999 Arne Ansper <arne@ats.cyber.ee>, integrated by Ben Laurie
- Add syslogging BIO.

* Sun Feb 21 1999 Ben Laurie
- Add support for new TLS export ciphersuites.

* Sun Feb 21 1999 Steve Henson
- Add preliminary user level config documentation for extension stuff. 
  Programming info will come later...    Feel free to reformat and tidy 
  this up...

* Sun Feb 21 1999 Ulf Moeller <ulf@fitug.de>
- Make RSA_NO_PADDING really use no padding.    Submitted by: Ulf 
  Moeller <ulf@fitug.de>

* Sat Feb 20 1999 Ben Laurie
- Generate errors when public/private key check is done.

* Fri Feb 19 1999 Steve Henson
- Overhaul 'crl' application, add a proper X509_CRL_print function and 
  start to support CRL extensions.

* Wed Feb 17 1999 Steve Henson
- Fuller authority key id support, partial support for private key 
  usage extension and really fix the ASN.1 IMPLICIT bug this time :-)

* Wed Feb 17 1999 Ulf Moeller <ulf@fitug.de>, reformatted, corrected and integrated by
+      Ben Laurie
- Add OAEP. 

* Tue Feb 16 1999 Eric A. Young, (from changes to C2Net SSLeay, integrated by Mark Cox)
- Updates to the new SSL compression code [Eric A. Young, (from changes 
  to C2Net SSLeay, integrated by Mark Cox)]    Fix so that the version 
  number in the master secret, when passed via RSA, checks that if TLS 
  was proposed, but we roll back to SSLv3 (because the server will not 
  accept higher), that the version number is 0x03,0x01, not 0x03,0x00 
  [Eric A. Young, (from changes to C2Net SSLeay, integrated by Mark Cox)] 
   Submitted by:  Reviewed by:  PR:  

* Mon Feb 15 1999 Steve Henson
- Fix various memory leaks in SSL, apps and DSA

* Sun Feb 14 1999 steve
- Add support for raw extensions. This means that you can include the 
  DER encoding of an arbitrary extension: e.g. 
  1.3.4.5=critical,RAW:12:34:56 Using this technique currently 
  unsupported extensions can be generated if you know their DER encoding. 
  Even if the extension is supported in future the raw extension will 
  still work: that is the raw version can always be used even if it is a 
  supported extension. 

* Sun Feb 14 1999 Lars Weber <3weber@informatik.uni-hamburg.de>
- Make sure latest Perl versions don't interpret some generated C array 
  as Perl array code in the crypto/err/err_genc.pl script.    Submitted 
  by: Lars Weber <3weber@informatik.uni-hamburg.de> Reviewed by: Ralf s. 
  Engelschall

* Sun Feb 14 1999 Steve Henson
- More Win32 fixes and upsdate INSTALL.W32 documentation.

* Sat Feb 13 1999 Steve Henson
- Oops... add other changes this time too.

* Sat Feb 13 1999 Ben Laurie
- Fix ghastly DES declarations, and all consequential warnings.

* Sat Feb 13 1999 Steve Henson
- Fix typo in asn1.h (PRINTABLESTRING_STRING) and fix a bug in object 
  creation perl script. It failed if the OID had any zeros in it.

* Sat Feb 13 1999 Ben Laurie
- Add support for 3DES CBCM mode.
- In the absence of feedback either way, commit the fix that looks 
  right for wrong keylength with export null ciphers.

* Thu Feb 11 1999 steve
- Make the 'crypto' and 'ssl' options in the perl script mkdef.pl 
  really work, also add an 'update' option to automatically append any 
  new functions to the ssleay.num and libeay.num files.

* Wed Feb 10 1999 Ralf S. Engelschall
- Overhauled the Perl interface (perl/*):
	* ported BN stuff to  OpenSSL's different BN library
	* made the perl/ source tree  CVS-aware
	* renamed the package from SSLeay to OpenSSL (the files still contain
	  their history because I've copied them in the repository)
	* removed obsolete files (the test scripts will be replaced by better
	  Test::Harness variants in the future)
- Remember the cleanup

* Wed Feb 10 1999 Steve Henson
- More extension code. Incomplete support for subject and issuer alt 
  name, issuer and authority key id. Change the i2v function parameters 
  and add an extra 'crl' parameter in the X509V3_CTX structure: guess 
  what that's for :-) Fix to ASN1 macro which messed up IMPLICIT tag and 
  add f_enum.c which adds a2i, i2a for ENUMERATED.

* Tue Feb  9 1999 Steve Henson
- Support for ASN1 ENUMERATED type. This copies and duplicates the 
  ASN1_INTEGER code and adds support to ASN1_TYPE and asn1parse.

* Sun Jan 31 1999 Eric A. Young, (from changes to C2Net SSLeay, integrated by Mark Cox)
- Add new function, EVP_MD_CTX_copy() to replace frequent use of 
  memcpy.    Submitted by: Eric A Young - from changes to C2Net SSLeay 
  Reviewed by: Mark Cox PR:  

* Sun Jan 31 1999 Ralf S. Engelschall, Matthias Loepfe <Matthias.Loepfe@adnovum.ch>
- Make sure `make rehash' target really finds the `openssl' program.

* Sat Jan 30 1999 Ben Laurie
- Squeeze a bit more speed out of MD5 assembler.

* Sat Jan 30 1999 Alan Batie <batie@aahz.jf.intel.com>
- Add CygWin32 platform information to Configure script.    Submitted 
  by: Alan Batie <batie@aahz.jf.intel.com>

* Sat Jan 30 1999 Rainer W. Gerling <gerling@mpg-gv.mpg.de>
- Fixed ms/32all.bat script: `no_asm' -> `no-asm'    Submitted by: 
  Rainer W. Gerling <gerling@mpg-gv.mpg.de> Reviewed by: Ralf S. 
  Engelschall

* Fri Jan 29 1999 Steve Henson
- New program 'nseq' added to apps to allow Netscape certificate 
  sequences to be pulled apart and built.
- Allow the -certfile argument to be used multiple times in crl2pkcs7. 
  Also fix typos in the usage messages: "inout" instead of "input".

* Thu Jan 28 1999 Eric A. Young, (from changes to C2Net SSLeay, integrated by Mark Cox)
- Fixes to BN code.  Previously the default was to define BN_RECURSION 
  but the BN code had some problems that would cause failures when doing 
  certificate verification and some other functions.    Submitted by: 
  Eric A Young from a C2Net version of SSLeay Reviewed by: Mark J Cox PR: 

* Thu Jan 28 1999 Steve Henson
- Add ASN1 code for netscape certificate sequences.

* Tue Jan 26 1999 Steve Henson
- Add a few extended key usage OIDs.
- Still more X509 V3 stuff. Modify ca.c to work with the new code and 
  modify openssl.cnf for the new syntax.

* Mon Jan 25 1999 Steve Henson
- More X509 V3 stuff. Add support for extensions in the 'req' 
  application so that: openssl req -x509 -new -out cert.pem will take 
  extensions from openssl.cnf a sample for a CA is included. Also change 
  the directory order so pem is nearer the end. Otherwise 'make links' 
  wont work because pem.h can't be built.

* Sun Jan 24 1999 steve
- Continuing adding X509 V3 support. This starts to integrate the code 
  with the main library, but only with printing at present. To see this 
  try: openssl x509 -in cert.pem -text on a certificate with some 
  extensions in it.

* Sun Jan 24 1999 Steve Henson
- Initial addition of new X509 V3 files, tidy of old files.

* Wed Jan 20 1999 Steve Henson
- Continued patches so certificates and CRLs now can support and use 
  GeneralizedTime.  

* Tue Jan 19 1999 Ben Laurie
- Finally lay dependencies to rest (I hope!).

* Tue Jan 19 1999 Ben Laurie, reported by Jeremy Hylton <jeremy@cnri.reston.va.us>
- Spelling mistake. 

* Mon Jan 18 1999 steve
- New err_code.pl script to retain old error codes. This should allow 
  the use of 'make errors' without causing huge re-organisations of files 
  when a new code is added.

* Sun Jan 17 1999 Ulf Möller <ulf@fitug.de>
- Fix major cockup with short keys in CAST-128.

* Sun Jan 17 1999 Steve Henson
- Update CHANGES for GeneralizedTime info.

* Sun Jan 17 1999 Ulf Möller <ulf@fitug.de>
- Correct Linux 1 recognition. Contributed by: Ulf Möller <ulf@fitug.de>

* Sun Jan 17 1999 Anonymous <nobody@replay.com>
- Remove pointless MD5 hash. Contributed by: Anonymous 
  <nobody@replay.com>

* Sun Jan 17 1999 Ben Laurie, reported by Anonymous <nobody@replay.com>
- Generate an error on an invalid directory.

* Sat Jan 16 1999 Ben Laurie
- More prototypes. 

* Thu Jan 14 1999 Steve Henson
- Fix parameters to dummy function BN_ref_mod_exp().

* Thu Jan 14 1999 Neil Costigan <neil.costigan@celocom.com>
-       Submitted by: Neil Costigan <neil.costigan@celocom.com> PR:  

* Tue Jan 12 1999 Steve Henson
- Fix OBJ_txt2nid(): old function was broken when input used the "dot" 
  form, e.g. 1.2.3.4 . Also added new function OBJ_txt2obj().

* Sun Jan 10 1999 Ben Laurie
- Add prototype, fix parameter passing bug.

* Sat Jan  9 1999 Ben Laurie
- Sort openssl functions by name.

* Sat Jan  9 1999 Steve Henson
- Fix the gendsa program and add it to the app list. The progs.h file 
  is auto generated but not auto updated so it is included. Also remove 
  the encryption from the sample DSA keys.

* Thu Jan  7 1999 Frans Heymans <fheymans@isaserver.be>
- Accept NULL in *_free.

* Thu Jan  7 1999 Anonymous <nobody@replay.com>
- Fix DH key generation. Contributed by: Anonymous <nobody@replay.com>

* Thu Jan  7 1999 Bodo Moeller <3moeller@informatik.uni-hamburg.de>
- Send the right CAs to the client.
- Fix numeric -newkey args. Contributed by: Bodo Moeller 
  <3moeller@informatik.uni-hamburg.de>

* Wed Jan  6 1999 Anonymous <nobody@replay.com>
- Fix export tests.

* Wed Jan  6 1999 Ben Laurie
- Make the world a safer place (if people object to this kind of 
  change, speak up soon - I intend to do a lot of it!).

* Wed Jan  6 1999 Steve Henson
- Oops! update CHANGES file properly.

* Wed Jan  6 1999 steve
- Fix things so DH_free() will be no-op when passed NULL, like 
  RSA_free() and DSA_free(): this was causing crashes when for example an 
  attempt was made to handle a (currently) unsupported DH public key. 
  Also X509_PUBKEY_set()i wasn't checking errors from d2i_PublicKey().

* Mon Jan  4 1999 Arne Ansper <arne@ats.cyber.ee>
- Free the right thing.
- Only free if it ain't NULL.
- Remove the bugfix that was really a bug. Submitted by: Arne Ansper 
  <arne@ats.cyber.ee>
- Pass on BIO_CTRL_FLUSH. Submitted by: Arne Ansper <arne@ats.cyber.ee>

* Sun Jan  3 1999 Ralf S. Engelschall
- Make sure the already existing X509_STORE->depth variable is 
  initialized in X509_STORE_new(), but document the fact that this 
  variable is still unused in the certificate verification process.

* Sun Jan  3 1999 Steve Henson
- Make sure applications free up pkey structures and add netscape 
  extension handling to x509.c

* Sat Jan  2 1999 Ralf S. Engelschall, Paul Sutton and Ben Laurie
- Fix reference counting.

* Sat Jan  2 1999 Ralf S. Engelschall
- First cut of a cleanup for apps/. First the `ssleay' program is now 
  named `openssl' and second, the shortcut symlinks for the `openssl 
  <command>' are no longer created. This way we have a single and 
  consistent command line interface `openssl <command>', similar to `cvs 
  <command>'.    Notice, the openssl.cnf, openssl.c and progs.pl files 
  were changed after a repository copy, i.e. they still contain the 
  complete file history.

* Sat Jan  2 1999 Steve Henson
- Move DSA test in ca.c inside #ifdef and make pubkey BIT STRING always 
  have zero unused bits.

* Fri Jan  1 1999 Steve Henson
- Add extended key usage OID and update STATUS file.

* Fri Jan  1 1999 Paul Sutton
- Make the installation documentation easier to follow.

- Makefiles updated to exit if an error occurs in a sub-directory make 
  (including if user presses ^C)

* Thu Dec 31 1998 Ben Laurie
- Document recent changes.

* Thu Dec 31 1998 rse
- Fix version stuff:    1. The already released version was 0.9.1c and 
  not 0.9.1b    2. The next release should be 0.9.2 and not 0.9.1d, 
  because first the changes are already too large, second we should avoid 
  any more 0.9.1x confusions and third, the Apache version semantics of 
  VERSION.REVISION.PATCHLEVEL for the version string is reasonable (and 
  here .2 is already just a patchlevel and not major change). tVS: 
---------------------------------------------------------------------- 

* Thu Dec 31 1998 Steve Henson
- Update CHANGES file for latest additions

* Wed Dec 30 1998 Ben Laurie - pointed out by Ulf Möller <ulf@fitug.de>
- MIME encoding and ISO chars at the same time messes up the stuff

* Wed Dec 30 1998 Ralf S. Engelschall
- Ops, forgot to commit the changes entry in recent commit...

* Tue Dec 29 1998 Ben Laurie
- Fix incorrect DER encoding of SETs and all knock-ons from that.

* Tue Dec 29 1998 Ben Laurie - pointed out by Ulf Möller <ulf@fitug.de>
- Add prototypes. Make Montgomery stuff explicitly for that purpose.

* Mon Dec 28 1998 Ben Laurie
- Deal with generated files.

* Mon Dec 28 1998 ben
- Typo.  

* Mon Dec 28 1998 Ben Laurie
- Autodetect FreeBSD 3.

- Add strictness, fix variable substition bugs.

* Sat Dec 26 1998 rse
- Test for new CVS repository

* Wed Dec 23 1998 The OpenSSL Project
- Switch to OpenSSL name

* Tue Dec 22 1998 Ralf S. Engelschall, Beckmann <beckman@acl.lanl.gov>
- Incorporation of RSEs assembled patches

