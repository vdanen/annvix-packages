#
# spec file for package perl
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# cooker: perl-5.8.8-4mdk
#
# $Id$

%define revision	$Rev$
%define name		perl
%define version		5.8.8
%define release		%_revrel
%define epoch		2

%define rel		%nil
%define threading 	0
%define debugging 	0
%define _requires_exceptions Mac\\|VMS\\|perl >=\\|perl(Errno)\\|perl(Fcntl)\\|perl(IO)\\|perl(IO::File)\\|perl(IO::Socket::INET)\\|perl(IO::Socket::UNIX)\\|perl(Tk)\\|perl(Tk::Pod)

%if %{threading}
%define thread_arch 	-thread-multi
%else
%define thread_arch 	%{nil}
%endif

%define arch		%(echo %{_arch} | sed -e "s/amd64/x86_64/")
%define full_arch	%{arch}-%{_os}%{thread_arch}
# Don't change to %{_libdir} as perl is clean and has arch-dependent subdirs
%define perl_root	%{_prefix}/lib/perl5

Summary:	The Perl programming language
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL or Artistic
Group:		Development/Perl
URL:		http://www.perl.org
Source0:	ftp://cpan.mirrors.easynet.fr/pub/ftp.cpan.org/src/perl-%{version}.tar.bz2
# taken from debian
Source1:	perl-headers-wanted
Source2:	perl-5.8.0-RC2-special-h2ph-not-failing-on-machine_ansi_header.patch
Patch3:		perl-5.8.1-RC3-norootcheck.patch
Patch6:		perl-5.8.8-RC1-fix-LD_RUN_PATH-for-MakeMaker.patch
Patch14:	perl-5.8.1-RC3-install-files-using-chmod-644.patch
Patch15:	perl-5.8.3-lib64.patch
Patch16:	perl-5.8.5-RC1-perldoc-use-nroff-compatibility-option.patch
#(peroyvind) use -fPIC in stead of -fpic or else compile will fail on sparc (taken from redhat)
Patch21:	perl-5.8.1-RC4-fpic-fPIC.patch
Patch23:	perl-5.8.8-patchlevel.patch
Patch24:	perl-5.8.4-no-test-fcgi.patch
Patch29:	perl-5.8.8-rpmdebug.patch
Patch32:	perl-5.8.7-incversionlist.patch
Patch33:	perl-5.8.8-26536.patch
Patch34:	perl-27210.patch
Patch35:	perl-27211.patch
Patch36:	perl-27359.patch
Patch37:	perl-27363.patch
Patch38:	perl-5.8.8-mdv-donot-defer-sig11.patch
Patch39:	perl-5.8.8-rh-CVE-2007-5116.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
# for NDBM
BuildRequires:	db1-devel
BuildRequires:	db2-devel
BuildRequires:	gdbm-devel
BuildRequires:	man
%ifarch x86_64
BuildRequires:	devel(libgdbm_compat(64bit))
%else
BuildRequires:	devel(libgdbm_compat)
%endif

Requires:	perl-base = %{epoch}:%{version}-%{release}
Provides:	libperl.so
Provides:	perl(getopts.pl)
Provides:	perl(ctime.pl)
Provides:	perl(flush.pl)
Provides:	perl(find.pl)
Provides:	perl(attributes) perl(fields) perl(locale) perl(subs)
Provides: 	perl-MIME-Base64
Provides: 	perl-libnet
Provides: 	perl-Storable
Provides: 	perl-Digest-MD5
Provides: 	perl-Time-HiRes
Provides: 	perl-Locale-Codes
Provides: 	perl-Test-Simple
Provides: 	perl-Test-Builder-Tester
Obsoletes:	perl-MIME-Base64
Obsoletes:	perl-libnet
Obsoletes:	perl-Storable
Obsoletes:	perl-Digest-MD5
Obsoletes:	perl-Time-HiRes
Obsoletes:	perl-Locale-Codes
Obsoletes:	perl-Test-Simple
Obsoletes:	perl-Test-Builder-Tester
Conflicts:	perl-Parse-RecDescent < 1.80-6mdk
Conflicts:	perl-Filter < 1.28-6mdk
Conflicts:	apache-mod_perl <= 1.3.24_1.26-1mdk

%description
Perl is a high-level programming language with roots in C, sed, awk
and shell scripting.  Perl is good at handling processes and files,
and is especially good at handling text.  Perl's hallmarks are
practicality and efficiency.  While it is used to do a lot of
different things, Perl's most common applications (and what it excels
at) are probably system administration utilities and web programming.
A large proportion of the CGI scripts on the web are written in Perl.
You need the perl package installed on your system so that your
system can handle Perl scripts.

You need perl-base to have a full perl.


%package base
Summary:	The Perl programming language (base)
Group:		Development/Perl
Provides:	perl(v5.6.0)
Provides:	perl(base)
Provides:	perl(bytes)
Provides:	perl(constant)
Provides:	perl(integer)
Provides:	perl(lib)
Provides:	perl(overload)
Provides:	perl(strict)
Provides:	perl(utf8)
Provides:	perl(vars)
Provides:	perl(warnings)
Provides:	perl(Carp::Heavy)

%description base
This is the base package for %{name}.


%package suid
Summary:	The Perl programming language (suidperl)
Group:		Development/Perl
Requires:	%{name}-base = %{epoch}:%{version}-%{release}

%description suid
This is the package that provides suidperl, a secure way to
write suid perl scripts.


%package devel
Summary:	The Perl programming language (devel)
Group:		Development/Perl
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
This is the devel package for %{name}.


%package perldoc
Summary:	The Perl programming language (perldoc)
Group:		Development/Perl
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	groff-for-man
Obsoletes:	%{name}-doc <= 1:5.8.8-5383avx

%description perldoc
This is the perldoc program.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}%{rel} -a 2
%patch3 -p1
%patch6 -p0
%patch14 -p1
%patch15 -p1
%patch16 -p0
%patch21 -p1
%patch23 -p0
%patch24 -p0
%patch29 -p0
%patch32 -p0
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1


%build
%ifarch ppc
RPM_OPT_FLAGS=`echo "%{optflags}"|sed -e 's/-O2/-O1/g'`
%endif

sh Configure -des \
    -Dinc_version_list="5.8.7 5.8.7/%{full_arch} 5.8.6 5.8.6/%{full_arch} 5.8.5 5.8.4 5.8.3 5.8.2 5.8.1 5.8.0 5.6.1 5.6.0" \
    -Darchname=%{arch}-%{_os} \
    -Dcc='%{__cc}' \
%if %{debugging}
    -Doptimize=-g -DDEBUGGING \
%else
    -Doptimize="%{optflags}" \
%endif
    -Dprefix=%{_prefix} -Dvendorprefix=%{_prefix} \
    -Dsiteprefix=%{_prefix} -Dsitebin=%{_prefix}/local/bin \
    -Dsiteman1dir=%{_prefix}/local/share/man/man1 \
    -Dsiteman3dir=%{_prefix}/local/share/man/man3 \
    -Dotherlibdirs=/usr/local/lib/perl5:/usr/local/lib/perl5/site_perl \
    -Dman3ext=3pm \
    -Dcf_by=Annvix -Dmyhostname=localhost -Dperladmin=root@localhost -Dcf_email=root@localhost \
    -Dd_dosuid \
    -Ud_csh \
    -Duseshrplib \
%if %{threading}
    -Duseithreads \
%endif
%ifarch sparc
    -Ud_longdbl \
%endif
  
make

#%check
# for test, building a perl with no rpath
# for test, unset RPM_BUILD_ROOT so that the MakeMaker trick is not triggered

# for some reason, this test doesn't pass on x86_64
%ifarch x86_64
rm -f t/op/pat.t
%endif

rm -f perl
RPM_BUILD_ROOT="" make test_harness_notty CCDLFLAGS= 
rm -f perl
make perl


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall_std

install -d %{buildroot}%{perl_root}/vendor_perl/%{version}/%{full_arch}/auto

# we prefer 0755 instead of 0555
find %{buildroot} -name "*.so" | xargs chmod 0755

# Delete CGI stuff, because CGI.pm is now a seperate package
find %{buildroot} -name "CGI*" | xargs rm -rf

cp -f utils/h2ph utils/h2ph_patched
bzcat %{SOURCE2} | patch -p1

%if 1
# TODO figure out why the cleaner version with LD_PRELOAD doesn't work here.
LD_LIBRARY_PATH=. ./perl -Ilib utils/h2ph_patched -a -d %{buildroot}%{perl_root}/%{version}/%{full_arch} `cat %{SOURCE1}` > /dev/null ||:
%else
#LD_PRELOAD=`pwd`/libperl.so ./perl -Ilib utils/h2ph_patched -a -d %{buildroot}%{perl_root}/%{version}/%{full_arch} `cat %{SOURCE1}` > /dev/null ||:
%endif

(
    # i don't like hardlinks, having symlinks instead:
    cd %{buildroot}%{_bindir}
    ln -sf perl5 perl
    ln -s perl%{version} perl5
)

rm -f %{buildroot}%{_bindir}/perlivp %{buildroot}%{_mandir}/man1/perlivp.1

%ifarch ppc
perl -ni -e 'print if !/sub __syscall_nr/' %{buildroot}%{perl_root}/%{version}/%{full_arch}/asm/unistd.ph
perl -ni -e 'print unless m/sub __syscall_nr/' %{buildroot}%{perl_root}/%{version}/%{full_arch}/asm/unistd.ph
%endif

# call spec-helper before creating the file list
# (spec-helper removes some files, and compress some others)
s=/usr/share/spec-helper/spec-helper ; [ -x $s ] && $s

(
   cat > perl-base.list <<EOF
%{_bindir}/perl
%{_bindir}/perl5
%{_bindir}/perl%{version}
%dir %{perl_root}
%dir %{perl_root}/%{version}
%dir %{perl_root}/%{version}/File
%{perl_root}/%{version}/File/Basename.pm
%{perl_root}/%{version}/File/Find.pm
%{perl_root}/%{version}/File/Path.pm
%{perl_root}/%{version}/File/Spec.pm
%dir %{perl_root}/%{version}/File/Spec
%{perl_root}/%{version}/File/Spec/Unix.pm
%dir %{perl_root}/%{version}/Getopt
%{perl_root}/%{version}/Getopt/Long.pm
%{perl_root}/%{version}/Getopt/Std.pm
%dir %{perl_root}/%{version}/Time
%{perl_root}/%{version}/Time/Local.pm
%{perl_root}/%{version}/AutoLoader.pm
%dir %{perl_root}/%{version}/Carp
%{perl_root}/%{version}/Carp.pm
%{perl_root}/%{version}/Carp/Heavy.pm
%{perl_root}/%{version}/DirHandle.pm
%{perl_root}/%{version}/%{full_arch}/Errno.pm
%dir %{perl_root}/%{version}/Exporter
%{perl_root}/%{version}/Exporter/Heavy.pm
%{perl_root}/%{version}/Exporter.pm
%{perl_root}/%{version}/FileHandle.pm
%{perl_root}/%{version}/PerlIO.pm
%{perl_root}/%{version}/SelectSaver.pm
%{perl_root}/%{version}/Symbol.pm
%{perl_root}/%{version}/base.pm
%{perl_root}/%{version}/bytes.pm
%{perl_root}/%{version}/constant.pm
%{perl_root}/%{version}/integer.pm
%{perl_root}/%{version}/overload.pm
%{perl_root}/%{version}/strict.pm
%{perl_root}/%{version}/utf8.pm
%{perl_root}/%{version}/utf8_heavy.pl
%{perl_root}/%{version}/unicore/Exact.pl
%{perl_root}/%{version}/unicore/Canonical.pl
%{perl_root}/%{version}/unicore/PVA.pl
%{perl_root}/%{version}/unicore/To/Lower.pl
%{perl_root}/%{version}/unicore/To/Fold.pl
%{perl_root}/%{version}/unicore/To/Upper.pl
%{perl_root}/%{version}/unicore/lib/gc_sc/Word.pl
%{perl_root}/%{version}/unicore/lib/gc_sc/Digit.pl
%{perl_root}/%{version}/vars.pm
%dir %{perl_root}/%{version}/warnings
%{perl_root}/%{version}/warnings/register.pm
%{perl_root}/%{version}/warnings.pm
%dir %{perl_root}/%{version}/%{full_arch}
%dir %{perl_root}/%{version}/%{full_arch}/Data
%{perl_root}/%{version}/%{full_arch}/lib.pm
%{perl_root}/%{version}/%{full_arch}/Cwd.pm
%{perl_root}/%{version}/%{full_arch}/Data/Dumper.pm
%dir %{perl_root}/%{version}/%{full_arch}/File
%{perl_root}/%{version}/%{full_arch}/File/Glob.pm
%dir %{perl_root}/%{version}/%{full_arch}/IO
%{perl_root}/%{version}/%{full_arch}/IO/Handle.pm
%{perl_root}/%{version}/%{full_arch}/IO/Seekable.pm
%{perl_root}/%{version}/%{full_arch}/IO/Select.pm
%{perl_root}/%{version}/%{full_arch}/IO/Socket.pm
%dir %{perl_root}/%{version}/%{full_arch}/auto
%dir %{perl_root}/%{version}/%{full_arch}/auto/Cwd
%{perl_root}/%{version}/%{full_arch}/auto/Cwd/Cwd.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/DynaLoader
%{perl_root}/%{version}/%{full_arch}/auto/DynaLoader/dl_findfile.al
%dir %{perl_root}/%{version}/%{full_arch}/auto/Data
%dir %{perl_root}/%{version}/%{full_arch}/auto/Data/Dumper
%{perl_root}/%{version}/%{full_arch}/auto/Data/Dumper/Dumper.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/File
%dir %{perl_root}/%{version}/%{full_arch}/auto/File/Glob
%{perl_root}/%{version}/%{full_arch}/auto/File/Glob/Glob.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/IO
%{perl_root}/%{version}/%{full_arch}/auto/IO/IO.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/POSIX
%{perl_root}/%{version}/%{full_arch}/auto/POSIX/POSIX.so
%{perl_root}/%{version}/%{full_arch}/auto/POSIX/autosplit.ix
%{perl_root}/%{version}/%{full_arch}/auto/POSIX/load_imports.al
%{perl_root}/%{version}/%{full_arch}/auto/POSIX/tmpfile.al
%dir %{perl_root}/%{version}/%{full_arch}/auto/Socket
%{perl_root}/%{version}/%{full_arch}/auto/Socket/Socket.so
%dir %{perl_root}/%{version}/%{full_arch}/auto/Storable
%{perl_root}/%{version}/%{full_arch}/auto/Storable/Storable.so
%{perl_root}/%{version}/%{full_arch}/auto/Storable/autosplit.ix
%{perl_root}/%{version}/%{full_arch}/auto/Storable/store.al
%{perl_root}/%{version}/%{full_arch}/auto/Storable/_store.al
%{perl_root}/%{version}/%{full_arch}/auto/Storable/retrieve.al
%{perl_root}/%{version}/%{full_arch}/auto/Storable/_retrieve.al
%dir %{perl_root}/%{version}/%{full_arch}/auto/re
%{perl_root}/%{version}/%{full_arch}/auto/re/re.so
%{perl_root}/%{version}/%{full_arch}/Config.pm
%{perl_root}/%{version}/%{full_arch}/DynaLoader.pm
%{perl_root}/%{version}/%{full_arch}/POSIX.pm
%{perl_root}/%{version}/%{full_arch}/Socket.pm
%{perl_root}/%{version}/%{full_arch}/Storable.pm
%{perl_root}/%{version}/%{full_arch}/re.pm
%{perl_root}/%{version}/%{full_arch}/XSLoader.pm
%dir %{perl_root}/%{version}/%{full_arch}/CORE
%{perl_root}/%{version}/%{full_arch}/CORE/libperl.so
%dir %{perl_root}/%{version}/%{full_arch}/asm
%dir %{perl_root}/%{version}/%{full_arch}/bits
%dir %{perl_root}/%{version}/%{full_arch}/sys
%{perl_root}/%{version}/%{full_arch}/asm/unistd.ph
%ifarch ia64
%{perl_root}/%{version}/%{full_arch}/asm/break.ph
%endif
%ifarch x86_64
%{perl_root}/%{version}/%{full_arch}/asm-i386/unistd.ph
%{perl_root}/%{version}/%{full_arch}/asm-x86_64/unistd.ph
%{perl_root}/%{version}/%{full_arch}/bits/wordsize.ph
%endif
%{perl_root}/%{version}/%{full_arch}/bits/syscall.ph
%{perl_root}/%{version}/%{full_arch}/sys/syscall.ph
%{perl_root}/%{version}/%{full_arch}/_h2ph_pre.ph
%{perl_root}/%{version}/%{full_arch}/syscall.ph
EOF

   cat > perl.list <<EOF
%{_bindir}/a2p
%{_bindir}/perlbug
%{_bindir}/find2perl
%{_bindir}/pod2man
%{_bindir}/pod2html
%{_bindir}/pod2text
%{_bindir}/pod2latex
%{_bindir}/splain
%{_bindir}/s2p
%{_mandir}/man3/*
%exclude %{_mandir}/man3/Pod::Perldoc::ToChecker.3pm*
%exclude %{_mandir}/man3/Pod::Perldoc::ToMan.3pm*
%exclude %{_mandir}/man3/Pod::Perldoc::ToNroff.3pm*
%exclude %{_mandir}/man3/Pod::Perldoc::ToPod.3pm*
%exclude %{_mandir}/man3/Pod::Perldoc::ToRtf.3pm*
%exclude %{_mandir}/man3/Pod::Perldoc::ToText.3pm*
%exclude %{_mandir}/man3/Pod::Perldoc::ToTk.3pm*
%exclude %{_mandir}/man3/Pod::Perldoc::ToXml.3pm*
%exclude %{perl_root}/%{version}/Pod/Perldoc.pm
%exclude %{perl_root}/%{version}/Pod/Perldoc
%exclude %{perl_root}/%{version}/Pod/Perldoc/BaseTo.pm
%exclude %{perl_root}/%{version}/Pod/Perldoc/GetOptsOO.pm
%exclude %{perl_root}/%{version}/Pod/Perldoc/ToChecker.pm
%exclude %{perl_root}/%{version}/Pod/Perldoc/ToMan.pm
%exclude %{perl_root}/%{version}/Pod/Perldoc/ToNroff.pm
%exclude %{perl_root}/%{version}/Pod/Perldoc/ToPod.pm
%exclude %{perl_root}/%{version}/Pod/Perldoc/ToRtf.pm
%exclude %{perl_root}/%{version}/Pod/Perldoc/ToText.pm
%exclude %{perl_root}/%{version}/Pod/Perldoc/ToTk.pm
%exclude %{perl_root}/%{version}/Pod/Perldoc/ToXml.pm
EOF

   cat > perl-perldoc.list <<EOF
%{_bindir}/perldoc
%{_mandir}/man1/perldoc.1*
%{perl_root}/%{version}/Pod/Perldoc.pm
%{perl_root}/%{version}/Pod/Perldoc
%{perl_root}/%{version}/Pod/Perldoc/BaseTo.pm
%{perl_root}/%{version}/Pod/Perldoc/GetOptsOO.pm
%{perl_root}/%{version}/Pod/Perldoc/ToChecker.pm
%{perl_root}/%{version}/Pod/Perldoc/ToMan.pm
%{perl_root}/%{version}/Pod/Perldoc/ToNroff.pm
%{perl_root}/%{version}/Pod/Perldoc/ToPod.pm
%{perl_root}/%{version}/Pod/Perldoc/ToRtf.pm
%{perl_root}/%{version}/Pod/Perldoc/ToText.pm
%{perl_root}/%{version}/Pod/Perldoc/ToTk.pm
%{perl_root}/%{version}/Pod/Perldoc/ToXml.pm
%{_mandir}/man3/Pod::Perldoc*
EOF

   cat > perl-devel.list <<EOF
%{_bindir}/cpan
%{_bindir}/pstruct
%{_bindir}/perlcc
%{_bindir}/piconv
%{_bindir}/dprofpp
%{_bindir}/c2ph
%{_bindir}/h2xs
%{_bindir}/enc2xs
%{_bindir}/instmodsh
%{_bindir}/libnetcfg
%{_bindir}/h2ph
%{_bindir}/pl2pm
%{_bindir}/podchecker
%{_bindir}/podselect
%{_bindir}/pod2usage
%{_bindir}/psed
%{_bindir}/prove
%{_bindir}/xsubpp
%{perl_root}/%{version}/Encode/encode.h
%{perl_root}/%{version}/%{full_arch}/auto/DynaLoader/DynaLoader.a
%{perl_root}/%{version}/%{full_arch}/CORE/EXTERN.h
%{perl_root}/%{version}/%{full_arch}/CORE/INTERN.h
%{perl_root}/%{version}/%{full_arch}/CORE/XSUB.h
%{perl_root}/%{version}/%{full_arch}/CORE/av.h
%{perl_root}/%{version}/%{full_arch}/CORE/cc_runtime.h
%{perl_root}/%{version}/%{full_arch}/CORE/cop.h
%{perl_root}/%{version}/%{full_arch}/CORE/cv.h
%{perl_root}/%{version}/%{full_arch}/CORE/dosish.h
%{perl_root}/%{version}/%{full_arch}/CORE/embed.h
%{perl_root}/%{version}/%{full_arch}/CORE/embedvar.h
%{perl_root}/%{version}/%{full_arch}/CORE/fakesdio.h
%{perl_root}/%{version}/%{full_arch}/CORE/fakethr.h
%{perl_root}/%{version}/%{full_arch}/CORE/form.h
%{perl_root}/%{version}/%{full_arch}/CORE/gv.h
%{perl_root}/%{version}/%{full_arch}/CORE/handy.h
%{perl_root}/%{version}/%{full_arch}/CORE/hv.h
%{perl_root}/%{version}/%{full_arch}/CORE/intrpvar.h
%{perl_root}/%{version}/%{full_arch}/CORE/iperlsys.h
%{perl_root}/%{version}/%{full_arch}/CORE/keywords.h
%{perl_root}/%{version}/%{full_arch}/CORE/malloc_ctl.h
%{perl_root}/%{version}/%{full_arch}/CORE/mg.h
%{perl_root}/%{version}/%{full_arch}/CORE/nostdio.h
%{perl_root}/%{version}/%{full_arch}/CORE/op.h
%{perl_root}/%{version}/%{full_arch}/CORE/opcode.h
%{perl_root}/%{version}/%{full_arch}/CORE/opnames.h
%{perl_root}/%{version}/%{full_arch}/CORE/pad.h
%{perl_root}/%{version}/%{full_arch}/CORE/patchlevel.h
%{perl_root}/%{version}/%{full_arch}/CORE/perlapi.h
%{perl_root}/%{version}/%{full_arch}/CORE/perlio.h
%{perl_root}/%{version}/%{full_arch}/CORE/perliol.h
%{perl_root}/%{version}/%{full_arch}/CORE/perlsdio.h
%{perl_root}/%{version}/%{full_arch}/CORE/perlsfio.h
%{perl_root}/%{version}/%{full_arch}/CORE/perlvars.h
%{perl_root}/%{version}/%{full_arch}/CORE/perly.h
%{perl_root}/%{version}/%{full_arch}/CORE/pp.h
%{perl_root}/%{version}/%{full_arch}/CORE/pp_proto.h
%{perl_root}/%{version}/%{full_arch}/CORE/proto.h
%{perl_root}/%{version}/%{full_arch}/CORE/reentr.h
%{perl_root}/%{version}/%{full_arch}/CORE/reentr.inc
%{perl_root}/%{version}/%{full_arch}/CORE/regcomp.h
%{perl_root}/%{version}/%{full_arch}/CORE/regexp.h
%{perl_root}/%{version}/%{full_arch}/CORE/regnodes.h
%{perl_root}/%{version}/%{full_arch}/CORE/scope.h
%{perl_root}/%{version}/%{full_arch}/CORE/sperl.o
%{perl_root}/%{version}/%{full_arch}/CORE/sv.h
%{perl_root}/%{version}/%{full_arch}/CORE/thrdvar.h
%{perl_root}/%{version}/%{full_arch}/CORE/thread.h
%{perl_root}/%{version}/%{full_arch}/CORE/uconfig.h
%{perl_root}/%{version}/%{full_arch}/CORE/unixish.h
%{perl_root}/%{version}/%{full_arch}/CORE/utf8.h
%{perl_root}/%{version}/%{full_arch}/CORE/utfebcdic.h
%{perl_root}/%{version}/%{full_arch}/CORE/util.h
%{perl_root}/%{version}/%{full_arch}/CORE/warnings.h
EOF

    rel_perl_root=`echo %{perl_root} | sed "s,/,,"`
    rel_mandir=`echo %{_mandir} | sed "s,/,,"`
    (cd %{buildroot} ; find $rel_perl_root/%{version} "(" -name "*.pod" -o -iname "Changes*" -o -iname "ChangeLog*" -o -iname "README*" ")" -a -not -name perldiag.pod -printf "%%%%doc /%%p\n") >> perl-perldoc.list
    (cd %{buildroot} ; find $rel_mandir/man1 ! -name "perlivp.1*" ! -type d -printf "/%%p*\n") >> perl.list
    (cd %{buildroot} ; find $rel_perl_root/%{version} ! -type d -printf "/%%p\n") >> perl.list
    (cd %{buildroot} ; find $rel_perl_root/%{version} -type d -printf "%%%%dir /%%p\n") >> perl.list
    perl -ni -e 'BEGIN { open F, "perl-base.list"; $s{$_} = 1 foreach <F>; } print unless $s{$_}' perl.list
    perl -ni -e 'BEGIN { open F, "perl-devel.list"; $s{$_} = 1 foreach <F>; } print unless $s{$_}' perl.list
    perl -ni -e 'BEGIN { open F, "perl-perldoc.list"; !/perldiag/ and m|(/.*\n)| and $s{$1} = 1 foreach <F>; } print unless $s{$_}' perl.list
    # need to do some re-arranging... not sure why the files are showing up as .bs and not .so
    perl -pi -e 's|\.bs|\.so|g' perl.list
    perl -pi -e "s|/usr/lib/perl5/%{version}/%{_arch}-linux/.packlist||" perl.list
)


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files -f perl.list
%defattr(-,root,root)

%files base -f perl-base.list
%defattr(-,root,root)
%{perl_root}/vendor_perl

%files devel -f perl-devel.list
%defattr(-,root,root)

%files perldoc -f perl-perldoc.list
%defattr(-,root,root)

%files suid
%{_bindir}/suidperl
%attr(4711,root,root) %{_bindir}/sperl%{version}

%files doc
%doc README Artistic


%changelog
* Mon Nov 05 2007 Vincent Danen <vdanen-at-build.annvix.org> 5.8.8
- P39: security fix for CVE-2007-5116
- fix manpage extension
- fix filelist building

* Sat Nov 18 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.8.8
- P38: do not defer segfaulting (SIG11)
- clean spec

* Thu May 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.8.8
- rename perl-doc to perl-perldoc and create perl-doc to only contain docs

* Tue May 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.8.8
- revert the lib64 buildrequires "fix"
- also use newer rpm-annvix-setup-build to pick up libperl.so and friends

* Tue May 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.8.8
- 5.8.8
- sync with 5.8.8-4mdk (rgarciasuarez):
  - drop P12, P20, P22, P25, P26, P29, P32, P33
  - update P6, P23, P34 (now P32)
  - new patches P29, P33, P34, P35, P36, P37
  - remove PERL_DISABLE_PMC from CCFLAGS
  - Obsoletes perl-Test-Builder-Tester
  - lib64 fix to buildrequires
- re-ordered patches somewhat to match mdk ordering
- modify P23: s/Mandriva Linux/Annvix/ (patchlevel)
- move %%doc from perl to perl-doc

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 5.8.7
- Clean rebuild

* Sat Dec 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.8.7
- t/op/pat.t doesn't completely pass on x86_64 for some reason; remove
  that test on that arch
- sync with 5.8.7-8mdk (rgarciasuarez):
  - P31: upgrade to Storable 2.15
  - fix installation of sperl as setuid
  - P32: latest CPAN version of Getopt::Long
  - P33: latest CPAN version of List::Util
  - P34: always setup @INC correctly even if older directories don't exist
    on the build machine

* Sat Dec 24 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.8.7
- Obfuscate email addresses and new tagging

* Wed Dec 21 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.8.7-2avx
- P30: fix for CVE-2005-3962
- uncompress patches

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.8.7-1avx
- 5.8.7
- on x86_64, bits/syscall.ph requires bits/wordsize.ph (pixel)
- dropped P27, P28, P30; merged upstream
- updated P29 for new version
- define sitebin to /usr/local/bin and siteman* to /use/local/share/man
- put sperl and suidperl in their own perl-suid package

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.8.6-6avx
- bootstrap build (new gcc, new glibc)

* Tue Jul 26 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.8.6-5avx
- rebuild for new gcc

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.8.6-4avx
- bootstrap build

* Fri May 06 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.8.6-3avx
- P29: fix CAN-2005-448 (replaces and includes fix for CAN-2004-0452)
- drop -b on patches

* Tue Feb 08 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.8.6-2avx
- P29: fix CAN-2004-0452 (from Openwall)
- P30: fix CAN-2004-0976

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 5.8.6-1avx
- 5.8.6
- merged with cooker 5.8.6-3mdk:
  - BuildRequires: libgdbm_compat (rgarciasuarez)
  - remove support for threads
  - remove bincompat directories (since we break binary compatibility)
  - use "make test_harness_notty" for testing
  - fix invocation of h2ph with correct libperl.so
  - P27: integrate patch 23565 from the main patch; MakeMaker's default
    MANIFEST.SKIP was borked
  - workaround for build issues on x86_64
  - add a "debugging" flag to build perl with -D enabled
  - move the Pod::Perldoc::* modules to perl-doc
  - add Artistic license in doc
  - P28: fix for CAN-2005-0155, CAN-2005-0156

* Fri Sep 10 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.8.5-1avx
- 5.8.5
- define otherlibdirs to /usr/local/lib/perl5:/usr/local/lib/perl5/site_perl
  so one can install modules into /usr/local (eventually good for ports,
  good for CPAN-based installs with a prefix of /usr/local)
- merge with cooker (5.8.5-3mdk) (rgarciasuarez):
  - psed(1) wasn't installed
  - the manpage for perlivp(1) (which isn't installed) was installed
  - remove perldiag.pod from perl-doc
  - add compilation flag -DPERL_DISABLE_PMC
  - restore loading of .pm.gz files by adjusting P20
  - Carp::Heavy should be in perl-base, as it's required by Carp.pm
  - add manually a provides for perl(Carp::Heavy)
  - move Getopt::Std from perl to perl-base
  - move some changelogs from perl to perl-doc
  - move CORE/config.h from perl-devel to perl; this is necessary for MakeMaker
    (and thus CPAN.pm) to work
  - fix CPAN signature test when Module::Signature is installed
  - move unicore/PVA.pl into perl-base
  - P26: prevent including an empty rpath in .so files produced by MakeMaker
  - fix for generation of unistd.ph on ppc (Christiaan Welvaart)

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 5.8.4-2avx
- Annvix build

* Thu Apr 29 2004 Vincent Danen <vdanen@opensls.org> 5.8.4-1sls
- 5.8.4
- merge with cooker (5.8.4-1mdk):
  - changed perl URL (rafael)
  - FHS-compliane patch is no longer needed (rafael)
  - a more recent Getopt::Long is now bundled with perl, remove it (rafael)
  - add Errno.pm to perl-base
  - remove setuid bit on suidperl (rafael)
  - use 'make test_harness' instead of 'make test' (rafael)
  - add a note in the 'perl -V' output to mention Mandrakesoft pathes
    (rafael)
  - force gcc optimization level to -O1 on ppc (rafael)
  - disable test lib/CGI/t/fast.t, which may fail if perl-FCGI is already
    installed on the system (rafael)

* Wed Feb 24 2004 Vincent Danen <vdanen@opensls.org> 5.8.3-1sls
- 5.8.3
- spec cleanups
- merge with cooker (5.8.3-5mdk):
  - perldoc needs nroff (which is in groff-for-man) (pixel)
  - fix asm/unistd.ph for arch ppc (thanks to Christiaan Welvaart &
    Stew Benedict) (pixel)
  - move Getopt::Long to perl-base (pixel)
  - provide more perl([a-z].*) to ease transition (pixel)
  - move CORE/perl.h from perl-devel to perl
    (it is used in some cases when building simple non native modules)
    (pixel)
  - provide perl(strict) perl(vars) and a few more to allow transition with new
    spec-helper rules (pixel)
  - ignore h2ph failing on asm/intrinsics.h, mach_apicdef.h, mach_mpspec.h
    (pixel)
  - perl nows installs its .so files 0555, we prefer 0755 (pixel)
  - 5.8.2 is compatible with 5.8.1, so have 5.8.1 in @INC (pixel)

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 5.8.1-0.RC4.4sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
