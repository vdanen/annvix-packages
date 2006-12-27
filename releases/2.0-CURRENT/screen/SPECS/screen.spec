#
# spec file for package screen
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		screen
%define version		4.0.3
%define release		%_revrel

Summary:	A screen manager that supports multiple logins on one terminal
Name:		%{name}
Version:	%{version}
Release: 	%{release}
License:	GPL
Group:		Terminals
URL:		http://www.gnu.org/software/screen
Source0:	ftp://ftp.uni-erlangen.de/pub/utilities/screen/%{name}-%{version}.tar.gz
Patch0:		screen-3.7.6-compat21.patch
Patch1: 	screen-ia64.patch
Patch3:		screen-makefile-ppc.patch
Patch4:		screen-3.9.11-fix-utmp.diff
Patch6:		screen-3.9.13-no-libelf.patch
Patch7:		screen-3.9.11-biarch-utmp.patch
Patch8:		screen-3.9.15-overflow.patch
Patch9:		screen-4.0.2-screenrc-utf8-switch.patch
Patch10:	screen-4.0.2-varargs.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	ncurses-devel
BuildRequires:	utempter-devel
BuildRequires:	texinfo

Requires(post):	info-install
Requires(preun): info-install

%description
The screen utility allows you to have multiple logins on just one
terminal.  Screen is useful for users who telnet into a machine or
are connected via a dumb terminal, but want to use more than just
one login.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
# (sb) seems to be needed on x86 now too 
%patch3 -p1
%patch4 -p1
%patch6 -p1 -b .no-libelf
%patch7 -p1 -b .biarch-utmp
%patch8 -p1 -b .overflow
%patch9 -p0 -b .utf8
%patch10 -p1 -b .varargs


%build
%configure
perl -pi -e 's|.*#.*PTYMODE.*|#define PTYMODE 0620|' config.h
perl -pi -e 's|.*#.*PTYGROUP.*|#define PTYGROUP 5|' config.h

perl -pi -e 's|.*#undef HAVE_BRAILLE.*|#define HAVE_BRAILLE 1|' config.h
perl -pi -e 's|.*#undef BUILTIN_TELNET.*|#define BUILTIN_TELNET 1|' config.h

perl -pi -e 's|%{_prefix}/etc/screenrc|%{_sysconfdir}/screenrc|' config.h
perl -pi -e 's|/usr/local/etc/screenrc|%{_sysconfdir}/screenrc|' etc/etcscreenrc doc/*
perl -pi -e 's|/local/etc/screenrc|%{_sysconfdir}/screenrc|' doc/*
rm doc/screen.info*

%make CFLAGS="%{optflags} -DETCSCREENRC=\\\"%{_sysconfdir}/screenrc\\\""


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/skel

%makeinstall SCREENENCODINGS=%{buildroot}%{_datadir}/screen/utf8encodings/

pushd %{buildroot}%{_bindir}
    rm -f screen.old screen
    mv screen-%{version} screen
popd

install -c -m 0644 etc/etcscreenrc %{buildroot}%{_sysconfdir}/screenrc
install -c -m 0644 etc/screenrc %{buildroot}%{_sysconfdir}/skel/.screenrc

mkdir -p %{buildroot}%{_sysconfdir}/profile.d

cat > %{buildroot}%{_sysconfdir}/profile.d/screen.sh <<EOF
#!/bin/sh
# %{_sysconfdir}/profile.d/screen.sh

if [ -z "\$SCREENDIR" ]; then
    export SCREENDIR=\$HOME/tmp
fi
EOF


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_install_info %{name}


%preun
%_remove_install_info %{name}


%files
%defattr(-,root,root)
%{_bindir}/screen
%{_mandir}/man1/screen.1.bz2
%{_infodir}/screen.info*
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/profile.d/screen.sh
%config(noreplace) %{_sysconfdir}/screenrc
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/skel/.screenrc
%{_datadir}/screen/

%files doc
%defattr(-,root,root)
%doc NEWS README doc/FAQ doc/README.DOTSCREEN ChangeLog


%changelog
* Sat Dec 02 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.3
- drop P5; it's not used anywhere
- rebuild against new ncurses

* Thu Oct 26 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.3
- 4.0.3 (fixes CVE-2006-4573)

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2
- rebuild against new libutempter

* Tue Jun 06 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2-5avx
- P9: add 'C-a U' binding to /etc/skel/.screenrc (rgarciasuarez)
- P10: varargs fixes (gbeauchesne)
- fix the screen profile.d script (rgarciasuarez)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2-4avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2-3avx
- rebuild

* Mon Jun 21 2004 Vincent Danen <vdanen-at-build.annvix.org> 4.0.2-2avx
- requires info-install rather than /sbin/install-info
- Annvix build

* Mon May 10 2004 Vincent Danen <vdanen@opensls.org> 4.0.2-1sls
- 4.0.2
- linked against new libutempter

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 3.9.15-4sls
- minor spec cleanups
- remove %%prefix

* Mon Dec 08 2003 Vincent Danen <vdanen@opensls.org> 3.9.15-3sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
