#
# spec file for package zlib
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		zsh
%define version		4.2.6
%define release		%_revrel
%define epoch		1

Summary:	A shell with lots of features
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
License:	GPL
Group:		Shells
URL:		http://www.zsh.org
Source0:	http://www.zsh.org/pub/%{name}-%{version}.tar.bz2
Source2:	zcfg-avx.tar.bz2
Source3:	zsh.urpmi_comp
Source4:	http://www.zsh.org/pub/%{name}-%{version}-doc.tar.bz2
Patch1:		zsh-3.1.6-dev-22-path.patch
Patch2:		zsh-4.0.1-pre-3-rpmnewopt.patch
Patch101:	zsh-serial.patch
Patch102:	zsh-4.1.0-dev-7-rebootin.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libtermcap-devel >= 2.0
BuildRequires:	texinfo
BuildRequires:	pcre-devel
BuildRequires:	ncurses-devel

Requires(postun): rpm-helper
Requires(post):	rpm-helper


%description
Zsh is a UNIX command interpreter (shell) usable as an
interactive login shell and as a shell script command
processor. Of the standard shells, zsh most closely resembles
ksh but includes many enhancements. Zsh has command-line editing,
built-in spelling correction, programmable command completion,
shell functions (with autoloading), a history mechanism, and a
lots of other features


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -a 2 -a 4
%patch1 -p1
%patch2 -p1
%patch101 -p1
%patch102 -p1

cp %{_sourcedir}/zsh.urpmi_comp Completion/Mandrake/Command/_urpmi

# remove temporary files
find | grep '~$' | xargs rm -f
perl -pi -e 's|/usr/local/bin/|%{_bindir}/|' Functions/Misc/{run-help,checkmail,zcalc}


%build
%ifarch sparc
EXTRA_CONFIGURE_ARGS="--disable-lfs"
%endif

%configure2_5x \
    --enable-etcdir=%{_sysconfdir} \
    --enable-function-subdirs \
    --disable-debug \
    $EXTRA_CONFIGURE_ARGS \
    --disable-max-jobtable-size \
    --enable-pcre 
    #--with-curses-terminfo

make all


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make install-strip DESTDIR=%{buildroot}
make install.info DESTDIR=%{buildroot}

# copy Annvix Configuration files.
mkdir -p %{buildroot}/{bin,etc}
cp -a zcfg/etc/z* %{buildroot}%{_sysconfdir}
cp -a zcfg/share/zshrc_default %{buildroot}%{_datadir}/zsh/%{version}/zshrc_default

# Backward compatibility should be removed in the others times.
pushd %{buildroot}/bin
    mv ..%{_bindir}/zsh ./zsh
popd

rm -f %{buildroot}%{_bindir}/zsh-%{version}

# Handle documentation
rm -rf docroot
mkdir -p docroot/{Info_html,Examples,Documentation}/

cp -a README docroot/
cp -a Functions/Misc/* Misc/* Util/* docroot/Examples/
cp -a INSTALL ChangeLog* docroot/Documentation 
cp -a StartupFiles docroot/
cp -a Etc/* docroot/Documentation
cp -a %{name}-%{version}/Doc/*html docroot/Info_html/

rm -f docroot/{StartupFiles/.distfiles,Examples/{Makefile*,*.yo},Documentation/{Makefile*,*.yo}}
find docroot/ -name 'Makefile*' -o -name '.yo'|xargs rm -f
find docroot/ -type f|xargs perl -pi -e 's@^#!%_prefix/local/bin/(perl|zsh)@#!%_bindir/\1@'
mv docroot/Examples/compctl-examples docroot/StartupFiles



%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_shelladd /bin/zsh
%_install_info %{name}.info


%preun
%_preun_shelldel /bin/zsh


%postun
%_remove_install_info %{name}.info


%files
%defattr(-,root,root,0755)
%config(noreplace) %{_sysconfdir}/z*
/bin/%{name}
%{_mandir}/man1/*.1*
%{_infodir}/*.info*
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/%{version}/
%{_datadir}/zsh/%{version}/functions
%{_datadir}/zsh/%{version}/zshrc_default
%{_datadir}/zsh/site-functions/
%dir %{_libdir}/zsh
%{_libdir}/zsh/%{version}/

%files doc
%defattr(-,root,root,0755)
%doc README NEWS
%doc docroot/Documentation/ docroot/Examples/ docroot/Info_html/ docroot/StartupFiles/
%doc ChangeLog*


%changelog
* Sun Sep 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2.6
- use %%_post_shelladd and %%_preun_shelldel

* Wed May 24 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2.6
- 4.2.6
- add -doc subpackage and add back the zsh docs
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.2.5
- Clean rebuild

* Wed Dec 28 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.5
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Sep 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.5-3avx
- rebuild against new pcre

* Wed Aug 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.5-2avx
- bootstrap build (new gcc, new glibc)

* Mon Jul 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.5-1avx
- 4.2.5
- spec cleanups
- remove the %%doc_version define

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.2.4-3avx
- bootstrap build

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.2.4-2avx
- update S2 to set resource limits in /etc/zshrc

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.2.4-1avx
- 4.2.4
- drop doc sources
- add urpmi completion
- use ncurses instead of termcap

* Fri Jun 18 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.1.1-8avx
- Annvix build

* Tue Mar 09 2004 Vincent Danen <vdanen@opensls.org> 4.1.1-7sls
- minor spec cleanups
- don't even process doc files
- remove S3 (guide)

* Mon Jan 12 2004 Vincent Danen <vdanen@opensls.org> 4.1.1-6sls
- remove %%build_opensls macro; remove -doc package

* Wed Dec 31 2003 Vincent Danen <vdanen@opensls.org> 4.1.1-5sls
- fix BuildReq and change %%configure handling

* Wed Dec 03 2003 Vincent Danen <vdanen@opensls.org> 4.1.1-4sls
- OpenSLS build
- tidy spec
- don't build doc for %%build_opensls
- don't need yodl as a BuildReq

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
