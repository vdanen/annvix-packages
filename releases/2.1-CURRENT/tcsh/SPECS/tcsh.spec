#
# spec file for package tcsh
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		tcsh
%define version		6.14
%define release		%_revrel
%define rversion	%{version}.00

Summary:	An enhanced version of csh, the C shell
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	BSD
Group:		Shells
URL:		http://www.tcsh.org/
Source:		ftp://ftp.funet.fi/pub/unix/shells/tcsh/tcsh-%{version}.00.tar.bz2
Source1:	alias.csh
Patch0:		tcsh-6.14.00-fdr-config.patch
Patch1:		tcsh-6.14.00-fdr-closem.patch
Patch2:		tcsh-6.14.00-fdr-iconv.patch
Patch3:		tcsh-6.14.00-fdr-lsF.patch
Patch4:		tcsh-6.14.00-fdr-dashn.patch
Patch5:		tcsh-6.14.00-fdr-read.patch
Patch6:		tcsh-6.14.00-fdr-sigint.patch
Patch7:		tcsh-6.14.00-fdr-wide-crash.patch
Patch8:		tcsh-6.14.00-fdr-colors.patch
Patch9:		tcsh-6.14.00-fdr-wide-seeks.patch
Patch10:	tcsh-6.14.00-fdr-spell-crash.patch
Patch11:	tcsh-6.14.00-fdr-remotehost.patch
Patch12:	tcsh-6.14.00-fdr-tinfo.patch
Patch13:	tcsh-6.09.00-mdv-termios.patch
Patch14:	tcsh-6.10.00-mdv-glibc_compat.patch
Patch15:	tcsh-6.14.00-mdv-getauthuid-is-not-in-auth_h.patch

BuildRoot:	%{_buildroot}/%{name}-%{version}
BuildRequires:	libtermcap-devel
BuildRequires:	groff-for-man

Provides:	csh = %{version}
Requires(post):	rpm-helper
Requires(postun): rpm-helper

%description
Tcsh is an enhanced but completely compatible version of csh, the C
shell.  Tcsh is a command language interpreter which can be used both
as an interactive login shell and as a shell script command processor.
Tcsh includes a command line editor, programmable word completion,
spelling correction, a history mechanism, job control and a C language
like syntax.


%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
This package contains the documentation for %{name}.


%prep
%setup -q -n %{name}-%{rversion}
%patch0 -p1 -b .config
%patch1 -p1 -b .closem
%patch2 -p1 -b .iconv
%patch3 -p1 -b .lsF
%patch4 -p1 -b .dashn
%patch5 -p1 -b .read
%patch6 -p1 -b .sigint
%patch7 -p1 -b .wide-crash
%patch8 -p1 -b .colors
%patch9 -p1 -b .wide-seeks
%patch10 -p1 -b .spell-crash
%patch11 -p1 -b .remotehost
%patch12 -p1 -b .tinfo
%patch13 -p1 -b .termios
%patch14 -p1 -b .glibc_compat
%patch15 -p1


%build
%configure \
    --bindir=/bin \
    --without-hesiod
%make
nroff -me eight-bit.me > eight-bit.txt


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man1 %{buildroot}/bin
install -s tcsh %{buildroot}/bin/tcsh
install -m 0644 tcsh.man %{buildroot}%{_mandir}/man1/tcsh.1
ln -s tcsh.1 %{buildroot}%{_mandir}/man1/csh.1
ln -sf tcsh %{buildroot}/bin/csh

mkdir -p %{buildroot}%{_sysconfdir}/profile.d/
install -m 0644 %{_sourcedir}/alias.csh %{buildroot}%{_sysconfdir}/profile.d/11alias.csh


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%post
%_post_shelladd /bin/csh
%_post_shelladd /bin/tcsh


%preun
%_preun_shelldel /bin/csh
%_preun_shelldel /bin/tcsh


%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/11alias.csh
/bin/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc NewThings FAQ Fixes eight-bit.txt complete.tcsh
%doc Ported README* WishList Y2K


%changelog
* Sat Dec 22 2007 Vincent Danen <vdanen-at-build.annvix.org> 6.14
- order the profile.d/ script and drop executable bit

* Mon Dec 03 2007 Vincent Danen <vdanen-at-build.annvix.org> 6.14
- sync patches with Mandriva 6.14-4mdv, which synced most patches to Fedora

* Sun Sep 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.14
- use %%_post_shelladd and %%_preun_shelldel

* Fri Jun 16 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.14
- add -doc subpackage
- rebuild with gcc4

* Thu Jan 12 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.14
- Clean rebuild

* Tue Jan 10 2006 Vincent Danen <vdanen-at-build.annvix.org> 6.14
- Obfuscate email addresses and new tagging
- Uncompress patches
- fix prereq

* Sat Sep 10 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.14-1avx
- 6.14
- drop P0, P5, P7
- P3, P4, new P5: from fedora
- build eight-bit.txt in build stage (pixel)

* Fri Aug 12 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.12-11avx
- bootstrap build (new gcc, new glibc)

* Thu Jun 09 2005 Vincent Danen <vdanen-at-build.annvix.org> 6.12-10avx
- rebuild

* Sat Jun 19 2004 Vincent Danen <vdanen-at-build.annvix.org> 6.12-9avx
- Annvix build

* Mon Mar 08 2004 Vincent Danen <vdanen@opensls.org> 6.12-8sls
- minor spec cleanups

* Tue Dec 30 2003 Vincent Danen <vdanen@opensls.org> 6.12-7sls
- OpenSLS build
- tidy spec

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
