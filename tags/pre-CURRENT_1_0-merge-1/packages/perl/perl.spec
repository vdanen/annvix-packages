%define threading 1

%if %threading
%define thread_arch -thread-multi
%else
%define thread_arch %{nil}
%endif

%define arch %(echo %{_arch} | sed -e "s/amd64/x86_64/")
%define full_arch %{arch}-%{_os}%{thread_arch}
# Don't change to %{_libdir} as perl is clean and has arch-dependent subdirs
%define perl_root %{_prefix}/lib/perl5

Summary: The Perl programming language.
Summary(de): Die Perl-Programmiersprache
Name: perl
Version: 5.8.1
Release: 0.RC4.3mdk
%define rel -RC4
License: GPL or Artistic
Group: Development/Perl
Url: http://www.perl.com
Epoch: 2
# ftp://ftp.funet.fi/pub/languages/perl/snap/perl@17574.tbz
#ftp://ftp.funet.fi/pub/languages/perl/CPAN/src/perl-%{version}.tar.bz2
Source0: http://www.cpan.org/authors/id/J/JH/JHI/perl-5.8.1-RC4.tar.bz2
# taken from debian
Source1: perl-headers-wanted
Source2: perl-5.8.0-RC2-special-h2ph-not-failing-on-machine_ansi_header.patch.bz2
Source3: http://www.cpan.org/authors/id/J/JV/JV/Getopt-Long-2.33_02.tar.bz2
Patch3: perl-5.8.1-RC3-norootcheck.patch.bz2
Patch6: perl-5.8.0-RC2-fix-LD_RUN_PATH-for-MakeMaker.patch.bz2
Patch12: perl-5.8.1-RC3-automatic-migration-from--make-install-PREFIX--to--makeinstall_std.patch.bz2
Patch13: perl-5.8.1-RC3-FHS-compliant-installvendorman-dirs.patch.bz2
Patch14: perl-5.8.1-RC3-install-files-using-chmod-644.patch.bz2
Patch15: perl-5.8.1-RC4-lib64.patch.bz2
Patch16: perl-5.8.1-RC3-perldoc-use-nroff-compatibility-option.patch.bz2
Patch20: perl-5.8.0-use_gzip_layer.patch.bz2
#(peroyvind) use -fPIC in stead of -fpic or else compile will fail on sparc (taken from redhat)
Patch21: perl-5.8.1-RC4-fpic-fPIC.patch.bz2
Patch22: perl-5.8.0-amd64.patch.bz2

Packager: Pixel <pixel@mandrakesoft.com>
Buildroot: %{_tmppath}/%{name}
Requires: perl-base = %{epoch}:%{version}-%{release}
Requires: %{name}-base
Provides: libperl.so
Provides: perl(getopts.pl)
Provides: perl(ctime.pl)
Provides: perl(flush.pl)
Provides: perl(find.pl)

Provides:  perl-MIME-Base64 perl-libnet perl-Storable perl-Digest-MD5 perl-Time-HiRes perl-Locale-Codes perl-Test-Simple perl-Time-HiRes
Obsoletes: perl-MIME-Base64 perl-libnet perl-Storable perl-Digest-MD5 perl-Time-HiRes perl-Locale-Codes perl-Test-Simple perl-Time-HiRes
Conflicts: perl-Parse-RecDescent < 1.80-6mdk
Conflicts: perl-Filter < 1.28-6mdk
Conflicts: apache-mod_perl <= 1.3.24_1.26-1mdk
%define _requires_exceptions Mac\\|VMS\\|perl >=\\|perl(Errno)\\|perl(Fcntl)\\|perl(IO)\\|perl(IO::File)\\|perl(IO::Socket::INET)\\|perl(IO::Socket::UNIX)\\|perl(Tk)\\|perl(Tk::Pod)


# for NDBM
BuildRequires: db1-devel 
BuildRequires: db2-devel 
BuildRequires: gdbm-devel

BuildRequires: man


%package base
Version: %{version}
Summary: The Perl programming language (base).
Provides: perl(v5.6.0)
Group: Development/Perl
Url: http://www.perl.com

%package devel
Version: %{version}
Summary: The Perl programming language (devel).
Group: Development/Perl
Url: http://www.perl.com
Requires: %{name} = %{epoch}:%{version}-%{release}

%package doc
Version: %{version}
Summary: The Perl programming language (documentation).
Group: Development/Perl
Url: http://www.perl.com
Requires: %{name} = %{epoch}:%{version}-%{release}

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

%description base
This is the base package for %{name}.

%description devel
This is the devel package for %{name}.

%description doc
This is the documentation package for %{name}.

%prep
%setup -q -n %{name}-%{version}%{rel} -a 3
%patch3 -p1
%patch6 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch20 -p1 -b .fpons
%patch21 -p1 -b .peroyvind
%patch22 -p1 -b .amd64

(cd lib/Getopt ; rm -f Long.pm ; mv ../../Getopt-Long-*/lib/Getopt/Long.pm .)
(cd lib/Getopt/Long ; rm -rf * ; mv ../../../Getopt-Long-*/{t,CHANGES,README} .)

%build
sh Configure -des \
  -Dinc_version_list="5.8.0/%{full_arch} 5.8.0 5.6.1 5.6.0" \
  -Darchname=%{arch}-%{_os} \
  -Dcc='%{__cc}' \
  -Doptimize="$RPM_OPT_FLAGS" \
  -Dprefix=%{_prefix} -Dvendorprefix=%{_prefix} -Dsiteprefix=%{_prefix} \
  -Dman3ext=3pm \
  -Dcf_by=MandrakeSoft -Dmyhostname=localhost -Dperladmin=root@localhost \
  -Dd_dosuid \
  -Ud_csh \
  -Duseshrplib \
%if %threading
  -Dusethreads \
%endif
%ifarch sparc
  -Ud_longdbl \
%endif
  
make

# for test, building a perl with no rpath
# for test, unset RPM_BUILD_ROOT so that the MakeMaker trick is not triggered
rm -f perl
RPM_BUILD_ROOT="" make test CCDLFLAGS= 
rm -f perl
make perl

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

install -d $RPM_BUILD_ROOT%{perl_root}/vendor_perl/%{version}/%{full_arch}/auto


# Delete CGI stuff, because CGI.pm is now a seperate package
find $RPM_BUILD_ROOT -name "CGI*" | xargs rm -rf

cp -f utils/h2ph utils/h2ph_patched
bzcat %{SOURCE2} | patch -p1

LD_LIBRARY_PATH=. ./perl -Ilib utils/h2ph_patched -a -d $RPM_BUILD_ROOT%{perl_root}/%{version}/%{full_arch} `cat %{SOURCE1}` > /dev/null

(
    # i don't like hardlinks, having symlinks instead:
    cd $RPM_BUILD_ROOT%{_bindir}
    ln -sf perl5 perl
    ln -s perl%{version} perl5
)

rm -f $RPM_BUILD_ROOT%{_bindir}/{perlivp,psed}

# call spec-helper before creating the file list
# (spec-helper removes some files, and compress some others)
s=/usr/share/spec-helper/spec-helper ; [ -x $s ] && $s

(
   cat > perl-base.list <<EOF
%{_bindir}/perl
%{_bindir}/perl5
%{_bindir}/perl%{version}
%attr(4711,root,root) %{_bindir}/sperl%{version}
%attr(4711,root,root) %{_bindir}/suidperl
%dir %{perl_root}
%dir %{perl_root}/%{version}
%dir %{perl_root}/%{version}/File
%{perl_root}/%{version}/File/Basename.pm
%{perl_root}/%{version}/File/Find.pm
%{perl_root}/%{version}/File/Path.pm
%{perl_root}/%{version}/File/Spec.pm
%dir %{perl_root}/%{version}/File/Spec
%{perl_root}/%{version}/File/Spec/Unix.pm
%dir %{perl_root}/%{version}/Time
%{perl_root}/%{version}/Time/Local.pm
%{perl_root}/%{version}/AutoLoader.pm
%{perl_root}/%{version}/Carp.pm
%{perl_root}/%{version}/DirHandle.pm
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
%{perl_root}/%{version}/unicore/To/Lower.pl
%{perl_root}/%{version}/unicore/To/Fold.pl
%{perl_root}/%{version}/unicore/To/Upper.pl
%{perl_root}/%{version}/unicore/lib/Word.pl
%{perl_root}/%{version}/unicore/lib/Digit.pl
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
%endif
%{perl_root}/%{version}/%{full_arch}/bits/syscall.ph
%{perl_root}/%{version}/%{full_arch}/sys/syscall.ph
%{perl_root}/%{version}/%{full_arch}/_h2ph_pre.ph
%{perl_root}/%{version}/%{full_arch}/syscall.ph
EOF

   cat > perl.list <<EOF
%doc README
%{_bindir}/a2p
%{_bindir}/perlbug
%{_bindir}/perldoc
%{_bindir}/find2perl
%{_bindir}/pod2man
%{_bindir}/pod2html
%{_bindir}/pod2text
%{_bindir}/pod2latex
%{_bindir}/splain
%{_bindir}/s2p
%{_mandir}/man3/*
EOF

   cat > perl-doc.list <<EOF
%{_bindir}/perldoc
%{_mandir}/man1/perldoc.1.bz2
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
%{_bindir}/libnetcfg
%{_bindir}/h2ph
%{_bindir}/pl2pm
%{_bindir}/podchecker
%{_bindir}/podselect
%{_bindir}/pod2usage
%{_bindir}/xsubpp
%{perl_root}/%{version}/Encode/encode.h
%{perl_root}/%{version}/%{full_arch}/auto/DynaLoader/DynaLoader.a
%{perl_root}/%{version}/%{full_arch}/CORE/EXTERN.h
%{perl_root}/%{version}/%{full_arch}/CORE/INTERN.h
%{perl_root}/%{version}/%{full_arch}/CORE/XSUB.h
%{perl_root}/%{version}/%{full_arch}/CORE/av.h
%{perl_root}/%{version}/%{full_arch}/CORE/cc_runtime.h
%{perl_root}/%{version}/%{full_arch}/CORE/config.h
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
%{perl_root}/%{version}/%{full_arch}/CORE/perl.h
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
   (cd $RPM_BUILD_ROOT ; find $rel_perl_root/%{version} "(" -name "*.pod" -o -iname "Changes*" -o -iname "README*" ")" -printf "%%%%doc /%%p\n") >> perl-doc.list
   (cd $RPM_BUILD_ROOT ; find $rel_mandir/man1          ! -type d -printf "/%%p\n") >> perl.list
   (cd $RPM_BUILD_ROOT ; find $rel_perl_root/%{version} ! -type d -printf "/%%p\n") >> perl.list
   (cd $RPM_BUILD_ROOT ; find $rel_perl_root/%{version} -type d -printf "%%%%dir /%%p\n") >> perl.list
   perl -ni -e 'BEGIN { open F, "perl-base.list"; $s{$_} = 1 foreach <F>; } print unless $s{$_}' perl.list
   perl -ni -e 'BEGIN { open F, "perl-devel.list"; $s{$_} = 1 foreach <F>; } print unless $s{$_}' perl.list
   perl -ni -e 'BEGIN { open F, "perl-doc.list"; !/perldiag/ and m|(/.*\n)| and $s{$1} = 1 foreach <F>; } print unless $s{$_}' perl.list
)

%clean
rm -rf $RPM_BUILD_ROOT

%files -f perl.list
%defattr(-,root,root)

%files base -f perl-base.list
%defattr(-,root,root)
%{perl_root}/vendor_perl

%files devel -f perl-devel.list
%defattr(-,root,root)

%files doc -f perl-doc.list
%defattr(-,root,root)

%changelog
* Mon Sep  1 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.8.1-0.RC4.3mdk
- perl-base shall have asm/break.ph on ia64

* Tue Aug 19 2003 Pixel <pixel@mandrakesoft.com> 5.8.1-0.RC4.2mdk
- add directories /usr/lib/perl5/vendor_perl down to /usr/lib/perl5/vendor_perl/5.8.1/i386-linux-thread-multi/auto in perl-base

* Sun Aug  3 2003 Pixel <pixel@mandrakesoft.com> 5.8.1-0.RC4.1mdk
- new release

* Fri Aug  1 2003 Pixel <pixel@mandrakesoft.com> 5.8.1-0.RC3.3mdk
- special case for "perl Makefile.PL PREFIX=..." which works correctly without using DESTDIR:
  do not set DESTDIR and let perl do what it does by default (which is ok),
  only warns the user that the DESTDIR way is better/simpler

* Fri Aug  1 2003 Pixel <pixel@mandrakesoft.com> 5.8.1-0.RC3.2mdk
- patch MakeMaker to automatically set DESTDIR to $RPM_BUILD_ROOT in perl modules,
  but warn that the correct way is now "%makeinstall_std" instead of "make PREFIX=$RPM_BUILD_ROOT/usr install"
- use %%makeinstall_std

* Thu Jul 31 2003 Pixel <pixel@mandrakesoft.com> 5.8.1-0.RC3.1mdk
- new release
- use DESTDIR for "make install" instead of using dirty tricks on Config.pm
- use inc_version_list to specify old perl module versions we want to be compatible with
  (5.8.0, 5.6.1, 5.6.0) instead of relying on perl auto detection 
  (which looks at the directories in /usr/lib/perl5/site_perl)

* Wed Jul 30 2003 Pixel <pixel@mandrakesoft.com> 5.8.0-31mdk
- Add epoch to Requires on perl-base and perl

* Wed Jul 30 2003 Pixel <pixel@mandrakesoft.com> 5.8.0-30mdk
- provides perl(find.pl) (for autoconf)

* Mon Jul 28 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.8.0-29mdk
- Patch22: Fix build in new AMD64 environment

* Wed Jul 16 2003 Pixel <pixel@mandrakesoft.com> 5.8.0-28mdk
- Getopt::Long 2.33 02

* Tue Jul 08 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.8.0-27mdk
- rebuild for devel deps

* Thu Jul  3 2003 Pixel <pixel@mandrakesoft.com> 5.8.0-26mdk
- remove the various requires perl >= 0.508 (esp. for perl-base)

* Thu Jun  5 2003 Pixel <pixel@mandrakesoft.com> 5.8.0-25mdk
- make it provide perl(flush.pl) (for kdeedu)

* Mon Jun 02 2003 Per �yvind Karlsen <peroyvind@sintrax.net> 5.8.0-24mdk
- fix compile problems on sparc related to the use of -fpic in stead of -fPIC (Patch21)

* Fri May 30 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 5.8.0-23mdk
- make it provide perl(ctime.pl)

* Thu May 22 2003 Pixel <pixel@mandrakesoft.com> 5.8.0-22mdk
- remove some bad automatic require: perl(Mac::BuildTools) perl(Mac::InternetConfig) perl(VMS::Filespec) perl(VMS::Stdio)

* Thu May 22 2003 Pixel <pixel@mandrakesoft.com> 5.8.0-21mdk
- add some Provides which are not automatically provided

* Tue May  6 2003 Pixel <pixel@mandrakesoft.com> 5.8.0-20mdk
- rebuild to have automatic Provides

* Thu Mar  6 2003 Pixel <pixel@mandrakesoft.com> 5.8.0-19mdk
- add Storable in perl-base for harddrake (only ->store and ->retrieve)

* Tue Feb 18 2003 Pixel <pixel@mandrakesoft.com> 5.8.0-18mdk
- add constant.pm
- add some unicore/* (same as the one in DrakX share/list)

* Thu Feb 13 2003 Pixel <pixel@mandrakesoft.com> 5.8.0-17mdk
- move PerlIO.pm to perl-base so that perl-PerlIO-gzip works with only perl-base

* Thu Feb 13 2003 Fran�ois Pons <fpons@mandrakesoft.com> 5.8.0-16mdk
- use :gzip layer for perl module (patch20)
- fix build with new stddef.h (pixel)

* Sun Nov 24 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-15mdk
- move perldoc manpage to perl-doc (thanks to G�tz Waschk)
- add a few missing binaries

* Sun Oct  6 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.8.0-14mdk
- perl_root is back to %{_prefix}/lib/perl5
- perl-base shall have biarch asm/unistd.ph headers too

* Fri Sep  6 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-13mdk
- perldiag.pod is used when "use diagnostics", so move it back from perl-doc

* Wed Sep  4 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-12mdk
- really have pod doc files in perl-doc

* Tue Sep  3 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-11mdk
- obsolete and provide perl-Time-HiRes

* Fri Aug 30 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-10mdk
- perldoc: use nroff compatibility option

* Mon Aug 26 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-9mdk
- obsolete and provide perl-Test-Simple (thanks to Guillaume Rousse)

* Wed Aug 21 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-8mdk
- fix duplicated files in perl/perl-base and perl/perl-devel

* Tue Aug 13 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.8.0-7mdk
- Automated rebuild with gcc 3.2-0.3mdk

* Fri Aug  2 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-6mdk
- enable threading 
  (rationale: as Jarkko Hietaniemi told me, debian and redhat have it)

* Thu Aug  1 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-5mdk
- Provides & Obsoletes perl-Locale-Codes

* Mon Jul 22 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.8.0-4mdk
- Make test everywhere, that looks 64-bit aware now
- Factorize references of perl root directory with %%perl_root macro

* Mon Jul 22 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-3mdk
- really move utf8.pm and utf8_heavy to perl-base :-(

* Sat Jul 20 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-2mdk
- move some more files in perl-base
  - base.pm (needed by Cwd.pm)
  - File/Spec.pm & File/Spec/Unix.pm (needed by File::Find)
  - utf8.pm & utf8_heavy.pl (needed by s///)

* Fri Jul 19 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-1mdk
- 5.8.0 !!
- move dprofpp to perl-devel (man pages should be there too...)
- add "BuildRequires: man"

* Thu Jul 18 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 5.8.0-0.17574.2mdk
- add missing dprofpp (only man page was there)

* Tue Jul 16 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-0.17574.1mdk
- new snapshot
- patch to have man pages installed in the right place (installsiteman1dir & installsiteman3dir)

* Mon Jul 15 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-0.17527.RC3.1mdk
- new release
- fix "make test" using the installed libperl.so due to rpath
- replace %%{make} with simple make (otherwise doesn't always build properly)

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-0.17412.5mdk
- add explictly a "Provides: libperl.so"
- rebuild with new rpm to get rid of "Requires: perl >= 5.800"

* Wed Jul 10 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-0.17412.4mdk
- add bytes.pm in perl-base (it is needed by Data::Dumper)

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-0.17412.3mdk
- ExtUtils::MakeMaker: use chmod 644 for installing files (esp. for building perl-PDL)
- use "Epoch: 2" to have the same as redhat
- Conflicts: perl-Filter < 1.28-6mdk

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-0.17412.2mdk
- ensure CGI::* man pages are not in "perl" package (they are in perl-CGI)
- add Obsoletes + Provides perl-MIME-Base64 perl-libnet perl-Storable perl-Digest-MD5 perl-Time-HiRes
- Conflict: perl-Parse-RecDescent < 1.80-6mdk 

* Tue Jul  9 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-0.17412.1mdk
- latest snapshot

* Tue Jun 25 2002 Pixel <pixel@mandrakesoft.com> 5.8.0-0.RC2.1mdk
- RC of 5.8.0 (breaks binary compatibility!)
- use "-Dinstallprefix" to enable clean&simple "make install"
- create new package "perl-doc" containing pod's
- cleanup the h2ph mess (switch from the redhat way to the debian way)
- perl modules now go to /usr/lib/perl5/vendor_perl instead of /usr/lib/perl5/site_perl
  (! need the use of "perl Makefile.PL INSTALLDIRS=vendor" !)
- man3 manpages goes to /usr/share/man/man3pm
- dropped many now-unneeded patches
- in MakeMaker:
    have "INSTALLBIN = $(PREFIX)/bin" instead of "INSTALLBIN = /usr/bin" in generated Makefile
    (and do the same for INSTALLSITELIB, INSTALLARCHLIB...)
    this allows to build with PREFIX=/usr, then "make install PREFIX=$RPM_BUILD_ROOT/usr"
    (this feature has been concensiously dropped since version 5.91_01, cf ExtUtils/Changes)

* Wed May 15 2002 Pixel <pixel@mandrakesoft.com> 5.601-14mdk
- add Conflicts: apache-mod_perl <= 1.3.24_1.26-1mdk
  (since mod_perl must be recompiled for uselargefiles)

* Sun May 12 2002 Pixel <pixel@mandrakesoft.com> 5.601-13mdk
- remove -Uuselargefiles (beware binary incompatibility, esp. apache...)

* Wed May  8 2002 Pixel <pixel@mandrakesoft.com> 5.601-12mdk
- adapt-to-new-gcc-_-A_-preprocessor-option

* Mon May 06 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.601-11mdk
- Automated rebuild in gcc3.1 environment

* Fri Apr 26 2002 Pixel <pixel@mandrakesoft.com> 5.601-10mdk
- back-port from perl-5.7.3 Cwd::getcwd which handle unreadable root directory

* Wed Apr 17 2002 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 5.601-9mdk
- Fix build with gcc-3.1:
  - Patch12: Don't add /usr/local/include et al. to the include path (RH patch)
  - Patch13: Strip out <built-in> and <command line> from preprocessed output

* Mon Mar 25 2002 Fran�ois Pons <fpons@mandrakesoft.com> 5.601-8mdk
- build release.

* Sun Oct 14 2001 Stefan van der Eijk <stefan@eijk.nu> 5.601-7mdk
- BuildRequires: db1-devel gdbm-devel

* Sun Sep  9 2001 Pixel <pixel@mandrakesoft.com> 5.601-6mdk
- add Data::Dumper in perl-base
- skip-syslog-tests-which-need-root-privilege.patch

* Wed Aug 15 2001 Pixel <pixel@mandrakesoft.com> 5.601-5mdk
- add syscall.ph and the dependency (needed for perl-MDK-Common)

* Thu Jun 14 2001 Pixel <pixel@mandrakesoft.com> 5.601-4mdk
- perl-5.6.1-fix-h2ph-and-xxxL-like-numbers.patch.bz2

* Wed Jun 13 2001 Pixel <pixel@mandrakesoft.com> 5.601-3mdk
- for now, add provides 'perl(getopts.pl)' and 'perl(v5.6.0)'

* Wed Jun 13 2001 Pixel <pixel@mandrakesoft.com> 5.601-2mdk
- rebuild with new rpm

* Mon Apr  9 2001 Pixel <pixel@mandrakesoft.com> 5.601-1mdk
- new version

* Wed Apr 04 2001 Francis Galiegue <fg@mandrakesoft.com> 5.600-30mdk
- Don't run make test on ia64

* Thu Mar 22 2001 Pixel <pixel@mandrakesoft.com> 5.600-29mdk
- add Exporter and some POSIX stuff in perl-base (needed for perl-gettext)

* Sat Mar  3 2001 Pixel <pixel@mandrakesoft.com> 5.600-28mdk
- Alexander Skwar: Removed CGI.pm from package - newer version is in a seperate package now!

* Wed Jan 31 2001 Pixel <pixel@mandrakesoft.com> 5.600-27mdk
- perl depends perl-base = version-release and not only version
- same for perl-devel

* Tue Jan 30 2001 Pixel <pixel@mandrakesoft.com> 5.600-26mdk
- add podselect and podchecker in perl-devel

* Mon Jan 22 2001 Pixel <pixel@mandrakesoft.com> 5.600-25mdk
- re-add "make test" (why did it go away?)
- build with GDBM, NDBM (small merge with RH's spec)

* Sat Dec 16 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 5.600-24mdk
- Fix typo in Syslog.pm.

* Fri Dec 15 2000 Pixel <pixel@mandrakesoft.com> 5.600-23mdk
- patch perl-5.6.0-use-LD_PRELOAD-for-libperl.so.patch.bz2 added
- patch perl-5.6.0-fix-for-coredump-bug-20000607.003.patch.bz2 added

* Thu Dec  7 2000 Pixel <pixel@mandrakesoft.com> 5.600-22mdk
- add "make test"

* Mon Nov 27 2000 Pixel <pixel@mandrakesoft.com> 5.600-21mdk
- corrected copyright

* Tue Nov  7 2000 Pixel <pixel@mandrakesoft.com> 5.600-20mdk
- add /usr/X11R6/lib to MakeMaker skipped rpath

* Sun Nov  5 2000 Pixel <pixel@mandrakesoft.com> 5.600-19mdk
- fix-errno_h-parsing-for-glibc-2.1.95.patch.bz2

* Thu Nov  2 2000 Pixel <pixel@mandrakesoft.com> 5.600-18mdk
- rebuild with new glibc so that i can build eperl (libposix doesn't exist
anymore)

* Sun Sep  3 2000 Pixel <pixel@mandrakesoft.com> 5.600-17mdk
- also move warnings/register.pm
- fix silly error

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 5.600-16mdk
- move Glob.pm and dependencies to perl-base

* Sat Sep  2 2000 Pixel <pixel@mandrakesoft.com> 5.600-15mdk
- fix filelist cleaning

* Wed Aug 23 2000 Pixel <pixel@mandrakesoft.com> 5.600-14mdk
- add Packager

* Tue Aug 22 2000 Pixel <pixel@mandrakesoft.com> 5.600-13mdk
- move dir .../CORE to perl-base
- move lib.pm to perl-base (to make installkernel happy)

* Fri Aug 18 2000 Pixel <pixel@mandrakesoft.com> 5.600-12mdk
- fix-LD_RUN_PATH-for-MakeMaker

* Mon Aug  7 2000 Pixel <pixel@mandrakesoft.com> 5.600-11mdk
- fix the mailx `!~' (in case you're using the old mailx or a bug appears in
mailx...)

* Tue Jul 25 2000 Pixel <pixel@mandrakesoft.com> 5.600-10mdk
- move DynaLoader.a to -devel
- remove menu

* Sat Jul 22 2000 Pixel <pixel@mandrakesoft.com> 5.600-9mdk
- patch CGI.pm to have $TempFile::TMPDIRECTORY = '/tmp'

* Fri Jul 21 2000 Pixel <pixel@mandrakesoft.com> 5.600-8mdk
- bad config.h

* Fri Jul 21 2000 Pixel <pixel@mandrakesoft.com> 5.600-7mdk
- oups, devel was bad :-(

* Wed Jul 19 2000 Pixel <pixel@mandrakesoft.com> 5.600-6mdk
- BM, macroization

* Fri May 19 2000 Fran�ois Pons <fpons@mandrakesoft.com> 5.600-5mdk
- changed asm/*.h to asm*/*.h during .ph generation for sparc.

* Fri Mar 31 2000 Pixel <pixel@mandrakesoft.com> 5.600-4mdk
- fix a bug causing missing .ph's

* Tue Mar 28 2000 Pixel <pixel@mandrakesoft.com> 5.600-3mdk
- really add menu

* Mon Mar 27 2000 Pixel <pixel@mandrakesoft.com> 5.600-2mdk
- add menu

* Thu Mar 23 2000 Pixel <pixel@mandrakesoft.com> 5.600-1mdk
- change version number for backward compatibility :(
(serial is not enough, cuz there are some requires >= 5.00503)

* Thu Mar 23 2000 Pixel <pixel@mandrakesoft.com> 5.6.0-1mdk
- new version

* Tue Mar 21 2000 Pixel <pixel@mandrakesoft.com> 5.6-0.3mdk
- RC3

* Thu Mar 16 2000 Pixel <pixel@mandrakesoft.com> 5.6-0.2mdk
- RC2

* Thu Mar  9 2000 Pixel <pixel@mandrakesoft.com> 5.6-0.1mdk
- new version

* Wed Mar  1 2000 Pixel <pixel@mandrakesoft.com> 5.5.670-1mdk
- new version

* Thu Feb 24 2000 Pixel <pixel@mandrakesoft.com> 5.5.660-1mdk
- remove the strip'ing and man page bzip'ing
- new version

* Wed Feb  9 2000 Pixel <pixel@mandrakesoft.com> 5.5.650-1mdk
- new version

* Thu Feb  3 2000 Pixel <pixel@mandrakesoft.com> 5.5.640-6mdk
- new version (and new version numbering)

* Mon Jan 17 2000 Fran�ois Pons <fpons@mandrakesoft.com>
- changed asm/*.h to asm*/*.h during .ph generation for sparc.

* Fri Dec 17 1999 Pixel <pixel@mandrakesoft.com>
- clean up
- fixed the reference to the egcs package

* Mon Nov 29 1999 Pixel <pixel@linux-mandrake.com>
- removed the `Provides: perl' in perl-base

* Mon Nov 22 1999 Stefan van der Eijk <s.vandereijk@chello.nl>
- changed i386 into ${RPM_ARCH}

* Mon Oct 25 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>
- Fix forget manpages from %files.

* Thu Oct 14 1999 Pixel <pixel@linux-mandrake.com>

- create hackperl based on perl's spec
- split in two packages
- removed csh dependencie
- merged redhat's spec (not everything)

* Mon Jul 12 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- ln /usr/lib/perl5 to /usr/lib/perl5%{current_version}
- bzip2 manpages.

* Tue Apr 13 1999 Chmouel Boudjnah <chmouel@mandrakesoft.com>

- Add patch from RedHat6.0.
- Update to 5.005_03

* Sat Apr 10 1999 Bernhard Rosenkraenzer <bero@linux-mandrake.com>
- Mandrake adaptions
- bzip2 man/info pages
- handle RPM_OPT_FLAGS
- add de locale

* Thu Jan 07 1999 Cristian Gafton <gafton@redhat.com>
- guilty of the inlined Makefile in the spec file
- adapted for the arm build

* Wed Sep 09 1998 Preston Brown <pbrown@redhat.com>
- added newer CGI.pm to the build
- changed the version naming scheme around to work with RPM

* Sun Jul 19 1998 Jeff Johnson <jbj@redhat.com>
- attempt to generate *.ph files reproducibly

* Mon Jun 15 1998 Jeff Johnson <jbj@redhat.com>
- update to 5.004_04-m4 (pre-5.005 maintenance release)

* Tue Jun 12 1998 Christopher McCrory <chrismcc@netus.com
- need stdarg.h from gcc shadow to fix "use Sys::Syslog" (problem #635)

* Fri May 08 1998 Cristian Gafton <gafton@redhat.com>
- added a patch to correct the .ph constructs unless defined (foo) to read
  unless(defined(foo))

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Mar 10 1998 Cristian Gafton <gafton@redhat.com>
- fixed strftime problem

* Sun Mar 08 1998 Cristian Gafton <gafton@redhat.com>
- added a patch to fix a security race
- do not use setres[ug]id - those are not implemented on 2.0.3x kernels

* Mon Mar 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 5.004_04 - 5.004_01 had some nasty memory leaks.
- fixed the spec file to be version-independent

* Fri Dec 05 1997 Erik Troan <ewt@redhat.com>
- Config.pm wasn't right do to the builtrooting

* Mon Oct 20 1997 Erik Troan <ewt@redhat.com>
- fixed arch-specfic part of spec file

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- updated to perl 5.004_01
- users a build root

* Thu Jun 12 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Tue Apr 22 1997 Erik Troan <ewt@redhat.com>
- Incorporated security patch from Chip Salzenberg <salzench@nielsenmedia.com>

* Fri Feb 07 1997 Erik Troan <ewt@redhat.com>
- Use -Darchname=i386-linux 
- Require csh (for glob)
- Use RPM_ARCH during configuration and installation for arch independence
