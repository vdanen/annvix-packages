#
# spec file for package bash
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		bash
%define version		3.2
%define release		%_revrel

%define i18ndate 	20010626

%define build_dietlibc	0

Summary:	The GNU Bourne Again shell (bash)
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Shells
License:	GPL
URL:		http://www.gnu.org/software/bash/bash.html

Source0:	ftp://ftp.gnu.org/pub/gnu/bash/bash-%{version}.tar.bz2
Source1:	ftp://ftp.gnu.org/pub/gnu/bash/bash-doc-%{version}.tar.bz2
Source2:	dot-bashrc
Source3:	dot-bash_profile
Source4:	dot-bash_logout
Source5:	alias.sh
Source6:	bashrc
Patch0:		bash-2.02-security.patch
Patch1:		bash-2.03-profile.patch
Patch2:		bash-2.04-compat.patch
Patch4:		bash-2.05b-dietlibc.patch
Patch5:		bash-2.05b-builtins.patch
Patch6:		bash-2.05b-disable-nontrivial-matches.patch
Patch7:		bash-strcoll-bug.diff
Patch8:		bash-2.05b-checkwinsize.patch
Patch9:		bash-3.1-extended_quote.patch
# upstream bugfixes
Patch20:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-001
Patch21:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-002
Patch22:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-003
Patch23:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-004
Patch24:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-005
Patch25:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-006
Patch26:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-007
Patch27:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-008
Patch28:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-009
Patch29:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-010
Patch30:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-011
Patch31:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-012
Patch32:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-013
Patch33:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-014
Patch34:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-015
Patch35:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-016
Patch36:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-017
Patch37:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-018
Patch38:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-019
Patch39:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-020
Patch40:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-021
Patch41:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-022
Patch42:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-023
Patch43:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-024
Patch44:	ftp://ftp.gnu.org/gnu/bash/bash-3.2-patches/bash32-025

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	autoconf2.5
BuildRequires:	bison
BuildRequires:	libtermcap-devel

Requires(post):	info-install
Requires(preun): info-install
Conflicts:	etcskel <= 1.63-11mdk
Conflicts:	fileutils < 4.1-5mdk
Conflicts:	setup < 2.9.1

%description
Bash is a GNU project sh-compatible shell or command language
interpreter. Bash (Bourne Again shell) incorporates useful features
from the Korn shell (ksh) and the C shell (csh). Most sh scripts
can be run by bash without modification.

Bash offers several improvements over sh, including command line
editing, unlimited size command history, job control, shell
functions and aliases, indexed arrays of unlimited size and 
integer arithmetic in any base from two to 64. Bash is ultimately
intended to conform to the IEEE POSIX P1003.2/ISO 9945.2 Shell and
Tools standard.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 1
mv doc/README .

%patch0 -p1 -b .security
%patch1 -p1 -b .profile
%patch2 -p1 -b .compat
%patch4 -p1 -b .dietlibc
%patch5 -p0 -b .fix_so
%patch6 -p0
%patch7 -p1 -b .strcoll_bugx
%patch8 -p1 -b .checkwinsize
%patch9 -p0 -b .quote

# upstream bugfixes
%patch20 -p0 -b .001
%patch21 -p0 -b .002
%patch22 -p0 -b .003
%patch23 -p0 -b .004
%patch24 -p0 -b .005
%patch25 -p0 -b .006
%patch26 -p0 -b .007
%patch27 -p0 -b .008
%patch28 -p0 -b .009
%patch29 -p0 -b .010
%patch30 -p0 -b .011
%patch31 -p0 -b .012
%patch32 -p0 -b .013
%patch33 -p0 -b .014
%patch34 -p0 -b .015
%patch35 -p0 -b .016
%patch36 -p0 -b .017
%patch37 -p0 -b .018
%patch38 -p0 -b .019
#%patch39 -p0 -b .020
#%patch40 -p0 -b .021
#%patch41 -p0 -b .022
#%patch42 -p0 -b .023
#%patch43 -p0 -b .024
#%patch44 -p0 -b .025

echo %{version} > _distribution
echo %{release} > _patchlevel
perl -p -i -e s/avx// _patchlevel

# needed by P6
autoconf


%build
libtoolize --copy --force

# build statically linked bash with dietlibc
%if %{build_dietlibc}
# TODO: --enable-minimal-config?
mkdir bash-static
pushd bash-static
    export CFLAGS="%{optflags} -Os"
    export CONFIGURE_TOP=".."
    %configure2_5x \
        --disable-command-timing \
        --enable-dietlibc
#       --enable-separate-helpfiles \
#       --disable-nls
#       --enable-minimal-config \
    %make
popd
%endif

# build dynamically linked bash
mkdir bash-dynamic
pushd bash-dynamic
    export CFLAGS="%{optflags}"
    export CONFIGURE_TOP=".."
    %configure2_5x \
        --disable-command-timing
    %make CFLAGS="%{optflags}"
popd


%check
pushd bash-dynamic
    make check
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
%makeinstall -C bash-dynamic

rm -rf %{buildroot}%{_datadir}/locale/en@boldquot/ %{buildroot}%{_datadir}/locale/en@quot/

# Sucks
chmod +w doc/texinfo.tex
chmod 0755 examples/misc/aliasconv.*
chmod 0755 examples/misc/cshtobash
chmod 0755 %{buildroot}%{_bindir}/bashbug

# Take out irritating ^H's from the documentation
for i in `/bin/ls doc/` ; do perl -pi -e 's/.//g' doc/$i ; done

mkdir -p %{buildroot}/bin
pushd %{buildroot}/bin
    mv ..%{_bindir}/bash .
    ln -s bash sh
    ln -sf bash bash3
popd

%if %{build_dietlibc}
install -m 0755 bash-static/bash %{buildroot}/bin/bash-diet
%endif

# make manpages for bash builtins as per suggestion in DOC/README
cd doc
sed -e '
/^\.SH NAME/, /\\- bash built-in commands, see \\fBbash\\fR(1)$/{
/^\.SH NAME/d
s/^bash, //
s/\\- bash built-in commands, see \\fBbash\\fR(1)$//
s/,//g
b
}
d
' builtins.1 > man.pages
install -m 0644 builtins.1 %{buildroot}%{_mandir}/man1/builtins.1

for i in `cat man.pages` ; do
    echo .so man1/builtins.1 > %{buildroot}%{_mandir}/man1/$i.1
done

install -m 0644 rbash.1 %{buildroot}%{_mandir}/man1/rbash.1

# now turn man.pages into a filelist for the man subpackage

cat man.pages |tr -s ' ' '\n' |sed '
1i\
%defattr(0644,root,root,0755)
s:^:%{_mandir}/man1/:
s/$/.1%{_extension}/
' > ../man.pages

perl -p -i -e 's!.*/(printf|export|echo|pwd|test|kill).1%{_extension}!!' ../man.pages

mkdir -p %{buildroot}%{_sysconfdir}/{skel,profile.d}
install -m 0644 %{_sourcedir}/dot-bashrc %{buildroot}%{_sysconfdir}/skel/.bashrc
install -m 0644 %{_sourcedir}/dot-bash_profile %{buildroot}%{_sysconfdir}/skel/.bash_profile
install -m 0644 %{_sourcedir}/dot-bash_logout %{buildroot}%{_sysconfdir}/skel/.bash_logout
install -m 0755 %{_sourcedir}/alias.sh %{buildroot}%{_sysconfdir}/profile.d/alias.sh
install -m 0644 %{_sourcedir}/bashrc %{buildroot}%{_sysconfdir}/bashrc

ln -s bash %{buildroot}/bin/rbash

# These are provided by other packages
rm -f %{buildroot}{%{_infodir}/dir,%{_mandir}/man1/{echo,export,kill,printf,pwd,test}.1}

cd ..

install -m 0644 bash-dynamic/doc/bash.info %{buildroot}%{_infodir}/

rm -rf %{buildroot}%{_datadir}/locale


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}.info


%preun
%_remove_install_info %{name}.info


%files -f man.pages
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/skel/.b*
%config(noreplace) %{_sysconfdir}/bashrc
%{_sysconfdir}/profile.d/alias.sh
/bin/rbash
/bin/bash
/bin/bash3
%if %{build_dietlibc}
/bin/bash-diet
%endif
/bin/sh
%{_infodir}/bash.info*
%{_mandir}/man1/bash.1*
%{_mandir}/man1/rbash.1*
%{_mandir}/man1/builtins.1*
%{_mandir}/man1/bashbug.1*
%{_bindir}/bashbug

%files doc
%defattr(-,root,root)
%doc README CHANGES


%changelog
* Fri Dec 14 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.2
- don't apply P39-P44; P39 causes a problem with user aliases and the rest
  don't apply without it

* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.2
- test profile scripts for readabiliy, not whether they're executable (/etc/bashrc)
- P37-P44: update to patchlevel 025
- put the tests in %%check

* Sat Oct 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.2
- the updated Mandriva bashrc had stupid umask settings so revert them
  to set umask to 022, not 002

* Sat Oct 06 2007 Vincent Danen <vdanen-at-build.annvix.org> 3.2
- 3.2
- updated upstream patches
- drop P3; we don't care about s390x archs
- use --color with {e,f,}grep by default
- put /etc/bashrc here instead of in setup and update it from Mandriva
- conflict on older setup packages

* Fri Aug 04 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1
- need to require info-install
- spec cleanups

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.1
- 3.1
- drop P50-P65; merged upstream
- drop P4, P8, P14: no longer needed or wanted
- renumber patches
- upstream fixes: P20-P36
- P9: extended quote fix (Novell)
- make alias.sh bourne-compliant (mdv bug #16188)
- install info pages
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- Clean rebuild

* Mon Jan 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 3.0
- Obfuscate email addresses and new tagging
- Uncompress patches

* Fri Sep 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-5avx
- minor spec cleanups
- alias.sh is not a config file

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-4avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-3avx
- rebuild for new gcc
- drop unapplied patches

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-2avx
- bootstrap build

* Fri Mar 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 3.0-1avx
- 3.0
- BuildRequires: s/byacc/bison/ (stefan)
- P13: dietlibc support (gb)
- P12: fix builds with --enable-minimal-config (gb)
- P14: really check for WCONTINUED support in waitpid() calls (gb)
- look at user-defined colors in ~/.dir_colors and don't waste resources
  with DIR_COLORS if it exists (robert.vojta)
- spec cleanups

* Fri Jun 25 2004 Vincent Danen <vdanen-at-build.annvix.org> 2.05b-17avx
- Annvix build

* Tue Mar 02 2004 Vincent Danen <vdanen@opensls.org> 2.05b-16sls
- remove %%build_opensls macro
- remove %%prefix
- minor spec cleanups

* Tue Dec 02 2003 Vincent Danen <vdanen@opensls.org> 2.05b-15sls
- OpenSLS build
- tidy spec
- use %%build_opensls macro to exclude docs
- clean up the descriptions somewhat

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
