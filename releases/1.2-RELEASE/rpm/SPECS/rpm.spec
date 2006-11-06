#
# spec file for package rpm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$
#
# mdk 4.4.2-4mdk

%define revision	$Rev$
%define name		rpm
%define version		4.4.2
%define poptver		1.10.2
%define release		%_revrel

%define srcver		4.4.2
%define libver		4.4
%define libpoptver	0
%define libname		%mklibname rpm %{libver}
%define libpoptname	%mklibname popt %{libpoptver}
%define url		ftp://ftp.rpm.org/pub/rpm/dist/rpm-4.0.x

%define pyver		%(python -V 2>&1 | cut -f2 -d" " | cut -f1,2 -d".")
%if %{?mklibname:0}%{?!mklibname:1}
%define mklibname(ds)	%{_lib}%{1}%{?2:%{2}}%{?3:_%{3}}%{-s:-static}%{-d:-devel}
%endif

%define lib64arches	x86_64 ppc64

#%ifarch ppc x86_64 amd64 ppc64 athlon pentium3 pentium4
#%define buildnptl	1
#%else
%define buildnptl	0
#%endif

%ifarch %{lib64arches}
%define _lib		lib64
%else
%define _lib		lib
%endif

%define _prefix		/usr
%define _libdir		%{_prefix}/%{_lib}
%define _bindir		%{_prefix}/bin
%define _sysconfdir	/etc
%define _datadir	/usr/share
%define _defaultdocdir	%{_datadir}/doc
%define _mandir		%{_datadir}/man
%define _infodir	%{_datadir}/info
%define _localstatedir	/var

%define _host_vendor	annvix

# Define directory which holds rpm config files, and some binaries actually
# NOTE: it remains */lib even on lib64 platforms as only one version
#       of rpm is supported anyway, per architecture
%define rpmdir %{_prefix}/lib/rpm

%define __os_install_post	%{_datadir}/spec-helper/spec-helper
%define __find_requires		%{rpmdir}/%{_host_vendor}/find-requires %{?buildroot:%{buildroot}} %{?_target_cpu:%{_target_cpu}}
%define __find_provides		%{rpmdir}/%{_host_vendor}/find-provides


Summary:	The RPM package management system
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Packaging
URL:            http://www.rpm.org/
Source:		ftp://ftp.jbj.org/pub/rpm-%{libver}.x/rpm-%{srcver}.tar.bz2
# Add some undocumented feature to gendiff
Patch17:	rpm-4.2-gendiff-improved.patch
# (fredl) add loging facilities through syslog
Patch31:	rpm-4.4.1-syslog.patch
# Still need :(
# Correctly check for PPC 74xx systems
Patch41:	rpm-4.2-ppc-74xx.patch
# Check amd64 vs x86_64, these arch are the same
Patch44:	rpm-4.4.1-amd64.patch
# Backport from 4.2.1 provides becoming obsoletes bug (fpons)
Patch49:	rpm-4.4.1-provides-obsoleted.patch
# Still need
Patch56:	rpm-4.2.2-ppc64.patch
# Colorize static archives and .so symlinks
Patch62:	rpm-4.4.2-coloring.patch
# ok for this
Patch63:	rpm-4.2.3-dont-install-delta-rpms.patch
# This patch ask to read /usr/lib/rpm/vendor/rpmpopt too
Patch64:    rpm-4.4.1-morepopt.patch
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=114385
# This patch fix set %_topdir to /usr/src/RPM
# modified files: macros.in Makefile.am
Patch66:    rpm-4.4.1-topdirinrpm.patch
# Being able to read old rpm (build with rpm v3)
# See https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=127113#c12
Patch68:    rpm-4.4.1-region_trailer.patch
# Fix some French translations
Patch69:	rpm-4.4.1-fr.patch
# In original rpm, -bb --short-circuit does not work and run all stage
# From popular request, we allow to do this
# http://qa.mandriva.com/show_bug.cgi?id=15896
Patch70:	rpm-4.4.1-bb-shortcircuit.patch
# http://www.redhat.com/archives/rpm-list/2005-April/msg00131.html
# http://www.redhat.com/archives/rpm-list/2005-April/msg00132.html
Patch71:	rpm-4.4.1-ordererase.patch
# File conflicts when rpm -i
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=151609
Patch72:	rpm-4.4.1-fileconflicts.patch
# Fix pre/post when erasing
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=155700
Patch74:	rpm-4.4.1-prepostun.patch
# Allow to rebuild db with --root option
Patch76:	rpm-4.4.1-rebuildchroot.patch
# Allow to set %_srcdefattr for src.rpm
Patch77:	rpm-source-defattr.patch
# Do not use futex, but fcntl
Patch78:	rpm-fcntl.patch
# from https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=146549
Patch79:	rpm-4.4.2-deadlock.patch
# Fix: http://qa.mandriva.com/show_bug.cgi?id=17774
# Patch from cvs HEAD (4.4.3)
Patch80:	rpm-4.4.2-buildsubdir-for-scriptlet.patch
Patch81:	rpm-4.4.2-legacyprereq.patch
Patch82:	rpm-4.4.2-ordering.patch
# don't conflict for doc files from colored packages
Patch83:	rpm-4.2.3-no-doc-conflicts.patch
Patch84:	rpm4-CVE-2006-5466.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5 >= 2.57
BuildRequires:	doxygen
BuildRequires:	python-devel
BuildRequires:	zlib-devel
BuildRequires:	automake1.8
BuildRequires:	glibc-static-devel
BuildRequires:	elfutils-static-devel
BuildRequires:	sed >= 4.0.3
BuildRequires:	libbeecrypt-devel
BuildRequires:	ed, gettext-devel
BuildRequires:	rpm-annvix-setup-build
BuildRequires:	readline-devel, ncurses-devel
BuildRequires:	neon-devel < 0.25
BuildRequires:	libsqlite3-devel

Requires:	bzip2 >= 0.9.0c-2
Requires:	cpio
Requires:	gawk
Requires:	glibc >= 2.1.92
Requires:	mktemp
Requires:	popt = %{poptver}-%{release}
Requires:	setup >= 2.2.0-8mdk
Requires:	multiarch-utils >= 1.0.7
Requires:	update-alternatives
Requires:	rpm-annvix-setup
Requires:	%{libname} = %{version}-%{release}
Conflicts:	locales < 2.3.1.1, patch < 2.5
PreReq:		rpm-helper >= 0.8

%description
RPM is a powerful command line driven package management system capable of
installing, uninstalling, verifying, querying, and updating software packages.
Each software package consists of an archive of files along with information
about the package like its version, a description, etc.

%package -n %{libname}
Summary:	Libraries used by rpm
Group:		System/Libraries
Provides:	librpm = %{version}-%{release}

%description -n %{libname}
RPM is a powerful command line driven package management system capable of
installing, uninstalling, verifying, querying, and updating software packages.
This packages contains common files to all applications based on rpm.


%package -n %{libname}-devel
Summary:	Development files for applications which will manipulate RPM packages
Group:		Development/C
Requires:	rpm = %{version}-%{release}
Requires:	popt-devel = %{poptver}-%{release}
Provides:	librpm-devel = %{version}-%{release}
Provides:	rpm-devel = %{version}-%{release}
Obsoletes:	rpm-devel < 4.4.1

%description -n %{libname}-devel
This package contains the RPM C library and header files.  These
development files will simplify the process of writing programs
which manipulate RPM packages and databases and are intended to make
it easier to create graphical package managers or any other tools
that need an intimate knowledge of RPM packages in order to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.


%package build
Summary:	Scripts and executable programs used to build packages
Group:		System/Configuration/Packaging
Requires:	autoconf
Requires:	automake
Requires:	file
Requires:	gcc-c++
# We need cputoolize & amd64-* alias to x86_64-* in config.sub
Requires:	libtool >= 1.4.3-5mdk
Requires:	patch, make, unzip, elfutils
Requires:	rpm = %{version}-%{release}
Requires:	spec-helper
Requires:	rpm-annvix-setup-build

%description build
This package contains scripts and executable programs that are used to
build packages using RPM.


%package -n python-rpm
Summary:	Python bindings for apps which will manipulate RPM packages
Group:		Development/Python
Requires:	python >= %{pyver}
Requires:	rpm = %{version}-%{release}
Obsoletes:	rpm-python
Provides:	rpm-python = %{version}-%{release}

%description -n python-rpm
The rpm-python package contains a module which permits applications
written in the Python programming language to use the interface
supplied by RPM (RPM Package Manager) libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.


%package -n popt-data
Summary:	popt static data
Group:		System/Libraries
Version:	%{poptver}
Release:	%{release}

%description -n popt-data
This package contains popt data files like locales.


%package -n %{libpoptname}
Summary:	A C library for parsing command line parameters
Group:		System/Libraries
Version:	%{poptver}
Release:	%{release}
Requires:	popt-data >= %{poptver}
Provides:	lib%{popt} = %{poptver}-%{release}
Provides:	popt = %{poptver}-%{release}
Obsoletes:	popt <= 1.8.3

%description -n %{libpoptname}
Popt is a C library for parsing command line parameters.  Popt was
heavily influenced by the getopt() and getopt_long() functions, but it
improves on them by allowing more powerful argument expansion.  Popt
can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments.  Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.


%package -n %{libpoptname}-devel
Summary:	A C library for parsing command line parameters
Group:		Development/C
Version:	%{poptver}
Release:	%{release}
Requires:	popt = %{poptver}-%{release}
Provides:	popt-devel = %{poptver}-%{release}
Provides:	libpopt-devel = %{poptver}-%{release}
Obsoletes:	popt-devel <= 1.8.3

%description -n %{libpoptname}-devel
Popt is a C library for parsing command line parameters.  Popt was
heavily influenced by the getopt() and getopt_long() functions, but it
improves on them by allowing more powerful argument expansion.  Popt
can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments.  Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.


%prep
%setup -q -n %{name}-%{srcver}
%patch17 -p1 -b .improved
%patch31 -p1 -b .syslog
%patch41 -p1 -b .ppc-74xx
%patch44 -p1 -b .amd64
%patch49 -p1 -b .provides
%patch56 -p1 -b .ppc64
%patch62 -p1 -b .coloring
%patch63 -p1 -b .dont-install-delta-rpms
%patch64 -p0 -b .morepopt
%patch66 -p0 -b .topdirinrpm
%patch68 -p0 -b .region_trailer
%patch69 -p0 -b .trans
%patch70 -p0 -b .shortcircuit
%patch71 -p1  -b .ordererase
%patch72 -p1  -b .fileconflicts
%patch74 -p1  -b .prepostun
%patch76 -p0  -b .rebuildchroot
%patch77 -p0  -b .srcdefattr

%if %{buildnptl}
%else
%patch78 -p0  -b .fcntl
%endif

%patch79 -p1 -b .deadlock
%patch80 -p0 -b .subdir-scriplet
%patch81 -p0 -b .legacyprereq
%patch82 -p0 -b .ordering
%patch83 -p1 -b .no-doc-conflicts
%patch84 -p0 -b .cve-2006-5466

# The sqlite from rpm tar ball is the same than the system one
# rpm author just add LINT comment for his checking purpose
mv sqlite sqlite.orig


%build
for dir in . popt file zlib db/dist; do
    (
    cd $dir
    libtoolize --force
    aclocal
    automake-1.8 -a
    autoconf
    )
done

# rpm take care of --libdir but explicitelly setting --libdir on
# configure breaks make install, but this does not matter.
# --build, we explicetly set 'annvix' as our config subdir and 
# _host_vendor are 'annvix'
%ifarch x86_64
fpic="-fPIC"
%endif

CFLAGS="%{optflags} $fpic" CXXFLAGS="%{optflags} $fpic" \
    ./configure \
        --build=%{_target_cpu}-%{_host_vendor}-%{_target_os}%{?_gnu} \
        --prefix=%{_prefix} \
        --sysconfdir=%{_sysconfdir} \
        --localstatedir=%{_localstatedir} \
        --mandir=%{_mandir} \
        --infodir=%{_infodir} \
        --enable-nls \
        --without-javaglue \
%if %{buildnptl}
        --enable-posixmutexes \
%else
        --with-mutex=UNIX/fcntl \
%endif
        --with-python=%{pyver} \
        --with-glob \
        --with-apidocs \
        --without-selinux

# We should use the zlib provided whit rpm:
# 21:17 < Nanar> why using ../../zlib in file/ instead system library ?
# 21:38 < jbj> Nanar: zlib modified to make *.rpm packages rsync friendly.
#              See https://svn.uhulinux.hu/packages/dev/zlib/patches/02-rsync.patch
# 21:38 < jbj> rip if you don't want to be rsync friendly. <shrug>

# Zlib tree don't support make -j
# building in first

(
    cd zlib
    make
)

%make


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

# We put a popt copy in /%_lib for application in /bin
# This is not for rpm itself as it requires all rpmlib
# from /usr/%_lib
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libpopt.so.* %{buildroot}/%{_lib}
ln -s ../../%{_lib}/libpopt.so.0 %{buildroot}%{_libdir}
ln -sf libpopt.so.0 %{buildroot}%{_libdir}/libpopt.so

%ifarch ppc powerpc
ln -sf ppc-annvix-linux %{buildroot}%{rpmdir}/powerpc-annvix-linux
%endif

mv -f %{buildroot}/%{rpmdir}/rpmdiff %{buildroot}/%{_bindir}

# Save list of packages through cron
mkdir -p %{buildroot}/etc/cron.daily
install -m 755 scripts/rpm.daily %{buildroot}/etc/cron.daily/rpm

mkdir -p %{buildroot}/etc/logrotate.d
install -m 644 scripts/rpm.log %{buildroot}/etc/logrotate.d/rpm

mkdir -p %{buildroot}/etc/rpm/
cat << E_O_F > %{buildroot}/etc/rpm/macros.cdb
%%__dbi_cdb      %%{nil}
%%__dbi_other    %%{?_tmppath:tmpdir=%%{_tmppath}} usedbenv create \
                 joinenv mpool mp_mmapsize=8Mb mp_size=512kb verify
E_O_F

mkdir -p %{buildroot}/var/lib/rpm
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Providename \
    Provideversion Removetid Requirename Requireversion Triggername \
    Packages __db.001 __db.002 __db.003 __db.004
do
    touch %{buildroot}/var/lib/rpm/$dbi
done

find apidocs -type f | xargs perl -p -i -e "s@$RPM_BUILD_DIR/%{name}-%{version}@@g"

test -d doc-copy || mkdir doc-copy
rm -rf doc-copy/*
ln -f doc/manual/* doc-copy/
rm -f doc-copy/Makefile*

mkdir -p %{buildroot}/var/spool/repackage

# make override
mkdir -p %{buildroot}/override
chmod 1777 %{buildroot}/override

# Get rid of unpackaged files
pushd %{buildroot}
    rm -rf .%{_includedir}/beecrypt/
    rm -f .%{_libdir}/libbeecrypt.{a,la,so*}
    rm -f .%{_libdir}/python*/site-packages/poptmodule.{a,la}
    rm -f .%{_libdir}/python*/site-packages/rpmmodule.{a,la}
    rm -f .%{rpmdir}/{Specfile.pm,cpanflute2,cpanflute,sql.prov,sql.req,tcl.req}
    rm -f .%{rpmdir}/{config.site,cross-build,rpmdiff.cgi}
    rm -f .%{rpmdir}/trpm
    rm -f .%{_bindir}/rpmdiff
popd

%{rpmdir}/%{_host_vendor}/find-lang.sh %{buildroot} %{name}
%{rpmdir}/%{_host_vendor}/find-lang.sh %{buildroot} popt


%check
make -C popt check-TESTS


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


# nuke __db.00? when updating to this rpm
%triggerun -- rpm < 4.4.2-1avx
rm -f /var/lib/rpm/__db.00?


%pre
if [ -f /var/lib/rpm/Packages -a -f /var/lib/rpm/packages.rpm ]; then
    echo "
You have both
	/var/lib/rpm/packages.rpm	db1 format installed package headers
	/var/lib/rpm/Packages		db3 format installed package headers
Please remove (or at least rename) one of those files, and re-install.
"
    exit 1
fi

/usr/share/rpm-helper/add-user rpm $1 rpm /var/lib/rpm /bin/false 68

rm -rf /usr/lib/rpm/*-annvix-*


%post
if [ ! -e %{_sysconfdir}/rpm/macros -a -e %{_sysconfdir}/rpmrc -a -f %{rpmdir}/convertrpmrc.sh ] 
then
    sh %{rpmdir}/convertrpmrc.sh 2>&1 > /dev/null
fi

if [ -f /var/lib/rpm/packages.rpm ]; then
    /bin/chown rpm:rpm /var/lib/rpm/*.rpm
elif [ ! -f /var/lib/rpm/Packages ]; then
    /bin/rpm --initdb
fi


%postun
/usr/share/rpm-helper/del-user rpm $1 rpm


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libpoptname} -p /sbin/ldconfig
%postun -n %{libpoptname} -p /sbin/ldconfig



%define	rpmattr		%attr(0755, rpm, rpm)
%files -f %{name}.lang
%defattr(-,root,root)
%doc RPM-PGP-KEY RPM-GPG-KEY GROUPS CHANGES doc/manual/[a-z]*
%attr(0755,rpm,rpm) /bin/rpm
%attr(0755,rpm,rpm) %{_bindir}/rpm2cpio
%attr(0755,rpm,rpm) %{_bindir}/gendiff
%attr(0755,rpm,rpm) %{_bindir}/rpmdb
%attr(0755,rpm,rpm) %{_bindir}/rpm[eiukqv]
%attr(0755,rpm,rpm) %{_bindir}/rpmsign
%attr(0755,rpm,rpm) %{_bindir}/rpmquery
%attr(0755,rpm,rpm) %{_bindir}/rpmverify

%dir %{_localstatedir}/spool/repackage
%dir %{rpmdir}
%{_sysconfdir}/rpm
%attr(0755,rpm,rpm) %{rpmdir}/config.guess
%attr(0755,rpm,rpm) %{rpmdir}/config.sub
%attr(0755,rpm,rpm) %{rpmdir}/convertrpmrc.sh
%attr(0755,rpm,rpm) %{rpmdir}/rpmdb_*
%attr(0644,rpm,rpm) %{rpmdir}/macros
%attr(0755,rpm,rpm) %{rpmdir}/mkinstalldirs
%attr(0755,rpm,rpm) %{rpmdir}/rpm.*
%attr(0755,rpm,rpm) %{rpmdir}/rpm[deiukqv]
%attr(0644,rpm,rpm) %{rpmdir}/rpmpopt*
%attr(0644,rpm,rpm) %{rpmdir}/rpmrc

%{_prefix}/lib/rpmpopt
%{_prefix}/lib/rpmrc
%rpmattr %{rpmdir}/rpm2cpio.sh
%rpmattr %{rpmdir}/tgpg

%ifarch i386 i486 i586 i686 k6 athlon
%attr(-,rpm,rpm) %{rpmdir}/i*86-*
#%attr(-,rpm,rpm) %{rpmdir}/k6*
%attr(-,rpm,rpm) %{rpmdir}/athlon*
%attr(-,rpm,rpm) %{rpmdir}/pentium*
%endif
%ifarch alpha
%attr(-,rpm,rpm) %{rpmdir}/alpha*
%endif
%ifarch sparc sparc64
%attr(-,rpm,rpm) %{rpmdir}/sparc*
%endif
%ifarch ppc powerpc
%attr(-,rpm,rpm) %{rpmdir}/ppc-*
%attr(-,rpm,rpm) %{rpmdir}/ppc64-*
%attr(-,rpm,rpm) %{rpmdir}/powerpc-*
%endif
%ifarch ppc powerpc ppc64
%attr(-,rpm,rpm) %{rpmdir}/ppc*series-*
%endif
%ifarch ppc64
%attr(-,rpm,rpm) %{rpmdir}/ppc-*
%attr(-,rpm,rpm) %{rpmdir}/ppc64-*
%endif
%ifarch ia64
%attr(-,rpm,rpm) %{rpmdir}/ia64-*
%endif
%ifarch x86_64
#%attr(-,rpm,rpm) %{rpmdir}/amd64-*
%attr(-,rpm,rpm) %{rpmdir}/x86_64-*
%endif
%attr(-,rpm,rpm) %{rpmdir}/noarch*

%{_prefix}/src/RPM/RPMS/*
%{_datadir}/man/man[18]/*.[18]*
%lang(pl) %{_datadir}/man/pl/man[18]/*.[18]*
%lang(ru) %{_datadir}/man/ru/man[18]/*.[18]*
%lang(ja) %{_datadir}/man/ja/man[18]/*.[18]*
%lang(sk) %{_datadir}/man/sk/man[18]/*.[18]*
%lang(fr) %{_datadir}/man/fr/man[18]/*.[18]*
%lang(ko) %{_datadir}/man/ko/man[18]/*.[18]*

%config(noreplace,missingok)	%{_sysconfdir}/cron.daily/rpm
%config(noreplace,missingok)	%{_sysconfdir}/logrotate.d/rpm

%attr(0755,rpm,rpm)	%dir %{_localstatedir}/lib/rpm

%define	rpmdbattr %attr(0644, rpm, rpm) %verify(not md5 size mtime) %ghost %config(missingok,noreplace)

%rpmdbattr	/var/lib/rpm/Basenames
%rpmdbattr	/var/lib/rpm/Conflictname
%rpmdbattr	/var/lib/rpm/__db.0*
%rpmdbattr	/var/lib/rpm/Dirnames
%rpmdbattr	/var/lib/rpm/Group
%rpmdbattr	/var/lib/rpm/Installtid
%rpmdbattr	/var/lib/rpm/Name
%rpmdbattr	/var/lib/rpm/Packages
%rpmdbattr	/var/lib/rpm/Providename
%rpmdbattr	/var/lib/rpm/Provideversion
%rpmdbattr	/var/lib/rpm/Removetid
%rpmdbattr	/var/lib/rpm/Requirename
%rpmdbattr	/var/lib/rpm/Requireversion
%rpmdbattr	/var/lib/rpm/Triggername

%files build
%defattr(-,root,root)
%doc CHANGES
%doc doc-copy/*
%dir %{_prefix}/src/RPM
%dir %{_prefix}/src/RPM/BUILD
%dir %{_prefix}/src/RPM/SPECS
%dir %{_prefix}/src/RPM/SOURCES
%dir %{_prefix}/src/RPM/SRPMS
%dir %{_prefix}/src/RPM/RPMS
%attr(1777,root,root) %dir /override
%rpmattr	%{_bindir}/rpmbuild
%rpmattr	%{_prefix}/lib/rpm/brp-*
%rpmattr	%{_prefix}/lib/rpm/check-files
%rpmattr	%{_prefix}/lib/rpm/check-prereqs
#%rpmattr	%{_prefix}/lib/rpm/config.site
#%rpmattr	%{_prefix}/lib/rpm/cross-build
#%rpmattr	%{_prefix}/lib/rpm/filter.sh
%rpmattr	%{_prefix}/lib/rpm/freshen.sh
%rpmattr	%{_prefix}/lib/rpm/debugedit
%rpmattr	%{_prefix}/lib/rpm/find-debuginfo.sh
%rpmattr	%{_prefix}/lib/rpm/find-lang.sh
%rpmattr	%{_prefix}/lib/rpm/find-prov.pl
%rpmattr	%{_prefix}/lib/rpm/find-provides
%rpmattr	%{_prefix}/lib/rpm/find-provides.perl
%rpmattr	%{_prefix}/lib/rpm/find-req.pl
%rpmattr	%{_prefix}/lib/rpm/find-requires
%rpmattr	%{_prefix}/lib/rpm/find-requires.perl
%rpmattr	%{_prefix}/lib/rpm/get_magic.pl
%rpmattr	%{_prefix}/lib/rpm/getpo.sh
%rpmattr	%{_prefix}/lib/rpm/http.req
%rpmattr	%{_prefix}/lib/rpm/javadeps
%rpmattr	%{_prefix}/lib/rpm/magic
%rpmattr	%{_prefix}/lib/rpm/magic.mgc
%rpmattr	%{_prefix}/lib/rpm/magic.mime
%rpmattr	%{_prefix}/lib/rpm/magic.mime.mgc
%rpmattr	%{_prefix}/lib/rpm/magic.prov
%rpmattr	%{_prefix}/lib/rpm/magic.req
%rpmattr	%{_prefix}/lib/rpm/perldeps.pl
%rpmattr	%{_prefix}/lib/rpm/perl.prov
%rpmattr	%{_prefix}/lib/rpm/perl.req

%rpmattr	%{_prefix}/lib/rpm/rpm[bt]
%rpmattr	%{_prefix}/lib/rpm/rpmdeps
#%rpmattr	%{_prefix}/lib/rpm/trpm
%rpmattr	%{_prefix}/lib/rpm/u_pkg.sh
%rpmattr	%{_prefix}/lib/rpm/vpkg-provides.sh
%rpmattr	%{_prefix}/lib/rpm/vpkg-provides2.sh
%rpmattr	%{_prefix}/lib/rpm/pythondeps.sh

%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*


%files -n python-rpm
%defattr(-,root,root)
%{_libdir}/python*/site-packages/rpm


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/librpm-%{libver}.so
%{_libdir}/librpmdb-%{libver}.so
%{_libdir}/librpmio-%{libver}.so
%{_libdir}/librpmbuild-%{libver}.so


%files -n %{libname}-devel
%defattr(-,root,root)
#%doc apidocs/html
%{_includedir}/rpm
%{_libdir}/librpm.a
%{_libdir}/librpm.la
%{_libdir}/librpm.so
%{_libdir}/librpmdb.a
%{_libdir}/librpmdb.la
%{_libdir}/librpmdb.so
%{_libdir}/librpmio.a
%{_libdir}/librpmio.la
%{_libdir}/librpmio.so
%{_libdir}/librpmbuild.a
%{_libdir}/librpmbuild.la
%{_libdir}/librpmbuild.so
%{_datadir}/man/man3/*
%rpmattr	%{rpmdir}/rpmcache
%rpmattr	%{rpmdir}/rpmdb_deadlock
%rpmattr	%{rpmdir}/rpmdb_dump
%rpmattr	%{rpmdir}/rpmdb_load
%rpmattr	%{rpmdir}/rpmdb_loadcvt
%rpmattr	%{rpmdir}/rpmdb_svc
%rpmattr	%{rpmdir}/rpmdb_stat
%rpmattr	%{rpmdir}/rpmdb_verify
%rpmattr	%{rpmdir}/rpmfile
%rpmattr	%{_bindir}/rpmgraph


%files -n popt-data -f popt.lang
%defattr(-,root,root)


%files -n %{libpoptname}
%defattr(-,root,root)
/%{_lib}/libpopt.so.*
%{_libdir}/libpopt.so.*


%files -n %{libpoptname}-devel
%defattr(-,root,root)
%{_includedir}/popt.h
%{_libdir}/libpopt.a
%{_libdir}/libpopt.la
%{_libdir}/libpopt.so


%changelog
* Mon Nov  6 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- P84: security fix for CVE-2006-5466

* Wed Feb  1 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- fix a stupid typeo in the %%postuninstall scriptlet of librpm4.4
  that would make it try to execute "***" via ldconfig and would thus
  bail on uninstall (resulting in multiple copies of librpm4.4 being
  installed)

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- Clean rebuild

* Mon Dec 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- rebuild against new python

* Sat Dec 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- Obfuscate email addresses and new tagging
- Uncompress patches

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2-3avx
- BuildRequires: rpm-annvix-setup-build
- P83: no-doc-conflicts for colored packages (gbeauchesne)
- update P62 (merge it correctly) (gbeauchesne)

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2-2avx
- always build without nptl support as it craps out on our systems in
  x86_64

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2-1avx
- 4.4.2
- Requires: rpm-annvix-setup
- merge with mandrake cooker 4.4.2-3mdk:
  - remove biarch; use mklibname (nanardon)
  - don't patch the config anymore, use /usr/lib/rpm/VENDOR/rpmrc instead
    (nanardon)
  - remove many obsolete patches (nanardon)
  - no longer provide update-alternatives
  - more defined macros in the spec, less hardcoded patch (nanardon)
  - force -fPIC on x86_64 for popt (nanardon)
  - perform test for popt (nanardon)
  - P67: fix build with gcc4
  - BuildRequires: readline-devel (P. O. Karlsen)
  - P68: allow the readinf of old rpms (nanardon)
  - P62: adapt part of the coloring patch (rgarciasuarez)
  - P69: fix a few french translations (rgarciasuarez)
  - P70: allow rpm -bb --short-circuit (nanardon)
  - remove locales files from libpopt (nanardon)
  - P71: ordering transaction on erasure (nanardon)
  - P72: rpm -[Ui] check files conflicts
  - P73, P74: from Fedora, fixing bugs (nanardon)
  - P76: allow rebuild db with --root option (rgarciasuarez)
  - P77: allow to set root/root as owner of files in src.rpm
  - move deps on unzip, make, and elfutils from rpm to rpm-build (rgarciasuarez)
  - reworked P77 to allow %_srcdefattr as a macro for src.rpm (nanardon)
  - removed P52, P67, P73, P78, P79: merged/fixed upstream (nanardon)
  - removed P32, P33, P36: no more need to hack (nanardon)
  - rename rpm-python to python-rpm (nanardon)
  - use fnctl when not using futex (nanardon)
  - use nptl only on a few arches (ppc*, x86_64, pentium3,4/athlon) (nanardon)
  - P79: fix deadlock from RH bug #146549 (flepied)
  - P80: fix #17774 (nanardon)
  - P81, P82: should fix ordering issue (nanardon)
  - BuildRequires: bzip2-devel (nanardon)

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.3-9avx
- bootstrap build (new gcc, new glibc)

* Mon Aug 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.3-8avx
- rebuild against rebuilt beecrypt

* Fri Jul 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.3-7avx
- split libs into separate package to make rpm update easier for URPM
  (nanardon)
- bump multiarch-utils requires (gb)
- encode ru man pages in KOI8-R (mdk bug #10219 and #12613) (flepied)
- try building rpm static to work around some glibc issues

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.3-6avx
- get rid of silly %%poptrelease
- rebuild for new gcc
- new macro: %%_buildroot
- include /override
- don't apply P52; we're not using SSP right now
- s/-mcpu/-mtune/ for %%optflags

* Thu Jun 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.3-5avx
- rebuild with stack protection enabled
- update macros to use -fstack-protector-all instead of -fstack-protector

* Thu Jun 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.3-4avx
- compile against ourself

* Thu Jun 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.3-3avx
- bootstrap build

* Tue Mar 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.3-2avx
- changed group System/XFree86 to System/X11
- require multiarch-utils >= 1.0.7
- drop P18; RPM_INSTALL_LANG support is obsolete (rafael)
- popt is now a biarch package (gb)
- rediff P54; get rid of mkrel macro

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.3-1avx
- 4.2.3
- regen P52
- drop %%build_ssp macro; always build with ssp
- build with -fno-stack-protector on x86_64 for now; the build
  complains about symbols for some reason, but on x86 it doesn't
  (figure it out later)
- some macros
- sync with cooker 4.2.3-4mdk:
  - fix build with python 2.4 (flepied)
  - P61: necessary for the smart package manager (new function
    rpmSingleHeaderFormFD() in the python bindings) (rgarciasuarez)
  - P62: make find-requires ignore dependencies on linux-incompatible
    perl modules; from Guillaume Rousse (rgarciasuarez)
  - compile --with-glob to avoid a problem with the internal glob
    code (flepied)
  - P63: multiarch-utils autoreq (gb)
  - allow build of 32bit rpms on x86_64 (gb)
  - ppc64 fixes (gb)
  - update from 4.2-branch: (gb)
    - auto-relocation fixes on ia64
    - change default behaviour to resolve file conflicts as LIFO
    - generate debuginfo for setuid binaries
  - P64: enable and improve file coloring (gb)
    - use file colors even if still using the external dependencies generator
    - assign a color to *.so symlinks to mix -devel packages
    - assign a color to *.a archives to mix -{static,}-devel packages
  - check for files that ought to be marked as %%multiarch
  - P65: don't install .delta.rpm directly, use applydeltarpm first (SUSE) (gb)
  - generate package script autoreqs only if requested (#13268) (gb)

* Sun Aug 08 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.2.2-5avx
- change %%build_propolice to %%build_ssp
- change brp-mandrake to brp-annvix
- on ppc builds use annvix rather than mandrake
- rediff P54 to add brp-annvix change and %%_ext change from sls to avx,
  and to change %%build_propolice to %%build_ssp
- sync with cooker 4.2.2-15mdk:
  - P59: use a correct implementation of cpuid (Gwenole)
  - P58: return None instead of [] in rpm-python (Paul Nasrat)
  - add /var/spool/repackage (bug #9874)
  - handle /usr/lib/gcc/ directories for devel() deps too (Gwenole)
  - P60: use mono-find-requires and mono-find-provides if present (Gotz Waschk)
    (bug #7201)
  - use system zlib

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.2.2-4avx
- rebuild with new gcc

* Thu Jun 17 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.2.2-3avx
- Annvix build

* Thu Jun 03 2004 Vincent Danen <vdanen@opensls.org> 4.2.2-2sls
- rpm needs a static uid/gid too: 68
- sync with cooker 4.2.2-10mdk:
  - fix /usr/lib/rpmpopt symlink (gbeauchesne)
  - switch back to x86_64 packages on 64bit extended platforms (gbeauchesne)

* Fri May 07 2004 Vincent Danen <vdanen@opensls.org> 4.2.2-1sls
- 4.2.2
- sync with cooker 4.2.2-8mdk:
  - rpm-spec-mode modifications (use of rpm-spec-user-mail-address and
    rpm-spec-user-full-name for changelog entries, tab or space use for new
    files) from Olivier Blin (flepied)
  - put back a type to be backward compatible (flepied) (P56)
  - BuildRequires: automake1.7 (flepied)
  - use system elfutils, beecrypt (flepied)
  - hack out O_DIRECT support in db4 for now (flepied)
  - fix RPMLOCK for rpm -r <root> --rebuilddb as user (flepied) (updated P13)
  - use DB_PRIVATE for the time being, nuke __db.00? when updating to this one
    (gbeauchesne) (P57)
  - BuildRequires: ed, gettext-devel (gbeauchesne)
  - fixed perl.prov and perl.req to inspect only real files (flepied)
  - when unlocking the RPMLOCK file, don't forget to close(2) it too
    (rgarciasuarez)

* Tue Feb 03 2004 Vincent Danen <vdanen@opensls.org> 4.2-29sls
- update P54 to add another field to %%_pre_groupadd for static gid

* Sat Jan 31 2004 Vincent Danen <vdanen@opensls.org> 4.2-28sls
- update P54 for new macro: %%_mkafterboot

* Tue Jan 27 2004 Vincent Danen <vdanen@opensls.org> 4.2-27sls
- update P54 for new macros: %%_post_srv and %%_preun_srv to manage
  supervise-controlled services
- add another field to %%_pre_useradd for static uid/gid

* Mon Jan 12 2004 Vincent Danen <vdanen@opensls.org> 4.2-26sls
- P54: OpenSLS macros -> %%_srvdir = /var/service, %%_srvlogdir =
  /var/log/supervise, %%build_propolice (on if gcc+propolice installed),
  %%_ext = sls, %%_target_platform is sls'ized (may cause some issues)
- get rid of emacs files
- sync with 26mdk/27mdk (pixel):
  - fix RPMLOCK patch (for rebuilddb)
  - cleanup lock patch (i sux)

* Thu Jan 01 2004 Vincent Danen <vdanen@opensls.org> 4.2-25sls
- fix /usr/lib/rpmpopt symlink
- amd64 fixes

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 4.2-24sls
- sync with 23mdk (flepied): 
  - don't put prefix in spec file template created by emacs
    spec-mode [bug #6282] (Gotz Waschk)
  - also abort build when a symlink isn't listed [bug #6370] (Gotz Waschk)
- sync with 24mdk (flepied):
  - corrected wrong automatic perl-base requires [bug #6439]
  - try to find interpreters only when the scripts begin with #! [bug #6430]
  - don't put an automatic devel(linux-gate) depedendency [ bug #6553]
  - auto-generate a dependency on pkgconfig if a .pc file is found in
    /usr/lib(64)?/pkgconfig [bug #6438]
- sync with 25mdk (flepied):
  - really fix bug #6553
  - take into account automatic perl Requires/Provides only when starting
    with a capital letter


* Mon Dec 15 2003 Vincent Danen <vdanen@opensls.org> 4.2-23sls
- bump to 23sls so we can upgrade from mdk 9.2+updates

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 4.2-20sls
- sync with Mandrake (4.2-22mdk):
  - fix crash in rpmalAllSatisfiesDepend() -- gbeauchesne
  - new lock scheme by Francois -- flepied
  - create the RPMLOCK file in %%post -- vdanen
  - corrected --rebuilddb problem (bug #6395) -- flepied

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 4.2-19sls
- rebuild
- tidy spec

* Fri Oct 24 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.2-18.2mdks
- fix patch

* Fri Oct 24 2003 Vincent Danen <vdanen@mandrakesoft.com> 4.2-18.1mdks
- P51: new macros for stack protection; only applied if %%{build_propolice}
  enabled

* Thu Sep 11 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2-18mdk
- really correct lock problem (patch13)

* Wed Sep 10 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2-17mdk
- Add new python macros: pyver
- Make "x86_64" the canonical arch on amd64
- correct patch15 to have good locks (flepied)

* Thu Aug  7 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2-16mdk
- rebuild for python 2.3

* Mon Aug  4 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2-15mdk
- fixed patch49 (François)

* Sat Jul 26 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2-14mdk
- Requires: libtool >= 1.4.3-5mdk
- Always call cputoolize in %%configure{,2_5x}

* Thu Jul 24 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2-13mdk
- Requires: libtool >= 1.4.3-4mdk
- Patch44: Default to .amd64.rpm packages

* Thu Jul 10 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2-12mdk
- Make find-provides look for gcc libraries too
- Unconditionnally expands LD_LIBRARY_PATH with lib64 dirs

* Wed Jul  9 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2-11mdk
- Make it build again without hacks ;-)
- Fix and make find-{requires,provides} lib64 aware
- BuildRequires: sed >= 4.0.3, otherwise sed -e '/.../!s,...,' doesn't work

* Tue Jul  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.2-10mdk
- BuildRequires: elfutils-static-devel
- Fix merge with older MDK AMD64 changes
- Apply configure-xpath patch on all lib64 platforms
- Patch42: Don't link against system libs when relinking in %%install

* Mon Jul  7 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2-9mdk
- devel requires/provides are now in the form devel(<soname>)
- -g is only activated when producing a -debug package

* Mon Jun 23 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2-8mdk
- BuildRequires libelf-static-devel
- disabled -debug package
- backported patch from 4.2.1 about provides becoming obsoletes (fpons)
- sparc modifications from Olivier Thauvin

* Tue May 13 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2-7mdk
- added ppc64-linux subdir on ppc (Olivier Thauvin)
- fixed build
- added -g to the compilation flags to be able to correctly
build -debug packages
- added %%_provides_exceptions and %%_requires_exceptions to be able to
pass a grep expression to filter provides and requires.

* Mon May 12 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2-6mdk
- ported syslog patch (patch31)
- BuildRequires: autoconf2.5 (Stefan)
- %%{rpmdir}/alpha-* --> %%{rpmdir}/alpha* (Stefan)
- corrected devel requires/provides (Stefan)

* Fri May  9 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2-5mdk
- updated patch41 to correctly detect IBM750FX (Gwenole)
- activated automatic requires for perl and devel packages

* Tue May  6 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2-4mdk
- corrected buggy find-provides

* Tue May  6 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2-3mdk
- better bootstrapping
- enabled automatic perl provides
- automatic devel provides (Stefan)
- automatic perl and devel requires will be activated later when the base
packages will have been rebuilt

* Wed Apr 30 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2-2mdk
- corrected upgrade
- add back the legacy aliases for building packages with the rpm command
- use external helpers to gather provides and requires

* Mon Apr 28 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.2-1mdk
- 4.2

* Mon Jan 13 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.4-28mdk
- Patch41: Correctly check for PPC 74xx systems
- Merge in real rpm tree:
  * Tue Jan  7 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.4-26mdk
  - Update Patch0 (mdkconf) to put back libtoolize for %%configure
  - Update Patch43 (configure-xpath) to match latest merges
  * Tue Jan  7 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-25mdk
  - merged patches that touched to macro/platform/installplatform into patch0
  - added BuildRequires glibc-static-devel

* Wed Jan  8 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.4-27mdk
- "Mama what is the food for dinner tonight" asked the young boy,
  looking in the eyes of his boy 'like always with straightness' the
  mum answered "Pancake with honey only Pancake with honey my
  boy". (BTW: fix rpm-spec-mode to load 'cl before initializing or it
  would not work).

* Wed Jan  8 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.4-26mdk
- fix my badness of rpm-spec-mode.
- add function rpm-spec-insert-changelog-version-with-shell which
  allow to find version-release with rpm command (usefully for tricky
  spec file like kernel).

* Tue Jan  7 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.4-25mdk
- fix rpm-spec-mode::rpm-add-change-log-entry to accept argument for
  non interactive changelog addition.
- Make latest rpm-spec-mode work with Gnu-Emacs.
- Upgrade rpm-spec-mode to 0.12.

* Tue Jan  7 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.4-26mdk
- Update Patch0 (mdkconf) to put back libtoolize for %%configure
- Update Patch43 (configure-xpath) to match latest merges
- Patch46: Backport prelink support and use mmap() when calculating
  file digests on verify

* Tue Jan  7 2003 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-25mdk
- merged patches that touched to macro/platform/installplatform into patch0
- added BuildRequires glibc-static-devel

* Tue Dec 31 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-24mdk
- correct %%configure2_5x macro to do the right stuff wrt to libtoolize
- %%_repackage_dir point to /var/tmp (bug #560)

* Tue Dec 24 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-23mdk
- recompile to have the macros really expanded

* Mon Dec 23 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-22mdk
- merged patches for platform.in
- %%configure2_5x do not use --target and --host options (bug #701)
- check for configure.ac in %%configure2_5x (bug #700)
- added %%_post_shelladd and %%_preun_shelldel

* Fri Nov 22 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.4-21mdk
- Ship with rpm2cpio.sh, python poptmodule.so
- Update Patch0 (mdkconf) with new RPM_OPT_FLAGS
- Patch50: Add %%_missing_doc_files_terminate_build
- Patch51: Add %%mdkversion, to ease numerical compares of MDK versions
- Patch52: Add %%{mklibname <name> [<major> [<minor>]] [-s] [-d]}

* Mon Nov 11 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.4-20mdk
- Patch49: Add %%_unpackaged_files_terminate_build from rpm-4.1 which
  is now set by default. Aka rpm build will now fail if files are
  found in %{buildroot} and not referenced in %files section.
- Update Patch39 (x86_64) to really leave config files in /usr/lib/rpm
- Update Patch5 (autoreq): Fix filelist filtering in find-provides

* Thu Sep 12 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-19mdk
- include /etc/rpm

* Mon Sep  9 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-18mdk
- strip binaries

* Thu Aug 29 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-17mdk
- correct locking behaviour

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.4-15mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Mon Jul 29 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-14mdk
- added 64bits architectures support in find-requires and find-provides
- added %%_pre_groupadd and %%_postun_groupdel macros

* Wed Jul 10 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-13mdk
- corrected find-provides typo

* Wed Jul 10 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-12mdk
- corrected find-requires wrt old/new perl paths
- oops forgot to add /usr/X11R6/lib to correct paths for find-requires
- use create-file from rpm-helper for %%create_ghostfile macro.

* Wed Jul 10 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-11mdk
- use a serial of 2 for perl-base Requires in find-requires
- auto provide soname only from files in /lib and /usr/lib in find-provides

* Tue Jul  9 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-10mdk
- handle old perl release in find-requires (new packages must go to vendor_perl).
- call rpm-helper scripts for service/user addition/removal in scriptlets.

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 4.0.4-9mdk
- Patch46: 
  - add %%perl_vendorarch and %%perl_vendorlib
  - better and uptodate perl spec example
- Patch5 (autodeps):
  - add "perl-base >= 1:5.8.0" instead of "perl-base >= 5.800"
  - search for perl modules in both site_perl and vendor_perl

* Fri Jul  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-8mdk
- corrected %%_pre_useradd macro

* Fri Jul  5 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-7mdk
- added %%_pre_useradd and %%_postun_userdel macros

* Mon Jul  1 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.4-6mdk
- BuildRequires: gettext-devel
- Patch39: Add initial support for x86-64
- Patch40: Fix handling of nested %%if/%%ifarch constructs (SuSE patch)
- Patch41: Let %%_menudir always be /usr/lib/menu
- Patch42: Restore libtoolize in %%configure, also take care of CONFIGURE_TOP
- Patch43: Correctly setup X11 paths on lib64 systems
- Patch44: Build python modules with PIC code
- Patch45: Python install dir is in $(libdir)

* Thu May 30 2002 Stefan van der Eijk <stefan@eijk.nu> 4.0.4-5mdk
- BuildRequires
- Add extra Requires for rpm and rpm-build (based on macros files)
- Fix Requires and removed redundant ones (basesystem is always on system)
- One BuildRequires / Requires per line
- 4.0.4-4mdk changelog missing?

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 4.0.4-3mdk
- Automated rebuild in gcc3.1 environment

* Wed May  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-2mdk
- regenerated patches 5 and 31
- use rpm-4.0.4-7x.18 (corrects the .rpmnew problem)

* Wed Mar 20 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.4-1mdk
- 4.0.4 (updated patches 0, 31 and removed patches 16, 30, 37, 38)

* Wed Mar 13 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-10mdk
- fix --resign (Jeff Johnson)

* Sat Mar  2 2002 Pixel <pixel@mandrakesoft.com> 4.0.3-9mdk
- fix-using-chroot_prefix-without-taking-care-of-trailing-slash
  (fix the "var/lib/rpm/Basenames" not found at install and oem)

* Thu Feb 28 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-8mdk
- default to compile to i586 on architecture compatible as it should
have always been the case.

* Tue Feb 26 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-7mdk
- added compile options for k6 and corrected alpha and other ix86
- set umask to 022 before running the scriplets
- don't exit 1 when there is no locale files in find-lang.sh

* Mon Feb 25 2002 Pablo Saratxaga <pablo@mandrakesoft.com> 4.0.3-6mdk
- improved find-lang.sh script, with --all-name switch

* Thu Feb 21 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-5mdk
- automatic requires on perl-base and python-base.

* Mon Feb  4 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-4mdk
- fix %%make macro

* Fri Feb  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-3mdk
- fixed typo in macros

* Fri Feb  1 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-2mdk
- really use the first arg in find-requires
- use Jeff Johnson's version of patch34.
- corrected %%_install_info and %%_remove_install_info macros to not bug with multiline

* Thu Jan 31 2002 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-1mdk
- add the use of CONFIGURE_TOP to allow the %%configure and
%%configure2_5x macros to work in subdirs. (Jeff)
- %%pyver calculated at compile time. (Alvaro Herrera)
- pass %%{buildroot} to find-requires (patch34). This allow to calculate
dependencies from compiled libraries instead of relying on installed ones.
- bump the release to 1mdk

* Thu Jan 24 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.3-0.37mdk
- Fix %%install_info again.

* Tue Jan 22 2002 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.3-0.36mdk
- Check file if exist before using %%install_info (fix %excludedocs).

* Sun Dec 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.35mdk
- python 2.2

* Tue Dec 11 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0.3-0.34mdk
- Upgrade to latest rpm-spec-mode.

* Mon Nov 26 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.33mdk
- fix find-requires (for David)
- use CXXFLAGS=$RPM_OPT_FLAGS when compiling (Jeff)

* Tue Nov 20 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.32mdk
- revert %%makeinstall and provide %%makeinstall_std to use DESTDIR.

* Wed Nov 14 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.31mdk
- %%makeinstall now use DESTDIR and provided %%old_makeinstall for incompatible
makefiles.

* Fri Nov  9 2001 Frederic Lepied <lepied@videotron.ca> 4.0.3-0.30mdk
- reworked the hash patch to add the missing newline.

* Wed Nov  7 2001 Frederic Lepied <lepied@videotron.ca> 4.0.3-0.29mdk
- updated source from Rawhide
- report a more meaningfull error when rpm-build isn't present (p33)
- added %%configure2_5x macro
- added %%create_ghostfile macro to be used in %%post args are: filename, user, group, mode

* Tue Oct 09 2001 Stefan van der Eijk <stefan@eijk.nu> 4.0.3-0.28mdk
- BuildRequires: byacc

* Wed Sep 19 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.27mdk
- reworked patch8 to really skip mount points starting by /mnt/.

* Sun Sep 16 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.26mdk
- fix comparison between 1mdk and 1.1mdk

* Sat Sep 15 2001 Pixel <pixel@mandrakesoft.com> 4.0.3-0.25mdk
- fix yet again patch26 (aka pablo sucks) setting the locales instead of only saving it

* Fri Sep 14 2001 Pixel <pixel@mandrakesoft.com> 4.0.3-0.24mdk
- fix patch26 (aka pablo sucks) causing segfault with bad locales

* Tue Sep  4 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.23mdk
- the syslog patch is back

* Mon Sep  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.22mdk
- new snapshot from cvs:
	- python: add exception to detect bad data in hdrUnload.
	- change dir creation message from warning to debug for now.
	- verify perms (but not mode) on %ghost files.
	- headers without RPMTAG_NAME are skipped when retrieved.
	- within a region, entries sort by address; added drips sort by tag.
	- fix: error message on failed package installs resurrected.
	- python: memory leaks in headerLoad/headerunload bindings.
	- python: retrofit sha1 digest using RPMTAG_SHA1RHN.
	- python: change rhnUnload bindings.
	- python: teach rhnLoad about RPMTAG_SHA1RHN as well.
	- fix: Provides: /path did not work with added packages (#52183).
	- fix: progress bar scaling did not include source rpm count.

* Fri Aug 24 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.21mdk
- updated patch13 to avoid loop when run as non root.

* Wed Aug 15 2001 Warly <warly@mandrakesoft.com> 4.0.3-0.20mdk
- new snapshot 20010814 with fix for old packages install

* Thu Aug  9 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.19mdk
- new snapshot 20010809 with fix for multi lang Summary and Description.

* Mon Jul 30 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.18mdk
- updated rpm-spec-mode
- new snapshot 20010730
- regenerated patches 0 and 16
- corrected compilation on up host.

* Tue Jul 24 2001 François Pons <fpons@mandrakesoft.com> 4.0.3-0.17mdk
- fix hashes printing using urpmi.

* Wed Jul 18 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.16mdk
- new snapshot from CVS (regenerate patches 0, 13, 16, 17)

* Thu Jul  5 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.15mdk
- test release of rpm 4.0.3

* Wed Jul  4 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.14mdk
- new snapshot from cvs (correct problem of files listed twice)
- removed patch29 (integrated upstream)

* Tue Jul  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.13mdk
- added ; at the end of _preun_service and _post_service. I though I
had corrected that before :-(

* Tue Jul  3 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.12mdk
- added -gnu if needed in %%_target_platform

* Mon Jul  2 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.11mdk
- added patch from Matthias to avoid core dumps on IA64.

* Mon Jul  2 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.10mdk
- new snapshot (0.55)

* Thu Jun 28 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.9mdk
- new snapshot.

* Mon Jun 25 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.8mdk
- corrected find-requires

* Wed Jun 20 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.7mdk
- use new snapshot.
- really changed Copyright => License in emacs rpm-spec-mode (Goetz Waschk).

* Sun Jun 17 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.6mdk
- removed install path from doc.
- changed regex to allow space at the end of release/version in rpm-spec-mode (Chmouel).
- changed Copyright => License in emacs rpm-spec-mode (Goetz Waschk).
- corrected find-requires for alpha (from CVS).
- added BuildRequires doxygen.

* Fri Jun 15 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 4.0.3-0.5mdk
- Correct type for make macro introducted in 4.0.3-0.4mdk

* Thu Jun 14 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.4mdk
- fixed C-c r to support all forms of release tags
- corrected emacs startup script (fcrozat)
- don't split macros on multiple lines (gc)
- don't try to auto requires perl packages (pixel)

* Wed Jun 13 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.3mdk
- corrected %%{_sysconfdir} macro.

* Wed Jun 13 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.2mdk
- added librpmdb to devel package

* Wed Jun 13 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0.3-0.1mdk
- 4.0.3

* Tue May 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-33mdk
- really added -mcpu=ev5 for alpha optflags (sorry Jeff).

* Mon May 28 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-32mdk
- added -mcpu=ev5 for alpha optflags (Jeff).

* Fri May 25 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-31mdk
- Make sure to compile again the rpm distribued libtool or we go in ld
  trouble, (until libtool will be fixed) (Chmouel).
- fix bad l10n for languages where I is not the uppercase of i (bug #3570, Pablo)
- rpm-devel requires zlib-devel (DindinX)
- rpm-build Conflicts autoconf < 2.50
- %%configure macro adapted to use the new --build macro (gc)

* Fri May 18 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-30mdk
- add [RPM] to the log (DindinX).
- set LD_LIBRARY_PATH in find-requires.

* Tue May  8 2001 Giuseppe Ghibò <ghibo@mandrakesoft.com> 4.0-29mdk
- added -fno-strength-reduce for i586 optflags.

* Mon May  7 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-28mdk
- don't exit on patch error (let the shell do it).

* Fri Apr 27 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-27mdk
- rpm-build added dependency on file
- rebuilt for python 2.1

* Thu Apr  5 2001 Pixel <pixel@mandrakesoft.com> 4.0-26mdk
- remove the relative symlinking in update-alternatives which causes pbs (it switches to "manual")

* Thu Mar 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-25mdk
- move emacs stuff to rpm-build
- rpm-devel doesn't depend on python

* Thu Mar 29 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-24mdk
- added serverbuild macro to be used at the beginning of %build for building
server packages with the right optimization flags.
- added _post_service and _preun_service macros to be used for server packages that
provide initscripts.

* Mon Mar 19 2001 Pixel <pixel@mandrakesoft.com> 4.0-23mdk
- fix the rpm.el (\\. -> \\\\.)

* Tue Mar 13 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0-22mdk
- Add rpm-completion-ignore-case option/function on completion of
  rpm-spec-mode.
- Upgrade rpm-spec-mode to official 0.11e (and add mdk adaptations).

* Mon Mar 12 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-21mdk
- rebuild with new db3 packages.

* Thu Mar  8 2001 Pixel <pixel@mandrakesoft.com> 4.0-20mdk
- patch for update-alternatives making relative symlinks

* Thu Mar  8 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-19mdk
- added LD_LIBRARY_PATH to RPM_BUILD_ROOT lib dirs when looking for libraries to
avoid linking with the system ones when a package provides its own libraries.

* Mon Mar  5 2001 Pixel <pixel@mandrakesoft.com> 4.0-18mdk
- fix update-alternatives --remove <name> <file> when <file>

* Wed Jan 24 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-17mdk
- scripts failures don't impact anymore package installation/upgrade/removal.

* Thu Jan 18 2001 Francis Galiegue <fg@mandrakesoft.com> 4.0-16mdk
- Added ia64 arch

* Tue Jan 16 2001 Frederic Lepied <Frederic.Lepied@sugix.frmug.org> 4.0-15mdk
- protect %%make macro with a test of /proc/stat
- updated update-alternatives from dpkg 1.8.3.
- log install and removal of packages through syslog.

* Mon Jan 15 2001 Frederic Lepied <flepied@mandrakesoft.com> 4.0-14mdk
- integrated ideas from conectiva: in find-requires, don't check /usr/share/doc and
put package name instead of script name.

* Wed Jan 10 2001 Pablo Saratxaga <pablo@mandrakesoft.comW> 4.0-13mdk
- corrected the bug that makes rpmget/puttext crash 

* Mon Dec 11 2000 Götz Waschk <waschk@linux-mandrake.com> 4.0-12mdk
- fixed inclusion of locale files

* Thu Dec  7 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-11mdk
- use RPM_INSTALL_LANG to choose which locales to install (Pablo).

* Wed Nov 22 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-10mdk
- corrected macros file installation (Dadou sucks).

* Tue Nov 21 2000 David BAUDENS <baudens@mandrakesoft.com> 4.0-9mdk
- Update optflags for PPC

* Mon Nov 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0-8mdk
- BuildRequires: python-devel 2.0
- Oups fix patch.

* Sun Nov 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0-7mdk
- Improve gendiff.

* Sat Nov 18 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-6mdk
- recompile for python 2.0

* Fri Nov 17 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-5mdk
- find-requires: check that a script begins with #!

* Wed Nov 08 2000 David BAUDENS <baudens@mandrakesoft.com> 4.0-4mdk
- Update optflags for PPC
- Fix some %%prefix

* Thu Oct 19 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-3mdk
- fixed optflags for i586.

* Thu Oct 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 4.0-2mdk
- Make poptversion same of version.
- Install ugid.h in the headers of misc.h will not work.

* Wed Oct 18 2000 Frederic Lepied <flepied@mandrakesoft.com> 4.0-1mdk
- 4.0

* Fri Oct 13 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.5-26mdk
- reverted back %%_lib to lib (fix #815).

* Mon Oct  9 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.5-25mdk
- put back %%_lib to /lib.

* Thu Oct  5 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.5-24mdk
- don't use %%configure because it makes bootstrapping fails.
- removed build requires on popt-devel.
- conflict with menu < 2.1.5-29mdk.
- added build requires on zlib-devel gettext automake autoconf.

* Wed Oct  4 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.5-23mdk
- rpm-devel depends on popt-devel (close bug #593).
- remove warning cannot get lock on database if not verbose.

* Thu Sep 28 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.5-22mdk
- remove path of keyring because the users couldn't verify anymore.
- wait while the database is locked to be able to launch multiple rpm
commands without failure.

* Thu Sep 21 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.5-21mdk
- added path of gpg keyring in /etc/rpm.

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 3.0.5-20mdk
- fix _lib in mdk macros, must be "lib" and not "/lib"
(hell, _libdir was /usr///lib, and was getting bigger at each rebuild!)

* Fri Sep 01 2000 David BAUDENS <baudens@mandrakesoft.com> 3.0.5-19mdk
- Remove -mcpu=pentiumpro for i586

* Wed Aug 30 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.5-18mdk
- _localstatedir => /var/lib
- _lib => /lib
- packager tag

* Tue Aug 29 2000 Pixel <pixel@mandrakesoft.com> 3.0.5-17mdk
- objdump shutup

* Sun Aug 27 2000 David BAUDENS <baudens@mandrakesoft.com> 3.0.5-16mdk
- Fix and include macros for PPC & Co

* Fri Aug 25 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-15mdk
- add -S short-circuit for --short-circuit.
- add -A to build and clean everything.
- Last rpm-spec-mode from my tree.

* Thu Aug 24 2000 Pixel <pixel@mandrakesoft.com> 3.0.5-14mdk
- move back to /etc/rc.d/init.d from /etc/init.d
- fix (workaround?) again %%_remove_install_info (modified rpm-3.0.5-mdkconf.patch.bz2)

* Thu Aug 24 2000 Pixel <pixel@mandrakesoft.com> 3.0.5-13mdk
- fix (workaround?) %%_remove_install_info (modified rpm-3.0.5-mdkconf.patch.bz2)

* Tue Aug 22 2000 Pixel <pixel@mandrakesoft.com> 3.0.5-12mdk
- add rpm-spec-mode-mdk.el

* Mon Aug 21 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.5-11mdk
- added _initrddir macro to point to %%{_sysconfdir}/init.d.

* Thu Aug 17 2000 Pixel <pixel@mandrakesoft.com> 3.0.5-10mdk
- use find_lang for .mo's
- hide objdump errors in find-requires

* Wed Aug 16 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0.5-9mdk
- remove beroneries for lord ginette

* Fri Aug 11 2000 David BAUDENS <baudens@mandrakesoft.com> 3.0.5-8mdk
- Allow build without macros
- Add popt-devel in BuildRequires

* Thu Aug  3 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-7mdk
- Reinsert all modifications who was gone from 2mdk (thanks titi :-\).

* Wed Aug  2 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-6mdk
- Define mandir and infodir with datadir for FHS.

* Wed Aug 02 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0.5-5mdk
- fix docdir (chmousucks :-()

* Tue Aug  1 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-4mdk
- Define localstatelibdir to /var/lib (for FHS).
- Move rpmdiff to /usr/bin/.

* Wed Jul 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-3mdk
- Add -bE options to preprocessor the spec file (Samuel Isaacson).

* Mon Jul 24 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0.5-2mdk
- fix cxxflags as required by lord ginette

* Sat Jul 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-1mdk
- 3.0.5 final.

* Fri Jul 21 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.32mdk
- Exclude Bourne Shell script when doing find-requires on exec files
  and want to play with ldd and objdump.

* Fri Jul 21 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.0.5-0.31mdk
- patched % _libexecdir

* Thu Jul 20 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.30mdk
- Upgrade groups.
- Define %%_libexcdir to /usr/lib
- Define %%_localstatedir to %{_var}/state.

* Wed Jul 19 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.5-0.29mdk
- updated the list of groups.
- new release candidate. Should correct the rpm -F problem (Jürgen Zimmermann).

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 3.0.5-0.28mdk
- fix macro %%{clean_menus} ;p

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0.5-0.27mdk
- fix post and postun script for lord rpmlint

* Tue Jul 18 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.0.5-0.26mdk
- urf, forgot to increase the release tag for popt :-(
- post/postun ldconfig

* Tue Jul 18 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 3.0.5-0.25mdk
- added macros: _menudir, _iconsdir, _miconsdir, _liconsdir

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0.5-0.24mdk
- BM
- use ... rpm macros ...

* Thu Jul 13 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.5-0.23mdk
- point libexec to /usr/lib.
- added %make to be able to transparently handle SMP compilation.
The NPROCS env variable overrides the automatic detection.

* Wed Jul 12 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0.5-0.22mdk
- fix chmousucks in %%clean_menu (thanks gc)

* Wed Jul 12 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0.5-0.21mdk
- fix chmousucks in %%makeinstall macro

* Tue Jul 11 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.20mdk
- Define _sysconfdir to /etc.
- Add PREFIX=%{buildroot}/%%{prefix} to %%makeinstall.
- Add titi patches for optimisations (you have better to ash him wich
  one ;)).

* Mon Jul 10 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.19mdk
- clean_up typo.

* Sun Jul  9 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.18mdk
- Macroszifications.
- Fix install_info and move it to platform.

* Sun Jul  9 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.17mdk
- Back to -O3.

* Thu Jul  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.16mdk
- Add more titi macros %%{make_session} and %%{clean_menu} (it will be
  documented by titi in few days ;)).

* Thu Jul  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.15mdk
- Fix typo and remove bad symlinks.

* Wed Jul 05 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 3.0.5-0.14mdk
- really build against latest libbz2 ...

* Wed Jul  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.13mdk
- add %%_gamesdir	games/ %%_gamesbindir   %%{prefix}/%%{_gamesdir}
  %%_gamesdatadir  %%{_datadir}/%%{_gamesdir}, for GG
- Better update-menu macros
- Rebuild agains last bzip2.

* Mon Jul  3 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.5-0.12mdk
- updated rpm source with new release candidate.

* Mon Jul  3 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.5-0.11mdk
- recompile with newest bzip2.

* Sat Jul  1 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.10mdk
- s|-O3|-O2|; since -O3 don't compile with gcc2.96

* Wed Jun 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.9mdk
- Add some links for macros when building with --target (should ok now
  guiseppe ?).

* Wed Jun 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.8mdk
- Rebuild again bzip2 1.0.

* Tue Jun 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.7mdk
- Another fix to platform.in to call brp-mandrake with the new vendor
  stuff (this one should work !!).

* Tue Jun 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.6mdk
- define a %real_vendor (mandrake) and change target_platforms  to use it.

* Tue Jun 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.5mdk
- Add %{update-menus} macros.
- define sysconfdir to /etc (thanks gg).
- Include macros file of %{_libdir}/% target_platforms/macros.

* Mon Jun 26 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.3mdk
- don't use %{vendor} to call brp-mandrake (use mandrake).
- s|%{_prefix}/|% prefix|; for prefix of infodir (titi are you happy ?)

* Sat Jun 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.2mdk
- Define a release for popt* package.

* Fri Jun 23 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.5-0.1mdk
- Upgrade groups to mdk Groups.
- More mandrakisations with build policies.
- 3.0.5 test series.
- updates-alternatives should be 755.
- Fix doc.

* Mon Jun 19 2000 Pixel <pixel@mandrakesoft.com> 3.0.4-10mdk
- patch for upgrading directory in symlink, won't work if new location already exists :(
  (fixes some "cpio: unlink failed - Bad file descriptor" errors)

* Fri Jun 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.4-9mdk
- Add patch to support rpm-4.0 format (at least work for sources).

* Fri Jun 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.4-8mdk
- Downgrade changes for the configure macros and makeinstall macros
  from rpm-4.0.

* Wed Jun 14 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.4-7mdk
- Forget to create the directory :p.

* Tue Jun  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.4-6mdk
- Add /etc/alternatives and /var/lib/rpm/alternatives directory.

* Tue Jun  6 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.4-5mdk
- Add updates-alternatives.

* Tue May 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.4-4mdk
- Merge pixel patchs in mdkconf patch.
- Fix gendiff changes.

* Mon May 15 2000 Pixel <pixel@mandrakesoft.com> 3.0.4-3mdk
- add CXXFLAGS to % configure

* Mon May 15 2000 Pixel <pixel@mandrakesoft.com> 3.0.4-2mdk
- add k6&k7 to ix86

* Mon May 15 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.4-1mdk
- Remove ugly patch and add clean fix from Jeff Johnson.
- 1mdk

* Thu Apr 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.4-0.12mdk
- Work Around (ugly ugly ugly but work) on popt bug with --define on alpha.

* Sun Apr 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.4-0.11mdk
- Improve gendiff.
- Define __extensions, and install-info macros install script.
- Add some usefull alias to rpmpopt.

* Sun Mar 26 2000 Pixel <pixel@mandrakesoft.com> 3.0.4-0.10mdk
- patch for supermount: skip mountpoints /mnt/.*

* Wed Mar 22 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.4-0.9mdk
- added dependencies on rpm for rpm-devel, rpm-python and rpm-build.
- split popt in popt and popt-devel

* Thu Mar 16 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.4-0.8mdk
- fix rpmHeaderGetEntry returned type for RPMTAG_OLDFILENAMES.
- fix syntax in find-requires.

* Thu Mar 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.4-0.7mdk
- 3.0.4 final.

* Sun Mar 12 2000 Pixel <pixel@mandrakesoft.com> 3.0.4-0.6mdk
- moved libpopt.so.0's in /lib

* Mon Mar 06 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 3.0.4-0.5mdk 
- added %{_libdir}/rpm to %files
- added support for RPM_INSTALL_LANG variable (the official way of
  doing it will be using %%{_install_langs} macro on /etc/rpm/macros;
  but there may be some installed systems with RPM_INSTALL_LANG in use
  out ther; and also it is easier for one-time change on the command line) 

* Tue Feb 22 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.4-4mdk
- Remove Makefile* from doc.

* Fri Feb 18 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.4-0.3mdk
- put back the man pages.

* Fri Feb 18 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.4-0.2mdk
- call spec-helper in __spec_install_post.

* Wed Feb 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.4-0.1mdk
- New spec clean-up.
- Remove pgp passphrase patch (use gpg instead).
- Obsoletes: popt-devel (now popt does also devel).
- Separate in multiple package like rpm-build popt rpm-devel rpm-python.
- New mdkconf patch.
- Use configure macros
- Hide your babys and womens rpm 3.0.4 from CVS is here.

* Thu Jan 27 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.3-48mdk
- Fix rpmrc again (thanks David Walluck <david@anti-microsoft.org>),
  to bothered me ;).

* Mon Jan 24 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.3-47mdk
- Reinsert flags for different arch.

* Fri Jan 21 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.3-46mdk
- add %{_libdir}/librpm.so to the devel package.

* Fri Jan 21 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 3.0.3-45mdk
- Major clean-up of specs and patchs.

* Wed Jan 19 2000 Frederic Lepied <flepied@mandrakesoft.com> 3.0.3-44mdk
- fix find-requires for fakeroot.

* Tue Nov  2 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- s/-O6/-O3/

* Thu Oct 28 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Remove the PGPPASS patch (gpgp conflict) but leave it in case.
- Add %prefix/locale/*/ in %files more doc and %prefix/man/%lang/*

* Thu Oct 28 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Add patch to check PGPPASS before signing.

* Tue Oct 26 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Build release.

* Wed Oct 13 1999 - David BAUDENS <baudens@mandrakesoft.com>
- Create a k6 directory in %{_prefix}/src/RPM/RPMS

* Fri Oct  8 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix %post # RPM bugs ?
- 3.0.3 final.

* Mon Sep 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- reEnable the rpm -ba --short-circuit from pixel.
- add patch to get work the python modules (#204).

* Sun Sep 26 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Whoops wrong k6 cflags

* Sun Sep 26 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Preliminary k6 support

* Thu Sep 23 1999 Pixel <pixel@mandrakesoft.com>
- fixed a bug in rpmlib

* Thu Aug 19 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add patch to fix wrong info path (tnks pablo).
- Fix CFLAGS with multiple gcc interface.

* Mon Aug 16 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Latest CVS - this finally permits us to Provide: versions.

* Wed Aug 11 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Latest CVS
- Put new preferred CFLAGS for {p,}gcc 2.95 in rpmrc by default
- enable support for RPM4 packages
- ignore autoconf version conflicts (autoconf 2.14 works, but rpm
  insists on 2.13)

* Sat Jul 31 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Last cvs version.
- More architecture in rpmputtext (Pablo).

* Tue Jul 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Last version from CVS (fix --rebuild bugs).
- s|i386|i586| in rpmputtext.

* Tue Jul 27 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- I wonder want to know why rpmlib is so buggy :-((.

* Wed Jul 21 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Fix rpmpopt wrong path.
- Last CVS snapshot.

* Tue Jul 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- oups Forget to add rpmputtext.

* Tue Jul 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Moving the rpmputtext rpmputtext to %{_bindir}
- 3.0.3 from CVS.
- Relifting of spec files.
- Build Patch.
- Merging old patch of libmisc and libtool.

* Wed Jul 07 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- 3.0.2 final (15mdk)
- fixed default build arch use --target if you need it
- added librpmbuild.*a and other libtool files

* Tue Jul  6 1999 Axalon Bloodstone <axalon@linux-mandrake.com>
- Could not find 11mdk srpm, snapshoted rpm cvs and incremented release

* Fri May 28 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Removing the CVS stuff when compiling.

* Thu May 27 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- Update to a recent 3.0.2 CVS snapshot (BuildRequire :) )
- add our CFLAGS to rpmrc
- Recompile with CFLAGS for devel

* Wed May 19 1999 Bernhard Rosenkränzer <bero@mandrakesoft.com>
- Update to more recent 3.0.1 CVS snapshot (more bugfixes)

* Tue May 11 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- I have forget to mkdir %{_prefix}/src/RPM instead of */*/redhat/
- 3.0.1 from Bero.

* Tue Apr 20 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Mandrake adptations.
- Add patch for %{_prefix}/src/rpm instead of /usr/src/redhat/.
