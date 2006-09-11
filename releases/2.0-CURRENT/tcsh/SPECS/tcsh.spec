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
Patch1:		tcsh-6.09.00-termios.patch
Patch3:		tcsh-6.14.00-lsF.patch
Patch4:		tcsh-6.14.00-dashn.patch
Patch5:		tcsh-6.14.00-read.patch
Patch6:		tcsh-6.10.00-glibc_compat.patch
Patch7:		tcsh-6.14.00-getauthuid-is-not-in-auth_h.patch

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
%patch1 -p1 -b .termios
%patch3 -p1 -b .lsF
%patch4 -p1 -b .dashn
%patch5 -p1 -b .read
%patch6 -p1 -b .glibc_compat
%patch7 -p1


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
install %{_sourcedir}/alias.csh %{buildroot}%{_sysconfdir}/profile.d/alias.csh


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
%config(noreplace) %{_sysconfdir}/profile.d/*
/bin/*
%{_mandir}/*/*

%files doc
%defattr(-,root,root)
%doc NewThings FAQ Fixes eight-bit.txt complete.tcsh
%doc Ported README* WishList Y2K


%changelog
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
