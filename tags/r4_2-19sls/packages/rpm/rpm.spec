%define name		rpm
%define rpmversion      4.2
%define poptver		1.8
# You need increase both release and poptrelease
%define poptrelease	%{release}
%define release		19sls

%define url		ftp://ftp.rpm.org/pub/rpm/dist/rpm-4.0.x
%define pyver		%(python -V 2>&1 | cut -f2 -d" " | cut -f1,2 -d".")
%define lib64arches	x86_64

%define __find_requires %{buildroot}%{rpmdir}/find-requires %{?buildroot:%{buildroot}} %{?_target_cpu:%{_target_cpu}}
%define __find_provides %{buildroot}%{rpmdir}/find-provides

%define _prefix /usr
%ifarch %{lib64arches}
%define _lib lib64
%define _libdir /usr/lib64
%else
%define _lib lib
%define _libdir /usr/lib
%endif
%define _bindir /usr/bin
%define _sysconfdir /etc
%define _datadir /usr/share
%define _defaultdocdir /usr/share/doc

%define build_propolice		1
%{expand: %{?_without_propolice:	%%define build_propolice 0}}
%{expand: %{?_with_propolice:		%%define build_propolice 1}}

# Define directory which holds rpm config files, and some binaries actually
# NOTE: it remains */lib even on lib64 platforms as only one version
#       of rpm is supported anyway, per architecture
%define rpmdir %{_prefix}/lib/rpm

Summary:	The RPM package management system
Name:		%{name}
Version:	%{rpmversion}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Packaging
URL:            http://www.rpm.org/
Source:		%{url}/rpm-%{version}.tar.bz2
Source2:	rpm-spec-mode.el.bz2
Source3:	filter.sh
Patch0:		rpm-4.2-mdkconf.patch.bz2
Patch3:		rpm-4.0-bashort.patch.bz2
Patch5:		rpm-4.2-autoreq.patch.bz2
Patch8:		rpm-4.2-skipmntpoints.patch.bz2
Patch10:	rpm-4.0-updates-alternatives.patch.bz2
Patch13:	rpm-4.2-wait-for-lock.patch.bz2
Patch17:	rpm-4.2-gendiff-improved.patch.bz2
# this patches adds support for RPM_INSTALL_LANG shell variable, with priority
# over the macro defined in /etc/rpm/macros
Patch18:	rpm-4.2-langvar.patch.bz2
# (fredl) script failures don't break install/upgrade/removal
Patch22:	rpm-4.0.3-script-dont-fail.patch.bz2
Patch23:	rpm-4.0.4-spec-mode-mdkconf.patch.bz2
Patch24:	rpm-4.0.3-patch-exit.patch.bz2
# (pablo) in turk I isn't the upper case of i
# test: LC_ALL=tr rpm -q glibc
Patch26:	rpm-4.0.3-turk.patch.bz2
# (chmou)
Patch27:	rpm-4.2-libtool-old-version.patch.bz2
# (fredl) add loging facilities through syslog
Patch31:	rpm-4.2-syslog.patch.bz2
Patch32:	rpm-4.2-rpmvercmp.patch.bz2
Patch33:	rpm-4.2-execvp-error-report.patch.bz2
Patch36:	rpm-4.2-umask.patch.bz2
# (pablo) improved version of find.lang.sh, from rpm mailing-list.
# it adds a --all-name switch that allows finding all localized files,
# whatever the name (useful in addition of --with-gnome/--with-kde to find
# the different html help directories
Patch35:	rpm-4.2-find-lang_all-name.patch.bz2
# Workaround nested %%if handling bug (SuSE patch)
Patch40:	rpm-4.0.4-if.patch.bz2
# Correctly check for PPC 74xx systems
Patch41:	rpm-4.2-ppc-74xx.patch.bz2
# Don't link against system libs when relinking in %%install
Patch42:	rpm-4.2-mad-relink.patch.bz2
# Correctly setup X11 paths on lib64 systems
Patch43:	rpm-4.2-configure-xpath.patch.bz2
# Build .amd64 packages by default on x86-64
Patch44:	rpm-4.2-amd64.patch.bz2
Patch45:	rpm-4.2-python-macros.patch.bz2
Patch47:	rpm-4.0.4-good-lock.patch.bz2
Patch48:	rpm-4.0.4-debug.patch.bz2
# Backport from 4.2.1 provides becoming obsoletes bug (fpons)
Patch49:	rpm-4.2-provides-obsoleted.patch.bz2
Patch50:	rpm-4.2-python-site-lisp.patch.bz2
# (vdanen) use stack protection by default
Patch51:	rpm-4.2-stackmacros.patch.bz2

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	autoconf2.5
BuildRequires:	doxygen
BuildRequires:	python-devel
BuildRequires:	zlib-devel
BuildRequires:	automake
BuildRequires:	glibc-static-devel
BuildRequires:	elfutils-static-devel
BuildRequires:	sed >= 4.0.3

Requires:	bzip2 >= 0.9.0c-2
Requires:	cpio
Requires:	gawk
Requires:	glibc >= 2.1.92
Requires:	make
Requires:	mktemp
Requires:	popt = %{poptver}-%{poptrelease}
Requires:	setup >= 2.2.0-8mdk
Requires:	unzip
Requires:	elfutils
Conflicts:	patch < 2.5
Conflicts:	menu < 2.1.5-29mdk
Conflicts:	locales < 2.3.1.1
PreReq:		rpm-helper >= 0.8

%description
RPM is a powerful command line driven package management system capable of
installing, uninstalling, verifying, querying, and updating software packages.
Each software package consists of an archive of files along with information
about the package like its version, a description, etc.

%package devel
Summary:	Development files for applications which will manipulate RPM packages
Group:		Development/C
Requires:	bzip2-devel
Requires:	rpm = %{version}-%{release}
Requires:	popt-devel = %{poptver}-%{poptrelease}
Requires:	zlib-devel

%description devel
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
Requires:	patch
Requires:	rpm = %{version}-%{release}
%if "%{_lib}" == "lib64"
# Need spec-helper recent enough to automatically fix up references to
# /lib/security on lib64 platforms
Requires:	spec-helper >= 0.6-5mdk
%else
Requires:	spec-helper
%endif

%description build
This package contains scripts and executable programs that are used to
build packages using RPM.

%package python
Summary:	Python bindings for apps which will manipulate RPM packages
Group:		Development/Python
Requires:	popt >= %{poptver}
Requires:	python >= %{pyver}
Requires:	rpm = %{version}-%{release}

%description python
The rpm-python package contains a module which permits applications
written in the Python programming language to use the interface
supplied by RPM (RPM Package Manager) libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.

%package -n popt
Summary:	A C library for parsing command line parameters
Group:		System/Libraries
Version:	%{poptver}
Release:	%{poptrelease}

%description -n popt
Popt is a C library for parsing command line parameters.  Popt was
heavily influenced by the getopt() and getopt_long() functions, but it
improves on them by allowing more powerful argument expansion.  Popt
can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments.  Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%package -n popt-devel
Summary:	A C library for parsing command line parameters
Group:		Development/C
Version:	%{poptver}
Release:	%{poptrelease}
Requires:	popt = %{poptver}-%{poptrelease}

%description -n popt-devel
Popt is a C library for parsing command line parameters.  Popt was
heavily influenced by the getopt() and getopt_long() functions, but it
improves on them by allowing more powerful argument expansion.  Popt
can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments.  Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

Install popt-devel if you're a C programmer and you'd like to use its
capabilities.

%prep
%setup -q
%patch0 -p1 -b .mdk
#%patch1 -p0
#%patch2 -p1
%patch3 -p0 -b .short
#%patch4 -p0
%patch5 -p1 -b .autoreq
#%patch6 -p1
%patch8 -p1 -b .skip
#%patch9 -p0
%patch10 -p1 -z .pix
#%patch11 -p1
%patch13 -p1 -b .lock
#%patch14 -p1
#%patch16 -p1 -b .python2.1

%patch17 -p1 -b .improved
%patch18 -p1 -b .langvar
#%patch20 -p1
%patch22 -p1 -b .dontfail

bzcat %{SOURCE2} > rpm-spec-mode.el

%patch23 -p1 -b .mdkel
%patch24 -p1 -b .patchexit
##%patch26 -p1 -b .turk
%patch27 -p1 -b .oldlibtool
#%patch30 -p1 -b .hashes
%patch31 -p1 -b .syslog
%patch32 -p1 -b .rpmvercmp
%patch33 -p1 -b .execvp-error-report
#%patch34 -p1 -b .expand-buildmacro
%patch35 -p1 -b .find-lang_all-name
%patch36 -p1 -b .umask
#%patch37 -p1 -b .chroot_prefix
#%patch38 -p1 -b .resign
%patch40 -p1 -b .if
%patch41 -p1 -b .ppc-74xx
%patch42 -p1 -b .mad-relink
%if "%{_lib}" == "lib64"
%patch43 -p1 -b .configure-xpath
%endif
%patch44 -p1 -b .amd64
%patch45 -p1 -b .python-macros
##%patch47 -p1 -b .good-lock
#%patch48 -p1 -b .debug
%patch49 -p1 -b .provides
%patch50 -p1 -b .python-site-lisp
%if %build_propolice
%patch51 -p1 -b .stackmacro
%endif

autoconf

%build
# NOTE: Don't add libdir specification here as rpm data files really
# have to go to /usr/lib/rpm and we support only one rpm program per
# architecture
# (vdanen): don't build rpm with stack protection
#CPPFLAGS="-I/usr/include/libelf" CFLAGS="$RPM_OPT_FLAGS -fno-stack-protector" CXXFLAGS="$RPM_OPT_FLAGS -fno-stack-protector" ./configure --prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --mandir=%{_datadir}/man --infodir=%{_datadir}/info --enable-nls --without-javaglue --enable-posixmutexes --with-python=%{pyver}
CPPFLAGS="-I/usr/include/libelf" CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" ./configure --prefix=%{_prefix} --sysconfdir=/etc --localstatedir=/var --mandir=%{_datadir}/man --infodir=%{_datadir}/info --enable-nls --without-javaglue --enable-posixmutexes --with-python=%{pyver}
perl -p -i -e 's/conftest\.s/conftest\$\$.s/' config.status

smp_flags=$([ -z "$RPM_BUILD_NCPUS" ] \
	&& RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"; \
	[ "$RPM_BUILD_NCPUS" -gt 1 ] && echo "-j$RPM_BUILD_NCPUS") || :

make $smp_flags

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_lib}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{rpmdir}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/src/RPM/{SOURCES,SPECS,SRPMS,BUILD}
%ifarch i386 i486 i586 i686 k6 athlon
mkdir -p $RPM_BUILD_ROOT%{_prefix}/src/RPM/RPMS/{i386,i486,i586,i686,k6,athlon}
%endif
%ifarch ppc
mkdir -p $RPM_BUILD_ROOT%{_prefix}/src/RPM/RPMS/{ppc,powerpc}
%endif
%ifarch ia64
mkdir -p $RPM_BUILD_ROOT%{_prefix}/src/RPM/RPMS/ia64
%endif
%ifarch x86_64 amd64
mkdir -p $RPM_BUILD_ROOT%{_prefix}/src/RPM/RPMS/{amd64,x86_64}
%endif
mkdir -p $RPM_BUILD_ROOT%{_prefix}/src/RPM/RPMS/noarch

make DESTDIR="$RPM_BUILD_ROOT" install

make DESTDIR="$RPM_BUILD_ROOT" PYVER=%{pyver} -C python install

install %{SOURCE3} $RPM_BUILD_ROOT%{_prefix}/lib/rpm/filter.sh

# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}/etc/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}/etc/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
install -m 755 scripts/rpm.log ${RPM_BUILD_ROOT}/etc/logrotate.d/rpm

mkdir -p $RPM_BUILD_ROOT%{_prefix}/sbin $RPM_BUILD_ROOT%{_datadir}/man/man8/
install -m644 update-alternatives.8 $RPM_BUILD_ROOT%{_datadir}/man/man8/
install -m755 update-alternatives $RPM_BUILD_ROOT%{_sbindir}/
install -d $RPM_BUILD_ROOT/etc/alternatives
install -d $RPM_BUILD_ROOT/var/lib/rpm/alternatives

mkdir -p $RPM_BUILD_ROOT/etc/alternatives
mkdir -p $RPM_BUILD_ROOT/var/lib/rpm/alternatives/

mkdir -p $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libpopt.so.* $RPM_BUILD_ROOT/%{_lib}
ln -s ../../%{_lib}/libpopt.so.0 $RPM_BUILD_ROOT%{_libdir}
ln -sf libpopt.so.0 $RPM_BUILD_ROOT%{_libdir}/libpopt.so

%ifarch ppc powerpc
ln -sf ppc-mandrake-linux $RPM_BUILD_ROOT%{rpmdir}/powerpc-mandrake-linux
%endif

mv -f $RPM_BUILD_ROOT%{rpmdir}/brp-redhat $RPM_BUILD_ROOT%{rpmdir}/brp-mandrake

mv -f $RPM_BUILD_ROOT/%{rpmdir}/rpmdiff $RPM_BUILD_ROOT/%{_bindir}

install -d $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/
install -m644 rpm-spec-mode.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/

install -d $RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d
cat <<EOF >$RPM_BUILD_ROOT%{_sysconfdir}/emacs/site-start.d/%{name}.el
(setq auto-mode-alist (cons '("\\\\.spec$" . rpm-spec-mode) auto-mode-alist))
(autoload 'rpm-spec-mode "rpm-spec-mode" "RPM spec mode (mandrakized)." t)
EOF

# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}/etc/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}/etc/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}/etc/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}/etc/logrotate.d/rpm

mkdir -p $RPM_BUILD_ROOT/etc/rpm
mkdir -p $RPM_BUILD_ROOT/etc/rpm
cat << E_O_F > $RPM_BUILD_ROOT/etc/rpm/macros.cdb
%%__dbi_cdb      %%{nil}
%%__dbi_other    %%{?_tmppath:tmpdir=%%{_tmppath}} usedbenv create \
                 joinenv mpool mp_mmapsize=8Mb mp_size=512kb verify
E_O_F

mkdir -p $RPM_BUILD_ROOT/var/lib/rpm
for dbi in \
	Basenames Conflictname Dirnames Group Installtid Name Providename \
	Provideversion Removetid Requirename Requireversion Triggername \
	Packages __db.001 __db.002 __db.003 __db.004
do
    touch $RPM_BUILD_ROOT/var/lib/rpm/$dbi
done

find apidocs -type f | xargs perl -p -i -e "s@$RPM_BUILD_DIR/%{name}-%{rpmversion}@@g"

test -d doc-copy || mkdir doc-copy
rm -rf doc-copy/*
ln -f doc/manual/* doc-copy/
rm -f doc-copy/Makefile*

#install -d $RPM_BUILD_ROOT/%{_datadir}/man/man3
#install -m 644 apidocs/man/man3/* $RPM_BUILD_ROOT/%{_datadir}/man/man3/

# Get rid of unpackaged files
(cd $RPM_BUILD_ROOT;
  rm -rf .%{_includedir}/beecrypt/
  rm -f  .%{_libdir}/libbeecrypt.{a,la,so*}
  rm -f  .%{_libdir}/python*/site-packages/poptmodule.{a,la}
  rm -f  .%{_libdir}/python*/site-packages/rpmmodule.{a,la}
  rm -f  .%{rpmdir}/{Specfile.pm,cpanflute2,cpanflute,sql.prov,sql.req,tcl.req}
  rm -f  .%{rpmdir}/{config.site,cross-build,rpmdiff.cgi}
  rm -f  .%{rpmdir}/trpm
  rm -f  .%{_bindir}/rpmdiff
)

$RPM_BUILD_ROOT%{rpmdir}/find-lang.sh $RPM_BUILD_ROOT %{name}
$RPM_BUILD_ROOT%{rpmdir}/find-lang.sh $RPM_BUILD_ROOT popt

$RPM_BUILD_ROOT%{rpmdir}/brp-mandrake
exit 0

%clean
rm -rf $RPM_BUILD_ROOT

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

/usr/share/rpm-helper/add-user rpm $1 rpm /var/lib/rpm /bin/false

rm -rf /usr/lib/rpm/*-mandrake-*

%post
/sbin/ldconfig

if [ ! -e /etc/rpm/macros -a -e /etc/rpmrc -a -f %{rpmdir}/convertrpmrc.sh ] 
then
	sh %{rpmdir}/convertrpmrc.sh 2>&1 > /dev/null
fi

if [ -f /proc/cpuinfo ] && grep -qi AMD-K6 /proc/cpuinfo; then
	perl -p -i -e "s/#K6#//g" %{rpmdir}/rpmrc
fi

if [ -f /var/lib/rpm/packages.rpm ]; then
    /bin/chown rpm.rpm /var/lib/rpm/*.rpm
elif [ ! -f /var/lib/rpm/Packages ]; then
    /bin/rpm --initdb
fi

%postun

/sbin/ldconfig

/usr/share/rpm-helper/del-user rpm $1 rpm

%post -n popt -p /sbin/ldconfig
%postun -n popt -p /sbin/ldconfig

%define	rpmattr		%attr(0755, rpm, rpm)

%files -f %{name}.lang
%defattr(-,root,root)
%doc RPM-PGP-KEY RPM-GPG-KEY GROUPS CHANGES doc/manual/[a-z]*
%attr(0755, rpm, rpm) /bin/rpm
%attr(0755, rpm, rpm) %{_bindir}/rpm2cpio
%attr(0755, rpm, rpm) %{_bindir}/gendiff
%attr(0755, rpm, rpm) %{_bindir}/rpmdb
%attr(0755, rpm, rpm) %{_bindir}/rpm[eiukqv]
%attr(0755, rpm, rpm) %{_bindir}/rpmsign
%attr(0755, rpm, rpm) %{_bindir}/rpmquery
%attr(0755, rpm, rpm) %{_bindir}/rpmverify
%{_sbindir}/update-alternatives

%{_libdir}/librpm-%{rpmversion}.so
%{_libdir}/librpmdb-%{rpmversion}.so
%{_libdir}/librpmio-%{rpmversion}.so
%{_libdir}/librpmbuild-%{rpmversion}.so

%dir /var/lib/rpm/alternatives/
%dir /etc/alternatives
%dir %{rpmdir}
/etc/rpm
%attr(0755, rpm, rpm) %{rpmdir}/config.guess
%attr(0755, rpm, rpm) %{rpmdir}/config.sub
%attr(0755, rpm, rpm) %{rpmdir}/convertrpmrc.sh
%attr(0644, rpm, rpm) %{rpmdir}/macros
%attr(0755, rpm, rpm) %{rpmdir}/mkinstalldirs
%attr(0755, rpm, rpm) %{rpmdir}/rpm.*
%attr(0755, rpm, rpm) %{rpmdir}/rpm[deiukqv]
%attr(0644, rpm, rpm) %{rpmdir}/rpmpopt*
%attr(0644, rpm, rpm) %{rpmdir}/rpmrc
%rpmattr	%{_prefix}/lib/rpm/rpm2cpio.sh
%rpmattr	%{_prefix}/lib/rpm/tgpg

%ifarch i386 i486 i586 i686 k6 athlon
%attr(   -, rpm, rpm) %{rpmdir}/i*86-*
%attr(   -, rpm, rpm) %{rpmdir}/k6*
%attr(   -, rpm, rpm) %{rpmdir}/athlon*
%endif
%ifarch alpha
%attr(   -, rpm, rpm) %{rpmdir}/alpha*
%endif
%ifarch sparc sparc64
%attr(   -, rpm, rpm) %{rpmdir}/sparc*
%endif
%ifarch ppc powerpc
%attr(   -, rpm, rpm) %{rpmdir}/ppc-*
%attr(   -, rpm, rpm) %{rpmdir}/ppc64-*
%attr(   -, rpm, rpm) %{rpmdir}/powerpc-*
%endif
%ifarch ia64
%attr(   -, rpm, rpm) %{rpmdir}/ia64-*
%endif
%ifarch x86_64
%attr(   -, rpm, rpm) %{rpmdir}/amd64-*
%attr(   -, rpm, rpm) %{rpmdir}/x86_64-*
%endif
%attr(   -, rpm, rpm) %{rpmdir}/noarch*

%{_prefix}/src/RPM/RPMS/*
%{_datadir}/man/man[18]/*.[18]*
%lang(pl) %{_datadir}/man/pl/man[18]/*.[18]*
%lang(ru) %{_datadir}/man/ru/man[18]/*.[18]*
%lang(ja) %{_datadir}/man/ja/man[18]/*.[18]*
%lang(sk) %{_datadir}/man/sk/man[18]/*.[18]*
%lang(fr) %{_datadir}/man/fr/man[18]/*.[18]*
%lang(ko) %{_datadir}/man/ko/man[18]/*.[18]*

%config(noreplace,missingok)	/etc/cron.daily/rpm
%config(noreplace,missingok)	/etc/logrotate.d/rpm

%attr(0755, rpm, rpm)	%dir /var/lib/rpm

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
%rpmattr	%{_bindir}/rpmbuild
%rpmattr	%{_prefix}/lib/rpm/brp-*
%rpmattr	%{_prefix}/lib/rpm/check-files
%rpmattr	%{_prefix}/lib/rpm/check-prereqs
#%rpmattr	%{_prefix}/lib/rpm/config.site
#%rpmattr	%{_prefix}/lib/rpm/cross-build
%rpmattr	%{_prefix}/lib/rpm/filter.sh
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

%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*

%{_datadir}/emacs/site-lisp/*
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*

%files python
%defattr(-,root,root)
%{_libdir}/python*/site-packages/rpmdb
%{_libdir}/python*/site-packages/rpmmodule.so

%files devel
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
%rpmattr	%{_prefix}/lib/rpm/rpmcache
%rpmattr	%{_prefix}/lib/rpm/rpmdb_deadlock
%rpmattr	%{_prefix}/lib/rpm/rpmdb_dump
%rpmattr	%{_prefix}/lib/rpm/rpmdb_load
%rpmattr	%{_prefix}/lib/rpm/rpmdb_loadcvt
%rpmattr	%{_prefix}/lib/rpm/rpmdb_svc
%rpmattr	%{_prefix}/lib/rpm/rpmdb_stat
%rpmattr	%{_prefix}/lib/rpm/rpmdb_verify
%rpmattr	%{_prefix}/lib/rpm/rpmfile
%rpmattr	%{_bindir}/rpmgraph

%files -n popt -f popt.lang
%defattr(-,root,root)
/%{_lib}/libpopt.so.*
%{_libdir}/libpopt.so.*

%files -n popt-devel
%defattr(-,root,root)
%{_libdir}/libpopt.a
%{_libdir}/libpopt.la
%{_libdir}/libpopt.so
%{_includedir}/popt.h

%changelog
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
  found in $RPM_BUILD_ROOT and not referenced in %files section.
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
- pass %%buildroot to find-requires (patch34). This allow to calculate
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
- corrected %%_sysconfdir macro.

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
- Add PREFIX=$RPM_BUILD_ROOT/%%{prefix} to %%makeinstall.
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
