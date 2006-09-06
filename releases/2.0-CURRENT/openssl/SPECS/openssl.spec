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
%define version		0.9.8b
%define release		%_revrel

%define maj		0.9.8
%define libname 	%mklibname %{name} %{maj}

# Number of threads to spawn when testing some threading fixes.
#%define thread_test_threads %{?threads:%{threads}}%{!?threads:1}

Summary:	Secure Sockets Layer communications libs & utils
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD-like
Group:		System/Libraries
URL:		http://www.openssl.org/

Source:		ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.openssl.org/source/%{name}-%{version}.tar.gz.asc
Source2:	Makefile.certificate
Source3:	make-dummy-cert
Source4:	openssl-thread-test.c
# (fg) 20010202 Patch from RH: some funcs now implemented with ia64 asm
Patch1:		openssl-0.9.7-mdk-ia64-asm.patch
# (gb) 0.9.7b-4mdk: Handle RPM_OPT_FLAGS in Configure
Patch2:		openssl-0.9.8a-mdk-optflags.patch
# (gb) 0.9.7b-4mdk: Make it lib64 aware. TODO: detect in Configure
Patch3:		openssl-0.9.8b-lib64.diff
Patch6:		openssl-0.9.8-beta6-icpbrasil.diff
Patch7:		openssl-0.9.8a-defaults.patch
Patch9:		openssl-0.9.8a-enginesdir.patch
Patch10:	openssl-0.9.7-beta6-ia64.patch
Patch12:	openssl-0.9.6-x509.patch
Patch13:	openssl-0.9.7-beta5-version-add-engines.patch
Patch14:	openssl-0.9.8a-use-poll.patch
Patch15:	openssl-CVE-2006-4339.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	chrpath
BuildRequires:	zlib-devel

Requires:	%{libname} = %{version}-%{release}
Requires:	perl

%description
The openssl certificate management tool and the shared libraries that provide
various encryption and decription algorithms and protocols, including DES, RC4,
RSA and SSL.  This product includes software developed by the OpenSSL Project
for use in the OpenSSL Toolkit (http://www.openssl.org/).  This product
includes cryptographic software written by Eric Young (eay@cryptsoft.com).
This product includes software written by Tim Hudson (tjh@cryptsoft.com).


%package -n %{libname}-devel
Summary:	Secure Sockets Layer communications static libs & headers & utils
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	libopenssl-devel openssl-devel = %{version}-%{release}
Obsoletes:	openssl-devel

%description -n %{libname}-devel
The static libraries and include files needed to compile apps with support
for various cryptographic algorithms and protocols, including DES, RC4, RSA
and SSL.  This product includes software developed by the OpenSSL Project
for use in the OpenSSL Toolkit (http://www.openssl.org/).  This product
includes cryptographic software written by Eric Young (eay@cryptsoft.com).
This product includes software written by Tim Hudson (tjh@cryptsoft.com).

Patches for many networking apps can be found at: 
	ftp://ftp.psy.uq.oz.au/pub/Crypto/SSLapps/


%package -n %{libname}-static-devel
Summary:	Secure Sockets Layer communications static libs & headers & utils
Group:		Development/Other
Requires:	%{libname}-devel = %{version}-%{release}
Provides:	libopenssl-static-devel openssl-static-devel = %{version}-%{release}

%description -n %{libname}-static-devel
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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .ia64-asm
%patch2 -p0 -b .optflags

%patch3 -p1 -b .lib64
%patch6 -p0 -b .icpbrasil
%patch7 -p1 -b .defaults
%patch9 -p1 -b .enginesdir
%patch10 -p1 -b .ia64
%patch12 -p1 -b .x509
%patch13 -p1 -b .version-add-engines
%patch14 -p1 -b .use-poll
%patch15 -p0 -b .cve-2006-4339

perl -pi -e "s,^(OPENSSL_LIBNAME=).+$,\1%{_lib}," Makefile.org engines/Makefile

# fix perl path
perl util/perlpath.pl %{_bindir}/perl

cp %{_sourcedir}/openssl-thread-test.c .


%build 
# Figure out which flags we want to use.
# default
sslarch=%{_os}-%{_arch}
%ifarch %ix86
sslarch=linux-elf
if ! echo %{_target} | grep -q i[56]86 ; then
    sslflags="no-asm"
fi
%endif
%ifarch sparc
sslarch=linux-sparcv9
sslflags=no-asm
%endif
%ifarch alpha
sslarch=linux-alpha-gcc
%endif
%ifarch s390
sslarch="linux-generic32 -DB_ENDIAN -DNO_ASM"
%endif
%ifarch s390x
sslarch="linux-generic64 -DB_ENDIAN -DNO_ASM"
%endif

# ia64, x86_64, ppc, ppc64 are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
./Configure \
    --prefix=%{_prefix} \
    --openssldir=%{_sysconfdir}/pki/tls \
    ${sslflags} \
    --enginesdir=%{_libdir}/openssl/engines \
    no-idea \
    no-rc5 \
    shared \
    ${sslarch}

#    zlib no-idea no-mdc2 no-rc5 no-ec no-ecdh no-ecdsa shared ${sslarch}

# antibork stuff...
perl -pi -e "s|^#define ENGINESDIR .*|#define ENGINESDIR \"%{_libdir}/openssl/engines\"|g" crypto/opensslconf.h

# Add -Wa,--noexecstack here so that libcrypto's assembler modules will be
# marked as not requiring an executable stack.
RPM_OPT_FLAGS="%{optflags} -Wa,--noexecstack"
make depend
make all build-shared

# Generate hashes for the included certs.
make rehash build-shared

# Verify that what was compiled actually works.
export LD_LIBRARY_PATH=`pwd`${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

make -C test apps tests

gcc -o openssl-thread-test \
    %{?_with_krb5:rb5-config --cflags} \
    -I./include \
    %{optflags} \
    openssl-thread-test.c \
    -L. -lssl -lcrypto \
    %{?_with_krb5:rb5-config --libs} \
    -lpthread -lz -ldl

./openssl-thread-test --threads %{thread_test_threads}


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall \
    INSTALL_PREFIX=%{buildroot} \
    MANDIR=%{_mandir} \
    build-shared

# the makefiles is too borked...
mkdir -p %{buildroot}%{_libdir}/openssl
mv %{buildroot}%{_libdir}/engines %{buildroot}%{_libdir}/openssl/

# make the rootcerts dir
mkdir -p %{buildroot}%{_sysconfdir}/pki/tls/rootcerts

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p %{buildroot}%{_sysconfdir}/pki/tls/certs
install -m 0644 %{_sourcedir}/Makefile.certificate %{buildroot}%{_sysconfdir}/pki/tls/certs/Makefile
install -m 0755 %{_sourcedir}/make-dummy-cert %{buildroot}%{_sysconfdir}/pki/tls/certs/make-dummy-cert

# Pick a CA script.
mv %{buildroot}%{_sysconfdir}/pki/tls/misc/CA.sh %{buildroot}%{_sysconfdir}/pki/tls/misc/CA

mkdir -p %{buildroot}%{_sysconfdir}/pki/CA
mkdir -p %{buildroot}%{_sysconfdir}/pki/CA/private

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

chmod 0755 %{buildroot}%{_libdir}/pkgconfig

%multiarch_includes %{buildroot}%{_includedir}/openssl/opensslconf.h

# strip cannot touch these unless 755
chmod 0755 %{buildroot}%{_libdir}/openssl/engines/*.so*
chmod 0755 %{buildroot}%{_libdir}/*.so*
chmod 0755 %{buildroot}%{_bindir}/*

# nuke a mistake
rm -f %{buildroot}%{_mandir}/man3/.3

# nuke rpath
chrpath -d %{buildroot}%{_bindir}/openssl

# Fix libdir.
pushd %{buildroot}%{_libdir}/pkgconfig
    for i in *.pc ; do
        sed 's,^libdir=${exec_prefix}/lib$,libdir=${exec_prefix}/%{_lib},g' \
            $i >$i.tmp && \
            cat $i.tmp >$i && \
            rm -f $i.tmp
    done
popd

# adjust ssldir
perl -pi -e "s|^CATOP=.*|CATOP=%{_sysconfdir}/pki/tls|g" %{buildroot}%{_sysconfdir}/pki/tls/misc/CA
perl -pi -e "s|^\\\$CATOP\=\".*|\\\$CATOP\=\"%{_sysconfdir}/pki/tls\";|g" %{buildroot}%{_sysconfdir}/pki/tls/misc/CA.pl
perl -pi -e "s|\./demoCA|%{_sysconfdir}/pki/tls|g" %{buildroot}%{_sysconfdir}/pki/tls/openssl.cnf

# fix one conflicting manpage with rsbac-admin
mv %{buildroot}%{_mandir}/man3/buffer.3 %{buildroot}%{_mandir}/man3/openssl_buffer.3

rm -f %{buildroot}%{_mandir}/man7/Modes*

# get rid of dangling symlinks in /usr/lib for 64bit arches
%ifarch x86_64 amd64 ppc64
rm -rf %{buildroot}%{_prefix}/lib
%endif


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
echo "Please note that OPENSSLDIR has moved from %{_libdir}/ssl to"
echo "%{_sysconfdir}/pki/tls"


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files 
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man[157]/*
%dir %{_sysconfdir}/pki
%dir %{_sysconfdir}/pki/CA
%dir %{_sysconfdir}/pki/CA/private
%dir %{_sysconfdir}/pki/tls
%dir %{_sysconfdir}/pki/tls/certs
%dir %{_sysconfdir}/pki/tls/misc
%dir %{_sysconfdir}/pki/tls/private
%dir %{_sysconfdir}/pki/tls/rootcerts
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pki/tls/openssl.cnf
%attr(0755,root,root) %{_sysconfdir}/pki/tls/certs/make-dummy-cert
%attr(0644,root,root) %{_sysconfdir}/pki/tls/certs/Makefile
%attr(0755,root,root) %{_sysconfdir}/pki/tls/misc/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*
%dir %{_libdir}/openssl/engines
%{_libdir}/openssl/engines/*.so

%files -n %{libname}-devel
%defattr(-,root,root)
%dir %{_includedir}/openssl/
%multiarch %{multiarch_includedir}/openssl/opensslconf.h
%{_includedir}/openssl/*
%{_libdir}/lib*.so
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*

%files -n %{libname}-static-devel
%defattr(-,root,root)
%{_libdir}/lib*.a

%files doc 
%defattr(-,root,root)
%doc CHANGES FAQ INSTALL LICENSE NEWS PROBLEMS README*
%doc main-doc-info/README*
%doc doc/*
%doc devel-doc-info/README*


%changelog
* Wed Sep 05 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8
- P15: security fix for CVE-2006-4339 (we'll upgrade to the latest later)

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8
- fix stupid error in %%post

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8
- 0.9.8b
- move ssldir from %%{_libdir}/ssl to %%{_sysconfdir}/pki/tls
- buildrequires chrpath
- buildrequires zlib-devel
- synced patches with mdv 0.9.8b-1mdv (P2, P6, P7, P9, P10, P12, P13, P14)
- dropped P4, P5
- added a makefile and such for creating certs from mandriva (S2, S3)
- spec cleanups

* Sun Jul 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8
- Clean rebuild

* Sun Jan 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 0.9.8
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
