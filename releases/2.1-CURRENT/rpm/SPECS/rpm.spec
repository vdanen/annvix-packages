#
# spec file for package rpm
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$
#
# mdk 4.4.5-2mdk

%define revision	$Rev$
%define name		rpm
%define version		4.4.5
%define poptver		1.10.5
%define pmodver		0.66
%define release		%_revrel

%define srcver		4.4.5
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
Group:		System/Configuration
URL:            http://www.rpm.org/
Source:		ftp://ftp.jbj.org/pub/rpm-%{libver}.x/rpm-%{srcver}.tar.bz2
Source1:        annvix-keys.tar.bz2
Source2:        annvix-keys.tar.bz2.asc

# Add some undocumented feature to gendiff
Patch17:	rpm-4.2-gendiff-improved.patch
# (fredl) add loging facilities through syslog
Patch31:	rpm-4.4.3-syslog.patch
# Check amd64 vs x86_64, these arch are the same
Patch44:	rpm-4.4.1-amd64.patch
# Backport from 4.2.1 provides becoming obsoletes bug (fpons)
Patch49:	rpm-4.4.3-provides-obsoleted.patch
# Still need
Patch56:	rpm-4.2.2-ppc64.patch
# Colorize static archives and .so symlinks
Patch62:	rpm-4.4.3-coloring.patch
# ok for this
Patch63:	rpm-4.2.3-dont-install-delta-rpms.patch
# This patch ask to read /usr/lib/rpm/vendor/rpmpopt too
Patch64:    rpm-4.4.1-morepopt.patch
# Being able to read old rpm (build with rpm v3)
# See https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=127113#c12
Patch68:    rpm-4.4.1-region_trailer.patch
# Fix some French translations
Patch69:	rpm-4.4.5-fr.patch
# In original rpm, -bb --short-circuit does not work and run all stage
# From popular request, we allow to do this
# http://qa.mandriva.com/show_bug.cgi?id=15896
Patch70:	rpm-4.4.1-bb-shortcircuit.patch
# http://www.redhat.com/archives/rpm-list/2005-April/msg00131.html
# http://www.redhat.com/archives/rpm-list/2005-April/msg00132.html
Patch71:	rpm-4.4.4-ordererase.patch
# File conflicts when rpm -i
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=151609
Patch72:	rpm-4.4.1-fileconflicts.patch
# Allow to set %_srcdefattr for src.rpm
Patch77:	rpm-source-defattr.patch
# Do not use futex, but fcntl
Patch78:	rpm-4.4.5-fcntl.patch
# Fix: http://qa.mandriva.com/show_bug.cgi?id=17774
# Patch from cvs HEAD (4.4.3)
Patch80:	rpm-4.4.2-buildsubdir-for-scriptlet.patch
Patch82:	rpm-4.4.3-ordering.patch
# don't conflict for doc files from colored packages
Patch83:	rpm-4.2.3-no-doc-conflicts.patch
# Fix http://qa.mandriva.com/show_bug.cgi?id=19392
Patch84:	rpm-4.4.4-rpmqv-ghost.patch
# Install perl module in vendor directory
Patch85:	rpm-4.4.4-perldirs.patch
# Use temporary table for Depends DB (Olivier Thauvin upstream)
Patch86:	rpm-4.4.4-depsdb.patch
Patch87:	rpm4-CVE-2006-5466.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5 >= 2.57
BuildRequires:	doxygen
BuildRequires:	python-devel
BuildRequires:	perl-devel
BuildRequires:	zlib-devel
BuildRequires:	automake1.8
BuildRequires:	glibc-static-devel
BuildRequires:	elfutils-static-devel
BuildRequires:	sed >= 4.0.3
BuildRequires:	libbeecrypt-devel
BuildRequires:	ed
BuildRequires:	gettext-devel
BuildRequires:	rpm-annvix-setup-build
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	neon-static-devel < 0.25
BuildRequires:	sqlite3-static-devel
BuildRequires:	openssl-static-devel >= 0.9.8
%if %buildnptl
BuildRequires:	nptl-devel
%endif

Requires:	bzip2 >= 0.9.0c-2
Requires:	cpio
Requires:	gawk
Requires:	glibc >= 2.1.92
Requires:	mktemp
Requires:	popt = %{poptver}-%{release}
Requires:	setup >= 2.2.0-8mdk
Requires:	multiarch-utils >= 1.0.7
Requires:	update-alternatives
Requires:	rpm-annvix-setup >= 1.10
Requires:	%{libname} = %{version}-%{release}
Conflicts:	locales < 2.3.1.1
Conflicts:	patch < 2.5
Requires(pre):	rpm-helper >= 0.8
Requires(pre):	coreutils
Requires(postun): rpm-helper >= 0.8

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
Group:		System/Configuration
Requires:	autoconf
Requires:	automake
Requires:	file
Requires:	gcc-c++
# We need cputoolize & amd64-* alias to x86_64-* in config.sub
Requires:	libtool >= 1.4.3-5mdk
Requires:	patch
Requires:	make
Requires:	unzip
Requires:	elfutils
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


%package -n perl-RPM
Summary:	Perl bindings for RPM
Group:		Development/Perl
Version:	%{pmodver}

%description -n perl-RPM
The RPM Perl module provides an object-oriented interface to querying both
the installed RPM database as well as files on the filesystem.


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


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{srcver}
%patch17 -p1 -b .improved
%patch31 -p0 -b .syslog
%patch44 -p1 -b .amd64
%patch49 -p0 -b .provides
%patch56 -p1 -b .ppc64
%patch62 -p0 -b .coloring
%patch63 -p1 -b .dont-install-delta-rpms
%patch64 -p0 -b .morepopt
%patch68 -p0 -b .region_trailer
%patch69 -p0 -b .trans
%patch70 -p0 -b .shortcircuit
%patch71 -p0  -b .ordererase
%patch72 -p1  -b .fileconflicts
%patch77 -p0  -b .srcdefattr

%if %{buildnptl}
%else
%patch78 -p0  -b .fcntl
%endif

%patch80 -p0 -b .subdir-scriplet
%patch82 -p0 -b .ordering
%patch83 -p1 -b .no-doc-conflicts
%patch84 -p0 -b .poptQVghost
%patch85 -p0 -b .perldirs
%patch86 -p0 -b .depsdb
%patch87 -p0 -b .cve-2006-5466

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

# rpm takes care of --libdir but explicitelly setting --libdir on
# configure breaks make install, but this does not matter.
# --build, we explictly set 'annvix' as our config subdir and 
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

rm -f %{buildroot}%{_prefix}/lib/rpmpopt
ln -s rpm/rpmpopt-%{rpmversion} %{buildroot}%{_prefix}/lib/rpmpopt
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

%{rpmdir}/%{_host_vendor}/kill-lang.sh %{buildroot} %{name}
%{rpmdir}/%{_host_vendor}/find-lang.sh %{buildroot} %{name}
%{rpmdir}/%{_host_vendor}/find-lang.sh %{buildroot} popt

# install RPM-GPG-KEYS
mkdir -p %{buildroot}%{_sysconfdir}/RPM-GPG-KEYS
tar xvjf %{_sourcedir}/annvix-keys.tar.bz2 -C %{buildroot}%{_sysconfdir}/RPM-GPG-KEYS


%check
#make -C popt check-TESTS


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


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
# nuke __db.00? when updating to this rpm
rm -f /var/lib/rpm/__db.00?

if [ ! -e %{_sysconfdir}/rpm/macros -a -e %{_sysconfdir}/rpmrc -a -f %{rpmdir}/convertrpmrc.sh ] 
then
    sh %{rpmdir}/convertrpmrc.sh 2>&1 > /dev/null
fi

if [ -f /var/lib/rpm/packages.rpm ]; then
    /bin/chown rpm:rpm /var/lib/rpm/*.rpm
elif [ ! -f /var/lib/rpm/Packages ]; then
    /bin/rpm --initdb
fi

#for i in `ls -1 /etc/RPM-GPG-KEYS/*.asc`
#do
#    key=`basename $i|cut -f 1 -d '.'`
#    if [ "`rpm -q gpg-pubkey-$key|grep 'not installed'`" ]; then
#        rpm --import $i
#        echo "NOTICE: imported new GPG key $i"
#    fi
#done



%postun
/usr/share/rpm-helper/del-user rpm $1 rpm


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libpoptname} -p /sbin/ldconfig
%postun -n %{libpoptname} -p /sbin/ldconfig



%define	rpmattr		%attr(0755, rpm, rpm)
%files -f %{name}.lang
%defattr(-,root,root)
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
%dir %{_sysconfdir}/RPM-GPG-KEYS
%{_sysconfdir}/RPM-GPG-KEYS/*.asc
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
%{_prefix}/lib/rpm/rpmrc
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

%{_prefix}/src/rpm/RPMS/*
%{_datadir}/man/man[18]/*.[18]*

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
%dir %{_prefix}/src/rpm
%dir %{_prefix}/src/rpm/BUILD
%dir %{_prefix}/src/rpm/SPECS
%dir %{_prefix}/src/rpm/SOURCES
%dir %{_prefix}/src/rpm/SRPMS
%dir %{_prefix}/src/rpm/RPMS
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
%rpmattr	%{_prefix}/lib/rpm/executabledeps.sh
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
%rpmattr	%{_prefix}/lib/rpm/javadeps.sh
%rpmattr	%{_prefix}/lib/rpm/libtooldeps.sh
%rpmattr	%{_prefix}/lib/rpm/magic
%rpmattr	%{_prefix}/lib/rpm/magic.mgc
%rpmattr	%{_prefix}/lib/rpm/magic.mime
%rpmattr	%{_prefix}/lib/rpm/magic.mime.mgc
%rpmattr	%{_prefix}/lib/rpm/magic.prov
%rpmattr	%{_prefix}/lib/rpm/magic.req
%rpmattr	%{_prefix}/lib/rpm/perldeps.pl
%rpmattr	%{_prefix}/lib/rpm/perl.prov
%rpmattr	%{_prefix}/lib/rpm/perl.req
%rpmattr	%{_prefix}/lib/rpm/pkgconfigdeps.sh

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


%files -n perl-RPM
%defattr(-,root,root)
%{perl_vendorarch}/RPM.pm
%{perl_vendorarch}/auto/RPM


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/librpm-%{libver}.so
%{_libdir}/librpmdb-%{libver}.so
%{_libdir}/librpmio-%{libver}.so
%{_libdir}/librpmbuild-%{libver}.so


%files -n %{libname}-devel
%defattr(-,root,root)
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
%{_datadir}/man/man3/RPM*
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
%{_datadir}/man/man3/popt.3*

%files doc
%defattr(-,root,root)
%doc RPM-PGP-KEY RPM-GPG-KEY GROUPS CHANGES doc/manual/[a-z]*
%doc CHANGES
%doc doc-copy/*


%changelog
* Sun Dec 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.5
- rebuild against new libneon that isn't built against krb5 as otherwise
  we end up requiring krb5-devel to have rpm-devel installed (not only
  that, but rpm doesn't build against 1.5.1 for some reason)

* Sat Dec 23 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.5
- rebuild against new gettext

* Fri Dec 08 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.5
- rebuild against new ncurses

* Tue Nov 07 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.5
- rebuild against new sqlite

* Mon Nov 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.5
- P87: security fix for CVE-2006-5466

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.5
- spec cleanups
- remove locales

* Sat Aug 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.5
- rebuild against new openssl
- spec cleanups

* Thu Aug 03 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.5
- don't install RPM-GPG-KEYS by default here -- the installer will
  do it instead (it somehow trashes the rpm db creating the install
  CD and I fear it might do the same to the installed system)
- spec cleanups

* Fri Jul 21 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.5
- rebuild against new elfutils

* Thu Jun 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.5
- add -doc subpackage
- rebuild with gcc4
- rebuild against new readline, python, and sqlite3
- include the RPM-GPG-KEYS here, rather than in gnupg
- on %%post, make rpm --import the gpg keys immediately

* Tue May 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.5
- 4.4.5 (sync with 4.4.5-2mdk):
  - dropped P41, P66, , P74, P76, P79, P81
  - updated P31, P49, P62, P69, P71, P78, P82
  - new patches P84, P85, P86
  - BuildRequires changes to use static neon-devel and libsqlite3-devel,
    add perl-devel and openssl-static-devel
  - add the perl-RPM package
  - move the triggerun script to the post script (rafael)
  - put the popt(3) man page into libpopt-devel (rafael)
  - add coreutils to prereq (rafael)
  - disable popt tests (rafael)
- update requires to most recent rpm-annvix-setup

* Mon May 01 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.4.2
- fix group

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

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
