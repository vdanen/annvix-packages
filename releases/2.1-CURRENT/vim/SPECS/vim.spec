#
# spec file for package vim
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# Notes / Warning :
# - this package is not prefixable
# - to update official patches, aka SOURCE4, see README.mdk in SOURCE4
#
# $Id$

%define revision	$Rev$
%define name		vim
%define version		7.1
%define release		%_revrel

%define patch_level	002
%define localedir	%{buildroot}%{_datadir}/locale/

%define perl_version	%(rpm -q --qf '%%{epoch}:%%{version}' perl)

Summary:	VIsual editor iMproved 
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	Charityware
Group:		Editors
URL:		http://www.vim.org
Source0:	ftp://ftp.vim.org/pub/vim/unix//%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.vim.org/pub/vim/unix//extra/%{name}-%{version}-lang.tar.bz2
Source2:	vim-%{version}.%{patch_level}-patches.tar.bz2
# http://vim.sourceforge.net/scripts/script.php?script_id=98
Source3:	vim-spec-3.0.tar.bz2
# MDK patches
Patch2:		vim-5.6a-paths.patch
Patch3:		vim-6.4-mdk-rpm-spec-syntax.patch
Patch8:		vim-6.0af-man-path.patch
Patch10:	xxd-locale.patch
Patch11:	vim-6.2-gcc31.patch
Patch20:	vimrc_hebrew.patch
Patch22:	vim-6.1-fix-xterms-comments.patch
Patch23:	vim-6.3-remove-docs.patch
Patch24:	vim-6.1-outline-mode.patch 
Patch25:	vim-6.1-xterm-s-insert.patch 
Patch26:	vim-7.0-mdk-changelog-mode.patch
Patch27:	vim-6.1-rpm42.patch
Patch28:	vim-6.4-mdk-po-mode.patch
Patch29:	vim-7.0-mdk-po-buildfix.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	perl-devel
BuildRequires:	python-devel
BuildRequires:	termcap-devel
BuildRequires:	acl-devel

%description
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more.  The vim-common package
contains files which every VIM binary will need in order to run.


%package common
Summary:	The common files needed by any version of the VIM editor
Group:		Editors
Requires:	perl = %{perl_version}
Requires(pre):	coreutils
Requires(preun): coreutils
Requires(post):	coreutils
Requires(postun): coreutils

%description common
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more.  The vim-common package
contains files which every VIM binary will need in order to run.


%package minimal
Summary:	A minimal version of the VIM editor
Group:		Editors
Provides:	vim = %{version}
Requires(post):	/usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives

%description minimal
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more.  The vim-minimal package
includes a minimal version of VIM, which is installed into /bin/vi for use
when only the root partition is present.


%package enhanced
Summary:	A version of the VIM editor which includes recent enhancements
Group:		Editors
Requires:	vim-common >= %{version}
Obsoletes:	vim-color
Provides:	vim = %{version}
Provides:	vim-color = %{version}
Requires(post):	/usr/sbin/update-alternatives
Requires(postun): /usr/sbin/update-alternatives

%description enhanced
VIM (VIsual editor iMproved) is an updated and improved version of the vi
editor.  Vi was the first real screen-based editor for UNIX, and is still
very popular.  VIM improves on vi by adding new features: multiple windows,
multi-level undo, block highlighting and more.  The vim-enhanced package
contains a version of VIM with extra, recently introduced features like
Python and Perl interpreters.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -b 1 -n vim71 -a2

# spec plugin
rm -f runtime/doc/pi_spec.txt
rm -f runtime/ftpplugin/spec.vim
tar tjf %{_sourcedir}/vim-spec-3.0.tar.bz2 -C runtime
#official patches
for i in vim-%{version}.%{patch_level}-patches/%{version}*; do
    patch -p0 -s < $i
done

#mdk patches
%patch2 -p1
%patch3 -p0 -b .spec
%patch8 -p1 -b .manpath
%patch10 -p1 -b .xxdloc
%patch11 -p1 -b .gcc31
%patch20 -p1 -b .warly
%patch22 -p0
%patch23 -p0 -b .doc
%patch24 -p0
%patch25 -p0
%patch26 -p0
%patch27 -p0
%patch28 -p0
%patch29 -p0

perl -pi -e 's|SYS_VIMRC_FILE "\$VIM/vimrc"|SYS_VIMRC_FILE "%{_sysconfdir}/vim/vimrc"|' src/os_unix.h
# disable command echo
perl -pi -e 's|^set showcmd|set noshowcmd|' runtime/vimrc_example.vim
perl -pi -e 's|\Qsvn-commit.*.tmp\E|svn-commit*.tmp|' ./runtime/filetype.vim


%build
# First build: vim-enhanced

CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"  ./configure \
    --prefix=%{_prefix} \
    --enable-acl \
    --enable-pythoninterp \
    --enable-perlinterp \
    --with-features=huge \
    --libdir=%{_libdir} \
    --with-compiledby="%{packager}" \
    --with-x=no \
    --enable-gui=no \
    --disable-gpm \
    --exec-prefix=%{_prefix}

make
mv src/vim src/vim-enhanced
make -C src/ clean

# Second build: vim-minimal
CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" ./configure  \
    --prefix=%{_prefix} \
    --with-features=tiny \
    --disable-tclinterp \
    --disable-cscope \
    --disable-multibyte \
    --disable-hangulinput \
    --disable-xim \
    --disable-fontset \
    --disable-gui \
    --disable-acl \
    --disable-pythoninterp \
    --disable-perlinterp \
    --libdir=%{_libdir} \
    --with-compiledby="%packager" \
    --with-x=no \
    --enable-gui=no \
    --exec-prefix=%{_prefix} \
    --with-tlib=termcap \
    --disable-gpm

make
cp src/vim src/vim-minimal
make -C src

cp -al runtime/doc doc
# apply os_doc.diff
pushd doc
    rm -f *.1
    rm -f os_{390,dos,msdos,risc,win32,amiga,mac,os2,beos,mint,qnx,vms}.txt
    rm -f gui_{w16,w32}.txt
    rm -f vim2html.pl Makefile *awk
popd

# britton support
ln -s tutor.fr runtime/tutor/tutor.br
ln -s menu_fr_fr.iso_8859-15.vim runtime/lang/menu_br


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

[ ! -e annvix ] && mv vim-%{version}.%{patch_level}-patches annvix

perl -pi -e 's!LOCALEDIR=\$\(DEST_LANG\)!LOCALEDIR=\$(DESTDIR)\$\(prefix\)/share/locale!g' src/Makefile

mkdir -p %{buildroot}{/bin,%{_bindir},%{_datadir}/{vim,locale},%{_mandir}/man1,%localedir}
%makeinstall_std VIMRTDIR=""


make -C src installmacros prefix=%{buildroot}%{_prefix} VIMRTDIR=""

install -s -m 0755 src/vim-enhanced %{buildroot}%{_bindir}
install -s -m 0755 src/vim-minimal %{buildroot}/bin/vim-minimal

pushd %{buildroot}
    rm -f ./bin/rvim
    for i in ex vimdiff; do
        ln -sf vim-enhanced ./usr/bin/$i
    done
    rm -f ./usr/man/man1/rvim.1.bz2
popd

# installing man pages
for i in %{buildroot}%{_mandir}/man1/{vi,rvi}; do
    cp %{buildroot}%{_mandir}/man1/vim.1 $i.1
done

ln -sf vimrc_example.vim %{buildroot}/usr/share/vim/vimrc

pushd %{buildroot}/%{_prefix}/share/vim/tools
    # i need to make a choice :(.
    rm -f vim132
    perl -p -i -e 's|#!/usr/bin/nawk|#!/usr/bin/gawk|' mve.awk
    perl -p -i -e 's|#!/usr/local/bin/perl|#!/usr/bin/perl|' *.pl
    perl -p -i -e 's|#!/usr/gnu/bin/perl|#!/usr/bin/perl|' *
popd
 
# Be short-circuit aware :
ln -f runtime/macros/README.txt README_macros.txt
ln -f runtime/tools/README.txt README_tools.txt
perl -p -i -e "s|#!/usr/local/bin/perl|#!/usr/bin/perl|" runtime/doc/*.pl

# fix the paths in the man pages
for i in %{buildroot}/usr/share/man/man1/*.1; do
    perl -p -i -e "s|%{buildroot}||" $i
done

# prevent including twice the doc
rm -fr %{buildroot}/usr/share/vim/doc
ln -sf ../../../%{_defaultdocdir}/%{name}-common-%{version}/doc %{buildroot}/usr/share/vim/doc

%kill_lang %{name}

# symlink locales in right place so that %find_land put needed %lang:
# see %pre common why this is needed
pushd %{buildroot}%{_datadir}/vim/lang
    ln -s ../../locale/* .
popd

rm -f %{buildroot}%{_bindir}/{rview,view,rvim}

%find_lang %{name}

find %{buildroot}%{_datadir}/vim/ -name "tutor.*" | egrep -v 'tutor(|\.vim)$' |
     sed -e "s^%{buildroot}^^" -e 's!^\(.*tutor.\)\(..\)!%lang(\2) \1\2!g' >> %{name}.lang

find %{buildroot}%{_datadir}/vim/ -name "menu*" |
    sed -e "s^%{buildroot}^^" -e 's!^\(.*menu_\)\(..\)\(_\)!%lang(\2) \1\2\3!g' \
        -e 's!^\(.*menu\)\(_chinese\)!%lang(zh) \1\2!g' \
        -e 's!^\(.*menu\)\(_czech_\)!%lang(cs) \1\2!g' \
        -e 's!^\(.*menu\)\(_french\)!%lang(fr) \1\2!g' \
        -e 's!^\(.*menu\)\(_german\)!%lang(de) \1\2!g' \
        -e 's!^\(.*menu\)\(_japanes\)!%lang(ja) \1\2!g' \
        -e 's!^\(.*menu\)\(_polish\)!%lang(pl) \1\2!g' \
        -e 's!^\(.*menu\)\(_slovak\)!%lang(sk) \1\2!g' \
        -e 's!^\(.*menu\)\(_spanis\)!%lang(es) \1\2!g' \
    >> %{name}.lang
rm -f %{buildroot}%{_bindir}/vim

rm -f %{buildroot}%{_mandir}/man1/evim.1*

mkdir -p %{buildroot}%{_sysconfdir}/vim
cat << EOF >> %{buildroot}%{_sysconfdir}/vim/vimrc
" Place your system-wide modifications here.
" %{_datadir}/vim/ files are overwritten on package update.

source %{_datadir}/vim/vimrc
EOF


%post minimal
update-alternatives --install /usr/bin/vi uvi /bin/vim-minimal 10
update-alternatives --install /bin/vi     vi  /bin/vim-minimal 10
update-alternatives --install /bin/vim    vim /bin/vim-minimal 10
for i in view ex rvi rview rvim; do
    update-alternatives --install /bin/$i $i /bin/vi 10 || :
done
:


%postun minimal
[ $1 = 0 ] || exit 0
update-alternatives --remove uvi /usr/bin/vim-minimal
update-alternatives --remove vi  /bin/vim-minimal
update-alternatives --remove vim /bin/vim-minimal

for i in view ex rvi rview rvim; do
    update-alternatives --remove $i /bin/$i || :
done
:


%post enhanced
update-alternatives --install /usr/bin/vi uvi /usr/bin/vim-enhanced 20
update-alternatives --install /bin/vi  vi     /usr/bin/vim-enhanced 20
update-alternatives --install /bin/vim vim    /usr/bin/vim-enhanced 20
:


%postun enhanced
[ $1 = 0 ] || exit 0
update-alternatives --remove uvi /usr/bin/vim-enhanced
update-alternatives --remove vi  /usr/bin/vim-enhanced
update-alternatives --remove vim /usr/bin/vim-enhanced
:


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files common -f %{name}.lang
%defattr(-,root,root)
%dir %{_datadir}/vim/
%{_datadir}/vim/*
%exclude %{_datadir}/vim/doc
%{_mandir}/man1/vim.1*
%{_mandir}/man1/ex.1*
%{_mandir}/man1/vi.1*
%{_mandir}/man1/view.1*
%{_mandir}/man1/rvi.1*
%{_mandir}/man1/rview.1*
%{_mandir}/man1/vimdiff.1*
%{_mandir}/man1/vimtutor.1*
%{_mandir}/man1/rvim.1*
%{_mandir}/man1/xxd.1*
%{_bindir}/xxd
%{_bindir}/vimtutor
#%exclude %{_bindir}/rview
#%exclude %{_bindir}/rvim
#%exclude %{_bindir}/view
%dir %{_sysconfdir}/vim
%config(noreplace) %{_sysconfdir}/vim/vimrc

%files minimal
%defattr(-,root,root)
/bin/vim-minimal

%files enhanced
%defattr(-,root,root)
%{_bindir}/vim-enhanced
%{_bindir}/ex
%{_bindir}/vimdiff

%files doc
%doc README*.txt runtime/termcap
%doc --parents annvix/README*
%doc doc
%{_datadir}/vim/doc


%changelog
* Mon Jun 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 7.1
- rebuild against new acl

* Fri May 25 2007 Vincent Danen <vdanen-at-build.annvix.org> 7.1
- 7.1
- rebuild against new python
- versioned provides

* Tue Dec 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.0
- update to patchlevel 30

* Tue Aug 15 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.0
- spec cleanups
- remove locales

* Tue Jun 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.0
- rebuild against new python
- move the /usr/share/vim/doc symlink to the right package

* Tue May 09 2006 Vincent Danen <vdanen-at-build.annvix.org> 7.0
- 7.0; patchlevel 1
- added P9
- updated P26
- BuildRequires: acl-devel; enable ACL support for vim-enhanced
- add -doc subpackage
- build against perl 5.8.8
- drop P31

* Wed Jan 25 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.4
- 6.4; patchlevel 1
- updated P3, P28 from Mandriva
- fix prereq
- remove useless triggers
- adapt P31 as tcltags is no longer shipped
- delete some uncommon locale files

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.3
- Clean rebuild

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.3
- Clean rebuild

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.3
- Obfuscate email addresses and new tagging
- Uncompress patches
- make S5 look like the tar file it is

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-6avx
- update to patchlevel 86
- update spec mode to 3.0
- fix perl version eval (nanardon)
- fix svn commit file detection (misc)
- BuildRequires: python-devel
- rebuild against new python and new perl
- drop S3; unused menu entry

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-5avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-4avx
- bootstrap build

* Thu Feb 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-3avx
- rebuild against new python

* Wed Feb 02 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-2avx
- rebuild against new perl

* Tue Feb 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.3-1avx
- 6.3; patchlevel 54
- S5: spec mode from Guillaume Rousse
- use a system-wide configfile in /etc/vim/ (misc)
- drop P29
- remove evim manpage, add rview symlink (bluca)
- disable command echo by default
- drop P30 (applied upstream)
- spec cosmetics

* Tue Feb 01 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.2-16avx
- P30: fix for CAN-2004-1138
- P31: fix for CAN-2005-0069

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 6.2-15avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 6.2-14sls
- minor spec cleanups

* Mon Jan 12 2004 Vincent Danen <vdanen@opensls.org> 6.2-13sls
- remove %%build_opensls tags

* Fri Dec 19 2003 Vincent Danen <vdanen@opensls.org> 6.2-12sls
- OpenSLS build
- don't build vim-x11 (use %%build_opensls macro)
- don't enable gpm support in vim-enhanced

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
