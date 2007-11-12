#
# spec file for package mingetty
#
# Package for the Annvix Linux distribution: http://annvix.org/
#
# Please submit bugfixes or comments via http://bugs.annvix.org/
#
# $Id$

%define revision	$Rev$
%define name		mingetty
%define version		1.07
%define release		%_revrel

Summary: 	A compact getty program for virtual consoles only
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		System/Base
URL:		ftp://jurix.jura.uni-sb.de/pub/linux/source/system/daemon/
Source0: 	ftp://jurix.jura.uni-sb.de/pub/linux/source/system/daemons/%{name}-%{version}.tar.bz2
Patch0:		mingetty-1.00-opt.patch

BuildRoot: 	%{_buildroot}/%{name}-%{version}
BuildRequires:	dietlibc-devel >= 0.27

%description
The mingetty program is a lightweight, minimalist getty program for
use only on virtual consoles.  Mingetty is not suitable for serial
lines (you should use the mgetty program instead for that purpose).


%prep
%setup -q
%patch0 -p1 -b .opt


%build
%ifarch x86_64
COMP="diet x86_64-annvix-linux-gnu-gcc"
%else
COMP="diet gcc"
%endif
make \
    CC="$COMP" \
    CFLAGS="-Os -Wall -pipe -D_GNU_SOURCE -D_BSD_SOURCE" \
    LDFLAGS="-Os -static -s"


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
mkdir -p %{buildroot}/{sbin,%{_mandir}/man8}

install -m 0755 mingetty %{buildroot}/sbin/
install -m 0644 mingetty.8 %{buildroot}/%{_mandir}/man8/


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
/sbin/mingetty
%{_mandir}/man8/*


%changelog
* Sun Nov 11 2007 Vincent Danen <vdanen-at-build.annvix.org> 1.07
- rebuild

* Fri Jul 14 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.07
- add -doc subpackage
- rebuild with gcc4

* Wed Jan 11 2006 Vincent Danen <vdanen-at-build.annvix.org> 1.07
- Clean rebuild

* Fri Dec 30 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.07
- re-enable dietlibc build on x86_64; have to specify the explicit
  arch'd compiler to use for it to work properly

* Thu Dec 29 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.07
- Obfuscate email addresses and new tagging
- Uncompress patches
- once again there are problems building against dietlibc on x86_64;
  this must be due to the SSP support

* Fri Sep 16 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.07-1avx
- 1.0.7

* Wed Aug 17 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.06-7avx
- bootstrap build (new gcc, new glibc)

* Fri Jun 03 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.06-6avx
- bootstrap build

* Fri Feb 04 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.06-5avx
- rebuild against new dietlibc

* Tue Jan 25 2005 Vincent Danen <vdanen-at-build.annvix.org> 1.06-4avx
- enable x86_64 build

* Tue Jun 22 2004 Vincent Danen <vdanen-at-build.annvix.org> 1.06-3avx
- Annvix build

* Wed Mar 17 2004 Oden Eriksson <oden.eriksson@opensls.org> 1.06-2sls
- build it against dietlibc for x86 (problems with amd64)
- nuke %%doc COPYING

* Mon Mar 15 2004 Vincent Danen <vdanen@opensls.org> 1.06-1sls
- 1.06

* Sat Mar 06 2004 Vincent Danen <vdanen@opensls.org> 1.00-5sls
- minor spec cleanups

* Mon Dec 01 2003 Vincent Danen <vdanen@opensls.org> 1.00-4sls
- OpenSLS build
- tidy spec
- regen P0 to use RPM_OPT_FLAGS and not RPM_OPTS

# vim: expandtab:shiftwidth=8:tabstop=8:softtabstop=8
